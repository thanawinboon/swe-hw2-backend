from datetime import datetime, timedelta

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.database import get_session
from src.main import app
from src.models.leave_requests import LeaveRequestStatus

REGISTER_URL = "/register"
LOGIN_URL = "/token"
CREATE_LEAVE_REQUEST = "/api/create-leave-request"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override() -> Session:
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_leave_request(session: Session, client: TestClient):
    username = "test"
    password = "password"
    full_name = "test user"

    registered_user = client.post(
        REGISTER_URL,
        json={"username": username, "password": password, "full_name": full_name},
    )
    assert registered_user.status_code == status.HTTP_201_CREATED

    login_response = client.post(
        LOGIN_URL,
        data={"username": username, "password": password, "grant_type": "password"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    access_token = login_response.json()["access_token"]
    assert login_response.status_code == status.HTTP_200_OK

    reason: str = "I need to take a break"
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now() + timedelta(days=5)

    response = client.post(
        CREATE_LEAVE_REQUEST,
        json={
            "reason": reason,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["reason"] == reason
    assert data["status"] == LeaveRequestStatus.pending
    assert data["start_date"] == start_date.isoformat()
    assert data["end_date"] == end_date.isoformat()
    assert data["requester_id"] == registered_user.json()["id"]
