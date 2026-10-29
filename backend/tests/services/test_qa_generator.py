import pytest
from app.models.interview import StarStory
from app.models.profile import UserProfile
from app.services.form_detective.detective import FormFieldQuestion
from app.services.qa_generator.generator import FormQAGenerator


@pytest.mark.asyncio
async def test_form_qa_generator_propose_probe_compose():
    generator = FormQAGenerator()

    profile = UserProfile(
        full_name="Niloy Sannyal",
        one_liner="AI Engineer building production agentic and RAG systems",
        portfolio_url="https://niloysannyal.dev",
        github_url="https://github.com/niloysannyal",
        notice_period="2 weeks",
    )

    story = StarStory(
        account_id="test-account-uuid",
        title="Betopia Odoo CRM AI Agent",
        situation="600+ salespersons struggled with manual inquiry turnaround in Odoo CRM. Required an autonomous AI agent operating under sub-100ms latency.",
        action="Engineered FastAPI microservice with Qdrant vector search and dynamic LLM priority failover.",
        result="Cut response turnaround by 65% with zero unplanned downtime for 600+ enterprise users.",
        is_verified=True,
    )

    questions = [
        FormFieldQuestion(
            id="why_company",
            prompt="Why do you want to join Scale AI as Senior AI Engineer?",
            field_type="paragraph",
            char_limit=1500,
        ),
        FormFieldQuestion(
            id="technical_challenge",
            prompt="Describe a production system or technical architecture you owned.",
            field_type="paragraph",
            char_limit=2000,
        ),
        FormFieldQuestion(
            id="portfolio_links",
            prompt="Links to your portfolio or GitHub repositories.",
            field_type="url",
        ),
        FormFieldQuestion(
            id="compensation_availability",
            prompt="What is your desired compensation and availability?",
            field_type="short_text",
        ),
    ]

    result = await generator.generate_answers(
        questions=questions,
        company_name="Scale AI",
        role_title="Senior AI Engineer",
        job_description="Looking for an AI engineer to scale RAG pipelines and vector search.",
        profile=profile,
        star_stories=[story],
    )

    assert result.total_questions == 4
    assert len(result.answers) == 4

    # Verify Why Company answer
    why_ans = next(a for a in result.answers if a.question_id == "why_company")
    assert "Scale AI" in why_ans.answer
    assert len(why_ans.candidate_angles) == 2  # Task-level recursion angles
    assert len(why_ans.verified_facts_used) > 0

    # Verify Technical Challenge answer
    tech_ans = next(a for a in result.answers if a.question_id == "technical_challenge")
    assert "Situation:" in tech_ans.answer
    assert "Betopia" in tech_ans.answer or "600+" in tech_ans.answer

    # Verify Links
    links_ans = next(a for a in result.answers if a.question_id == "portfolio_links")
    assert "github.com/niloysannyal" in links_ans.answer
