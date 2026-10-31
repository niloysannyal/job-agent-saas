"""
Phase 1 Personal Validation / Live Dogfooding Runner
Automates the Find -> Channel Discovery -> STAR Q&A -> CV Tailoring -> Draft Review pipeline
for Niloy's live job search, adhering strictly to multi-tenancy, fact ledger integrity,
and the non-negotiable human-in-the-loop Send gate.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add backend to sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.db.session import SessionLocal
from app.models.application import Application, ApplicationFormAnswer
from app.models.cv_template import AccountCvVersion
from app.models.interview import StarStory
from app.models.job import Job
from app.models.profile import UserProfile
from app.services.cv_tailor.tailor_service import CVTailorService
from app.services.form_detective.detective import FormDetectiveService
from app.services.qa_generator.generator import FormQAGenerator

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("dogfooding")

NILOY_ID = "6e488188-0015-4657-94c9-92d01413dcfb"

TARGET_JOBS = [
    ("04f41f11-9dbc-421d-ab0b-9609974c640a", "webbyfox consultancy"),
    ("2cb41a14-9bd1-45a6-b099-63a822da4d74", "Vega"),
    ("bed0d76a-63d2-4cbe-a397-a3ee89374581", "Pay.UK"),
]


async def run():
    print("=" * 72)
    print("  PHASE 1 PERSONAL VALIDATION -- LIVE JOB SEARCH PIPELINE")
    print("=" * 72)

    with SessionLocal() as db:
        profile = db.query(UserProfile).filter_by(account_id=NILOY_ID).first()
        if not profile:
            print("Candidate profile not found for Niloy. Aborting.")
            return

        stories = db.query(StarStory).filter_by(account_id=NILOY_ID).all()
        print(f"Loaded Profile: {profile.full_name} ({profile.current_role})")
        print(f"Loaded STAR Stories in Bank: {len(stories)}")
        print("-" * 72)

        qa_gen = FormQAGenerator()
        cv_tailor = CVTailorService(db_session=db)

        results = []

        for job_id, company_name in TARGET_JOBS:
            job = db.query(Job).filter_by(id=job_id, account_id=NILOY_ID).first()
            if not job:
                print(f"Job {job_id} ({company_name}) not found. Skipping.")
                continue

            print(f"\n[JOB MATCH] {job.role} @ {job.company}")
            print(f"  Source: {job.source} | Match Score: {job.match_score:.1f}%")
            print(f"  Apply Link: {job.apply_link}")

            # 1. Channel Detection & Form Detective
            inspection = FormDetectiveService.detect_channel(
                apply_url=job.apply_link,
                posting_text=job.description,
                company_name=job.company,
                role_title=job.role,
            )
            detected_channel = (
                "form"
                if ("portal" in inspection.channel_type.value or "form" in inspection.channel_type.value)
                else "email"
            )

            print(f"  1. Channel Detective: {inspection.channel_type.value} -> mapped to '{detected_channel}'")
            print(f"     Platform: {inspection.platform_name}")
            print(f"     Action: {inspection.action_summary}")
            print(f"     Form Questions Discovered: {len(inspection.questions)}")

            # 2. Recursive STAR-Grounded Q&A Generation
            qa_res = await qa_gen.generate_answers(
                questions=inspection.questions,
                company_name=job.company,
                role_title=job.role,
                job_description=job.description or "",
                profile=profile,
                star_stories=stories,
            )
            print(f"  2. Task-Level Recursive Q&A Generation:")
            print(f"     Total Questions Answered: {qa_res.total_questions}")
            print(f"     Fact Integrity Verified: {'PASS' if qa_res.all_facts_verified else 'FAIL'}")
            for a in qa_res.answers[:2]:
                print(f"       * Prompt: {a.question_prompt[:65]}...")
                print(f"         Answer: {a.answer[:90]}...")
                print(f"         Facts: {a.verified_facts_used}")

            # 3. CV Tailoring & Fact Ledger Verification
            existing_app = (
                db.query(Application)
                .filter_by(account_id=NILOY_ID, job_id=job.id)
                .first()
            )

            target_app = None
            if existing_app:
                print(f"  3. CV & Application already persisted:")
                print(f"     App ID: {existing_app.id} | Status: {existing_app.status} | Channel: {existing_app.channel}")
                cv_ver = db.query(AccountCvVersion).filter_by(id=existing_app.cv_version_id).first()
                if cv_ver:
                    print(f"     CV Version: {cv_ver.id} | ATS Score: {cv_ver.ats_score:.1f}% | Pages: {cv_ver.page_count}")
                target_app = existing_app
                results.append((job, existing_app, qa_res))
            else:
                tailor_res = await cv_tailor.tailor_for_job(
                    account_id=NILOY_ID,
                    job=job,
                    channel=detected_channel,
                )
                print(f"  3. CV Tailoring & Application Creation:")
                print(f"     CV Version ID: {tailor_res.cv_version.id}")
                print(f"     ATS Score: {tailor_res.ats_score:.1f}%")
                print(f"     Fact Ledger Audit: {'PASSED (0 hallucinations)' if tailor_res.fact_audit_passed else 'FLAGGED'}")
                print(f"     Page Budget: {tailor_res.cv_version.page_count} page(s) ({len(tailor_res.cv_version.tailored_latex)} chars)")
                print(f"     Identified Gaps: {tailor_res.gaps_detected}")
                print(f"     Application Record Created: ID={tailor_res.application.id}")
                print(f"     Status: {tailor_res.application.status} (Strict Human-in-the-Loop, sent_at={tailor_res.application.sent_at})")
                target_app = tailor_res.application
                results.append((job, tailor_res.application, qa_res))

            # 4. Persist structured form answers
            if target_app and qa_res.answers:
                db.query(ApplicationFormAnswer).filter_by(application_id=target_app.id).delete()
                import json
                for a in qa_res.answers:
                    fa = ApplicationFormAnswer(
                        account_id=NILOY_ID,
                        application_id=target_app.id,
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
                print(f"  4. Form Q&A DB Persistence: {len(qa_res.answers)} answers linked to app {target_app.id}")

        print("\n" + "=" * 72)
        print(f"  DOGFOODING VALIDATION COMPLETED -- {len(results)} APPLICATIONS READY FOR HUMAN REVIEW")
        print("=" * 72)


if __name__ == "__main__":
    asyncio.run(run())

