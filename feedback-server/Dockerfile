FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

# State (tally + epoch) lives here; mount a volume to survive container restarts.
RUN useradd --create-home --uid 1000 feedback \
    && mkdir -p /data \
    && chown feedback:feedback /data
USER feedback

VOLUME ["/data"]
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2)"

# One worker on purpose: the tally is process-local state, so workers must not
# be forked. Threads handle concurrent votes.
CMD ["gunicorn", "--workers", "1", "--threads", "8", \
     "--bind", "0.0.0.0:8000", "--access-logfile", "-", "app:app"]
