import asyncio
import random
import time
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

async def send_burst(stub, burst_id):
    """Envía una ráfaga de métricas lo más rápido posible."""
    # 70% de probabilidad de anomalía para impacto visual en el log
    is_anomaly = random.random() < 0.70
    
    if is_anomaly:
        val = float(random.uniform(1000.0, 5000.0))
        service = "CRITICAL-APP"
    else:
        val = float(random.uniform(10.0, 50.0))
        service = "STABLE-APP"

    try:
        await stub.SendMetric(MetricRequest(service_name=service, value=val))
    except Exception:
        pass

async def main():
    async with Channel('127.0.0.1', 50051) as chan:
        stub = MetricsServiceStub(chan)
        total_metrics = 500  # Incrementamos a 500 para una ráfaga larga
        batch_size = 10      # Enviamos de 10 en 10 simultáneamente
        
        print(f"Iniciando Stress Test Masivo: {total_metrics} métricas (70% Anomalías)")
        start_time = time.time()

        for i in range(0, total_metrics, batch_size):
            tasks = [send_burst(stub, j) for j in range(batch_size)]
            await asyncio.gather(*tasks)
            # Pequeña pausa de 0.01s para que la terminal no se congele 
            # y se vea el scroll de colores a toda velocidad
            await asyncio.sleep(0.01)

        end_time = time.time()
        duration = end_time - start_time
        print(f"Test finalizado en {duration:.2f} segundos.")
        print(f"Throughput: {total_metrics / duration:.2f} métricas por segundo.")

if __name__ == "__main__":
    asyncio.run(main())