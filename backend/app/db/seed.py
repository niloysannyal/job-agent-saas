import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_session_factory
from app.models.account import Account
from app.models.cv_template import CvTemplate
from app.models.llm_provider import LLMProviderConfig
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
    """
    close_session = False
    if session is None:
        factory = get_session_factory()
        session = factory()
        close_session = True

    try:
        # 1. Tenant #1: Niloy
        account = session.query(Account).filter_by(email="niloy@example.com").first()
        if not account:
            account = Account(
                email="niloy@example.com",
                plan_tier="free",
                account_template_limit=None,
            )
            session.add(account)
            session.flush()
            logger.info(f"Seeded default tenant #1: {account.id} ({account.email})")

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
