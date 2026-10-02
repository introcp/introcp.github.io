#!/usr/bin/env python3
"""Live in-class feedback server.

Tiny key-value poll: students vote Yes/No, the lecturer watches the tally and
resets it between questions. State lives in memory and is mirrored to a JSON
file so a container restart does not wipe an ongoing poll.

Endpoints (all return JSON, kept compatible with the previous client):

    GET /feedback?t=positive|negative   record a vote, return the tally
    GET /feedback                       return the tally (no vote)
    GET /status                         return the tally (no vote)
    GET /epoch                          return a token that changes on reset
    GET /reset?p=<password>             reset the tally, return true/false
    GET /healthz                        liveness probe

Light abuse filtering (no authentication beyond the reset password): browser
User-Agent required, allow-listed Origin, a custom client header set by the
page, and a per-IP vote rate limit. Nothing here is meant to stop a determined
attacker, only trivial `curl`/script spam, as before.
"""

from __future__ import annotations

import hmac
import json
import logging
import os
import re
import secrets
import threading
import time
from pathlib import Path

from flask import Flask, jsonify, request

LOG = logging.getLogger("feedback")

# --- configuration ---------------------------------------------------------


def _env_int(name: str, default: int) -> int:
    """Parse a positive integer env var, falling back to `default` on garbage.

    A typo in .env must not stop the container from booting.
    """
    raw = os.environ.get(name, "")
    try:
        value = int(raw)
    except ValueError:
        if raw:
            LOG.warning("invalid %s=%r, using default %d", name, raw, default)
        return default
    if value < 1:
        LOG.warning("%s=%d must be positive, using default %d", name, value, default)
        return default
    return value


PASSWORD = os.environ.get("FEEDBACK_PASSWORD", "")
STATE_FILE = Path(os.environ.get("STATE_FILE", "/data/state.json"))
ALLOWED_ORIGINS = tuple(
    origin.strip()
    for origin in os.environ.get(
        "ALLOWED_ORIGINS", "https://introcp.github.io,http://localhost:3500"
    ).split(",")
    if origin.strip()
)
CLIENT_HEADER = "X-Feedback-Client"
CLIENT_VALUE = os.environ.get("CLIENT_VALUE", "web")
VOTES_PER_MINUTE = _env_int("VOTES_PER_MINUTE", 20)
RESETS_PER_MINUTE = _env_int("RESETS_PER_MINUTE", 10)

# Substring match against the User-Agent; rejects non-browser clients such as
# curl/wget/requests while leaving real browser UAs alone.
BLOCKED_UA = re.compile(
    r"curl|wget|python-requests|python-urllib|urllib|httpx|aiohttp|httpie|"
    r"go-http-client|libwww|java/|okhttp|scrapy|node-fetch|axios|postman|"
    r"insomnia|headlesschrome",
    re.IGNORECASE,
)

# --- state -----------------------------------------------------------------

_lock = threading.Lock()
_state = {"positive": 0, "neutral": 0, "negative": 0, "epoch": ""}
_rate_lock = threading.Lock()
_rate: dict[tuple[str, str], list[float]] = {}


def _new_epoch() -> str:
    return secrets.token_hex(8)


def _save_locked() -> None:
    """Persist state; failures degrade to in-memory only. Caller holds _lock."""
    tmp = STATE_FILE.with_suffix(".tmp")
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(_state))
        os.replace(tmp, STATE_FILE)
    except OSError as exc:  # read-only/broken volume must not kill the poll
        LOG.warning("could not persist state to %s: %s", STATE_FILE, exc)


def _load() -> None:
    with _lock:
        try:
            data = json.loads(STATE_FILE.read_text())
            for key in ("positive", "neutral", "negative"):
                _state[key] = max(0, int(data.get(key, 0)))
            _state["epoch"] = str(data.get("epoch") or _new_epoch())
        except (OSError, ValueError, TypeError):
            _state["epoch"] = _new_epoch()
        _save_locked()


