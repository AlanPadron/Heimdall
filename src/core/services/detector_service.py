import logging
import os
from datetime import datetime
from src.core.interfaces.repositories import IMetricRepository
from src.domain.anomaly_detector import AnomalyDetector
from src.core.entities.metric import MetricReading

# Códigos de color ANSI para la terminal
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

audit_logger = logging.getLogger("heimdall.audit")
audit_logger.setLevel(logging.INFO)

if not audit_logger.handlers:
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler("logs/audit_system.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s'))
    audit_logger.addHandler(file_handler)
    # También enviamos a consola para el video
    audit_logger.addHandler(logging.StreamHandler())

class DetectorService:
    def __init__(self, repository: IMetricRepository):
        self.repository = repository
        self.detector = AnomalyDetector(threshold=3.0)

    async def process_metric(self, service_name: str, value: float) -> tuple[bool, str]:
        metric = MetricReading(
            service_name=service_name, 
            metric_name="performance", 
            value=value,
            timestamp=datetime.utcnow(),
            type="gauge"
        )
        await self.repository.save(metric)
        history = await self.repository.get_history(service_name, "performance")
        
        is_anomaly = self.detector.is_anomalous(value, history)
        
        if is_anomaly:
            status = "CRITICAL"
            color = RED
            msg = f"{color}[{status}] - {service_name} - Value: {value} - ANOMALY DETECTED{RESET}"
        else:
            status = "NORMAL"
            color = GREEN
            msg = f"{color}[{status}] - {service_name} - Value: {value} - HEALTHY{RESET}"
            
        audit_logger.info(msg)
        return is_anomaly, msg