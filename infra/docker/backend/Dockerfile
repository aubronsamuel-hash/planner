FROM python:3.12-slim

WORKDIR /workspace
COPY ../../.. /workspace
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ./backend

ENV PLANNER_JWT_SECRET="changeme" \
    PLANNER_ACCESS_TOKEN_MINUTES="15" \
    PLANNER_REFRESH_TOKEN_MINUTES="1440" \
    PLANNER_REDIS_URL="redis://redis:6379/0"

WORKDIR /workspace/backend

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
