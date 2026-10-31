"""
Phase 1 Personal Job Search Acceleration Runner
Executes live ingestion across top-tier ATS (Greenhouse, Lever) and aggregator sources,
scores and ranks postings against Niloy's profile, runs Form Detective and STAR Q&A generation,
and tailors ATS-optimized LaTeX CVs into draft applications ready for human review and 1-click autofill.
"""
import asyncio
import json
import logging
import sys
from pathlib import Path

# Set UTF-8 encoding for stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend to sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.db.session import SessionLocal
from app.models.application import Application, ApplicationFormAnswer
from app.models.cv_template import AccountCvVersion
from app.models.interview import StarStory
from app.models.job import Job, JobSearchQuery
from app.models.profile import UserProfile
from app.services.cv_tailor.tailor_service import CVTailorService
from app.services.form_detective.detective import FormDetectiveService
from app.services.job_ingestion import JobIngestionService
from app.services.job_sources.greenhouse import GreenhouseJobSource
from app.services.job_sources.lever import LeverJobSource
from app.services.job_sources.remoteok import RemoteOKJobSource
from app.services.matching.service import MatchingService
from app.services.qa_generator.generator import FormQAGenerator

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("phase1_acceleration")

NILOY_ID = "6e488188-0015-4657-94c9-92d01413dcfb"

TARGET_COMPANIES = ["anthropic", "canonical", "gitlab", "spotify"]
SEARCH_QUERIES = [
    JobSearchQuery(what="AI Engineer"),
    JobSearchQuery(what="Machine Learning"),
]


