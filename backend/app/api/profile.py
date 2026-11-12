"""
Profile management API — CRUD for UserProfile, TargetDesignation, TargetLocation,
CompensationExpectation, SpokenLanguage, WorkExperience, Education, ProfileSkill,
Project, Certification, plus CV auto-parsing and template compilation.

All endpoints are scoped to account_id (multi-tenant, Phase 0 trusted parameter —
see ARCHITECTURE.md §13 for the Phase 3 auth migration plan).
"""
import base64
import io
import json
import logging
import re
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends, File, Form, Header, HTTPException, Query, Response, UploadFile, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload
import pypdf

logger = logging.getLogger(__name__)

from app.core.auth import get_current_account
from app.db.session import get_db
from app.models.account import Account
from app.models.cv_template import CvTemplate
from app.services.cv_tailor.template_compiler import CVTemplateCompiler
from app.services.cv_tailor.texlive_compiler import TeXLiveCompilerService
from app.services.llm.service import LLMService
from app.services.matching.experience_reflector import ExperienceReflector
from app.services.profile.cv_parser import CVParserService
from app.models.profile import (
    Certification,
    CertificationCreate,
    CertificationRead,
    CertificationUpdate,
    CompensationExpectation,
    CompensationBase,
    CompensationCreate,
    CompensationRead,
    Education,
    EducationCreate,
    EducationRead,
    EducationUpdate,
    ProfileSkill,
    ProfileSkillCreate,
    ProfileSkillRead,
    ProfileSkillUpdate,
    Project,
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
    SpokenLanguage,
    SpokenLanguageCreate,
    SpokenLanguageRead,
    TargetDesignation,
    TargetDesignationCreate,
    TargetDesignationRead,
    TargetLocation,
    TargetLocationCreate,
    TargetLocationRead,
    UserProfile,
    UserProfileCreate,
    UserProfileRead,
    UserProfileUpdate,
    WorkExperience,
    WorkExperienceCreate,
    WorkExperienceRead,
    WorkExperienceUpdate,
    UserResume,
    UserResumeCreate,
    UserResumeRead,
    UserResumeSummary,
    UserResumeUpdate,
)

router = APIRouter(prefix="/profile", tags=["profile"])


def _get_or_create_profile(db: Session, account_id: str) -> UserProfile:
    """Ensure a UserProfile row exists for an account, auto-creating a clean default if needed."""
    profile = db.scalars(
        select(UserProfile).where(UserProfile.account_id == account_id)
    ).first()
    if not profile:
        profile = UserProfile(account_id=account_id, full_name="Candidate")
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


# ---------------------------------------------------------------------------
# UserProfile CRUD & Account Discovery
# ---------------------------------------------------------------------------

