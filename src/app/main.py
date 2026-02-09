import asyncio
import logging
import sys
from src.infrastructure.grpc_server import start_grpc_server

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("heimdall.main")

async def main():
    logger.info("Initializing Heimdall Enterprise Engine...")
    try:
        await start_grpc_server()
    except Exception as e:
        logger.error(f"Failed to start gRPC server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service shut down by user")