# Pi Emulator DevOps — Monitoring Stack

Containerized observability for a Raspberry Pi 5:
- node-exporter (Pi system metrics)
- cAdvisor (container metrics)
- Prometheus (scrapes & stores)
- Grafana (dashboards)

Run:
```bash
cd monitoring
docker compose up -d
