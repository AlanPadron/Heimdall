import asyncio
import random
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

async def send_load():
    async with Channel('127.0.0.1', 50051) as chan:
        stub = MetricsServiceStub(chan)
        print("Iniciando flujo de 100 métricas con 40% de probabilidad de anomalía...")
        
        for i in range(1, 101):
            # 60% probabilidad Normal (45-55), 40% probabilidad Anomalía (750-999)
            is_anomaly = random.random() < 0.40
            
            if not is_anomaly:
                val = float(random.uniform(45.0, 55.0))
                tag = "NORMAL"
            else:
                val = float(random.uniform(750.0, 999.0))
                tag = "CRITICAL"
            
            # Envío vía gRPC
            await stub.SendMetric(MetricRequest(service_name='PROD-SERVER', value=val))
            
            print(f"Métrica {i:03}/100 | Valor: {val:.2f} | Tag: {tag}")
            
            # 100ms de pausa: lo suficientemente rápido para verse "pro", 
            # pero lento para que el ojo humano siga el cambio de color.
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(send_load())