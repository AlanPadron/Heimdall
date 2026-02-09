import asyncio
import random
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

async def send_continuous_metrics():
    async with Channel('127.0.0.1', 50051) as channel:
        stub = MetricsServiceStub(channel)
        service = "e-commerce-api"
        
        print(f"🚀 Enviando ráfaga de datos para {service}...")
        
        for i in range(1, 101):
            # Comportamiento normal: entre 40 y 60ms de latencia
            value = random.uniform(40.0, 60.0)
            
            # Forzar una anomalía cada 25 registros
            if i % 25 == 0:
                value = random.uniform(200.0, 350.0)
                print(f"⚠️  Inyectando anomalía en envío {i}...")

            await stub.SendMetric(MetricRequest(
                service_name=service,
                value=value
            ))
            
            if i % 10 == 0:
                print(f"✅ {i} métricas enviadas...")
            
            await asyncio.sleep(0.05) # Simula flujo constante

if __name__ == "__main__":
    asyncio.run(send_continuous_metrics())