def _snapshot() -> dict[str, int]:
    return {
        "positive": _state["positive"],
        "neutral": _state["neutral"],
        "negative": _state["negative"],
    }


def _vote(kind: str | None) -> dict[str, int]:
    with _lock:
        if kind is not None:
            _state[kind] += 1
            _save_locked()
        return _snapshot()


def _epoch() -> str:
    with _lock:
        return _state["epoch"]


def _reset(password: str) -> bool:
    if not PASSWORD or not hmac.compare_digest(password, PASSWORD):
        return False
    with _lock:
        _state["positive"] = _state["neutral"] = _state["negative"] = 0
        _state["epoch"] = _new_epoch()
        _save_locked()
    return True


# --- abuse filtering -------------------------------------------------------


def _client_ip() -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:  # behind the reverse proxy; rate limiting only, not auth
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _rate_limited(bucket: str, limit: int) -> bool:
    now = time.monotonic()
    key = (bucket, _client_ip())
    with _rate_lock:
        hits = [t for t in _rate.get(key, ()) if now - t < 60.0]
        if len(hits) >= limit:
            _rate[key] = hits
            return True
        hits.append(now)
        _rate[key] = hits
        if len(_rate) > 10000:  # opportunistic cleanup on classroom-scale load
            for stale in [k for k, v in _rate.items() if not v or now - v[-1] > 60.0]:
                _rate.pop(stale, None)
    return False


def _rejection() -> str | None:
    user_agent = request.headers.get("User-Agent", "")
    if not user_agent or BLOCKED_UA.search(user_agent):
        return "blocked user-agent"
    origin = request.headers.get("Origin")
    if origin is not None and origin not in ALLOWED_ORIGINS:
        return "origin not allowed"
    if request.headers.get(CLIENT_HEADER) != CLIENT_VALUE:
        return "missing client marker"
    return None


# --- app -------------------------------------------------------------------

app = Flask(__name__)


@app.after_request
def _cors(response):
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = CLIENT_HEADER
        response.headers["Access-Control-Max-Age"] = "600"
    return response


def _preflight() -> tuple[str, int] | None:
    if request.method == "OPTIONS":
        return "", 204
    return None


def _denied() -> tuple[object, int] | None:
    reason = _rejection()
    if reason:
        return jsonify({"error": reason}), 403
    return None


@app.route("/feedback", methods=["GET", "OPTIONS"])
def feedback():
    if (response := _preflight()) is not None:
        return response
    if (response := _denied()) is not None:
        return response
    kind = request.args.get("t")
    if kind not in ("positive", "negative"):
        kind = None
    if kind is not None and _rate_limited("vote", VOTES_PER_MINUTE):
        return jsonify({"error": "rate limited"}), 429
    return jsonify(_vote(kind))


@app.route("/status", methods=["GET", "OPTIONS"])
def status():
    if (response := _preflight()) is not None:
        return response
    if (response := _denied()) is not None:
        return response
    with _lock:
        return jsonify(_snapshot())


@app.route("/epoch", methods=["GET", "OPTIONS"])
def epoch():
    if (response := _preflight()) is not None:
        return response
    if (response := _denied()) is not None:
        return response
    return jsonify(_epoch())


@app.route("/reset", methods=["GET", "OPTIONS"])
def reset():
    if (response := _preflight()) is not None:
        return response
    if (response := _denied()) is not None:
        return response
    if _rate_limited("reset", RESETS_PER_MINUTE):
        return jsonify({"error": "rate limited"}), 429
    return jsonify(_reset(request.args.get("p", "")))


@app.route("/healthz", methods=["GET"])
def healthz():
    return "ok\n", 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route("/", methods=["GET"])
def index():
    return (
        "feedback server: /feedback /status /epoch /reset\n",
        200,
        {"Content-Type": "text/plain; charset=utf-8"},
    )


_load()

if not PASSWORD:
    LOG.warning("FEEDBACK_PASSWORD is empty: /reset will always fail")
if not ALLOWED_ORIGINS:
    LOG.warning("ALLOWED_ORIGINS is empty: browser CORS requests will be rejected")
