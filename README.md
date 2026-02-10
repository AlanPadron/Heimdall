<p align="center">
  <img src="docs/logo.png" alt="Heimdall Logo" width="200">
</p>

# Heimdall: Enterprise Observability & Attack Detection Engine


# Heimdall: Enterprise Observability & Attack Detection Engine By Alan Padron

# HEIMDALL: Observability & Identity Engine (Beta 1.8.1)

I have integrated key functional layers to the project, enabling the system to operate in a distributed environment.

### What was added in this version:
* **Technician Detection System:** Added a networking layer. The engine now broadcasts live alerts to remote agents via TCP Sockets.
* **Technician Management System:** Implemented an IAM module for security tokens. Provisioning or revoking access for technical personnel is now possible in real-time.
* **Actionable Telemetry:** Refined alert format delivering forensic diagnostics and immediate mitigation steps.
---

## Technical Specifications: v1.8 Attack Detector Update

This update transitions the engine into an active security tool with the following capabilities:

* **Data Sovereignty (In-House Logging):** Implementation of a local audit system that eliminates dependency on external services, ensuring corporate privacy and compliance.
* **DDoS Resilience:** Engine optimized via asynchronous processes to handle bursts exceeding 2,000 RPS (Requests Per Second).
* **Local Anomaly Detection:** Integrated Z-Score statistical analysis for immediate state classification: `NORMAL`, `WARNING`, and `CRITICAL`.
* **Multi-tenant Audit Logs:** Audit logs with service-level segregation and visual prioritization via ANSI color codes for rapid DevOps response.

---

## Technical Stack

* **Protocol:** gRPC (Protocol Buffers) for ultra-low latency communication.
* **Language:** Python 3.12+ (Asyncio stack).
* **Database:** TimescaleDB (PostgreSQL optimized for time-series).
* **Infrastructure:** Docker & Docker Compose for scalable deployment.
* **Visualization:** Grafana Enterprise for observability dashboards.

---

## Infrastructure Analysis & Security Testing

To validate the stability of version 1.8, the system was subjected to the following stress protocols:

### 1. Volumetric Attack Simulation (DDoS)
A Metric Flooding attack of 2,000 concurrent requests was executed against the `EDGE-LOAD-BALANCER` component. The engine maintained operational integrity and classified 100% of the load as critical instantaneously.

### 2. High-Density Stress Test (70% Anomaly Injection)
Throughput evaluation under CPU saturation, injecting a load where 70% of data represented critical deviations. Validated TimescaleDB write efficiency and real-time log generation.

### 3. Context Isolation Test
Validation of business logic by processing multiple microservices (`AUTH-API`, `CORE-DB`, `PAYMENT-GATEWAY`) simultaneously, ensuring the engine maintains independent statistical baselines for each service.

---

## Audit System Output

The internal audit system generates immediate visual status reports directly within the container stream:

```text
2026-02-09 20:25:01 | [NORMAL]   - AUTH-API - Value: 42.0 - Status: Healthy
2026-02-09 20:25:05 | [CRITICAL] - CORE-DB  - Value: 9999.0 - ANOMALY DETECTED
