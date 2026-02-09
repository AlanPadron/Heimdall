CREATE TABLE IF NOT EXISTS metrics (
    id SERIAL,
    service_name VARCHAR(50) NOT NULL,
    metric_name VARCHAR(50) NOT NULL,
    value FLOAT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Convertir la tabla en una Hypertable de TimescaleDB
SELECT create_hypertable('metrics', 'timestamp', if_not_exists => TRUE);

-- Crear índices adicionales para mejorar el rendimiento del historial
CREATE INDEX IF NOT EXISTS ix_service_metric_time 
ON metrics (service_name, metric_name, timestamp DESC);