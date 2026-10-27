"""
Profile management API — CRUD for UserProfile, TargetDesignation, TargetLocation,
CompensationExpectation, and SpokenLanguage.

All endpoints are scoped to account_id (multi-tenant, Phase 0 trusted parameter —
see ARCHITECTURE.md §13 for the Phase 3 auth migration plan).
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.account import Account
from app.models.profile import (
    CompensationExpectation,
    CompensationBase,
    CompensationCreate,
    CompensationRead,
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
)

router = APIRouter(prefix="/profile", tags=["profile"])


def _get_or_create_profile(db: Session, account_id: str) -> UserProfile:
    """Ensure a UserProfile row exists for an account, auto-creating a clean default if needed."""
    profile = db.scalars(
        select(UserProfile).where(UserProfile.account_id == account_id)
    ).first()
    if not profile:
        profile = UserProfile(account_id=account_id)
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
def get_current_account(
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
        raise HTTPException(status_code=404, detail="Designation not found.")
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
    location = TargetLocation(
        account_id=account_id,
        profile_id=profile.id,
        **payload.model_dump(),
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


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
    location = db.scalars(
        select(TargetLocation).where(
            TargetLocation.id == location_id,
            TargetLocation.account_id == account_id,
        )
    ).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found.")
    db.delete(location)
    db.commit()


# ---------------------------------------------------------------------------
# Compensation Expectation
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
    comp = db.scalars(
        select(CompensationExpectation).where(
            CompensationExpectation.account_id == account_id
        )
    ).first()
    return comp


@router.put(
    "/compensation",
    response_model=CompensationRead,
    summary="Set or update compensation expectations",
)
def upsert_compensation(
    account_id: str = Query(...),
    payload: CompensationCreate = ...,
    db: Session = Depends(get_db),
) -> CompensationRead:
    profile = _get_or_create_profile(db, account_id)

    comp = db.scalars(
        select(CompensationExpectation).where(
            CompensationExpectation.account_id == account_id
        )
    ).first()

    if comp:
        for field, value in payload.model_dump().items():
            setattr(comp, field, value)
    else:
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
