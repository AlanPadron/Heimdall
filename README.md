# Heimdall: Enterprise Observability & Attack Detection Engine By Alan Padron 2026
**Version:** 1.8 Beta (Attack Detector Update)

Heimdall es un motor de monitoreo de alta disponibilidad diseñado para la ingesta masiva de métricas, análisis estadístico de anomalías y detección de vectores de ataque en tiempo real. Esta versión se centra en la resiliencia del sistema ante condiciones de estrés extremo y la soberanía de los datos mediante logs de auditoría locales.

---

## 🚀 Release Highlights: v1.8 Attack Detector Update

Esta actualización transforma el motor en una herramienta de seguridad activa con las siguientes capacidades:

* **Soberanía de Datos (In-House Logging):** Implementación de un sistema de auditoría local que elimina la dependencia de servicios externos, garantizando la privacidad corporativa.
* **Resiliencia DDoS:** Motor optimizado mediante procesos asíncronos para manejar ráfagas superiores a 2,000 RPS (Requests Per Second).
* **Detección de Anomalías Local:** Algoritmo de análisis estadístico (Z-Score) integrado para la clasificación inmediata de estados: `NORMAL`, `WARNING` y `CRITICAL`.
* **Multi-tenant Audit Logs:** Registro de auditoría con segregación por servicio y priorización visual mediante códigos de color ANSI para una respuesta rápida del equipo DevOps.

---

## 🛠 Technical Stack

* **Protocolo:** gRPC (Protocol Buffers) para comunicación de ultra-baja latencia.
* **Lenguaje:** Python 3.12+ (Asyncio stack).
* **Base de Datos:** TimescaleDB (PostgreSQL optimizado para series temporales).
* **Infraestructura:** Docker & Docker Compose para despliegue escalable.
* **Visualización:** Grafana Enterprise para dashboards de observabilidad.

---

## 🧪 Infrastructure Analysis & Security Testing

Para validar la estabilidad de la versión 1.8, el sistema ha sido sometido a los siguientes protocolos de estrés:

### 1. Simulación de Ataque Volumétrico (DDoS)
Se ejecutó una inundación de métricas (Metric Flooding) de 2,000 peticiones concurrentes sobre el componente `EDGE-LOAD-BALANCER`. El motor mantuvo la integridad operativa y clasificó el 100% de la carga como crítica de forma instantánea.

### 2. High-Density Stress Test (70% Anomaly Injection)
Evaluación de throughput bajo saturación de CPU, inyectando una carga donde el 70% de los datos representaban desviaciones críticas. Se validó la eficiencia de la escritura en TimescaleDB y la generación de logs en tiempo real.

### 3. Context Isolation Test
Validación de la lógica de negocio procesando múltiples microservicios (`AUTH-API`, `CORE-DB`, `PAYMENT-GATEWAY`) de forma simultánea, asegurando que el motor mantiene líneas base estadísticas independientes por cada servicio.

---

## 📊 Audit System Output

El sistema de auditoría interna genera reportes de estado inmediatos y visuales directamente en el flujo del contenedor:

```text
2026-02-09 20:25:01 | [NORMAL]   - AUTH-API - Value: 42.0 - Status: Healthy
2026-02-09 20:25:05 | [CRITICAL] - CORE-DB  - Value: 9999.0 - ANOMALY DETECTED
