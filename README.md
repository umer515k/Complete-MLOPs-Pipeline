# 🚀 End-to-End MLOps Pipeline

> From a single Python script to a fully monitored, auto-deploying, cloud-native ML system.

[![CI/CD Pipeline](https://github.com/umer515k/Complete-MLOPs-Pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/umer515k/Complete-MLOPs-Pipeline/actions/workflows/ci.yml)

---

## What This Is

This project is a production-grade MLOps platform built from scratch. It trains a sentiment analysis model, versions the data, serves predictions via a REST API, orchestrates containers with Kubernetes, automates deployments through CI/CD, and monitors everything with real-time dashboards.

Every layer was built intentionally — not just to work, but to demonstrate the kind of systems thinking that separates engineers who deploy code from engineers who run production systems.

---

## Architecture

### Full System Overview

```
Developer pushes code
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                  │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Test Job   │→ │  Build & Push│→ │  Deploy Job  │  │
│  │              │  │  Docker Hub  │  │              │  │
│  │ train model  │  │              │  │ SSH → EC2    │  │
│  │ pytest suite │  │ :latest tag  │  │ pull & run   │  │
│  │              │  │ :sha tag     │  │ new image    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│                    AWS EC2 (t2.micro)                    │
│                                                         │
│  Docker Container: mlops-pipeline:latest                │
│  ├── FastAPI server (port 8000)                         │
│  ├── /health   → health check                          │
│  ├── /predict  → sentiment inference                   │
│  └── /metrics  → Prometheus scrape endpoint            │
└─────────────────────────────────────────────────────────┘
        │                         │
        ▼                         ▼
┌──────────────┐         ┌─────────────────────┐
│  Kubernetes  │         │     Monitoring       │
│  (k3s local) │         │                     │
│              │         │  Prometheus (9090)   │
│  3 replicas  │         │  scrapes /metrics    │
│  self-healing│         │  every 15 seconds    │
│  load balance│         │         │            │
└──────────────┘         │         ▼            │
                         │  Grafana (3000)      │
                         │  dashboards &        │
                         │  alerting            │
                         └─────────────────────┘
```

### ML Pipeline

```
Raw Data (IMDB 50k reviews)
        │
        ▼ DVC tracks version
┌───────────────────┐
│  data/imdb.json   │ ←── stored in S3
│  (versioned)      │     pointer in git
└───────────────────┘
        │
        ▼ training/train.py
┌─────────────────────────────────────┐
│           MLflow Experiment          │
│                                     │
│  Run 1: Logistic Regression         │
│  Run 2: Naive Bayes                 │
│  Run 3: Linear SVM                  │
│                                     │
│  Logs: accuracy, precision,         │
│        recall, F1 per run           │
└─────────────────────────────────────┘
        │
        ▼ best model saved
┌───────────────────┐
│ sentiment_model   │
│      .pkl         │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  FastAPI + Docker │
│  /predict endpoint│
└───────────────────┘
```

### CI/CD Flow

```
git push → GitHub Actions
               │
               ├─ Job 1: Test
               │    ├─ pip install requirements
               │    ├─ python training/train.py
               │    └─ pytest tests/ -v
               │         │
               │    (must pass)
               │
               ├─ Job 2: Build & Push
               │    ├─ train model
               │    ├─ docker build
               │    └─ push to Docker Hub
               │         :latest
               │         :<commit-sha>
               │         │
               │    (must pass)
               │
               └─ Job 3: Deploy (main branch only)
                    ├─ SSH into EC2
                    ├─ docker pull latest
                    ├─ stop old container
                    └─ start new container
                         --restart unless-stopped
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **ML Model** | scikit-learn (TF-IDF + 3 classifiers) | Sentiment classification |
| **Experiment Tracking** | MLflow | Track runs, metrics, model versions |
| **Data Versioning** | DVC + AWS S3 | Version datasets, reproducible training |
| **API** | FastAPI + Uvicorn | Serve predictions, expose metrics |
| **Containerization** | Docker | Package app + model |
| **Orchestration** | Kubernetes (k3s) | Replicas, self-healing, load balancing |
| **CI/CD** | GitHub Actions | Automated test → build → deploy |
| **Image Registry** | Docker Hub | Store versioned Docker images |
| **Infrastructure** | Terraform | Infrastructure as code on AWS |
| **Cloud** | AWS EC2 | Live production server |
| **Metrics** | Prometheus | Scrape and store time-series metrics |
| **Dashboards** | Grafana | Visualize request rate, latency, errors |

---

## Project Structure

```
mlops-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml                  # Full CI/CD pipeline
├── app/
│   ├── main.py                     # FastAPI app with /predict, /health, /metrics
│   └── requirements.txt            # App dependencies
├── data/
│   ├── prepare.py                  # Download and save IMDB dataset
│   └── imdb.json.dvc               # DVC pointer (actual data in S3)
├── k8s/
│   ├── deployment.yaml             # 3 replicas, liveness/readiness probes
│   └── service.yaml                # NodePort service
├── model/
│   └── sentiment_model.pkl         # Best trained model (generated)
├── monitoring/
│   ├── docker-compose.yml          # Prometheus + Grafana stack
│   └── prometheus.yml              # Scrape config pointing at EC2
├── terraform/
│   ├── main.tf                     # EC2, security group, SSH key pair
│   ├── variables.tf                # Region, instance type, port
│   └── outputs.tf                  # Server IP and app URL
├── training/
│   ├── train.py                    # Train 3 models, log to MLflow, save best
│   └── requirements.txt            # Training dependencies
├── tests/
│   └── test_api.py                 # API contract tests
├── Dockerfile                      # Container definition
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Docker
- Terraform
- AWS CLI + account
- Git

### Local Setup

```bash
# Clone
git clone https://github.com/umer515k/Complete-MLOPs-Pipeline.git
cd Complete-MLOPs-Pipeline

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r training/requirements.txt
pip install -r app/requirements.txt

# Train model (runs 3 experiments, logs to MLflow, saves best)
python training/train.py

# View MLflow experiment results
mlflow ui
# Open http://localhost:5000

# Start API
uvicorn app.main:app --reload
# Open http://localhost:8000/docs
```

### Docker

```bash
docker build -t mlops-pipeline:v1 .
docker run -p 8000:8000 mlops-pipeline:v1
```

### Kubernetes (k3s)

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods   # should show 3 running replicas
```

### Infrastructure (Terraform)

```bash
cd terraform
terraform init
terraform plan
terraform apply
# Outputs server IP and app URL
```

### Monitoring Stack

```bash
cd monitoring
docker compose up -d
# Prometheus → http://localhost:9090
# Grafana    → http://localhost:3000 (admin/admin)
```

---

## CI/CD Pipeline

Every push to `main` triggers three jobs in sequence. PRs trigger Test and Build but never Deploy. Only merges to `main` ship to production.

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `EC2_HOST` | Public IP of EC2 instance |
| `EC2_USER` | SSH username (`ec2-user`) |
| `EC2_SSH_KEY` | Private SSH key |
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

---

## ML Experiments

Three models trained and compared on every run via MLflow.

| Model | Accuracy | F1 Score |
|---|---|---|
| Logistic Regression | ~0.89 | ~0.89 |
| Naive Bayes | ~0.85 | ~0.85 |
| Linear SVM | ~0.90 | ~0.90 |

Best model by F1 score is automatically saved and used for serving.

---

## Data Versioning

Dataset tracked with DVC, stored in S3. To reproduce:

```bash
dvc pull   # fetches imdb.json from S3
```

Every model is traceable to the exact dataset version it trained on.

---

## API Reference

### `GET /health`
```bash
curl http://SERVER_IP:8000/health
# {"status": "ok"}
```

### `POST /predict`
```bash
curl -X POST http://SERVER_IP:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is absolutely amazing"}'
# {"text": "...", "sentiment": "positive", "confidence": 0.923}
```

### `GET /metrics`
Prometheus-format metrics endpoint scraped every 15 seconds.

### `GET /docs`
Interactive Swagger UI — test the API in the browser.

---

## Monitoring

Prometheus scrapes `/metrics` from the live EC2 deployment every 15 seconds.

Grafana dashboards track:
- Requests per second
- 95th percentile latency
- Total request count
- Requests by endpoint

---

## Lessons Learned

This project involved real production debugging — not just following tutorials:

- k3s v1.35 dropped cgroup v1 support, requiring a version downgrade to v1.28
- GitHub Secret scanning blocked pushes containing AWS credentials, requiring full git history rewriting with `git filter-branch`
- Prometheus couldn't scrape FastAPI from inside Docker because uvicorn was bound to `127.0.0.1` — fixed with `--host 0.0.0.0`
- `prometheus-fastapi-instrumentator` uses Python 3.9+ syntax, breaking on Python 3.8 venvs — fixed by pinning to v5.9.1
- Terraform's security group config silently dropped port 22 when adding new ingress rules — SSH locked out, fixed via AWS CLI

These weren't tutorial problems. They were real infrastructure failures with real root causes.

---

## Roadmap

- [x] FastAPI model serving
- [x] Docker containerization
- [x] GitHub Actions CI pipeline
- [x] Docker Hub image registry
- [x] Terraform infrastructure as code
- [x] AWS EC2 deployment
- [x] Automated CD via GitHub Actions
- [x] Kubernetes orchestration (k3s)
- [x] MLflow experiment tracking
- [x] DVC data versioning with S3
- [x] Prometheus metrics
- [x] Grafana dashboards
- [ ] Canary deployments
- [ ] Data drift detection
- [ ] PR performance bot
