FROM python:3.11-slim as builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv pip install --system --no-cache -r pyproject.toml

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

# Configuración de entorno y permisos
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN useradd -m heimdall && \
    mkdir -p /app/logs && \
    chown -R heimdall:heimdall /app

USER heimdall

CMD ["python", "-m", "src.app.main"]