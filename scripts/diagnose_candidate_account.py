"""
scripts/diagnose_candidate_account.py

Diagnostic on Niloy Sannyal's candidate account (niloy@example.com) in localhost:5433/jobeazy:
1. CV Template & Master Resume status (LaTeX compilation test via TeXLiveCompilerService).
2. Google OAuth connection status.
3. LLM Providers active status & priority order for the account.
4. Jobs ingestion status & readiness in /studio.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.db.session import get_session_factory
from app.models.account import Account
from app.models.cv_template import AccountCvVersion, CvTemplate
from app.models.dispatch import AccountDispatchSettings
from app.models.job import Job
from app.models.llm_provider import LLMProviderConfig
from app.models.oauth import OAuthConnection
from app.models.profile import UserProfile, UserResume
from app.services.cv_tailor.texlive_compiler import TeXLiveCompilerService
from app.services.llm.service import LLMService


def main():
    session = get_session_factory()()
    try:
        print("=" * 80)
        print("  CANDIDATE ACCOUNT DIAGNOSTIC (niloy@example.com)")
        print("=" * 80)

        # Find Niloy's Account
        account = session.query(Account).filter_by(email="niloy@example.com").first()
        if not account:
            print("ERROR: Could not find account with email 'niloy@example.com'!")
            return

        account_id = account.id
        print(f"\n[1] ACCOUNT OVERVIEW:")
        print(f"  - Account ID: {account_id}")
        print(f"  - Email: {account.email}")
        print(f"  - Role: {account.role}")
        print(f"  - Plan Tier: {account.plan_tier}")
        print(f"  - Status: {account.status}")

        # Check Dispatch Settings
        dispatch_set = session.query(AccountDispatchSettings).filter_by(account_id=account_id).first()
        if dispatch_set:
            print(f"  - Autonomy Mode: {dispatch_set.autonomy_mode}")
            print(f"  - Daily Auto Cap: {dispatch_set.autonomous_daily_cap}")
            print(f"  - Kill Switch: {dispatch_set.kill_switch}")
        else:
            print("  - Dispatch Settings: None (defaults apply)")

        # [2] MASTER CV & COMPILATION TEST
        print(f"\n[2] MASTER RESUME & TEX LIVE COMPILER:")
        user_resumes = session.query(UserResume).filter_by(account_id=account_id).all()
        print(f"  - User Resumes in DB: {len(user_resumes)}")
        for r in user_resumes:
            print(f"    * ID: {r.id} | Name: {r.name} | File: {r.filename} | Source: {r.source_type} | Default: {r.is_default} | Has LaTeX: {bool(r.latex_source)}")

        # Check cv_templates
        templates = session.query(CvTemplate).all()
        print(f"  - System CV Templates: {len(templates)}")
        for t in templates:
            print(f"    * {t.id}: {t.name} (is_admin_default={t.is_admin_default})")

        # Test compiling 01_MASTER_CV.tex from disk or template
        master_cv_path = os.path.join(os.path.dirname(__file__), "..", "cv_templates", "01_MASTER_CV.tex")
        master_cv_exists = os.path.exists(master_cv_path)
        print(f"  - cv_templates/01_MASTER_CV.tex on disk: {'Found' if master_cv_exists else 'NOT FOUND'}")

        if master_cv_exists:
            with open(master_cv_path, "r", encoding="utf-8") as f:
                latex_source = f.read()
            print(f"  - Master LaTeX Source: {len(latex_source)} chars, {len(latex_source.splitlines())} lines.")

            print("  - Running compilation test via TeXLiveCompilerService...")
            compile_res = TeXLiveCompilerService.compile_latex(latex_source)
            print(f"    * Compilation Success: {compile_res.get('success')}")
            print(f"    * PDF Output Size: {compile_res.get('pdf_size')} bytes")
            print(f"    * Compiler Used: {compile_res.get('compiler')}")
            print(f"    * Duration: {compile_res.get('duration_ms')}ms")
            if not compile_res.get('success'):
                print(f"    * Error Log: {compile_res.get('error')}")

        # [3] GOOGLE OAUTH CONNECTION
        print(f"\n[3] GOOGLE OAUTH CONNECTION:")
        oauth_rows = session.query(OAuthConnection).filter_by(account_id=account_id).all()
        print(f"  - OAuth Connections for Niloy: {len(oauth_rows)}")
        for o in oauth_rows:
            has_access = bool(o.encrypted_access_token)
            has_refresh = bool(o.encrypted_refresh_token)
            print(f"    * Provider: {o.provider} | Email: {o.email} | Has Access Token: {has_access} | Has Refresh Token: {has_refresh} | Expires: {o.token_expires_at}")
        if not oauth_rows:
            print("    * STATUS: NO Google OAuth connection exists for niloy@example.com.")
            print("    * ACTION NEEDED: Niloy needs to connect Gmail in the UI or seed real OAuth credentials.")

        # [4] LLM PROVIDERS RESOLUTION & PRIORITY ORDER
        print(f"\n[4] LLM PROVIDERS & PRIORITY ORDER:")
        all_llms = session.query(LLMProviderConfig).order_by(
            LLMProviderConfig.account_id.desc().nulls_last(),
            LLMProviderConfig.priority.asc(),
        ).all()
        print(f"  - All LLM Provider rows in DB: {len(all_llms)}")
        for l in all_llms:
            print(f"    * Provider: {l.provider:<10} | Model: {l.model_name:<20} | Priority: {l.priority} | Account: {l.account_id or 'GLOBAL'} | Active: {l.is_active} | Key: {'Present' if l.encrypted_api_key else 'None'}")

        llm_service = LLMService(db_session=session, account_id=account_id)
        resolved_providers = llm_service._resolve_providers()
        print(f"\n  - Resolved Provider Chain for Niloy's Account ({len(resolved_providers)}):")
        for idx, p in enumerate(resolved_providers, start=1):
            prov_name = p.__class__.__name__
            model = getattr(p, "model_name", "unknown")
            has_key = bool(getattr(p, "api_key", None))
            print(f"    #{idx}: {prov_name} (model={model}, api_key_configured={has_key})")
        if resolved_providers:
            print(f"  -> CURRENT #1 PRIMARY LLM: {resolved_providers[0].__class__.__name__} (model={getattr(resolved_providers[0], 'model_name', 'unknown')})")

        # [5] INGESTED JOBS & STUDIO READINESS
        print(f"\n[5] INGESTED JOBS & STUDIO READINESS:")
        jobs = session.query(Job).filter_by(account_id=account_id).all()
        print(f"  - Total Jobs for Account: {len(jobs)}")
        active_jobs = [j for j in jobs if j.is_active and not j.vetoed]
        print(f"  - Active / Un-vetoed Jobs: {len(active_jobs)}")

        # Sources breakdown
        sources = {}
        for j in active_jobs:
            sources[j.source or "unknown"] = sources.get(j.source or "unknown", 0) + 1
        print("  - Jobs Breakdown by Ingestion Source:")
        for src, count in sorted(sources.items()):
            print(f"    * {src}: {count} jobs")

        print("\n  - Sample Jobs Ready in /studio:")
        for j in active_jobs[:5]:
            print(f"    * [{j.id[:8]}] {j.title} @ {j.company} ({j.source}) | Apply: {j.apply_link[:60] if j.apply_link else 'None'}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
