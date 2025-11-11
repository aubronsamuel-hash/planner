FROM python:3.12-slim

WORKDIR /app
COPY ../../.. /workspace
RUN pip install --no-cache-dir fastapi uvicorn

ENV PLANNER_JWT_SECRET="changeme" \
    PLANNER_ACCESS_TOKEN_MINUTES="15" \
    PLANNER_REFRESH_TOKEN_MINUTES="1440"

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
