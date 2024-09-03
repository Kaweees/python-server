# syntax=docker/dockerfile:1
# Use full image for building virtualenv/installing requirements
FROM python:3.9 AS base-image

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Smaller runtime image for running the application
FROM python:3.9-slim AS runtime-image

COPY --from=base-image /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . /app/

WORKDIR /app

EXPOSE 8000

# Run server through the nv-otel entry point for auto-instrumentation
# Assumes OTEL_SERVICE_NAME and OTEL_NVAUTH_TOKEN have environment variables been set
CMD ["nv-otel", "uvicorn", "batch_status_api.main:app", "--host", "0.0.0.0", "--port", "8000"]


