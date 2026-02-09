import asyncio
import logging
from grpclib.server import Server
from grpclib.const import Status
from grpclib.exceptions import GRPCError

# Imports de Protocol Buffers

from src.infrastructure.proto.metrics_grpc import MetricsServiceBase
from src.infrastructure.proto.metrics_pb2 import MetricResponse


from src.domain.anomaly_detector import AnomalyDetector

# Configuración de logs para ver la magia en la terminal de Docker
logger = logging.getLogger(__name__)

class MetricsHandler(MetricsServiceBase):
    def __init__(self):
        #detector con un umbral de 3 desviaciones estándar
        self.detector = AnomalyDetector(threshold=3.0)
        logger.info("✅ Handler de Métricas listo y vinculado a AnomalyDetector")

    async def SendMetric(self, stream):
        try:
            #  Recibir el mensaje gRPC
            request = await stream.recv_message()
            if request is None:
                return

            logger.info(f"📥 Recibido: {request.service_name} -> {request.value}")

        
            mock_history = [10.5, 12.0, 11.8, 12.2, 11.9, 12.1]

         
            is_anomaly = self.detector.is_anomalous(
                current_value=request.value, 
                history=mock_history
            )

          #logica de respuesta basada en el resultado del detector
            if is_anomaly:
                logger.warning(f"🚨 ANOMALÍA detectada en {request.service_name}: {request.value}")
                msg = f"Alerta de Heimdall: El valor {request.value} es una anomalía crítica."
            else:
                logger.info(f"✨ Métrica normal en {request.service_name}")
                msg = "Comportamiento dentro de los parámetros normales."

            # Enviar la respuesta gRPC al cliente (test_heimdall.py)
            await stream.send_message(MetricResponse(
                success=True, 
                message=msg
            ))

        except Exception as e:
            logger.error(f"❌ Error procesando métrica: {e}")
            import traceback
            traceback.print_exc()
            raise GRPCError(Status.INTERNAL, f"Error interno: {str(e)}")


async def start_grpc_server():
    handler = MetricsHandler()
    server = Server([handler])
    
    # 0.0.0.0 es fundamental para Docker
    await server.start('0.0.0.0', 50051)
    print("🚀 Servidor gRPC de Heimdall escuchando en el puerto 50051")
    
    await server.wait_closed()