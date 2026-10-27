import uuid
from datetime import datetime, timezone
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models.account import Account, AccountCreate
from app.models.application import (
    Application,
    ApplicationCreate,
    ApplicationRead,
)
from app.models.cv_template import (
    AccountCvVersion,
    AccountCvVersionCreate,
    CvTemplate,
    CvTemplateCreate,
)
from app.models.interview import (
    StarStory,
    StarStoryCreate,
    StarStoryRead,
)
from app.models.job import Job, JobPosting
from app.models.llm_provider import (
    LLMProviderConfig,
    LLMProviderCreate,
)
from app.models.profile import (
    CompensationExpectation,
    CompensationCreate,
    SpokenLanguage,
    SpokenLanguageCreate,
    TargetDesignation,
    TargetDesignationCreate,
    TargetLocation,
    TargetLocationCreate,
    UserProfile,
    UserProfileCreate,
)
from app.models.subscription import (
    Entitlement,
    EntitlementCreate,
    SubscriptionPlan,
    SubscriptionPlanCreate,
)


@pytest.fixture
def db_session():
    """In-memory SQLite session with all multi-tenant tables for testing models."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_account_model(db_session: Session):
    """Test Account model defaults and multi-tenant fields."""
    account = Account(email="niloy@example.com")
    db_session.add(account)
    db_session.commit()
    db_session.refresh(account)

    assert account.id is not None
    assert len(account.id) == 36  # UUID string
    assert account.email == "niloy@example.com"
    assert account.plan_tier == "free"
    assert account.account_template_limit is None
    assert account.created_at is not None


def test_job_model_matching_architecture_spec(db_session: Session):
    """
    Test Job model matches ARCHITECTURE.md §7:
    (account_id, company, role, salary, deadline, location_type, country,
     visa_required, target_company, match_score, status, source, apply_link, found_at)
    """
    account = Account(email="niloy@example.com")
    db_session.add(account)
    db_session.commit()

    now = datetime.now(timezone.utc)
    job = Job(
        account_id=account.id,
        company="Optimizely",
        role="AI/ML Engineer",
        description="Build LLM and agentic AI systems.",
        salary="£65,000 - £75,000",
        salary_min=65000.0,
        salary_max=75000.0,
        currency="£",
        deadline=now,
        location_type="hybrid",
        country="UK",
        city="London",
        visa_required=True,
        target_company=True,
        match_score=0.92,
        status="new",
        integrity_status="clean",
        source="adzuna",
        source_job_id="12345",
        apply_link="https://jobs.optimizely.com/12345",
        found_at=now,
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    assert job.id is not None
    assert job.account_id == account.id
    assert job.company == "Optimizely"
    assert job.role == "AI/ML Engineer"
    assert job.visa_required is True
    assert job.target_company is True
    assert job.match_score == 0.92
    assert job.status == "new"
    assert job.integrity_status == "clean"
    assert job.source == "adzuna"
    assert job.apply_link == "https://jobs.optimizely.com/12345"
    assert job.location_type == "hybrid"
    assert job.country == "UK"

    # Verify relationship
    assert job.account.email == "niloy@example.com"
    assert len(account.jobs) == 1
    assert account.jobs[0].id == job.id


def test_cv_template_and_version_models(db_session: Session):
    """Test CvTemplate and AccountCvVersion models matching ARCHITECTURE.md §5 & §7."""
    account = Account(email="niloy@example.com")
    db_session.add(account)
    db_session.commit()

    # Admin global template (account_id = None)
    admin_template = CvTemplate(
        account_id=None,
        name="01_MASTER_CV",
        description="Default single-page LaTeX template with tagged control blocks",
        latex_source="\\documentclass{article}\\begin{document}Hello\\end{document}",
        is_admin_default=True,
    )
    db_session.add(admin_template)
    db_session.commit()
    db_session.refresh(admin_template)

    assert admin_template.id is not None
    assert admin_template.account_id is None
    assert admin_template.is_admin_default is True

    # Tailored CV Version for a job
    job = Job(
        account_id=account.id,
        company="Anthropic",
        role="Research Engineer",
        apply_link="https://anthropic.com/careers/1",
        source="direct",
    )
    db_session.add(job)
    db_session.commit()

    cv_version = AccountCvVersion(
        account_id=account.id,
        job_id=job.id,
        cv_template_id=admin_template.id,
        tailored_latex="\\documentclass{article}\\begin{document}Tailored for Anthropic\\end{document}",
        ats_score=0.88,
        page_count=1,
        cut_summary={"cut_lines": 3, "strategy": "relevance_weighted"},
        status="compiled",
    )
    db_session.add(cv_version)
    db_session.commit()
    db_session.refresh(cv_version)

    assert cv_version.id is not None
    assert cv_version.account_id == account.id
    assert cv_version.job_id == job.id
    assert cv_version.ats_score == 0.88
    assert cv_version.page_count == 1
    assert cv_version.cut_summary["cut_lines"] == 3
    assert cv_version.template.name == "01_MASTER_CV"


def test_application_model_and_human_in_the_loop_gate(db_session: Session):
    """Test Application model matching ARCHITECTURE.md §3, §6 & §7."""
    account = Account(email="niloy@example.com")
    db_session.add(account)
    db_session.commit()

    job = Job(
        account_id=account.id,
        company="DeepMind",
        role="Staff Research Engineer",
        apply_link="https://deepmind.google/careers/1",
        source="greenhouse",
    )
    db_session.add(job)
    db_session.commit()

    app = Application(
        account_id=account.id,
        job_id=job.id,
        channel="email",
        draft_content="Dear Hiring Team, I am excited to apply...",
        status="draft",
        sent_at=None,  # Not sent yet — strictly adheres to human-in-the-loop gate
        follow_up_count=0,
    )
    db_session.add(app)
    db_session.commit()
    db_session.refresh(app)

    assert app.id is not None
    assert app.sent_at is None
    assert app.status == "draft"
    assert app.follow_up_count == 0
    assert app.job.company == "DeepMind"
    assert app.account.email == "niloy@example.com"

    # Human reviews and triggers Send
    now = datetime.now(timezone.utc)
    app.sent_at = now
    app.status = "sent"
    db_session.commit()
    db_session.refresh(app)

    assert app.sent_at is not None
    assert app.status == "sent"


def test_subscription_plans_and_entitlements(db_session: Session):
    """Test SubscriptionPlan and Entitlement models matching ARCHITECTURE.md §0 & §7."""
    plan = SubscriptionPlan(
        name="Free Tier",
        tier="free",
        price_cents=0,
        currency="USD",
        interval="month",
        features={"max_applications": 50, "custom_templates": True},
    )
    db_session.add(plan)
    db_session.commit()
    db_session.refresh(plan)

    assert plan.id is not None
    assert plan.tier == "free"
    assert plan.price_cents == 0

    account = Account(email="niloy@example.com", plan_tier="free")
    db_session.add(account)
    db_session.commit()

    # Default all-access entitlement per ARCHITECTURE.md §7
    entitlement = Entitlement(
        account_id=account.id,
        plan_tier="free",
        all_access=True,
        max_active_applications=None,
        custom_templates_allowed=True,
        max_cv_versions=20,
    )
    db_session.add(entitlement)
    db_session.commit()
    db_session.refresh(entitlement)

    assert entitlement.id is not None
    assert entitlement.all_access is True
    assert entitlement.account_id == account.id
    assert account.entitlement.all_access is True


def test_llm_provider_config_model(db_session: Session):
    """Test LLMProviderConfig model matching ARCHITECTURE.md §11 (admin-configurable provider table)."""
    # System default primary OpenAI provider
    openai_prov = LLMProviderConfig(
        account_id=None,
        provider="openai",
        model_name="gpt-4o-mini",
        encrypted_api_key="enc:testkey123",
        is_active=True,
        priority=1,
        config={"temperature": 0.2, "max_tokens": 4096},
    )
    # Secondary fallback Claude provider
    claude_prov = LLMProviderConfig(
        account_id=None,
        provider="anthropic",
        model_name="claude-3-5-sonnet",
        encrypted_api_key="enc:claudekey456",
        is_active=True,
        priority=2,
    )
    db_session.add_all([openai_prov, claude_prov])
    db_session.commit()

    providers = db_session.query(LLMProviderConfig).order_by(LLMProviderConfig.priority).all()
    assert len(providers) == 2
    assert providers[0].provider == "openai"
    assert providers[0].priority == 1
    assert providers[1].provider == "anthropic"
    assert providers[1].priority == 2


def test_multi_tenant_cascade_deletes(db_session: Session):
    """Verify that deleting an account cascades to all tenant-scoped rows."""
    account = Account(email="tenant@example.com")
    db_session.add(account)
    db_session.commit()

    job = Job(account_id=account.id, company="Co", role="Role", apply_link="http://co.com", source="direct")
    template = CvTemplate(account_id=account.id, name="Custom", latex_source="...")
    entitlement = Entitlement(account_id=account.id, plan_tier="free")
    db_session.add_all([job, template, entitlement])
    db_session.commit()

    app = Application(account_id=account.id, job_id=job.id, channel="email")
    db_session.add(app)
    db_session.commit()

    # Delete account
    db_session.delete(account)
    db_session.commit()

    assert db_session.query(Job).filter_by(account_id=account.id).count() == 0
    assert db_session.query(Application).filter_by(account_id=account.id).count() == 0
    assert db_session.query(CvTemplate).filter_by(account_id=account.id).count() == 0
    assert db_session.query(Entitlement).filter_by(account_id=account.id).count() == 0


def test_pydantic_schemas():
    """Verify Pydantic schemas serialize and validate correctly across all models."""
    acc_in = AccountCreate(email="test@user.com", plan_tier="free")
    assert acc_in.email == "test@user.com"
    assert acc_in.plan_tier == "free"

    posting = JobPosting(
        id="adzuna:999",
        source="adzuna",
        company="DeepMind",
        role="Research Engineer",
        apply_link="https://deepmind.google/careers",
        location_type="on-site",
    )
    assert posting.id == "adzuna:999"
    assert posting.source == "adzuna"
    assert posting.company == "DeepMind"

    app_in = ApplicationCreate(
        account_id=str(uuid.uuid4()),
        job_id=str(uuid.uuid4()),
        channel="email",
        draft_content="Cover letter draft",
    )
    assert app_in.status == "draft"
    assert app_in.channel == "email"

    tmpl_in = CvTemplateCreate(
        name="Academic",
        latex_source="\\documentclass{article}",
        is_admin_default=False,
    )
    assert tmpl_in.name == "Academic"

    sub_in = SubscriptionPlanCreate(name="Pro", tier="pro", price_cents=2900)
    assert sub_in.price_cents == 2900

    ent_in = EntitlementCreate(account_id=str(uuid.uuid4()), plan_tier="pro", all_access=True)
    assert ent_in.all_access is True

    llm_in = LLMProviderCreate(provider="openai", model_name="gpt-4o")
    assert llm_in.provider == "openai"


def test_seed_initial_data(db_session: Session):
    """Test seed_initial_data populates default templates, plans, entitlements, and providers."""
    from app.db.seed import seed_initial_data

    seed_initial_data(session=db_session)

    # 1. Tenant #1
    account = db_session.query(Account).filter_by(email="niloy@example.com").first()
    assert account is not None

    # 2. 01_MASTER_CV template
    template = db_session.query(CvTemplate).filter_by(name="01_MASTER_CV").first()
    assert template is not None
    assert template.is_admin_default is True
    assert template.account_id is None

    # 3. Subscription plan
    plan = db_session.query(SubscriptionPlan).filter_by(tier="free").first()
    assert plan is not None

    # 4. Entitlements
    entitlement = db_session.query(Entitlement).filter_by(account_id=account.id).first()
    assert entitlement is not None
    assert entitlement.all_access is True

    # 5. LLM Provider
    provider = db_session.query(LLMProviderConfig).filter_by(provider="openai").first()
    assert provider is not None
    assert provider.priority == 1
    assert provider.model_name == "gpt-4o-mini"

    # 6. User Profile
    profile = db_session.query(UserProfile).filter_by(account_id=account.id).first()
    assert profile is not None
    assert profile.full_name == "Niloy Sannyal"
    assert "Betopia" in profile.current_company
    assert len(profile.target_designations) >= 5
    assert len(profile.target_locations) >= 2
    assert profile.compensation is not None
    assert len(profile.spoken_languages) >= 2

    # 7. STAR stories
    stories = db_session.query(StarStory).filter_by(account_id=account.id).all()
    assert len(stories) >= 3
    assert all(s.is_verified for s in stories)


def test_user_profile_and_relations(db_session: Session):
    """Test UserProfile and related models (designations, locations, compensation, languages)."""
    account = Account(email="alice@example.com")
    db_session.add(account)
    db_session.commit()

    profile = UserProfile(
        account_id=account.id,
        full_name="Alice Smith",
        current_role="Senior ML Engineer",
        current_company="Acme AI",
        core_narrative="Alice builds production ML systems.",
    )
    db_session.add(profile)
    db_session.commit()

    # Add Target Designation
    desig = TargetDesignation(
        account_id=account.id,
        profile_id=profile.id,
        title="AI Engineer",
        priority=1,
    )
    db_session.add(desig)

    # Add Target Location
    loc = TargetLocation(
        account_id=account.id,
        profile_id=profile.id,
        location_name="Remote EU",
        location_type="remote",
    )
    db_session.add(loc)

    # Add Compensation
    comp = CompensationExpectation(
        account_id=account.id,
        profile_id=profile.id,
        min_salary=70000.0,
        max_salary=90000.0,
        currency="USD",
        period="yearly",
    )
    db_session.add(comp)

    # Add Language
    lang = SpokenLanguage(
        account_id=account.id,
        profile_id=profile.id,
        language="English",
        proficiency="Fluent",
    )
    db_session.add(lang)
    db_session.commit()

    db_session.refresh(profile)
    assert len(profile.target_designations) == 1
    assert profile.target_designations[0].title == "AI Engineer"
    assert len(profile.target_locations) == 1
    assert profile.compensation.min_salary == 70000.0
    assert len(profile.spoken_languages) == 1


def test_star_story_model(db_session: Session):
    """Test StarStory model creation, tags, and account cascade."""
    account = Account(email="bob@example.com")
    db_session.add(account)
    db_session.commit()

    story = StarStory(
        account_id=account.id,
        title="Scaling Vector Search",
        situation="Query latency spiked to 500ms under load.",
        action="Introduced HNSW indexing with quantized vectors.",
        result="Reduced latency to 25ms, a 20x improvement.",
        good_for_tags="performance, vector search, scale, optimization",
        company="VectorCorp",
        role="Search Engineer",
        is_verified=True,
    )
    db_session.add(story)
    db_session.commit()

    db_session.refresh(story)
    assert story.id is not None
    assert story.account_id == account.id
    assert story.title == "Scaling Vector Search"
    assert "vector search" in story.good_for_tags
    assert story.is_verified is True


