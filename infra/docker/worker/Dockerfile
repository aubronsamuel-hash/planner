FROM python:3.12-slim

WORKDIR /workspace
COPY ../../.. /workspace
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ./backend

WORKDIR /workspace/backend

ENV PLANNER_REDIS_URL="redis://redis:6379/0" \
    PLANNER_WORKER_METRICS_PORT="9000"

CMD ["python", "-m", "backend.app.worker.main"]
