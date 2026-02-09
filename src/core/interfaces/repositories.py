from abc import ABC, abstractmethod
from src.core.entities.metric import MetricReading

class IMetricRepository(ABC):
    @abstractmethod
    async def save(self, metric: MetricReading) -> None:
        pass

    @abstractmethod
    async def get_history(self, service_name: str, metric_name: str, limit: int = 20) -> list[float]:
        pass