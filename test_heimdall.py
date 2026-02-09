import asyncio
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

async def send_test():
    # Conectamos al puerto que mapeamos en docker-compose
    async with Channel('127.0.0.1', 50051) as channel:
        stub = MetricsServiceStub(channel)

        print("📡 Enviando métrica sospechosa a Heimdall...")
        response = await stub.SendMetric(MetricRequest(
            service_name="auth-service",
            metric_name="response_time",
            value=5000.0,  # Un valor alto para forzar la anomalía
            metric_type="gauge"
        ))
        print(f"✅ Respuesta de Heimdall: {response.message}")

if __name__ == '__main__':
    asyncio.run(send_test())

