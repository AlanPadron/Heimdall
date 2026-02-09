import asyncio
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

async def warm():
    async with Channel('127.0.0.1', 50051) as chan:
        stub = MetricsServiceStub(chan)
        print("Cargando historial base para CORE-DB y AUTH-API...")
        
        # Enviamos 10 datos normales para cada servicio
        for _ in range(10):
            await stub.SendMetric(MetricRequest(service_name='CORE-DB', value=50.0))
            await stub.SendMetric(MetricRequest(service_name='AUTH-API', value=40.0))
        
        print("Historial cargado correctamente. El motor ya puede detectar anomalias.")

if __name__ == "__main__":
    asyncio.run(warm())