import asyncio
import logging
from grpclib.server import Server
from grpclib.const import Status
from grpclib.exceptions import GRPCError

from src.infrastructure.proto.metrics_grpc import MetricsServiceBase
from src.infrastructure.proto.metrics_pb2 import MetricResponse

from src.infrastructure.database.config import async_session_factory
from src.infrastructure.database.repository import TimescaleMetricRepository
from src.core.services.detector_service import DetectorService

logger = logging.getLogger(__name__)

class MetricsHandler(MetricsServiceBase):
    async def SendMetric(self, stream):
        try:
            request = await stream.recv_message()
            if request is None:
                return

            logger.info(f"GRPC_INPUT: {request.service_name} -> {request.value}")

            async with async_session_factory() as session:
                repo = TimescaleMetricRepository(session)
                service = DetectorService(repo)
                
                is_anomaly, message = await service.process_metric(
                    request.service_name, 
                    request.value
                )

            if is_anomaly:
                logger.warning(message)
            else:
                logger.info(message)

            await stream.send_message(MetricResponse(
                success=True, 
                message=message
            ))

        except Exception as e:
            logger.error(f"FLOW_ERROR: {e}")
            raise GRPCError(Status.INTERNAL, str(e))

async def start_grpc_server():
    handler = MetricsHandler()
    server = Server([handler])
    await server.start('0.0.0.0', 50051)
    logger.info("Heimdall Engine listening on port 50051")
    await server.wait_closed()