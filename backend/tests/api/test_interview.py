import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.interview import StarStory


@pytest.fixture
def api_test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(api_test_db: Session):
    app = create_app()

    def override_get_db():
        yield api_test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def account_a(api_test_db: Session):
    acc = Account(email="alice@example.com")
    api_test_db.add(acc)
    api_test_db.commit()
    api_test_db.refresh(acc)
    return acc


@pytest.fixture
def account_b(api_test_db: Session):
    acc = Account(email="bob@example.com")
    api_test_db.add(acc)
    api_test_db.commit()
    api_test_db.refresh(acc)
    return acc


def test_list_stories_empty(client: TestClient, account_a: Account):
    """GET /api/v1/interview/stories returns empty list when none exist."""
    res = client.get(f"/api/v1/interview/stories?account_id={account_a.id}")
    assert res.status_code == 200
    assert res.json() == []


def test_create_and_get_story(client: TestClient, account_a: Account):
    """POST /api/v1/interview/stories creates STAR story and GET retrieves it."""
    payload = {
        "title": "Betopia Sales Agent End-to-End Ownership",
        "situation": "600+ salespersons struggled to query inventory and pricing rapidly.",
        "action": "Built an agentic RAG system using LangChain, FastAPI, and Qdrant with hybrid search.",
        "result": "Reduced query resolution time from 15 mins to under 100ms with 94% user adoption.",
        "good_for_tags": "ownership, rag, latency, production ai",
        "company": "Betopia Limited",
        "role": "AI Engineer",
        "is_verified": True,
        "sort_order": 1,
    }
    res = client.post(f"/api/v1/interview/stories?account_id={account_a.id}", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == payload["title"]
    assert data["account_id"] == account_a.id
    assert data["is_verified"] is True
    story_id = data["id"]

    # Get by ID
    get_res = client.get(f"/api/v1/interview/stories/{story_id}?account_id={account_a.id}")
    assert get_res.status_code == 200
    assert get_res.json()["company"] == "Betopia Limited"

    # Non-existent ID returns 404
    fake_id = str(uuid.uuid4())
    bad_res = client.get(f"/api/v1/interview/stories/{fake_id}?account_id={account_a.id}")
    assert bad_res.status_code == 404


def test_update_and_delete_story(client: TestClient, account_a: Account):
    """PATCH and DELETE endpoints for STAR stories."""
    res = client.post(
        f"/api/v1/interview/stories?account_id={account_a.id}",
        json={
            "title": "Legacy Refactoring",
            "situation": "Monolith was slow.",
            "action": "Split into microservices.",
            "result": "3x throughput.",
            "is_verified": False,
        },
    )
    story_id = res.json()["id"]

    # Patch
    patch_res = client.patch(
        f"/api/v1/interview/stories/{story_id}?account_id={account_a.id}",
        json={"is_verified": True, "title": "Legacy Refactoring & Modernization"},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["is_verified"] is True
    assert patch_res.json()["title"] == "Legacy Refactoring & Modernization"

    # Delete
    del_res = client.delete(f"/api/v1/interview/stories/{story_id}?account_id={account_a.id}")
    assert del_res.status_code == 204

    # Verify deleted
    get_res = client.get(f"/api/v1/interview/stories/{story_id}?account_id={account_a.id}")
    assert get_res.status_code == 404


def test_filter_stories_by_verification_and_tag(client: TestClient, account_a: Account):
    """Test filtering STAR stories by tag and verified_only flag."""
    # Story 1: verified with rag tag
    client.post(
        f"/api/v1/interview/stories?account_id={account_a.id}",
        json={
            "title": "RAG Production",
            "situation": "S1",
            "action": "A1",
            "result": "R1",
            "good_for_tags": "rag, vector search, latency",
            "is_verified": True,
        },
    )
    # Story 2: unverified with architecture tag
    client.post(
        f"/api/v1/interview/stories?account_id={account_a.id}",
        json={
            "title": "Architecture Redesign",
            "situation": "S2",
            "action": "A2",
            "result": "R2",
            "good_for_tags": "architecture, system design",
            "is_verified": False,
        },
    )

    # Filter verified only
    ver_res = client.get(f"/api/v1/interview/stories?account_id={account_a.id}&verified_only=true")
    assert ver_res.status_code == 200
    assert len(ver_res.json()) == 1
    assert ver_res.json()[0]["title"] == "RAG Production"

    # Filter by tag
    tag_res = client.get(f"/api/v1/interview/stories?account_id={account_a.id}&tag=vector")
    assert tag_res.status_code == 200
    assert len(tag_res.json()) == 1
    assert tag_res.json()[0]["title"] == "RAG Production"

    # Filter by tag that doesn't exist
    tag_none = client.get(f"/api/v1/interview/stories?account_id={account_a.id}&tag=kubernetes")
    assert tag_none.status_code == 200
    assert len(tag_none.json()) == 0


def test_list_tags(client: TestClient, account_a: Account):
    """GET /api/v1/interview/tags returns deduplicated sorted tags."""
    client.post(
        f"/api/v1/interview/stories?account_id={account_a.id}",
        json={
            "title": "S1", "situation": "s", "action": "a", "result": "r",
            "good_for_tags": "ownership, leadership, python",
        },
    )
    client.post(
        f"/api/v1/interview/stories?account_id={account_a.id}",
        json={
            "title": "S2", "situation": "s", "action": "a", "result": "r",
            "good_for_tags": "python, fast-api, microservices",
        },
    )

    tags_res = client.get(f"/api/v1/interview/tags?account_id={account_a.id}")
    assert tags_res.status_code == 200
    tags = tags_res.json()
    assert "ownership" in tags
    assert "python" in tags
    assert "microservices" in tags
    assert len(tags) == len(set(tags))  # unique


def test_interview_multi_tenant_isolation(client: TestClient, account_a: Account, account_b: Account):
    """Verify tenant isolation on STAR stories."""
    res = client.post(
        f"/api/v1/interview/stories?account_id={account_a.id}",
        json={"title": "Alice Story", "situation": "s", "action": "a", "result": "r"},
    )
    alice_story_id = res.json()["id"]

    # Bob's list should not include Alice's story
    bob_list = client.get(f"/api/v1/interview/stories?account_id={account_b.id}")
    assert len(bob_list.json()) == 0

    # Bob cannot GET Alice's story
    bob_get = client.get(f"/api/v1/interview/stories/{alice_story_id}?account_id={account_b.id}")
    assert bob_get.status_code == 404

    # Bob cannot PATCH Alice's story
    bob_patch = client.patch(
        f"/api/v1/interview/stories/{alice_story_id}?account_id={account_b.id}",
        json={"title": "Hacked Title"},
    )
    assert bob_patch.status_code == 404

    # Bob cannot DELETE Alice's story
    bob_del = client.delete(f"/api/v1/interview/stories/{alice_story_id}?account_id={account_b.id}")
    assert bob_del.status_code == 404
