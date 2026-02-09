import asyncio
import logging

# Importamos la función desde la infraestructura
from src.infrastructure.grpc_server import start_grpc_server

# Configuración básica de logs para ver qué pasa en Docker
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("🛡️ Iniciando Motor Heimdall...")
    try:
        # Arrancamos el servidor gRPC
        await start_grpc_server()
    except Exception as e:
        logger.error(f"❌ Fallo fatal en el main: {e}")

if __name__ == "__main__":
    asyncio.run(main())