import asyncio
import time
import random
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

async def attack_request(stub):
    """Simula una petición maliciosa de botnet"""
    try:
        # Los ataques DDoS suelen enviar valores basura o extremos
        await stub.SendMetric(MetricRequest(
            service_name="EDGE-LOAD-BALANCER", 
            value=float(random.randint(5000, 9999))
        ))
    except Exception:
        pass

async def simulate_ddos():
    async with Channel('127.0.0.1', 50051) as chan:
        stub = MetricsServiceStub(chan)
        
        total_requests = 2000
        batch_size = 50  # 50 peticiones simultáneas por ráfaga
        
        print(f"ALERTA: Iniciando simulación de ataque DDoS sobre EDGE-LOAD-BALANCER")
        print(f"Enviando {total_requests} peticiones concurrentes...")
        
        start_time = time.time()

        for i in range(0, total_requests, batch_size):
            tasks = [attack_request(stub) for _ in range(batch_size)]
            await asyncio.gather(*tasks)
            # Sin pausa o pausa mínima para simular inundación real
            await asyncio.sleep(0.001)

        duration = time.time() - start_time
        rps = total_requests / duration
        print(f"\n--- REPORTE DE ATAQUE ---")
        print(f"Duración: {duration:.2f} segundos")
        print(f"Carga generada: {rps:.2f} Peticiones por segundo (RPS)")
        print(f"Estado del motor: Operativo")

if __name__ == "__main__":
    asyncio.run(simulate_ddos())