async def run_acceleration():
    print("=" * 76)
    print("  PHASE 1 ACCELERATION -- LIVE FIND -> MATCH -> TAILOR -> AUTOFILL PIPELINE")
    print("=" * 76)

    with SessionLocal() as db:
        profile = db.query(UserProfile).filter_by(account_id=NILOY_ID).first()
        if not profile:
            print("Candidate profile not found for Niloy. Aborting.")
            return

        stories = db.query(StarStory).filter_by(account_id=NILOY_ID).all()
        print(f"Candidate: {profile.full_name} | Target: {profile.current_role}")
        print(f"STAR Story Bank: {len(stories)} verified stories available")
        print("-" * 76)

        # -------------------------------------------------------------------
        # STEP 1: Live Job Ingestion across Greenhouse, Lever, and RemoteOK
        # -------------------------------------------------------------------
        print("\n>>> STEP 1: Ingesting postings from Greenhouse, Lever, and RemoteOK...")
        sources = [
            GreenhouseJobSource(max_postings=100),
            LeverJobSource(max_postings=100),
            RemoteOKJobSource(),
        ]

        ingestion_service = JobIngestionService(db=db)
        ingest_res = await ingestion_service.ingest(
            account_id=NILOY_ID,
            sources=sources,
            search_queries=SEARCH_QUERIES,
            target_companies=TARGET_COMPANIES,
        )

        print(f"  Ingestion Finished:")
        print(f"    Total Postings Fetched : {ingest_res.total_fetched}")
        print(f"    New Jobs Persisted     : {len(ingest_res.saved_jobs)}")
        print(f"    Duplicates Skipped     : {ingest_res.duplicate_count}")
        print(f"    Prompt Injections Caught: {ingest_res.flagged_count}")
        if ingest_res.errors:
            print(f"    Ingestion Warnings     : {len(ingest_res.errors)} warnings logged")

        # -------------------------------------------------------------------
        # STEP 2: Rank & Select Top-Matching Unapplied Clean Jobs
        # -------------------------------------------------------------------
        print("\n>>> STEP 2: Ranking clean postings against Niloy's profile & MASTER_CV...")
        applied_job_ids = {
            a.job_id for a in db.query(Application).filter_by(account_id=NILOY_ID).all()
        }

        # Query highest-matching clean, unvetoed jobs that haven't been applied to yet
        candidate_jobs = (
            db.query(Job)
            .filter(
                Job.account_id == NILOY_ID,
                Job.integrity_status == "clean",
                Job.vetoed == False,
                Job.id.notin_(applied_job_ids),
            )
            .order_by(Job.match_score.desc().nullslast())
            .limit(15)
            .all()
        )

        print(f"  Found {len(candidate_jobs)} unapplied clean candidate roles.")
        if not candidate_jobs:
            print("  No new candidate roles to process.")
            return

        # Pick top 3 diverse target roles across top companies
        selected_jobs: list[Job] = []
        seen_companies = set()
        for j in candidate_jobs:
            company_key = (j.company or "").lower().strip()
            if company_key not in seen_companies and j.role:
                seen_companies.add(company_key)
                selected_jobs.append(j)
            if len(selected_jobs) >= 3:
                break

        # Fallback if diversity filtering produces < 3
        if len(selected_jobs) < 3:
            for j in candidate_jobs:
                if j not in selected_jobs:
                    selected_jobs.append(j)
                if len(selected_jobs) >= 3:
                    break

        print(f"  Selected {len(selected_jobs)} high-priority target opportunities for live tailoring:")
        for idx, sj in enumerate(selected_jobs, 1):
            score_str = f"{sj.match_score:.1f}%" if sj.match_score is not None else "N/A"
            print(f"    {idx}. [{score_str}] {sj.role} @ {sj.company} ({sj.source})")

        # -------------------------------------------------------------------
        # STEP 3: Form Detective, STAR-Grounded Q&A & CV Tailoring
        # -------------------------------------------------------------------
        print("\n>>> STEP 3: Running Form Detective, Recursive Q&A & Two-Pass CV Tailoring...")
        qa_gen = FormQAGenerator()
        cv_tailor = CVTailorService(db_session=db)
        ready_applications = []

        for j in selected_jobs:
            print(f"\n  ------------------------------------------------------------------")
            print(f"  Target: {j.role} @ {j.company}")
            print(f"  Apply Link: {j.apply_link}")

            # 3a. Channel Detection
            inspection = FormDetectiveService.detect_channel(
                apply_url=j.apply_link,
                posting_text=j.description,
                company_name=j.company,
                role_title=j.role,
            )
            channel = (
                "form"
                if ("portal" in inspection.channel_type.value or "form" in inspection.channel_type.value)
                else "email"
            )
            print(f"  [Channel Detective] {inspection.channel_type.value} -> '{channel}' (Platform: {inspection.platform_name})")
            print(f"                      Discovered Form Prompts: {len(inspection.questions)}")

            # 3b. STAR-Grounded Q&A Generation
            qa_res = await qa_gen.generate_answers(
                questions=inspection.questions,
                company_name=j.company,
                role_title=j.role,
                job_description=j.description or "",
                profile=profile,
                star_stories=stories,
            )
            print(f"  [STAR Q&A Generator] Generated {qa_res.total_questions} answers | Integrity: {'PASS (0 hallucinations)' if qa_res.all_facts_verified else 'FLAGGED'}")
            for a in qa_res.answers[:2]:
                print(f"    * Q: {a.question_prompt[:60]}...")
                print(f"      A: {a.answer[:80]}...")

            # 3c. Two-Pass CV Tailoring (Drafter + Reviewer)
            print(f"  [CV Tailor Engine] Generating ATS-tailored LaTeX CV...")
            tailor_res = await cv_tailor.tailor_for_job(
                account_id=NILOY_ID,
                job=j,
                channel=channel,
            )
            cv_ver = tailor_res.cv_version
            app = tailor_res.application

            print(f"  [CV Tailor Engine] Result:")
            print(f"    - Application ID : {app.id}")
            print(f"    - Status         : {app.status} (Strict Human-in-the-Loop, sent_at={app.sent_at})")
            ats_pct = tailor_res.ats_score * 100 if tailor_res.ats_score <= 1.0 else tailor_res.ats_score
            print(f"    - ATS Match Score: {ats_pct:.1f}%")
            print(f"    - Fact Ledger    : {'PASSED (100% verified)' if tailor_res.fact_audit_passed else 'FLAGGED'}")
            print(f"    - Page Budget    : {cv_ver.page_count} page(s) ({len(cv_ver.tailored_latex)} characters)")

            # 3d. Form Answer Database Persistence
            if app and qa_res.answers:
                db.query(ApplicationFormAnswer).filter_by(application_id=app.id).delete()
                for a in qa_res.answers:
                    fa = ApplicationFormAnswer(
                        account_id=NILOY_ID,
                        application_id=app.id,
                        question_id=a.question_id,
                        question_prompt=a.question_prompt,
                        field_type="paragraph",
                        tailored_answer=a.answer,
                        candidate_angles=json.dumps(a.candidate_angles),
                        verified_facts_used=json.dumps(a.verified_facts_used),
                        char_count=a.char_count,
                    )
                    db.add(fa)
                db.commit()
                print(f"  [Form DB Store] {len(qa_res.answers)} answers saved for Application {app.id}")

            ready_applications.append((j, app, cv_ver, qa_res, inspection))

        # -------------------------------------------------------------------
        # SUMMARY
        # -------------------------------------------------------------------
        print("\n" + "=" * 76)
        print(f"  ACCELERATION BATCH COMPLETE: {len(ready_applications)} APPLICATIONS READY IN DRAFT")
        print("=" * 76)
        for idx, (j, app, cv_ver, qa, insp) in enumerate(ready_applications, 1):
            ats_pct = cv_ver.ats_score * 100 if cv_ver.ats_score and cv_ver.ats_score <= 1.0 else (cv_ver.ats_score or 0.0)
            print(f"\n[{idx}] {j.role} @ {j.company}")
            print(f"    * Application ID : {app.id}")
            print(f"    * Apply URL      : {j.apply_link}")
            print(f"    * Platform       : {insp.platform_name} ({app.channel})")
            print(f"    * ATS Match Score: {ats_pct:.1f}%")
            print(f"    * Form Answers   : {len(qa.answers)} customized answers ready")
            print(f"    * Status         : {app.status} (Human review required before Send)")

        print("\n" + "-" * 76)
        print("  NEXT STEPS FOR NILOY:")
        print("  1. Open Application Studio in frontend: http://localhost:5173")
        print("  2. Drag the '⚡ JobEazy Autofill' bookmarklet to your browser bookmarks bar.")
        print("  3. Click 'Open Application Form' to launch the employer's portal.")
        print("  4. Click the bookmarklet on the employer's page to autofill all fields and STAR answers.")
        print("  5. Review and submit with full human-in-the-loop control!")
        print("-" * 76)


if __name__ == "__main__":
    asyncio.run(run_acceleration())

