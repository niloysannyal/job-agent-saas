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
from app.models.profile import (
    CompensationExpectation,
    SpokenLanguage,
    TargetDesignation,
    TargetLocation,
    UserProfile,
)


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


def test_get_profile_empty(client: TestClient, account_a: Account):
    """GET /api/v1/profile returns null when account has no profile."""
    res = client.get(f"/api/v1/profile?account_id={account_a.id}")
    assert res.status_code == 200
    assert res.json() is None


def test_create_and_get_profile(client: TestClient, account_a: Account):
    """POST /api/v1/profile creates user profile and GET retrieves it."""
    payload = {
        "full_name": "Alice Smith",
        "current_role": "AI Engineer",
        "current_company": "Beta AI",
        "core_narrative": "Alice builds reliable production agents.",
        "primary_identity": "AI/ML Engineer",
        "one_liner": "Building scalable AI pipelines.",
        "engineering_principle": "Orchestration and clean state over raw prompts.",
        "dealbreakers": "No gambling, no non-engineering roles",
        "notice_period": "1 month",
        "visa_needs": "None (Remote or local)",
    }
    res = client.post(f"/api/v1/profile?account_id={account_a.id}", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["full_name"] == "Alice Smith"
    assert data["account_id"] == account_a.id
    assert data["current_role"] == "AI Engineer"

    # Fetch via GET
    get_res = client.get(f"/api/v1/profile?account_id={account_a.id}")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["full_name"] == "Alice Smith"
    assert get_data["current_company"] == "Beta AI"

    # Duplicate creation yields 409 Conflict
    dup_res = client.post(f"/api/v1/profile?account_id={account_a.id}", json=payload)
    assert dup_res.status_code == 409


def test_update_profile(client: TestClient, account_a: Account):
    """PATCH /api/v1/profile updates fields partially."""
    client.post(
        f"/api/v1/profile?account_id={account_a.id}",
        json={"full_name": "Alice Initial", "current_role": "Junior ML"},
    )
    patch_res = client.patch(
        f"/api/v1/profile?account_id={account_a.id}",
        json={"current_role": "Staff AI Engineer", "location_city": "Berlin"},
    )
    assert patch_res.status_code == 200
    data = patch_res.json()
    assert data["full_name"] == "Alice Initial"
    assert data["current_role"] == "Staff AI Engineer"
    assert data["location_city"] == "Berlin"


def test_target_designations_crud(client: TestClient, account_a: Account):
    """CRUD operations on target designations."""
    client.post(
        f"/api/v1/profile?account_id={account_a.id}",
        json={"full_name": "Alice Smith"},
    )

    # Add designation
    desig_res = client.post(
        f"/api/v1/profile/designations?account_id={account_a.id}",
        json={"title": "Senior AI Engineer", "priority": 1, "is_active": True},
    )
    assert desig_res.status_code == 201
    desig_id = desig_res.json()["id"]

    # List
    list_res = client.get(f"/api/v1/profile/designations?account_id={account_a.id}")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1
    assert list_res.json()[0]["title"] == "Senior AI Engineer"

    # Delete
    del_res = client.delete(f"/api/v1/profile/designations/{desig_id}?account_id={account_a.id}")
    assert del_res.status_code == 204

    # Verify empty
    list_res_after = client.get(f"/api/v1/profile/designations?account_id={account_a.id}")
    assert len(list_res_after.json()) == 0


def test_target_locations_crud(client: TestClient, account_a: Account):
    """CRUD operations on target locations."""
    client.post(
        f"/api/v1/profile?account_id={account_a.id}",
        json={"full_name": "Alice Smith"},
    )

    # Add location
    loc_res = client.post(
        f"/api/v1/profile/locations?account_id={account_a.id}",
        json={"location_name": "EU Remote", "location_type": "remote", "relocation_willing": False},
    )
    assert loc_res.status_code == 201
    loc_id = loc_res.json()["id"]

    # List
    list_res = client.get(f"/api/v1/profile/locations?account_id={account_a.id}")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1
    assert list_res.json()[0]["location_name"] == "EU Remote"

    # Delete
    del_res = client.delete(f"/api/v1/profile/locations/{loc_id}?account_id={account_a.id}")
    assert del_res.status_code == 204


def test_compensation_upsert(client: TestClient, account_a: Account):
    """GET and PUT on compensation expectations."""
    client.post(
        f"/api/v1/profile?account_id={account_a.id}",
        json={"full_name": "Alice Smith"},
    )

    # Check initially None
    get_res = client.get(f"/api/v1/profile/compensation?account_id={account_a.id}")
    assert get_res.status_code == 200
    assert get_res.json() is None

    # Upsert compensation
    put_res = client.put(
        f"/api/v1/profile/compensation?account_id={account_a.id}",
        json={
            "min_salary": 80000.0,
            "max_salary": 110000.0,
            "currency": "EUR",
            "period": "yearly",
            "is_negotiable": True,
            "is_sensitive": True,
        },
    )
    assert put_res.status_code == 200
    data = put_res.json()
    assert data["min_salary"] == 80000.0
    assert data["currency"] == "EUR"
    assert data["is_sensitive"] is True

    # Update compensation
    put_update = client.put(
        f"/api/v1/profile/compensation?account_id={account_a.id}",
        json={
            "min_salary": 90000.0,
            "max_salary": 120000.0,
            "currency": "EUR",
            "period": "yearly",
            "is_negotiable": False,
            "is_sensitive": True,
        },
    )
    assert put_update.status_code == 200
    assert put_update.json()["min_salary"] == 90000.0


def test_spoken_languages_crud(client: TestClient, account_a: Account):
    """CRUD operations on spoken languages."""
    client.post(
        f"/api/v1/profile?account_id={account_a.id}",
        json={"full_name": "Alice Smith"},
    )

    lang_res = client.post(
        f"/api/v1/profile/languages?account_id={account_a.id}",
        json={"language": "English", "proficiency": "Native/Fluent", "is_primary": True},
    )
    assert lang_res.status_code == 201
    lang_id = lang_res.json()["id"]

    list_res = client.get(f"/api/v1/profile/languages?account_id={account_a.id}")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    del_res = client.delete(f"/api/v1/profile/languages/{lang_id}?account_id={account_a.id}")
    assert del_res.status_code == 204


def test_multi_tenant_isolation(client: TestClient, account_a: Account, account_b: Account):
    """Verify complete isolation between tenants A and B for profile and related records."""
    # Profile for Alice
    client.post(
        f"/api/v1/profile?account_id={account_a.id}",
        json={"full_name": "Alice A"},
    )
    # Profile for Bob
    client.post(
        f"/api/v1/profile?account_id={account_b.id}",
        json={"full_name": "Bob B"},
    )

    # Bob cannot view Alice's profile
    res_b = client.get(f"/api/v1/profile?account_id={account_b.id}")
    assert res_b.json()["full_name"] == "Bob B"

    # Alice adds a designation
    desig_res = client.post(
        f"/api/v1/profile/designations?account_id={account_a.id}",
        json={"title": "ML Ops Lead", "priority": 0},
    )
    alice_desig_id = desig_res.json()["id"]

    # Bob's designations list should be empty
    bob_desig = client.get(f"/api/v1/profile/designations?account_id={account_b.id}")
    assert len(bob_desig.json()) == 0

    # Bob attempting to delete Alice's designation yields 404
    bob_del = client.delete(f"/api/v1/profile/designations/{alice_desig_id}?account_id={account_b.id}")
    assert bob_del.status_code == 404

    # Alice's designation is still intact
    alice_desig = client.get(f"/api/v1/profile/designations?account_id={account_a.id}")
    assert len(alice_desig.json()) == 1
