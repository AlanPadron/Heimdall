# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv pip install --system --no-cache -r pyproject.toml

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

# No correr como root por seguridad
RUN useradd -m heimdall
USER heimdall

CMD ["python", "src/app/main.py"]