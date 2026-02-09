import asyncio
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

async def run_demo(service, value, scenario_name):
    async with Channel('127.0.0.1', 50051) as channel:
        stub = MetricsServiceStub(channel)
        print(f"--- ESCENARIO: {scenario_name} ---")
        print(f"SOLICITUD: Service={service}, Value={value}")
        
        try:
            response = await stub.SendMetric(MetricRequest(
                service_name=service,
                value=value
            ))
            
            print(f"RESPUESTA_MOTOR: {response.message}")
            # Usamos el campo detectado 'anomali'
            print(f"ESTADO_ANOMALIA: {response.anomali}")
            print("-" * 30)
            
        except Exception as e:
            print(f"ERROR_TECNICO: {e}")

async def main():
    # Escenario 1: Operacion normal
    await run_demo("AUTH-API", 42.0, "OPERACION_NORMAL")
    
    await asyncio.sleep(2) 
    
    # Escenario 2: Pico critico
    # Usamos 9999.0 para asegurar que la desviacion sea detectada
    await run_demo("CORE-DB", 9999.0, "DETECCION_ANOMALIA_CRITICA")

if __name__ == "__main__":
    asyncio.run(main())