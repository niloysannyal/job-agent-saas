import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.account import Account
from app.models.agent import AgentActionProposal, AgentConversation, AgentMessage
from app.models.application import Application
from app.models.interview import StarStory
from app.models.job import Job
from app.models.profile import ProfileSkill, Project, UserProfile, WorkExperience
from app.services.agent.base_tool import ToolExecutionContext
from app.services.agent.engine import AgentEngine
from app.services.agent.registry import AgentToolRegistry
from app.services.agent.tools.experience_reflector_tool import ExperienceReflectorTool
from app.services.agent.tools.search_jobs_tool import SearchAndRankJobsTool, SearchJobsInput
from app.services.agent.tools.stage_proposal_tool import StageApplicationProposalTool, StageProposalInput
from app.services.agent.tools.star_coach_tool import StarCoachInput, StarCoachTool


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


def test_agent_tools_registry():
    """Verify tool registration and schema generation."""
    registry = AgentToolRegistry()
    registry.register(SearchAndRankJobsTool())
    registry.register(StageApplicationProposalTool())
    registry.register(StarCoachTool())
    registry.register(ExperienceReflectorTool())

    assert len(registry.list_tools()) == 4
    defs = registry.get_tool_definitions()
    assert len(defs) == 4
    assert any(d["function"]["name"] == "search_and_rank_jobs" for d in defs)
    assert any(d["function"]["name"] == "stage_application_proposal" for d in defs)


def test_search_and_rank_jobs_tool(api_test_db: Session, account_a: Account):
    """Test job search tool returns JobRadarCarousel widget."""
    job1 = Job(
        account_id=account_a.id,
        role="Senior AI Engineer",
        company="Solutions Ltd",
        location_type="Remote",
        salary="$140,000 - $180,000",
        match_score=94,
        source="adzuna",
        apply_link="https://example.com/apply/1",
    )
    job2 = Job(
        account_id=account_a.id,
        role="Backend Python Lead",
        company="Fintech Co",
        location_type="Hybrid",
        salary="$130,000",
        match_score=88,
        source="remotive",
        apply_link="https://example.com/apply/2",
    )
    api_test_db.add_all([job1, job2])
    api_test_db.commit()

    tool = SearchAndRankJobsTool()
    ctx = ToolExecutionContext(
        account_id=account_a.id,
        user_email=account_a.email,
        db_session=api_test_db,
    )
    result = pytest.importorskip("asyncio").run(
        tool.execute(ctx, SearchJobsInput(query="AI Engineer", limit=5))
    )

    assert result.success is True
    assert result.ui_widget is not None
    assert result.ui_widget["type"] == "JobRadarCarousel"
    assert len(result.ui_widget["props"]["jobs"]) == 1
    assert result.ui_widget["props"]["jobs"][0]["company"] == "Solutions Ltd"

    # Query without filter returns all matching opportunities
    all_res = pytest.importorskip("asyncio").run(
        tool.execute(ctx, SearchJobsInput(query=None, limit=5))
    )
    assert len(all_res.ui_widget["props"]["jobs"]) == 2


