import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_session_factory
from app.models.account import Account
from app.models.cv_template import CvTemplate
from app.models.interview import StarStory
from app.models.llm_provider import LLMProviderConfig
from app.models.profile import (
    CompensationExpectation,
    SpokenLanguage,
    TargetDesignation,
    TargetLocation,
    UserProfile,
)
from app.models.subscription import Entitlement, SubscriptionPlan

logger = logging.getLogger(__name__)


def seed_initial_data(session: Optional[Session] = None) -> None:
    """
    Seed initial multi-tenant defaults matching ARCHITECTURE.md §0, §5, §7, §11:
    1. Niloy's account (tenant #1).
    2. Admin default LaTeX template (01_MASTER_CV).
    3. Default subscription plan (free tier).
    4. Default entitlement (all-access for Phase 0/1).
    5. Admin-configurable LLM provider config (OpenAI primary).
    6. Niloy's user profile (basic info, narrative, preferences).
    7. Target designations, locations, compensation, spoken languages.
    8. STAR interview stories (verified production stories from USER_PROFILE.md).
    """
    close_session = False
    if session is None:
        factory = get_session_factory()
        session = factory()
        close_session = True

    try:
        # 0. SuperAdmin Ops Account (dedicated administrative console)
        SUPERADMIN_ID = "00000000-0000-4000-a000-000000000001"
        superadmin = session.query(Account).filter((Account.id == SUPERADMIN_ID) | (Account.email == "admin@jobeazy.com")).first()
        if not superadmin:
            superadmin = Account(
                id=SUPERADMIN_ID,
                email="admin@jobeazy.com",
                plan_tier="enterprise",
                role="superadmin",
                status="active",
            )
            superadmin.set_password("AdminSecure2026!")
            session.add(superadmin)
            session.flush()
            logger.info(f"Seeded superadmin: {superadmin.id} ({superadmin.email})")
        else:
            superadmin.role = "superadmin"
            superadmin.status = "active"
            superadmin.set_password("AdminSecure2026!")
            session.flush()

        # 1. Tenant #1: Niloy (deterministic default tenant UUID)
        DEFAULT_TENANT_ID = "6e488188-0015-4657-94c9-92d01413dcfb"
        account = session.query(Account).filter_by(email="niloy@example.com").first()
        if not account:
            account = Account(
                id=DEFAULT_TENANT_ID,
                email="niloy@example.com",
                plan_tier="free",
                role="tenant",
                status="active",
                account_template_limit=None,
            )
            account.set_password("JobEazy2026!")
            session.add(account)
            session.flush()
            logger.info(f"Seeded default tenant #1: {account.id} ({account.email})")
        else:
            account.role = "tenant"
            account.status = "active"
            account.set_password("JobEazy2026!")
            session.flush()



        # 2. Admin default template #1 (01_MASTER_CV)
        master_cv_path = settings.resolve_cv_path()
        cv_source = ""
        if master_cv_path.exists():
            cv_source = master_cv_path.read_text(encoding="utf-8")
        else:
            cv_source = "% Fallback 01_MASTER_CV template\n\\documentclass{article}\n\\begin{document}\nMaster CV\n\\end{document}"

        admin_template = session.query(CvTemplate).filter_by(name="01_MASTER_CV").first()
        if not admin_template:
            admin_template = CvTemplate(
                account_id=None,  # Global platform template
                name="01_MASTER_CV",
                description="Admin-curated default LaTeX CV template with tagged control blocks",
                latex_source=cv_source,
                is_admin_default=True,
            )
            session.add(admin_template)
            logger.info("Seeded default CV template: 01_MASTER_CV")

        # 3. Default subscription plan (Free tier, all access)
        free_plan = session.query(SubscriptionPlan).filter_by(tier="free").first()
        if not free_plan:
            free_plan = SubscriptionPlan(
                name="Free Tier (Personal Validation)",
                tier="free",
                price_cents=0,
                currency="USD",
                interval="month",
                is_active=True,
                features={"all_access": True, "max_cv_versions": 20},
            )
            session.add(free_plan)
            logger.info("Seeded default subscription plan: Free Tier")

        # 4. Entitlements for Tenant #1
        entitlement = session.query(Entitlement).filter_by(account_id=account.id).first()
        if not entitlement:
            entitlement = Entitlement(
                account_id=account.id,
                plan_tier="free",
                all_access=True,
                max_active_applications=None,
                custom_templates_allowed=True,
                max_cv_versions=20,
            )
            session.add(entitlement)
            logger.info(f"Seeded default entitlement for account {account.id}")

        # 5. LLM Provider table configuration (OpenAI primary)
        openai_provider = session.query(LLMProviderConfig).filter_by(provider="openai", account_id=None).first()
        if not openai_provider:
            openai_provider = LLMProviderConfig(
                account_id=None,  # Platform default
                provider="openai",
                model_name="gpt-4o-mini",
                is_active=True,
                priority=1,
                config={"temperature": 0.2, "max_tokens": 4096},
            )
            session.add(openai_provider)
            logger.info("Seeded default LLM provider: OpenAI (gpt-4o-mini, priority=1)")

        # 6. Niloy's user profile
        profile = session.query(UserProfile).filter_by(account_id=account.id).first()
        if not profile:
            profile = UserProfile(
                account_id=account.id,
                full_name="Niloy Sannyal",
                current_role="AI Engineer",
                current_company="Betopia Limited",
                education="B.Sc. in Information and Communication Engineering, University of Rajshahi",
                location_city="Dhaka",
                location_country="Bangladesh",
                core_narrative=(
                    "Niloy builds real AI systems, integrates them with business software, "
                    "deploys them, and takes responsibility for keeping them working."
                ),
                primary_identity=(
                    "AI/ML Engineer focused on production AI systems — Agentic AI, LLM "
                    "applications, RAG, backend/API engineering, MLOps, applied ML — not "
                    "someone who only experiments with models."
                ),
                one_liner=(
                    "AI/ML Engineer building and deploying scalable AI-powered systems "
                    "using Python, FastAPI, LLMs, RAG, Agentic AI, and MLOps."
                ),
                engineering_principle=(
                    "The model is only one component — a useful AI product needs data, "
                    "retrieval, state, orchestration, APIs, infrastructure, monitoring, "
                    "and a reliable user workflow around the model."
                ),
                avoid_phrases=(
                    "passionate AI enthusiast, generic claims with no engineering evidence, "
                    "keyword stuffing, fabricated technologies, inflated metrics, fake leadership claims"
                ),
                working_style=(
                    "Hands-on, curious, self-directed, comfortable taking ownership, "
                    "execution-oriented; learns by building and debugging real systems "
                    "rather than staying theoretical."
                ),
                leadership_example=(
                    "Led the Betopia Sales Agent largely solo, covering requirement gathering, "
                    "visiting SBUs and talking to salespeople, knowledge collection, AI/RAG "
                    "development, agent development, UI/backend integration, CEO-level updates, "
                    "salesperson reviews, deployment, CI/CD, monitoring, Odoo integration, "
                    "and production debugging."
                ),
                dealbreakers="generic/low-substance roles that don't involve real production systems",
                reason_for_leaving=(
                    "Looking for a role with broader ownership and scale, ideally one that "
                    "also moves my trajectory toward robotics/physical AI."
                ),
                tone_preferences=(
                    "Direct, technically precise, no corporate fluff, no excessive motivational "
                    "language. Concise and credible; avoid exaggerated claims and buzzwords. "
                    "Every statement must be defensible if asked about in an interview."
                ),
                master_cv_latex=cv_source,
            )
            session.add(profile)
            session.flush()
            logger.info(f"Seeded user profile for {profile.full_name}")

            # 7a. Target Designations (from USER_PROFILE.md §"Target roles")
            designations = [
                ("AI Engineering", 0),
                ("Machine Learning Engineering", 1),
                ("Generative AI", 2),
                ("LLM Engineering", 3),
                ("Agentic AI", 4),
                ("Applied AI", 5),
                ("Computer Vision", 6),
                ("AI Backend Engineering", 7),
                ("MLOps/AI Infrastructure", 8),
                ("Production AI Systems", 9),
                ("Robotics/Robotic AI", 10),
            ]
            for title, priority in designations:
                session.add(TargetDesignation(
                    account_id=account.id,
                    profile_id=profile.id,
                    title=title,
                    priority=priority,
                    is_active=True,
                ))
            logger.info(f"Seeded {len(designations)} target designations")

            # 7b. Target Locations (from USER_PROFILE.md §"Target locations")
            locations = [
                ("EU (any)", "any", True),
                ("Dhaka, Bangladesh", "onsite", False),
            ]
            for name, loc_type, relocation in locations:
                session.add(TargetLocation(
                    account_id=account.id,
                    profile_id=profile.id,
                    location_name=name,
                    location_type=loc_type,
                    relocation_willing=relocation,
                    is_active=True,
                ))
            logger.info(f"Seeded {len(locations)} target locations")

            # 7c. Compensation (placeholder — marked sensitive, user must fill in)
            session.add(CompensationExpectation(
                account_id=account.id,
                profile_id=profile.id,
                min_salary=None,
                max_salary=None,
                currency="USD",
                period="yearly",
                is_negotiable=True,
                is_sensitive=True,
            ))
            logger.info("Seeded compensation expectation (placeholder)")

            # 7d. Spoken Languages
            languages = [
                ("English", "fluent"),
                ("Bengali", "native"),
            ]
            for lang, prof in languages:
                session.add(SpokenLanguage(
                    account_id=account.id,
                    profile_id=profile.id,
                    language=lang,
                    proficiency=prof,
                ))
            logger.info(f"Seeded {len(languages)} spoken languages")

        # 8. STAR Interview Stories (from USER_PROFILE.md §"Interview story bank")
        existing_stories = session.query(StarStory).filter_by(account_id=account.id).count()
        if existing_stories == 0:
            stories = [
                StarStory(
                    account_id=account.id,
                    title="Betopia Sales Agent — end-to-end ownership",
                    situation=(
                        "Betopia needed a production AI sales assistant embedded in Odoo CRM, "
                        "with no existing team or infrastructure for it."
                    ),
                    action=(
                        "Owned the project solo end-to-end — requirement gathering, visiting SBUs and "
                        "salespeople, collecting won/lost cases and objection-handling knowledge, building "
                        "the RAG/LLM pipeline, multi-provider routing with failover, the agent itself, "
                        "backend and admin frontend, CI/CD, deployment, and ongoing production operation."
                    ),
                    result="Production system used by 700+ salespersons across Betopia Group.",
                    good_for_tags="ownership, ambiguity, end-to-end execution, working solo",
                    company="Betopia Limited",
                    role="AI Engineer",
                    is_verified=True,
                    sort_order=0,
                ),
                StarStory(
                    account_id=account.id,
                    title="Self-onboarding onto an unfamiliar stack",
                    situation=(
                        "The Sales Agent required Odoo, Redis, Qdrant, and Next.js — none used "
                        "hands-on before."
                    ),
                    action=(
                        "Learned and integrated all four directly inside a live production build, "
                        "rather than deferring the project or staying in familiar tools."
                    ),
                    result="All four are now core, reliable parts of the production system.",
                    good_for_tags="learning speed, adaptability, comfort with the unfamiliar",
                    company="Betopia Limited",
                    role="AI Engineer",
                    is_verified=True,
                    sort_order=1,
                ),
                StarStory(
                    account_id=account.id,
                    title="Vision/document information extraction",
                    situation=(
                        "The Sales Agent needed to read Fiverr inbox screenshots, PDFs, and other "
                        "documents and extract structured information reliably."
                    ),
                    action=(
                        "Evaluated vision-capable models (including self-hosted options) for extraction "
                        "accuracy, structured output, and cost/latency trade-offs, and built the "
                        "extraction pipeline into the agent."
                    ),
                    result="Working document/image understanding inside the production agent.",
                    good_for_tags="multimodal AI, practical model evaluation, production trade-offs",
                    company="Betopia Limited",
                    role="AI Engineer",
                    is_verified=True,
                    sort_order=2,
                ),
            ]
            for story in stories:
                session.add(story)
            logger.info(f"Seeded {len(stories)} STAR interview stories")

        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to seed initial data: {e}")
        raise
    finally:
        if close_session:
            session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_initial_data()
    print("Initial multi-tenant seed completed successfully.")
