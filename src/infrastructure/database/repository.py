from sqlalchemy.ext.asyncio import AsyncSession
from src.core.interfaces.repositories import IMetricRepository
from src.core.entities.metric import MetricReading

class TimescaleMetricRepository(IMetricRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, metric: MetricReading) -> None:
        # Aquí iría el mapeo de la entidad Core a la tabla de la DB
        # Un Senior usa 'insert(...).values(...)' para alto rendimiento
        pass

    async def get_history(self, service_name: str, metric_name: str, limit: int = 20) -> list[float]:
        # Consulta asíncrona para obtener los últimos valores
        return [10.5, 12.0, 11.5, 30.0, 11.0] # Mock por ahora