def test_stage_proposal_and_approval_flow(api_test_db: Session, account_a: Account, account_b: Account, client: TestClient):
    """
    Test human-in-the-loop Send gate:
    1. Tool creates AgentActionProposal with status 'pending' and SendApprovalGate widget.
    2. Candidate verifies and clicks Approve.
    3. Status transitions to 'approved' and Application.sent_at is populated.
    4. Tenant B is forbidden from approving Tenant A's proposal.
    """
    job = Job(
        account_id=account_a.id,
        role="Staff Machine Learning Engineer",
        company="NeuralTech",
        source="greenhouse",
        apply_link="https://example.com/apply/staff-ml",
    )
    api_test_db.add(job)
    api_test_db.commit()

    app = Application(
        account_id=account_a.id,
        job_id=job.id,
        channel="email",
        draft_content="Dear NeuralTech Hiring Team, I am submitting my application.",
        status="draft",
    )
    api_test_db.add(app)
    api_test_db.commit()

    # Step 1: Stage proposal via tool
    tool = StageApplicationProposalTool()
    ctx = ToolExecutionContext(
        account_id=account_a.id,
        user_email=account_a.email,
        db_session=api_test_db,
    )
    result = pytest.importorskip("asyncio").run(
        tool.execute(ctx, StageProposalInput(application_id=app.id))
    )

    assert result.success is True
    assert result.ui_widget["type"] == "SendApprovalGate"
    proposal_id = result.data["proposal_id"]

    # Verify stored proposal in database
    prop = api_test_db.query(AgentActionProposal).filter_by(id=proposal_id).first()
    assert prop is not None
    assert prop.status == "pending"
    assert prop.account_id == account_a.id

    # Step 2: Tenant B tries to approve Tenant A's proposal (must fail with 403 or 404)
    res_b = client.post(f"/api/v1/agent/proposals/{proposal_id}/approve?account_id={account_b.id}")
    assert res_b.status_code in [403, 404]

    # Step 3: Tenant A approves proposal
    res_a = client.post(f"/api/v1/agent/proposals/{proposal_id}/approve?account_id={account_a.id}")
    assert res_a.status_code == 200
    approval_data = res_a.json()
    assert approval_data["success"] is True
    assert approval_data["status"] == "executed"

    # Step 4: Verify Application sent_at and status updated
    api_test_db.refresh(app)
    assert app.sent_at is not None
    assert app.status == "applied"


def test_agent_chat_stream(api_test_db: Session, account_a: Account, client: TestClient):
    """Test SSE streaming response from /api/v1/agent/chat."""
    job = Job(
        account_id=account_a.id,
        role="Lead Python Architect",
        company="Distributed Inc",
        source="remoteok",
        apply_link="https://example.com/apply/distributed",
    )
    api_test_db.add(job)
    api_test_db.commit()

    payload = {
        "message": "Run daily radar scan for python jobs",
        "context_filters": {"screen": "jobs"},
    }

    response = client.post(
        f"/api/v1/agent/chat?account_id={account_a.id}",
        json=payload,
    )
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]

    body = response.text
    assert "event: frame" in body
    assert "event: done" in body
    assert "JobRadarCarousel" in body or "thought" in body


def test_star_coach_tool(api_test_db: Session, account_a: Account):
    """Test STAR interview coach tool aligns story to competency."""
    story = StarStory(
        account_id=account_a.id,
        title="Betopia Sales Agent — Production Scale",
        situation="Serving 600+ sales agents required sub-100ms response time with high reliability.",
        action="Engineered caching and parallelized LLM completions.",
        result="Achieved sub-100ms response and 99.9% uptime.",
        good_for_tags="System Architecture, Scalability, High Availability",
    )
    api_test_db.add(story)
    api_test_db.commit()

    tool = StarCoachTool()
    ctx = ToolExecutionContext(
        account_id=account_a.id,
        user_email=account_a.email,
        db_session=api_test_db,
    )
    result = pytest.importorskip("asyncio").run(
        tool.execute(ctx, StarCoachInput(competency="Scalability"))
    )

    assert result.success is True
    assert result.ui_widget is not None
    assert result.ui_widget["type"] == "STARStoryMatch"
    assert "Betopia" in result.ui_widget["props"]["story_title"]


def test_experience_reflector_tool(api_test_db: Session, account_a: Account):
    """Test canonical profile reflection without hallucinating facts."""
    prof = UserProfile(
        account_id=account_a.id,
        full_name="Niloy Sannyal",
        headline="AI & Autonomous Systems Engineer",
    )
    api_test_db.add(prof)
    api_test_db.commit()

    skill = ProfileSkill(
        account_id=account_a.id,
        profile_id=prof.id,
        name="FastAPI",
        category="backend"
    )
    project = Project(
        account_id=account_a.id,
        profile_id=prof.id,
        title="Autonomous Job Application Agent",
        technologies="FastAPI, React, PostgreSQL",
        github_url="https://github.com/niloysannyal/job-agent-saas",
    )
    api_test_db.add_all([skill, project])
    api_test_db.commit()

    tool = ExperienceReflectorTool()
    ctx = ToolExecutionContext(
        account_id=account_a.id,
        user_email=account_a.email,
        db_session=api_test_db,
    )
    result = pytest.importorskip("asyncio").run(
        tool.execute(ctx, ExperienceReflectorTool.input_schema(section="all"))
    )

    assert result.success is True
    data = result.data
    assert data["name"] == "Niloy Sannyal"
    assert "FastAPI" in data["skills"]
    assert data["projects"][0]["name"] == "Autonomous Job Application Agent"


