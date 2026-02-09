import asyncio
import random
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

async def send_multiservice_load():
    async with Channel('127.0.0.1', 50051) as chan:
        stub = MetricsServiceStub(chan)
        services = {
            "PAYMENT-GATEWAY": {"min": 200, "max": 250, "anomaly": 1500},
            "INVENTORY-API": {"min": 50, "max": 70, "anomaly": 500},
            "LEGACY-AUTH": {"min": 10, "max": 20, "anomaly": 200}
        }

        print("Iniciando Monitoreo Multi-Servicio...")
        
        for i in range(60): # 60 ráfagas de métricas
            for s_name, s_config in services.items():
                # Decisión aleatoria de anomalía por servicio
                if random.random() < 0.15: # 15% de probabilidad de fallo por servicio
                    val = float(s_config["anomaly"] + random.uniform(0, 100))
                else:
                    val = float(random.uniform(s_config["min"], s_config["max"]))
                
                await stub.SendMetric(MetricRequest(service_name=s_name, value=val))
            
            await asyncio.sleep(0.2) # Velocidad de crucero para el video

if __name__ == "__main__":
    asyncio.run(send_multiservice_load())