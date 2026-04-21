import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import User, RoleEnum

# Basic SQLite memory database for fast testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_user_registration():
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@test.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["role"] == "user"

def test_admin_registration():
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "admin", "email": "admin@test.com", "password": "adminpassword"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "admin"
    assert response.json()["role"] == "admin"

def test_user_login():
    client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "email": "test@test.com", "password": "password123"}
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_task_creation_and_retrieval():
    # Register & Login
    client.post(
        "/api/v1/auth/register",
        json={"username": "taskuser", "email": "task@test.com", "password": "password123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "taskuser", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create task
    task_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Test Task", "description": "This is a test task"},
        headers=headers
    )
    assert task_response.status_code == 201
    assert task_response.json()["title"] == "Test Task"

    # Get task
    get_response = client.get("/api/v1/tasks/", headers=headers)
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1
    assert get_response.json()[0]["title"] == "Test Task"
