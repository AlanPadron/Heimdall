from sqlalchemy import select, insert, desc
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.interfaces.repositories import IMetricRepository
from src.core.entities.metric import MetricReading
from .models import MetricModel

class TimescaleMetricRepository(IMetricRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, metric: MetricReading) -> None:
        try:
            stmt = insert(MetricModel).values(
                service_name=metric.service_name,
                metric_name=metric.metric_name,
                value=metric.value,
                timestamp=metric.timestamp
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def get_history(self, service_name: str, metric_name: str, limit: int = 20) -> list[float]:
        try:
            query = (
                select(MetricModel.value)
                .where(MetricModel.service_name == service_name)
                .where(MetricModel.metric_name == metric_name)
                .order_by(desc(MetricModel.timestamp))
                .limit(limit)
            )
            
            result = await self.session.execute(query)
            return [float(v) for v in result.scalars().all()]
        except Exception:
            return []