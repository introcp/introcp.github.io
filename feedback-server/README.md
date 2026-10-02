# Live feedback server

Minimal Yes/No poll API for the *Introduction to Computer Programming* website.
Students vote from the "Live Feedback" page, the lecturer shows the live tally
and resets the poll between questions.

The API is stateless from the client's point of view: it just keeps a tally and
an "epoch" token that changes on every reset, so a browser that already voted
stays locked until the next reset.

## Endpoints

All responses are JSON and mirror the previous client's contract.

| Request | Effect |
| --- | --- |
| `GET /feedback?t=positive` | Record a Yes vote, return the tally |
| `GET /feedback?t=negative` | Record a No vote, return the tally |
| `GET /feedback` / `GET /status` | Return the tally without voting |
| `GET /epoch` | Return the current epoch token (`"<hex>"`) |
| `GET /reset?p=<password>` | Reset the tally and rotate the epoch (`true`/`false`) |
| `GET /healthz` | Liveness probe |

Tally shape: `{"positive": <int>, "neutral": 0, "negative": <int>}` (`neutral`
is kept only for backward compatibility and is always `0`).

Every endpoint except `/healthz` and `/` requires the request to look like a
browser: a real `User-Agent` (curl/wget/python-requests/... are rejected), an
allow-listed `Origin` when present, and the `X-Feedback-Client: web` header that
the page sets. Votes are additionally capped **globally** (not per IP, so a whole
class behind one campus NAT IP can vote at once) and resets are capped per IP.

## Configuration

Copy `.env.example` to `.env` and edit it:

| Variable | Default | Meaning |
| --- | --- | --- |
| `FEEDBACK_PASSWORD` | *(empty)* | Password for `/reset`. Empty disables reset. |
| `ALLOWED_ORIGINS` | `https://introcp.github.io,http://localhost:3500` | Browser origins allowed by CORS. |
| `MAX_VOTES_PER_MINUTE` | `3000` | Global vote cap (not per IP, see note below). |
| `RESETS_PER_MINUTE` | `10` | Per-IP reset attempts limit (brute-force guard). |
| `STATE_FILE` | `/data/state.json` | Where the tally is persisted. |

## Run

```bash
cd feedback-server
cp .env.example .env   # then set FEEDBACK_PASSWORD and CLOUDFLARE_TUNNEL_TOKEN
docker compose up -d --build
```

Compose brings up two services:

- `feedback`: the API, listening on `:8000` inside the compose network and on
  host `127.0.0.1:8000` (debugging only).
- `tunnel`: `cloudflared` running the remotely-managed tunnel
  `tunnel --no-autoupdate run --token $CLOUDFLARE_TUNNEL_TOKEN`, which publishes
  the service as `feedback.nosec.it`.

TLS and the hostname live in the Cloudflare dashboard (Zero Trust > Networks >
Tunnels): the public hostname for the tunnel must target the **compose service**
`http://feedback:8000`, not `127.0.0.1` (each container has its own loopback).
Stop the tunnel with `docker compose stop tunnel` if you ever need to expose the
API another way.

### Alternative: host reverse proxy

Instead of the tunnel, the container can sit behind a TLS-terminating reverse
proxy on the host (then remove or stop the `tunnel` service). Example nginx
server block:

```nginx
server {
    listen 443 ssl;
    server_name feedback.nosec.it;

    ssl_certificate     /etc/letsencrypt/live/feedback.nosec.it/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/feedback.nosec.it/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Notes

- The tally is process-local state, so the image runs a **single** gunicorn
  worker; concurrency is handled with threads. Do not scale workers/replicas
  without moving the state to a shared store.
- The `feedback-data` volume keeps the tally across container restarts.
- The reset password travels in the query string (`/reset?p=`); it relies on TLS
  (provided by Cloudflare or the reverse proxy), so keep the endpoint behind
  HTTPS only.
- Client-side vote locking uses `localStorage`; a student who clears it can vote
  again. That matches the previous tool's "light filtering" approach.
- Vote limiting is global on purpose: students on university WiFi share a single
  public IP, so any per-IP vote limit would block the whole class after a few
  votes. Only the reset endpoint is per-IP limited.
