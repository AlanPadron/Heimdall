from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class MetricType(str, Enum):
    COUNTER = "counter"    # Para cosas que solo suben (ej. total de peticiones)
    GAUGE = "gauge"        # Para valores que suben y bajan (ej. uso de CPU)
    HISTOGRAM = "histogram" # Para observar latencias

@dataclass(frozen=True) # Frozen lo hace inmutable, procesamiento de flujos
class MetricReading:
    service_name: str
    metric_name: str
    value: float
    type: str = "generic"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    id: UUID = field(default_factory=uuid4)
    labels: dict[str, str] = field(default_factory=dict) # Ej: {"env": "prod", "region": "us-east-1"}