def test_agent_conversation_lifecycle_endpoints(api_test_db: Session, account_a: Account):
    """Test listing, fetching, and deleting agent conversations with isolation."""
    from app.core.auth import get_current_account
    app = create_app()

    def override_db():
        yield api_test_db

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_account] = lambda: account_a

    with TestClient(app) as test_client:
        convo = AgentConversation(
            account_id=account_a.id,
            title="Test Conversation Session",
        )
        api_test_db.add(convo)
        api_test_db.commit()

        msg = AgentMessage(
            conversation_id=convo.id,
            account_id=account_a.id,
            role="user",
            content="Find AI jobs",
        )
        api_test_db.add(msg)
        api_test_db.commit()

        # List conversations
        res = test_client.get("/api/v1/agent/conversations")
        assert res.status_code == 200
        data = res.json()
        assert len(data) >= 1
        assert data[0]["id"] == convo.id
        assert data[0]["title"] == "Test Conversation Session"

        # Get single conversation
        res_get = test_client.get(f"/api/v1/agent/conversations/{convo.id}")
        assert res_get.status_code == 200
        data_get = res_get.json()
        assert data_get["id"] == convo.id
        assert len(data_get["messages"]) == 1
        assert data_get["messages"][0]["content"] == "Find AI jobs"

        # Delete conversation
        res_del = test_client.delete(f"/api/v1/agent/conversations/{convo.id}")
        assert res_del.status_code == 204

        # Verify deleted
        res_verify = test_client.get(f"/api/v1/agent/conversations/{convo.id}")
        assert res_verify.status_code == 404


def test_agent_conversation_patch_and_pin(api_test_db: Session, account_a: Account):
    """Test renaming and pinning/unpinning a conversation."""
    from app.core.auth import get_current_account
    app = create_app()

    def override_db():
        yield api_test_db

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_account] = lambda: account_a

    with TestClient(app) as test_client:
        convo = AgentConversation(
            account_id=account_a.id,
            title="Initial Title",
            is_pinned=False,
        )
        api_test_db.add(convo)
        api_test_db.commit()

        # Update title and pin
        patch_res = test_client.patch(
            f"/api/v1/agent/conversations/{convo.id}",
            json={"title": "Renamed AI Search", "is_pinned": True},
        )
        assert patch_res.status_code == 200
        data = patch_res.json()
        assert data["title"] == "Renamed AI Search"
        assert data["is_pinned"] is True

        # Verify in DB
        api_test_db.refresh(convo)
        assert convo.title == "Renamed AI Search"
        assert convo.is_pinned is True


def test_agent_file_upload_endpoint(api_test_db: Session, account_a: Account):
    """Test uploading files and extracting text/data for agent context."""
    from app.core.auth import get_current_account
    app = create_app()

    def override_db():
        yield api_test_db

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_current_account] = lambda: account_a

    with TestClient(app) as test_client:
        files = [
            ("files", ("notes.txt", b"Skills: Python, FastAPI, Docker", "text/plain")),
            ("files", ("data.csv", b"Skill,Years\nPython,5\nReact,3", "text/csv")),
        ]
        res = test_client.post("/api/v1/agent/upload", files=files)
        assert res.status_code == 200
        data = res.json()
        assert len(data["files"]) == 2
        assert data["files"][0]["filename"] == "notes.txt"
        assert "Python" in data["files"][0]["extracted_text"]
        assert data["files"][1]["filename"] == "data.csv"
        assert data["files"][1]["file_type"] == "spreadsheet"
