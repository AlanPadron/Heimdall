# Heimdall: Intelligent Monitoring & Anomaly Detection (Beta 1.0.2) By Alan Padron

Heimdall is a distributed monitoring system designed to detect behavioral deviations in real-time metrics. It uses a microservices architecture to process data via gRPC and applies statistical analysis to identify anomalies.

## Core Features
- **Real-time Processing**: High-performance gRPC server for metric ingestion.
- **Statistical Analysis**: Anomaly detection engine based on Z-Score (Standard Deviation).
- **Time-Series Storage**: Optimized data persistence using TimescaleDB (PostgreSQL).
- **Containerized**: Fully orchestrated environment using Docker and Docker Compose.

## Tech Stack
- **Language**: Python 3.10+
- **Communication**: gRPC / Protocol Buffers
- **Database**: TimescaleDB (PostgreSQL)
- **Infrastructure**: Docker / Docker Compose

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.x (for local testing)

### Installation & Deployment
1. Clone the repository:
   ```bash
   git clone [https://github.com/AlanPadron/Heimdall.git](https://github.com/AlanPadron/Heimdall.git)
   cd Heimdall
