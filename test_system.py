import asyncio
import random
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

async def run_test():
    async with Channel('127.0.0.1', 50051) as channel:
        stub = MetricsServiceStub(channel)
        service = "payment-gateway"
        
        print(f"Iniciando test para: {service}")
        
        # 1. Enviamos 10 métricas normales para calibrar el Z-Score
        for i in range(10):
            value = random.uniform(100.0, 105.0)
            response = await stub.SendMetric(MetricRequest(
                service_name=service,
                value=value
            ))
            print(f"[ENVÍO {i+1}] Valor: {value:.2f} | Respuesta: {response.message}")
            await asyncio.sleep(0.1)

        # 2. Enviamos la anomalía (un pico repentino)
        print("\n--- Lanzando pico de tráfico (Anomalía) ---")
        anomaly_value = 450.0
        response = await stub.SendMetric(MetricRequest(
            service_name=service,
            value=anomaly_value
        ))
        print(f"[RESULTADO] Valor: {anomaly_value} | Respuesta: {response.message}")

if __name__ == "__main__":
    asyncio.run(run_test())