@router.get(
    "/current",
    summary="Discover active account and associated profile",
)
def get_current_user_profile(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Return the default/active tenant account and profile for frontend bootstrapping."""
    account = db.scalars(select(Account).order_by(Account.created_at)).first()
    if not account:
        return {"account_id": None, "email": None, "profile": None}

    stmt = (
        select(UserProfile)
        .where(UserProfile.account_id == account.id)
        .options(
            selectinload(UserProfile.target_designations),
            selectinload(UserProfile.target_locations),
            selectinload(UserProfile.compensation),
            selectinload(UserProfile.spoken_languages),
            selectinload(UserProfile.work_experiences),
            selectinload(UserProfile.educations),
            selectinload(UserProfile.skills),
            selectinload(UserProfile.projects),
            selectinload(UserProfile.certifications),
        )
    )
    profile = db.scalars(stmt).first()
    return {
        "account_id": account.id,
        "email": account.email,
        "profile": UserProfileRead.model_validate(profile) if profile else None,
    }


@router.get(
    "",
    response_model=Optional[UserProfileRead],
    summary="Get the user profile for an account",
)
def get_profile(
    account_id: str = Query(..., description="Target account ID"),
    db: Session = Depends(get_db),
) -> Optional[UserProfileRead]:
    """Fetch the full user profile with all nested relations."""
    stmt = (
        select(UserProfile)
        .where(UserProfile.account_id == account_id)
        .options(
            selectinload(UserProfile.target_designations),
            selectinload(UserProfile.target_locations),
            selectinload(UserProfile.compensation),
            selectinload(UserProfile.spoken_languages),
            selectinload(UserProfile.work_experiences),
            selectinload(UserProfile.educations),
            selectinload(UserProfile.skills),
            selectinload(UserProfile.projects),
            selectinload(UserProfile.certifications),
        )
    )
    profile = db.scalars(stmt).first()
    if not profile:
        return None
    return profile


@router.post(
    "",
    response_model=UserProfileRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user profile",
)
def create_profile(
    account_id: str = Query(..., description="Target account ID"),
    payload: UserProfileCreate = ...,
    db: Session = Depends(get_db),
) -> UserProfileRead:
    """Create a user profile for an account (one per account)."""
    existing = db.scalars(
        select(UserProfile).where(UserProfile.account_id == account_id)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile already exists for this account. Use PATCH to update.",
        )

    profile = UserProfile(account_id=account_id, **payload.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.patch(
    "",
    response_model=UserProfileRead,
    summary="Update the user profile",
)
def update_profile(
    account_id: str = Query(..., description="Target account ID"),
    payload: UserProfileUpdate = ...,
    db: Session = Depends(get_db),
) -> UserProfileRead:
    """Partial-update the user profile for an account (auto-creates if missing)."""
    profile = _get_or_create_profile(db, account_id)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile


# ---------------------------------------------------------------------------
# Work Experiences CRUD
# ---------------------------------------------------------------------------

@router.get(
    "/experiences",
    response_model=List[WorkExperienceRead],
    summary="List work experiences",
)
def list_work_experiences(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[WorkExperienceRead]:
    profile = _get_or_create_profile(db, account_id)
    stmt = (
        select(WorkExperience)
        .where(WorkExperience.profile_id == profile.id)
        .order_by(WorkExperience.order_index)
    )
    return list(db.scalars(stmt).all())


@router.post(
    "/experiences",
    response_model=WorkExperienceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a work experience",
)
def add_work_experience(
    account_id: str = Query(...),
    payload: WorkExperienceCreate = ...,
    db: Session = Depends(get_db),
) -> WorkExperienceRead:
    profile = _get_or_create_profile(db, account_id)
    exp = WorkExperience(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


@router.patch(
    "/experiences/{experience_id}",
    response_model=WorkExperienceRead,
    summary="Update a work experience",
)
def update_work_experience(
    experience_id: str,
    account_id: str = Query(...),
    payload: WorkExperienceUpdate = ...,
    db: Session = Depends(get_db),
) -> WorkExperienceRead:
    exp = db.scalars(
        select(WorkExperience).where(
            WorkExperience.id == experience_id,
            WorkExperience.account_id == account_id,
        )
    ).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Work experience not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(exp, field, value)

    db.commit()
    db.refresh(exp)
    return exp


@router.delete(
    "/experiences/{experience_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a work experience",
)
def delete_work_experience(
    experience_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    exp = db.scalars(
        select(WorkExperience).where(
            WorkExperience.id == experience_id,
            WorkExperience.account_id == account_id,
        )
    ).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Work experience not found.")
    db.delete(exp)
    db.commit()


# ---------------------------------------------------------------------------
# Educations CRUD
# ---------------------------------------------------------------------------

@router.get(
    "/educations",
    response_model=List[EducationRead],
    summary="List educations",
)
def list_educations(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[EducationRead]:
    profile = _get_or_create_profile(db, account_id)
    stmt = (
        select(Education)
        .where(Education.profile_id == profile.id)
        .order_by(Education.order_index)
    )
    return list(db.scalars(stmt).all())


@router.post(
    "/educations",
    response_model=EducationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add education",
)
def add_education(
    account_id: str = Query(...),
    payload: EducationCreate = ...,
    db: Session = Depends(get_db),
) -> EducationRead:
    profile = _get_or_create_profile(db, account_id)
    edu = Education(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(edu)
    db.commit()
    db.refresh(edu)
    return edu


@router.patch(
    "/educations/{education_id}",
    response_model=EducationRead,
    summary="Update education",
)
def update_education(
    education_id: str,
    account_id: str = Query(...),
    payload: EducationUpdate = ...,
    db: Session = Depends(get_db),
) -> EducationRead:
    edu = db.scalars(
        select(Education).where(
            Education.id == education_id,
            Education.account_id == account_id,
        )
    ).first()
    if not edu:
        raise HTTPException(status_code=404, detail="Education not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(edu, field, value)

    db.commit()
    db.refresh(edu)
    return edu


@router.delete(
    "/educations/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete education",
)
def delete_education(
    education_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    edu = db.scalars(
        select(Education).where(
            Education.id == education_id,
            Education.account_id == account_id,
        )
    ).first()
    if not edu:
        raise HTTPException(status_code=404, detail="Education not found.")
    db.delete(edu)
    db.commit()


# ---------------------------------------------------------------------------
# Skills CRUD & Bulk
# ---------------------------------------------------------------------------

@router.get(
    "/skills",
    response_model=List[ProfileSkillRead],
    summary="List skills",
)
def list_skills(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[ProfileSkillRead]:
    profile = _get_or_create_profile(db, account_id)
    stmt = (
        select(ProfileSkill)
        .where(ProfileSkill.profile_id == profile.id)
        .order_by(ProfileSkill.order_index)
    )
    return list(db.scalars(stmt).all())


@router.post(
    "/skills",
    response_model=ProfileSkillRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a skill",
)
def add_skill(
    account_id: str = Query(...),
    payload: ProfileSkillCreate = ...,
    db: Session = Depends(get_db),
) -> ProfileSkillRead:
    profile = _get_or_create_profile(db, account_id)
    skill = ProfileSkill(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.post(
    "/skills/bulk",
    response_model=List[ProfileSkillRead],
    summary="Bulk add or replace skills",
)
def bulk_skills(
    account_id: str = Query(...),
    payload: List[ProfileSkillCreate] = Body(...),
    replace: bool = Query(False),
    db: Session = Depends(get_db),
) -> List[ProfileSkillRead]:
    profile = _get_or_create_profile(db, account_id)
    if replace:
        existing = db.scalars(
            select(ProfileSkill).where(ProfileSkill.profile_id == profile.id)
        ).all()
        for s in existing:
            db.delete(s)
        db.flush()

    created: List[ProfileSkill] = []
    for idx, item in enumerate(payload):
        d = item.model_dump()
        if d.get("order_index") == 0:
            d["order_index"] = idx
        skill = ProfileSkill(
            account_id=account_id,
            profile_id=profile.id,
            **d,
        )
        db.add(skill)
        created.append(skill)

    db.commit()
    for s in created:
        db.refresh(s)
    return created


@router.patch(
    "/skills/{skill_id}",
    response_model=ProfileSkillRead,
    summary="Update a skill",
)
def update_skill(
    skill_id: str,
    account_id: str = Query(...),
    payload: ProfileSkillUpdate = ...,
    db: Session = Depends(get_db),
) -> ProfileSkillRead:
    skill = db.scalars(
        select(ProfileSkill).where(
            ProfileSkill.id == skill_id,
            ProfileSkill.account_id == account_id,
        )
    ).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(skill, field, value)

    db.commit()
    db.refresh(skill)
    return skill


@router.delete(
    "/skills/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a skill",
)
def delete_skill(
    skill_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    skill = db.scalars(
        select(ProfileSkill).where(
            ProfileSkill.id == skill_id,
            ProfileSkill.account_id == account_id,
        )
    ).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found.")
    db.delete(skill)
    db.commit()


# ---------------------------------------------------------------------------
# Projects CRUD
# ---------------------------------------------------------------------------

@router.get(
    "/projects",
    response_model=List[ProjectRead],
    summary="List projects",
)
def list_projects(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[ProjectRead]:
    profile = _get_or_create_profile(db, account_id)
    stmt = (
        select(Project)
        .where(Project.profile_id == profile.id)
        .order_by(Project.order_index)
    )
    return list(db.scalars(stmt).all())


@router.post(
    "/projects",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a project",
)
def add_project(
    account_id: str = Query(...),
    payload: ProjectCreate = ...,
    db: Session = Depends(get_db),
) -> ProjectRead:
    profile = _get_or_create_profile(db, account_id)
    proj = Project(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj


@router.patch(
    "/projects/{project_id}",
    response_model=ProjectRead,
    summary="Update a project",
)
def update_project(
    project_id: str,
    account_id: str = Query(...),
    payload: ProjectUpdate = ...,
    db: Session = Depends(get_db),
) -> ProjectRead:
    proj = db.scalars(
        select(Project).where(
            Project.id == project_id,
            Project.account_id == account_id,
        )
    ).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(proj, field, value)

    db.commit()
    db.refresh(proj)
    return proj


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
def delete_project(
    project_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    proj = db.scalars(
        select(Project).where(
            Project.id == project_id,
            Project.account_id == account_id,
        )
    ).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found.")
    db.delete(proj)
    db.commit()


# ---------------------------------------------------------------------------
# Certifications CRUD
# ---------------------------------------------------------------------------

@router.get(
    "/certifications",
    response_model=List[CertificationRead],
    summary="List certifications",
)
def list_certifications(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[CertificationRead]:
    profile = _get_or_create_profile(db, account_id)
    stmt = (
        select(Certification)
        .where(Certification.profile_id == profile.id)
        .order_by(Certification.order_index)
    )
    return list(db.scalars(stmt).all())


@router.post(
    "/certifications",
    response_model=CertificationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a certification",
)
def add_certification(
    account_id: str = Query(...),
    payload: CertificationCreate = ...,
    db: Session = Depends(get_db),
) -> CertificationRead:
    profile = _get_or_create_profile(db, account_id)
    cert = Certification(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


@router.patch(
    "/certifications/{certification_id}",
    response_model=CertificationRead,
    summary="Update a certification",
)
def update_certification(
    certification_id: str,
    account_id: str = Query(...),
    payload: CertificationUpdate = ...,
    db: Session = Depends(get_db),
) -> CertificationRead:
    cert = db.scalars(
        select(Certification).where(
            Certification.id == certification_id,
            Certification.account_id == account_id,
        )
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cert, field, value)

    db.commit()
    db.refresh(cert)
    return cert


@router.delete(
    "/certifications/{certification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a certification",
)
def delete_certification(
    certification_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    cert = db.scalars(
        select(Certification).where(
            Certification.id == certification_id,
            Certification.account_id == account_id,
        )
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found.")
    db.delete(cert)
    db.commit()


# ---------------------------------------------------------------------------
# Target Designations
# ---------------------------------------------------------------------------

@router.get(
    "/designations",
    response_model=List[TargetDesignationRead],
    summary="List target designations",
)
def list_designations(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[TargetDesignationRead]:
    profile = db.scalars(
        select(UserProfile).where(UserProfile.account_id == account_id)
    ).first()
    if not profile:
        return []
    stmt = (
        select(TargetDesignation)
        .where(TargetDesignation.profile_id == profile.id)
        .order_by(TargetDesignation.priority)
    )
    return list(db.scalars(stmt).all())


@router.post(
    "/designations",
    response_model=TargetDesignationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a target designation",
)
def add_designation(
    account_id: str = Query(...),
    payload: TargetDesignationCreate = ...,
    db: Session = Depends(get_db),
) -> TargetDesignationRead:
    profile = _get_or_create_profile(db, account_id)
    designation = TargetDesignation(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(designation)
    db.commit()
    db.refresh(designation)
    return designation


@router.delete(
    "/designations/{designation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a target designation",
)
def delete_designation(
    designation_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    designation = db.scalars(
        select(TargetDesignation).where(
            TargetDesignation.id == designation_id,
            TargetDesignation.account_id == account_id,
        )
    ).first()
    if not designation:
        raise HTTPException(status_code=404, detail="Target designation not found.")
    db.delete(designation)
    db.commit()


# ---------------------------------------------------------------------------
# Target Locations
# ---------------------------------------------------------------------------

@router.get(
    "/locations",
    response_model=List[TargetLocationRead],
    summary="List target locations",
)
def list_locations(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[TargetLocationRead]:
    profile = db.scalars(
        select(UserProfile).where(UserProfile.account_id == account_id)
    ).first()
    if not profile:
        return []
    stmt = select(TargetLocation).where(TargetLocation.profile_id == profile.id)
    return list(db.scalars(stmt).all())


@router.post(
    "/locations",
    response_model=TargetLocationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a target location",
)
def add_location(
    account_id: str = Query(...),
    payload: TargetLocationCreate = ...,
    db: Session = Depends(get_db),
) -> TargetLocationRead:
    profile = _get_or_create_profile(db, account_id)
    loc = TargetLocation(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc


@router.delete(
    "/locations/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a target location",
)
def delete_location(
    location_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    loc = db.scalars(
        select(TargetLocation).where(
            TargetLocation.id == location_id,
            TargetLocation.account_id == account_id,
        )
    ).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Target location not found.")
    db.delete(loc)
    db.commit()


# ---------------------------------------------------------------------------
# Compensation Expectations
# ---------------------------------------------------------------------------

@router.get(
    "/compensation",
    response_model=Optional[CompensationRead],
    summary="Get compensation expectations",
)
def get_compensation(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> Optional[CompensationRead]:
    profile = db.scalars(
        select(UserProfile).where(UserProfile.account_id == account_id)
    ).first()
    if not profile:
        return None
    stmt = select(CompensationExpectation).where(
        CompensationExpectation.profile_id == profile.id
    )
    return db.scalars(stmt).first()


@router.put(
    "/compensation",
    response_model=CompensationRead,
    summary="Set or update compensation expectations",
)
def set_compensation(
    account_id: str = Query(...),
    payload: CompensationCreate = ...,
    db: Session = Depends(get_db),
) -> CompensationRead:
    profile = _get_or_create_profile(db, account_id)
    existing = db.scalars(
        select(CompensationExpectation).where(
            CompensationExpectation.profile_id == profile.id
        )
    ).first()

    if existing:
        for field, value in payload.model_dump().items():
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return existing

    comp = CompensationExpectation(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp


# ---------------------------------------------------------------------------
# Spoken Languages
# ---------------------------------------------------------------------------

@router.get(
    "/languages",
    response_model=List[SpokenLanguageRead],
    summary="List spoken languages",
)
def list_languages(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[SpokenLanguageRead]:
    profile = db.scalars(
        select(UserProfile).where(UserProfile.account_id == account_id)
    ).first()
    if not profile:
        return []
    stmt = select(SpokenLanguage).where(SpokenLanguage.profile_id == profile.id)
    return list(db.scalars(stmt).all())


@router.post(
    "/languages",
    response_model=SpokenLanguageRead,
    status_code=status.HTTP_201_CREATED,
    summary="Add a spoken language",
)
def add_language(
    account_id: str = Query(...),
    payload: SpokenLanguageCreate = ...,
    db: Session = Depends(get_db),
) -> SpokenLanguageRead:
    profile = _get_or_create_profile(db, account_id)
    lang = SpokenLanguage(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(lang)
    db.commit()
    db.refresh(lang)
    return lang


@router.delete(
    "/languages/{language_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a spoken language",
)
def delete_language(
    language_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    lang = db.scalars(
        select(SpokenLanguage).where(
            SpokenLanguage.id == language_id,
            SpokenLanguage.account_id == account_id,
        )
    ).first()
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found.")
    db.delete(lang)
    db.commit()


# ---------------------------------------------------------------------------
# CV Auto-Parser & Profile Population
# ---------------------------------------------------------------------------

@router.post(
    "/parse-cv",
    summary="Upload CV file (PDF, DOCX, TXT) and extract structured career data via LLM",
)
@router.post(
    "/parse_cv",
    include_in_schema=False,
)
async def parse_cv_file(
    file: UploadFile = File(...),
    account_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    try:
        raw_text = CVParserService.extract_text(contents, file.filename or "cv.pdf")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not extract text from document: {e}")

    if len(raw_text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Uploaded document contains no readable text.")

    llm = LLMService(db_session=db, account_id=account_id)
    try:
        parsed = await CVParserService.parse_cv_text(raw_text, llm)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse career profile with AI: {e}")

    return {
        "status": "success",
        "filename": file.filename,
        "extracted_chars": len(raw_text),
        "data": parsed,
    }


@router.post(
    "/apply-parsed-cv",
    summary="Save parsed CV data directly into user's profile and career tables",
)
def apply_parsed_cv(
    account_id: str = Query(...),
    payload: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    profile = _get_or_create_profile(db, account_id)

    # 1. Update Profile identity fields
    for field in [
        "full_name",
        "headline",
        "phone",
        "summary",
        "location_city",
        "location_country",
        "linkedin_url",
        "github_url",
        "portfolio_url",
    ]:
        if payload.get(field):
            setattr(profile, field, payload[field])

    # 1b. Set active template if selected
    tmpl_name = payload.get("template_name") or payload.get("selected_template")
    if tmpl_name:
        tmpl = db.scalars(select(CvTemplate).where(CvTemplate.name == tmpl_name)).first()
        if tmpl:
            profile.active_template_id = tmpl.id
    elif payload.get("active_template_id"):
        profile.active_template_id = payload["active_template_id"]

    # 2. Add Target Designations
    if payload.get("target_designations"):
        existing_desigs = {d.title.lower() for d in profile.target_designations}
        for idx, title in enumerate(payload["target_designations"]):
            if title and title.strip() and title.strip().lower() not in existing_desigs:
                db.add(
                    TargetDesignation(
                        account_id=account_id,
                        profile_id=profile.id,
                        title=title.strip(),
                        priority=idx,
                        is_active=True,
                    )
                )

    # 3. Add Work Experiences
    if payload.get("work_experiences"):
        for idx, exp_data in enumerate(payload["work_experiences"]):
            highlights = exp_data.get("highlights")
            if isinstance(highlights, list):
                highlights = json.dumps(highlights)
            db.add(
                WorkExperience(
                    account_id=account_id,
                    profile_id=profile.id,
                    company=exp_data.get("company") or "Company",
                    title=exp_data.get("title") or "Role",
                    location=exp_data.get("location"),
                    location_type=exp_data.get("location_type") or "onsite",
                    start_date=exp_data.get("start_date") or "2020",
                    end_date=exp_data.get("end_date"),
                    is_current=bool(exp_data.get("is_current")),
                    description=exp_data.get("description"),
                    highlights=highlights,
                    order_index=idx,
                )
            )

    # 4. Add Educations
    if payload.get("educations"):
        for idx, edu_data in enumerate(payload["educations"]):
            db.add(
                Education(
                    account_id=account_id,
                    profile_id=profile.id,
                    institution=edu_data.get("institution") or "University",
                    degree=edu_data.get("degree") or "Degree",
                    field_of_study=edu_data.get("field_of_study"),
                    location=edu_data.get("location"),
                    start_date=edu_data.get("start_date"),
                    end_date=edu_data.get("end_date"),
                    grade=edu_data.get("grade"),
                    activities=edu_data.get("activities"),
                    order_index=idx,
                )
            )

    # 5. Add Skills
    if payload.get("skills"):
        for idx, sk_data in enumerate(payload["skills"]):
            name = sk_data.get("name") if isinstance(sk_data, dict) else str(sk_data)
            category = sk_data.get("category", "Technical") if isinstance(sk_data, dict) else "Technical"
            proficiency = sk_data.get("proficiency", "Intermediate") if isinstance(sk_data, dict) else "Intermediate"
            yrs = sk_data.get("years_of_experience") if isinstance(sk_data, dict) else None
            if name and name.strip():
                db.add(
                    ProfileSkill(
                        account_id=account_id,
                        profile_id=profile.id,
                        name=name.strip(),
                        category=category,
                        proficiency=proficiency,
                        years_of_experience=yrs,
                        order_index=idx,
                    )
                )

    # 6. Add Projects
    if payload.get("projects"):
        for idx, p_data in enumerate(payload["projects"]):
            highlights = p_data.get("highlights")
            if isinstance(highlights, list):
                highlights = json.dumps(highlights)
            db.add(
                Project(
                    account_id=account_id,
                    profile_id=profile.id,
                    title=p_data.get("title") or "Project",
                    role=p_data.get("role"),
                    url=p_data.get("url"),
                    github_url=p_data.get("github_url"),
                    start_date=p_data.get("start_date"),
                    end_date=p_data.get("end_date"),
                    description=p_data.get("description"),
                    highlights=highlights,
                    technologies=p_data.get("technologies"),
                    order_index=idx,
                )
            )

    # 7. Add Certifications
    if payload.get("certifications"):
        for idx, c_data in enumerate(payload["certifications"]):
            db.add(
                Certification(
                    account_id=account_id,
                    profile_id=profile.id,
                    name=c_data.get("name") or "Certification",
                    issuing_organization=c_data.get("issuing_organization") or "Issuer",
                    issue_date=c_data.get("issue_date"),
                    expiration_date=c_data.get("expiration_date"),
                    credential_id=c_data.get("credential_id"),
                    credential_url=c_data.get("credential_url"),
                    order_index=idx,
                )
            )

    db.commit()
    db.refresh(profile)
    return {"status": "success", "message": "Profile updated with parsed CV data."}


# ---------------------------------------------------------------------------
# Template Preview & Compilation
# ---------------------------------------------------------------------------

@router.get(
    "/preview-cv",
    summary="Generate compiled LaTeX CV preview from candidate's profile entities",
)
@router.get(
    "/preview_cv",
    include_in_schema=False,
)
def preview_cv(
    account_id: str = Query(...),
    template_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    stmt = (
        select(UserProfile)
        .where(UserProfile.account_id == account_id)
        .options(
            selectinload(UserProfile.target_designations),
            selectinload(UserProfile.target_locations),
            selectinload(UserProfile.compensation),
            selectinload(UserProfile.spoken_languages),
            selectinload(UserProfile.work_experiences),
            selectinload(UserProfile.educations),
            selectinload(UserProfile.skills),
            selectinload(UserProfile.projects),
            selectinload(UserProfile.certifications),
        )
    )
    profile = db.scalars(stmt).first()
    if not profile:
        # Check if account exists
        account = db.scalars(select(Account).where(Account.id == account_id)).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found.")
        _get_or_create_profile(db, account_id)
        profile = db.scalars(stmt).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    target_template_id = template_id or profile.active_template_id
    template = None
    if target_template_id:
        template = db.scalars(
            select(CvTemplate).where(
                or_(
                    CvTemplate.id == target_template_id,
                    CvTemplate.name == target_template_id,
                )
            )
        ).first()
        if template and template_id:
            profile.active_template_id = template.id
            db.commit()
    if not template:
        template = db.scalars(select(CvTemplate).where(CvTemplate.is_admin_default == True)).first()
    if not template:
        template = db.scalars(select(CvTemplate)).first()

    template_source = template.latex_source if template else (
        "\\documentclass{article}\n\\begin{document}\n"
        "\\textbf{{{FULL_NAME}}} \\quad {{HEADLINE}}\n"
        "{{SUMMARY_SECTION}}\n{{EXPERIENCE_SECTION}}\n{{EDUCATION_SECTION}}\n{{SKILLS_SECTION}}\n{{PROJECTS_SECTION}}\n{{CERTIFICATIONS_SECTION}}\n"
        "\\end{document}"
    )
    t_id = template.id if template else "fallback-modern"
    t_name = template.name if template else "Modern Tech Fallback"

    compiled = CVTemplateCompiler.compile_cv(
        template_source=template_source,
        profile={
            "full_name": profile.full_name,
            "headline": profile.headline,
            "phone": profile.phone,
            "email": profile.account.email if profile.account else None,
            "summary": profile.summary,
            "location_city": profile.location_city,
            "location_country": profile.location_country,
            "linkedin_url": profile.linkedin_url,
            "github_url": profile.github_url,
            "portfolio_url": profile.portfolio_url,
        },
        experiences=[
            {
                "company": e.company,
                "title": e.title,
                "location": e.location,
                "start_date": e.start_date,
                "end_date": e.end_date,
                "is_current": e.is_current,
                "description": e.description,
                "highlights": e.highlights,
            }
            for e in profile.work_experiences
        ],
        educations=[
            {
                "institution": ed.institution,
                "degree": ed.degree,
                "field_of_study": ed.field_of_study,
                "location": ed.location,
                "start_date": ed.start_date,
                "end_date": ed.end_date,
                "grade": ed.grade,
            }
            for ed in profile.educations
        ],
        skills=[{"name": s.name, "category": s.category, "proficiency": s.proficiency} for s in profile.skills],
        projects=[
            {
                "title": pr.title,
                "role": pr.role,
                "url": pr.url,
                "github_url": pr.github_url,
                "start_date": pr.start_date,
                "end_date": pr.end_date,
                "technologies": pr.technologies,
                "highlights": pr.highlights,
            }
            for pr in profile.projects
        ],
        certifications=[
            {"name": c.name, "issuing_organization": c.issuing_organization, "issue_date": c.issue_date}
            for c in profile.certifications
        ],
    )

    return {
        "template_id": t_id,
        "template_name": t_name,
        "latex_source": compiled,
    }


@router.post(
    "/compile-texlive",
    summary="Compile raw LaTeX into PDF using server TeX Live engine (Overleaf CLSI pattern)",
)
def compile_texlive(
    payload: Dict[str, Any] = Body(...),
) -> Dict[str, Any]:
    latex_source = payload.get("latex_source", "")
    account_id = payload.get("account_id", "anon")
    compiler = payload.get("compiler", "pdflatex")

    result = TeXLiveCompilerService.compile_latex(
        latex_source=latex_source,
        account_id=account_id,
        compiler=compiler,
    )

    pdf_bytes = result.pop("pdf_bytes", None)
    pdf_base64 = base64.b64encode(pdf_bytes).decode("ascii") if pdf_bytes else None

    return {
        **result,
        "pdf_base64": pdf_base64,
    }


# ---------------------------------------------------------------------------
# Saved Resumes & CV Keeper Endpoints (Max 5 Resumes Per Tenant)
# ---------------------------------------------------------------------------

def _resolve_target_account_id(
    account_id: Optional[str],
    x_account_id: Optional[str],
    authorization: Optional[str],
    db: Session,
) -> str:
    from app.core.auth import decode_access_token
    if authorization and authorization.startswith("Bearer "):
        try:
            token = authorization.split("Bearer ")[1].strip()
            payload = decode_access_token(token)
            sub = payload.get("sub")
            if sub:
                return sub
        except Exception:
            pass
    target = account_id or x_account_id
    if target:
        return target
    first_acc = db.scalars(select(Account).order_by(Account.created_at)).first()
    if first_acc:
        return first_acc.id
    raise HTTPException(status_code=400, detail="account_id required")


@router.get(
    "/resumes",
    summary="List all saved resumes for the tenant account (max 5)",
)
def list_user_resumes(
    account_id: Optional[str] = Query(None),
    x_account_id: Optional[str] = Header(None, alias="X-Account-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    target_id = _resolve_target_account_id(account_id, x_account_id, authorization, db)

    stmt = (
        select(UserResume)
        .where(UserResume.account_id == target_id)
        .order_by(UserResume.is_default.desc(), UserResume.created_at.desc())
    )
    resumes = db.scalars(stmt).all()

    items = [
        UserResumeSummary(
            id=r.id,
            account_id=r.account_id,
            profile_id=r.profile_id,
            name=r.name,
            filename=r.filename,
            source_type=r.source_type,
            file_size_bytes=r.file_size_bytes,
            page_count=r.page_count,
            is_default=r.is_default,
            has_latex=bool(r.latex_source and r.latex_source.strip()),
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in resumes
    ]
    return {
        "account_id": target_id,
        "count": len(items),
        "max_limit": 5,
        "resumes": items,
    }


@router.post(
    "/resumes/upload",
    summary="Upload a readymade PDF resume/CV document (max 5 enforced)",
)
async def upload_user_resume(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None),
    is_default: bool = Form(False),
    account_id: Optional[str] = Form(None),
    query_account_id: Optional[str] = Query(None, alias="account_id"),
    x_account_id: Optional[str] = Header(None, alias="X-Account-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    effective_acc_id = account_id or query_account_id
    target_id = _resolve_target_account_id(effective_acc_id, x_account_id, authorization, db)

    existing_count = db.scalar(
        select(func.count(UserResume.id)).where(UserResume.account_id == target_id)
    ) or 0
    if existing_count >= 5:
        raise HTTPException(
            status_code=400,
            detail="Maximum limit of 5 saved resumes reached. Please delete an existing resume to upload a new one.",
        )

    filename = file.filename or "resume.pdf"
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds maximum 10MB limit.")

    try:
        reader = pypdf.PdfReader(io.BytesIO(content))
        page_count = max(1, len(reader.pages))
        extracted_text_pieces = []
        for p in reader.pages:
            t = p.extract_text()
            if t:
                extracted_text_pieces.append(t)
        extracted_text = "\n".join(extracted_text_pieces).strip()
    except Exception as e:
        logger.warning(f"Failed to parse PDF text with pypdf: {e}")
        page_count = 1
        extracted_text = ""

    display_name = (name or "").strip()
    if not display_name:
        display_name = filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()

    should_be_default = is_default or (existing_count == 0)
    if should_be_default:
        db.query(UserResume).filter(UserResume.account_id == target_id).update({"is_default": False})

    profile = _get_or_create_profile(db, target_id)
    pdf_b64 = base64.b64encode(content).decode("ascii")

    resume = UserResume(
        account_id=target_id,
        profile_id=profile.id,
        name=display_name,
        filename=filename,
        source_type="uploaded",
        latex_source=None,
        pdf_data=pdf_b64,
        file_size_bytes=len(content),
        page_count=page_count,
        extracted_text=extracted_text,
        is_default=should_be_default,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "id": resume.id,
        "account_id": resume.account_id,
        "name": resume.name,
        "filename": resume.filename,
        "source_type": resume.source_type,
        "file_size_bytes": resume.file_size_bytes,
        "page_count": resume.page_count,
        "is_default": resume.is_default,
        "has_latex": False,
        "created_at": resume.created_at.isoformat(),
        "updated_at": resume.updated_at.isoformat(),
    }


@router.post(
    "/resumes/save-builder",
    summary="Save or compile a resume from LaTeX Resume Builder",
)
def save_builder_resume(
    payload: Dict[str, Any] = Body(...),
    account_id: Optional[str] = Query(None),
    x_account_id: Optional[str] = Header(None, alias="X-Account-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    effective_acc_id = account_id or payload.get("account_id")
    target_id = _resolve_target_account_id(effective_acc_id, x_account_id, authorization, db)

    name = (payload.get("name") or "Built Resume").strip()
    latex_source = (payload.get("latex_source") or "").strip()
    pdf_base64 = payload.get("pdf_base64")
    resume_id = payload.get("resume_id")
    is_default = payload.get("is_default", False)

    if not latex_source:
        raise HTTPException(status_code=400, detail="latex_source cannot be empty.")

    existing_resume = None
    if resume_id:
        existing_resume = db.scalars(
            select(UserResume).where(UserResume.id == resume_id, UserResume.account_id == target_id)
        ).first()

    if not existing_resume:
        count = db.scalar(select(func.count(UserResume.id)).where(UserResume.account_id == target_id)) or 0
        if count >= 5:
            raise HTTPException(
                status_code=400,
                detail="Maximum limit of 5 saved resumes reached. Please delete an existing resume to save a new one.",
            )

    pdf_bytes = None
    if pdf_base64:
        try:
            pdf_bytes = base64.b64decode(pdf_base64)
        except Exception:
            pdf_bytes = None

    if not pdf_bytes:
        comp_res = TeXLiveCompilerService.compile_latex(
            latex_source=latex_source,
            account_id=target_id,
            compiler="pdflatex",
        )
        pdf_bytes = comp_res.get("pdf_bytes")
        if pdf_bytes:
            pdf_base64 = base64.b64encode(pdf_bytes).decode("ascii")

    page_count = 1
    extracted_text = ""
    if pdf_bytes:
        try:
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            page_count = max(1, len(reader.pages))
            extracted_text = "\n".join(p.extract_text() or "" for p in reader.pages).strip()
        except Exception:
            pass

    if not extracted_text:
        from app.services.matching.profile_parser import ProfileParser
        extracted_text = ProfileParser.extract_clean_cv_text(latex_source)

    profile = _get_or_create_profile(db, target_id)
    total_count = db.scalar(select(func.count(UserResume.id)).where(UserResume.account_id == target_id)) or 0
    should_be_default = is_default or (total_count == 0)

    if should_be_default:
        db.query(UserResume).filter(UserResume.account_id == target_id).update({"is_default": False})

    clean_slug = re.sub(r"[^a-zA-Z0-9_-]", "_", name.lower()).strip("_") or "resume"
    filename = f"{clean_slug}.pdf"

    if existing_resume:
        existing_resume.name = name
        existing_resume.filename = filename
        existing_resume.latex_source = latex_source
        if pdf_base64:
            existing_resume.pdf_data = pdf_base64
            existing_resume.file_size_bytes = len(pdf_bytes) if pdf_bytes else len(pdf_base64)
            existing_resume.page_count = page_count
        existing_resume.extracted_text = extracted_text
        if is_default is not None:
            existing_resume.is_default = should_be_default
        db.commit()
        db.refresh(existing_resume)
        res_obj = existing_resume
    else:
        new_resume = UserResume(
            account_id=target_id,
            profile_id=profile.id,
            name=name,
            filename=filename,
            source_type="builder",
            latex_source=latex_source,
            pdf_data=pdf_base64,
            file_size_bytes=len(pdf_bytes) if pdf_bytes else 0,
            page_count=page_count,
            extracted_text=extracted_text,
            is_default=should_be_default,
        )
        db.add(new_resume)
        db.commit()
        db.refresh(new_resume)
        res_obj = new_resume

    return {
        "id": res_obj.id,
        "account_id": res_obj.account_id,
        "name": res_obj.name,
        "filename": res_obj.filename,
        "source_type": res_obj.source_type,
        "file_size_bytes": res_obj.file_size_bytes,
        "page_count": res_obj.page_count,
        "is_default": res_obj.is_default,
        "has_latex": True,
        "created_at": res_obj.created_at.isoformat(),
        "updated_at": res_obj.updated_at.isoformat(),
    }


@router.put(
    "/resumes/{resume_id}/default",
    summary="Set a saved resume as the default resume for the account",
)
def set_default_resume(
    resume_id: str,
    account_id: Optional[str] = Query(None),
    x_account_id: Optional[str] = Header(None, alias="X-Account-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    target_id = _resolve_target_account_id(account_id, x_account_id, authorization, db)
    resume = db.scalars(
        select(UserResume).where(UserResume.id == resume_id, UserResume.account_id == target_id)
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    acc_id = resume.account_id
    db.query(UserResume).filter(UserResume.account_id == acc_id).update({"is_default": False})
    resume.is_default = True
    db.commit()
    db.refresh(resume)
    return {"id": resume.id, "name": resume.name, "is_default": True}


@router.get(
    "/resumes/{resume_id}",
    summary="Get detailed resume document including PDF data and LaTeX source",
)
def get_user_resume(
    resume_id: str,
    account_id: Optional[str] = Query(None),
    x_account_id: Optional[str] = Header(None, alias="X-Account-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    target_id = _resolve_target_account_id(account_id, x_account_id, authorization, db)
    resume = db.scalars(
        select(UserResume).where(UserResume.id == resume_id, UserResume.account_id == target_id)
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    return {
        "id": resume.id,
        "account_id": resume.account_id,
        "profile_id": resume.profile_id,
        "name": resume.name,
        "filename": resume.filename,
        "source_type": resume.source_type,
        "latex_source": resume.latex_source,
        "pdf_data": resume.pdf_data,
        "file_size_bytes": resume.file_size_bytes,
        "page_count": resume.page_count,
        "extracted_text": resume.extracted_text,
        "is_default": resume.is_default,
        "created_at": resume.created_at.isoformat(),
        "updated_at": resume.updated_at.isoformat(),
    }


@router.get(
    "/resumes/{resume_id}/download",
    summary="Download PDF binary for a saved resume",
)
def download_user_resume(
    resume_id: str,
    account_id: Optional[str] = Query(None),
    x_account_id: Optional[str] = Header(None, alias="X-Account-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
):
    target_id = _resolve_target_account_id(account_id, x_account_id, authorization, db)
    resume = db.scalars(
        select(UserResume).where(UserResume.id == resume_id, UserResume.account_id == target_id)
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    if not resume.pdf_data:
        if resume.latex_source:
            res = TeXLiveCompilerService.compile_latex(latex_source=resume.latex_source, account_id=resume.account_id)
            pdf_bytes = res.get("pdf_bytes")
            if pdf_bytes:
                return Response(
                    content=pdf_bytes,
                    media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="{resume.filename}"'},
                )
        raise HTTPException(status_code=404, detail="No PDF binary available for this resume.")

    try:
        pdf_bytes = base64.b64decode(resume.pdf_data)
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid PDF base64 encoding.")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{resume.filename}"'},
    )


@router.delete(
    "/resumes/{resume_id}",
    summary="Delete a saved resume document",
)
def delete_user_resume(
    resume_id: str,
    account_id: Optional[str] = Query(None),
    x_account_id: Optional[str] = Header(None, alias="X-Account-ID"),
    authorization: Optional[str] = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    target_id = _resolve_target_account_id(account_id, x_account_id, authorization, db)
    resume = db.scalars(
        select(UserResume).where(UserResume.id == resume_id, UserResume.account_id == target_id)
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    acc_id = resume.account_id
    was_default = resume.is_default
    db.delete(resume)
    db.commit()

    if was_default:
        next_default = db.scalars(
            select(UserResume).where(UserResume.account_id == acc_id).order_by(UserResume.created_at.desc())
        ).first()
        if next_default:
            next_default.is_default = True
            db.commit()

    return {"message": "Resume deleted successfully", "id": resume_id}


# ---------------------------------------------------------------------------
# Experience Reflector Insights
# ---------------------------------------------------------------------------

@router.get(
    "/experience-insights",
    summary="Get autonomous Experience Reflector insights, channel conversion, and dynamic skill multipliers",
)
def get_experience_insights(
    account_id: Optional[str] = Query(None),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    target_id = account_id or current_account.id
    reflector = ExperienceReflector(db)
    insights = reflector.reflect_for_account(target_id)
    return {
        "account_id": insights.account_id,
        "total_applications": insights.total_applications,
        "interviews_count": insights.interviews_count,
        "offers_count": insights.offers_count,
        "rejections_count": insights.rejections_count,
        "overall_conversion_rate": insights.overall_conversion_rate,
        "channel_performance": {
            k: {
                "channel": v.channel,
                "total_applied": v.total_applied,
                "interviews": v.interviews,
                "offers": v.offers,
                "rejections": v.rejections,
                "conversion_rate": v.conversion_rate,
            }
            for k, v in insights.channel_performance.items()
        },
        "top_performing_skills": insights.top_performing_skills,
        "underperforming_keywords": insights.underperforming_keywords,
        "skill_weight_multipliers": insights.skill_weight_multipliers,
        "strategic_recommendations": insights.strategic_recommendations,
        "generated_at": insights.generated_at,
    }
