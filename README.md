# 🚀 AI Financial Intelligence Platform

> A production-style AI-powered financial market intelligence platform built with **FastAPI**, **TimescaleDB**, **Docker**, and **LLMs**, designed to provide real-time market data, historical analytics, and AI-driven financial insights.

---

# 📖 Overview

The AI Financial Intelligence Platform is an end-to-end backend system designed using enterprise software engineering practices.

The platform currently provides:

- 📈 Real-time market data retrieval
- 🪙 Generic instrument support (Gold, Forex, Futures)
- 🔍 Instrument discovery API
- 🐳 Fully containerised local development
- 🗄️ PostgreSQL + TimescaleDB
- 🔄 Alembic database migrations
- ❤️ Health & readiness endpoints

The long-term goal is to evolve the platform into an AI-powered financial research and decision-support system capable of market analysis, sentiment analysis, forecasting, and agentic workflows.

---

# 🏗️ System Architecture

```text
                        Browser / Swagger
                                │
                                ▼
                        FastAPI Backend
                                │
        ┌───────────────────────┼────────────────────────┐
        ▼                       ▼                        ▼
   Health API             Market API             Instruments API
        │                       │                        │
        ▼                       ▼                        ▼
Database Health          Market Service        Instrument Service
        │                       │                        │
        └───────────────┬───────┴────────────────────────┘
                        ▼
                Provider Resolver
                        │
            ┌───────────┴────────────┐
            ▼                        ▼
      Yahoo Finance            Twelve Data
                        │
                        ▼
                  SQLAlchemy ORM
                        │
                        ▼
            PostgreSQL + TimescaleDB
```

---

# ✨ Features

## 📊 Market Data

- Latest market prices
- Historical OHLCV candles
- Multiple market data providers
- Provider abstraction layer

Supported instruments:

- 🥇 Gold Spot (`XAUUSD`)
- 📦 Gold Futures (`GC=F`)
- 💱 GBP/USD
- 💱 EUR/USD

---

## 🏛️ Backend Architecture

- Python 3.14
- FastAPI
- SQLAlchemy 2
- Pydantic v2
- Alembic
- Repository-ready architecture
- Dependency Injection
- Generic Instrument Registry

---

## 🗄️ Database

- PostgreSQL 17
- TimescaleDB
- Docker Compose
- Connection pooling
- Health checks
- Alembic migrations

---

## 🧪 Testing

Current automated test coverage:

- ✅ API routes
- ✅ Services
- ✅ Providers
- ✅ Database
- ✅ Instrument Registry
- ✅ Configuration

**Current Status**

```
84 tests passing
```

---

# 📂 Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── database/
│   ├── providers/
│   ├── services/
│   ├── instruments/
│   ├── models/
│   └── core/
│
├── alembic/
├── tests/
└── Dockerfile
```

---

# 🐳 Running with Docker

## Start

```bash
docker compose --env-file backend/.env up --build -d
```

---

## Stop

```bash
docker compose down
```

---

## View Logs

```bash
docker compose logs
```

or

```bash
docker compose logs -f api
```

---

# 💻 Running Locally

Create a virtual environment

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the API

```bash
python -m uvicorn app.main:app --reload
```

---

# 🔄 Local vs Docker

When running locally:

```
DATABASE_HOST=localhost
```

because FastAPI runs directly on your machine.

When running inside Docker:

```
DATABASE_HOST=timescaledb
```

because Docker Compose provides internal DNS using service names.

---

# 🗄️ Database Migrations

Create a migration

```bash
alembic revision -m "description"
```

Apply migrations

```bash
alembic upgrade head
```

Current migration status

```bash
alembic current
```

Migration history

```bash
alembic history
```

---

# 📡 API Endpoints

## ❤️ Health

| Method | Endpoint           |
| ------ | ------------------ |
| GET    | `/health`          |
| GET    | `/health/database` |

---

## 📈 Market

| Method | Endpoint                       |
| ------ | ------------------------------ |
| GET    | `/market/{instrument}/latest`  |
| GET    | `/market/{instrument}/history` |

---

## 🪙 Instruments

| Method | Endpoint                    |
| ------ | --------------------------- |
| GET    | `/instruments`              |
| GET    | `/instruments/{instrument}` |

---

# 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### Database

- PostgreSQL
- TimescaleDB
- Alembic

### Infrastructure

- Docker
- Docker Compose

### Market Data

- Yahoo Finance
- Twelve Data

### Testing

- Pytest

---

# 🗺️ Roadmap

## ✅ Epic 1 – Backend Platform Foundation

- Generic Market API
- Multi-provider architecture
- Docker
- PostgreSQL
- TimescaleDB
- SQLAlchemy
- Alembic
- Health endpoints

## 🚧 Epic 1 Remaining

- Instrument Repository
- Historical Market Storage
- Scheduled Data Ingestion
- Production Observability

## 🔮 Future Epics

- AI Sentiment Analysis
- Financial Intelligence Dashboard
- AI Research Agent
- Multi-Agent Investment Analyst

---

# 👨‍💻 Author

Developed as a portfolio project demonstrating enterprise backend engineering and AI platform architecture using modern Python technologies.
