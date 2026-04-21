# PrimeTrade AI - Intern Assignment

A Full-stack scalable web application featuring a Python FastAPI backend and a React (Vanilla CSS) frontend.

## 🚀 Features
- **Backend:** FastAPI, PostgreSQL via SQLAlchemy, Pytest, JWT Authentication
- **Frontend:** React + Vite, Dark-Mode Glassmorphism Design
- **Security:** Bcrypt Password Hashing, RBAC (Role-based access control), Input Validations.
- **Tools:** Docker & Docker-Compose

---

## 🛠️ Quick Start

### 1. Database Setup (Docker)
Ensure you have Docker and Docker-Compose installed.
```bash
docker-compose up -d db
```
This spins up a PostgreSQL server running on `localhost:5432`.

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
# Activate venv: .venv\Scripts\activate (Windows) or source .venv/bin/activate (Unix)
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
- Pytests can be run strictly with: `pytest`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🏗️ Scalability Note

This architecture has been designed with robust scalability principles in mind:

1. **Microservices Readiness**: 
   The current monolithic repository strictly adheres to a decoupled Router-Schema-Model paradigm. The `tasks` CRUD domain and the `auth` domain are completely modularized. If the system experiences extreme load, we can effortlessly detach the `tasks` service into its own independent microservice, routing behind an API Gateway (like Nginx, Traefik, or Kong).

2. **Database & Load Balancing**:
   FastAPI operates asynchronously in an event-loop. To handle high traffic, we would deploy multiple worker instances of the backend application utilizing **Gunicorn** configured with *Uvicorn Workers* behind an AWS Application Load Balancer or an Nginx reverse proxy. For database scalability, PostgreSQL can be vertically scaled, but more importantly, we can easily orchestrate **Read-Replicas** and use SQLAlchemy’s capabilities to route Read traffic to the replicas, reserving the master DB exclusively for Writes.

3. **Caching with Redis (Optional / Next Steps)**:
   For further performance improvements, frequent read payloads (like fetching the list of tasks for the same user repeatedly, or token blacklisting/caching user permission hashes) can be cached temporarily in a Redis layer. This would drop database queries by over 80% for read-heavy entities.
