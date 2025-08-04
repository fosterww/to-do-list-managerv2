import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
import models 
from config import settings
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

TEST_DATABASE_URL = settings.test_database_url

logger.debug(f"Test database URL: {TEST_DATABASE_URL}")

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {},
    echo=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

async def override_get_api_key():
    return settings.api_key

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[app.dependency_overrides.get("get_api_key")] = override_get_api_key
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    logger.info("Setting up test PostgreSQL database")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Tearing down test database")
    Base.metadata.drop_all(bind=engine)


def test_create_task():
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description", "status": "todo"},
        headers={"X-API-Key": settings.api_key}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "todo"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_task_invalid_api_key():
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description", "status": "todo"},
        headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API Key"}

def test_get_tasks():
    client.post(
        "/tasks/",
        json={"title": "Task 1", "description": "Desc 1", "status": "todo"},
        headers={"X-API-Key": settings.api_key}
    )
    response = client.get("/tasks/", headers={"X-API-Key": settings.api_key})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Task 1"

def test_get_tasks_by_status():
    client.post(
        "/tasks/",
        json={"title": "Task 2", "description": "Desc 2", "status": "in_progress"},
        headers={"X-API-Key": settings.api_key}
    )
    response = client.get("/tasks/?status=in_progress", headers={"X-API-Key": settings.api_key})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["status"] == "in_progress"

def test_get_task_by_id():
    create_response = client.post(
        "/tasks/",
        json={"title": "Task 3", "description": "Desc 3", "status": "completed"},
        headers={"X-API-Key": settings.api_key}
    )
    task_id = create_response.json()["id"]
    response = client.get(f"/tasks/{task_id}", headers={"X-API-Key": settings.api_key})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Task 3"

def test_get_task_not_found():
    response = client.get("/tasks/999", headers={"X-API-Key": settings.api_key})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_update_task():
    create_response = client.post(
        "/tasks/",
        json={"title": "Task 4", "description": "Desc 4", "status": "todo"},
        headers={"X-API-Key": settings.api_key}
    )
    task_id = create_response.json()["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Task", "status": "in_progress"},
        headers={"X-API-Key": settings.api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["status"] == "in_progress"

def test_update_task_not_found():
    response = client.put(
        "/tasks/999",
        json={"title": "Updated Task"},
        headers={"X-API-Key": settings.api_key}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_task():
    create_response = client.post(
        "/tasks/",
        json={"title": "Task 5", "description": "Desc 5", "status": "todo"},
        headers={"X-API-Key": settings.api_key}
    )
    task_id = create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}", headers={"X-API-Key": settings.api_key})
    assert response.status_code == 204
    response = client.get(f"/tasks/{task_id}", headers={"X-API-Key": settings.api_key})
    assert response.status_code == 404

def test_delete_task_not_found():
    response = client.delete("/tasks/999", headers={"X-API-Key": settings.api_key})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}