# PrimeTrade AI - Backend Intern Assignment

A scalable, well-architected REST API built with FastAPI and PostgreSQL, featuring JWT authentication, role-based access control, and task management.

## 🚀 Features

- **Robust Authentication**: JWT-based stateless authentication with secure password hashing (bcrypt).
- **Role-Based Access Control (RBAC)**: Distinct permissions for `Admin` and `User` roles.
    - Admins can view and manage all tasks across the system.
    - Users can only manage their own tasks.
- **Task Management**: Full CRUD (Create, Read, Update, Delete) functionality for tasks.
- **Clean Architecture**: 
    - **Service Layer**: Decoupled business logic from API endpoints for better testability.
    - **Modular Packages**: Organized by models, schemas, and routers.
    - **Versioned API**: Future-proof `/api/v1` structure.
- **Configuration Management**: Centralized settings using Pydantic and `.env` files.
- **Containerization**: Fully Dockerized database (PostgreSQL) support.
- **API Documentation**: Interactive Swagger UI available at `/docs`.

## 🛠️ Tech Stack

- **Backend**: Python 3.13, FastAPI
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Validation**: Pydantic v2
- **Auth**: PyJWT, passlib[bcrypt]
- **Frontend**: React + Vite

## 🛠️ Quick Start

### 1. Database Setup (Docker)
Ensure you have Docker and Docker-Compose installed.
```bash
docker-compose up -d db
```

### 2. Backend Setup
1. Create a `.env` file in the `backend/` directory (see `.env.example`).
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run with uvicorn:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🏗️ Clean Architecture

This project follows a structured approach to ensure scalability:
- **`app/api/v1/`**: Endpoint definitions and API versioning.
- **`app/services/`**: The "Brain" of the app. All business logic and DB queries live here.
- **`app/models/`**: SQLAlchemy database models.
- **`app/schemas/`**: Pydantic models for request/response validation.
- **`app/core/`**: Centralized configuration and security logic.
