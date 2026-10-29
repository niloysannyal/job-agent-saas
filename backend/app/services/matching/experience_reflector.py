from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.job import Job
from app.models.profile import UserProfile
from app.services.matching.profile_parser import ProfileParser

logger = logging.getLogger(__name__)


@dataclass
class ChannelStat:
    channel: str
    total_applied: int = 0
    interviews: int = 0
    offers: int = 0
    rejections: int = 0

    @property
    def conversion_rate(self) -> float:
        if self.total_applied == 0:
            return 0.0
        return round((self.interviews + self.offers) / self.total_applied * 100, 1)


@dataclass
class ExperienceInsights:
    account_id: str
    total_applications: int
    interviews_count: int
    offers_count: int
    rejections_count: int
    overall_conversion_rate: float
    channel_performance: Dict[str, ChannelStat]
    top_performing_skills: List[Dict[str, Any]]
    underperforming_keywords: List[str]
    skill_weight_multipliers: Dict[str, float]
    strategic_recommendations: List[str]
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ExperienceReflector:
    """
    Harness² Experiential Reflector:
    Analyzes historical application trajectories and outcomes (interview invites,
    offers, rejections) to recursively refine candidate positioning, channel
    prioritization, and match scoring weights.
    """

    def __init__(self, db: Session):
        self.db = db

    def reflect_for_account(self, account_id: str) -> ExperienceInsights:
        """
        Analyze all applications for an account and compute actionable
        insights, channel conversion metrics, and dynamic skill multipliers.
        """
        applications = (
            self.db.query(Application)
            .filter_by(account_id=account_id)
            .all()
        )

        total_apps = len(applications)
        interviews = [a for a in applications if a.status in ("interview", "offer")]
        offers = [a for a in applications if a.status == "offer"]
        rejections = [a for a in applications if a.status == "rejected"]

        conv_rate = round(len(interviews) / total_apps * 100, 1) if total_apps > 0 else 0.0

        # 1. Channel Performance Analysis
        channel_stats: Dict[str, ChannelStat] = {
            "email": ChannelStat(channel="email"),
            "form": ChannelStat(channel="form"),
            "dm": ChannelStat(channel="dm"),
        }

        for app in applications:
            ch = app.channel or "email"
            if ch not in channel_stats:
                channel_stats[ch] = ChannelStat(channel=ch)
            
            cstat = channel_stats[ch]
            cstat.total_applied += 1
            if app.status == "interview":
                cstat.interviews += 1
            elif app.status == "offer":
                cstat.offers += 1
                cstat.interviews += 1
            elif app.status == "rejected":
                cstat.rejections += 1

        # 2. Skill Weight Refinement & Keyword Association
        # Track which skills/keywords appear most in successful applications vs rejections
        successful_tokens: Counter = Counter()
        rejected_tokens: Counter = Counter()

        for app in applications:
            job = app.job or self.db.query(Job).filter_by(id=app.job_id).first()
            content_bag = ""
            if job:
                content_bag += f" {job.title} {job.description}"
            if app.draft_content:
                content_bag += f" {app.draft_content}"

            words = [
                w.strip().lower()
                for w in content_bag.split()
                if len(w.strip()) > 3 and w.strip().isalnum()
            ]

            if app.status in ("interview", "offer"):
                successful_tokens.update(words)
            elif app.status == "rejected":
                rejected_tokens.update(words)

        # Retrieve candidate's listed skills to compute individualized multipliers
        profile = (
            self.db.query(UserProfile)
            .filter_by(account_id=account_id)
            .first()
        )

        candidate_skills = [
            "FastAPI", "Python", "Qdrant", "PostgreSQL", "Redis", "Docker",
            "PyTorch", "MLOps", "React", "Next.js", "TypeScript", "Agentic AI", "AWS",
            "WordPress", "PHP",
        ]

        if profile and profile.master_cv_latex:
            cv_text = ProfileParser.extract_clean_cv_text(profile.master_cv_latex)
            for skill in ["GraphQL", "Kubernetes", "LangChain", "Celery", "Pandas", "Scikit-Learn"]:
                if skill.lower() in cv_text.lower() and skill not in candidate_skills:
                    candidate_skills.append(skill)

        skill_multipliers: Dict[str, float] = {}
        top_skills_report: List[Dict[str, Any]] = []

        for skill in candidate_skills:
            skill_name = skill.lower()
            success_count = sum(successful_tokens[token] for token in successful_tokens if skill_name in token)
            reject_count = sum(rejected_tokens[token] for token in rejected_tokens if skill_name in token)

            # Baseline multiplier is 1.0; successful applications boost weight up to 1.35
            multiplier = 1.0
            if success_count > 0:
                boost = min(0.35, success_count * 0.08)
                multiplier += boost
            elif reject_count > 2 and success_count == 0:
                multiplier = max(0.85, 1.0 - (reject_count * 0.04))

            skill_multipliers[skill] = round(multiplier, 2)
            if success_count > 0 or reject_count > 0:
                top_skills_report.append({
                    "skill": skill,
                    "category": "technical",
                    "success_frequency": success_count,
                    "multiplier": round(multiplier, 2),
                })

        top_skills_report.sort(key=lambda s: s["multiplier"], reverse=True)

        # 3. Formulate Strategic Recommendations
        recommendations = []
        best_channel = max(
            channel_stats.values(),
            key=lambda c: c.conversion_rate if c.total_applied > 0 else -1,
            default=None,
        )

        if best_channel and best_channel.total_applied > 0 and best_channel.conversion_rate > 0:
            recommendations.append(
                f"Your highest conversion channel is '{best_channel.channel.upper()}' with a {best_channel.conversion_rate}% interview rate. Prioritize this channel for high-fit roles."
            )
        else:
            recommendations.append(
                "Direct recruiter outreach via personalized email currently demonstrates the fastest turnaround for senior engineering applications."
            )

        if top_skills_report and top_skills_report[0]["multiplier"] > 1.0:
            top_skill = top_skills_report[0]["skill"]
            recommendations.append(
                f"Highlighting '{top_skill}' has correlated with positive response rates. Ensure STAR stories emphasizing '{top_skill}' remain prominent in LaTeX CV tailoring."
            )

        if len(rejections) > len(interviews) and len(rejections) >= 3:
            recommendations.append(
                "Consider refining cover letter intros to focus on quantifiable business impact within the first 3 sentences to arrest recruiter attention."
            )

        return ExperienceInsights(
            account_id=account_id,
            total_applications=total_apps,
            interviews_count=len(interviews),
            offers_count=len(offers),
            rejections_count=len(rejections),
            overall_conversion_rate=conv_rate,
            channel_performance=channel_stats,
            top_performing_skills=top_skills_report[:6],
            underperforming_keywords=[w for w, c in rejected_tokens.most_common(5) if successful_tokens[w] == 0],
            skill_weight_multipliers=skill_multipliers,
            strategic_recommendations=recommendations,
        )
