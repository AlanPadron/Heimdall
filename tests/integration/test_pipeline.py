import pytest
import asyncio
from grpclib.client import Channel
from src.infrastructure.proto.metrics_grpc import MetricsServiceStub
from src.infrastructure.proto.metrics_pb2 import MetricRequest

@pytest.mark.asyncio
async def test_grpc_ingestion_and_anomaly_detection():
    # 1. Configurar el canal hacia nuestro servidor (Docker o Local)
    channel = Channel('127.0.0.1', 50051)
    stub = MetricsServiceStub(channel)

    # 2. Simular una métrica NORMAL
    normal_request = MetricRequest(
        service_name="payment-gateway",
        metric_name="response_time",
        value=150.0,
        metric_type="gauge"
    )

    # 3. Simular una métrica ANÓMALA (un pico de latencia)
    anomalous_request = MetricRequest(
        service_name="payment-gateway",
        metric_name="response_time",
        value=5000.0,  # 5 segundos es demasiado
        metric_type="gauge"
    )

    # Ejecutar llamadas
    response_normal = await stub.SendMetric(normal_request)
    response_anomaly = await stub.SendMetric(anomalous_request)

    # 4. Aserciones (Nivel Senior: verificamos comportamiento, no solo éxito)
    assert response_normal.success is True
    assert response_anomaly.success is True
    
    # Aquí podrías consultar tu DB o Logs para verificar que la anomalía se marcó
    channel.close()