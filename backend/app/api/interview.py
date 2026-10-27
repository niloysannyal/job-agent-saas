"""
STAR Interview Coach API — CRUD for interview stories + tag-based querying.

All endpoints are scoped to account_id (multi-tenant, Phase 0 trusted parameter).
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.interview import (
    StarStory,
    StarStoryCreate,
    StarStoryRead,
    StarStoryUpdate,
)

router = APIRouter(prefix="/interview", tags=["interview"])


# ---------------------------------------------------------------------------
# STAR Stories CRUD
# ---------------------------------------------------------------------------

@router.get(
    "/stories",
    response_model=List[StarStoryRead],
    summary="List all STAR stories for an account",
)
def list_stories(
    account_id: str = Query(..., description="Target account ID"),
    tag: Optional[str] = Query(
        None,
        description="Filter stories containing this tag (case-insensitive substring match on good_for_tags)",
    ),
    verified_only: bool = Query(
        False,
        description="Only return stories marked as verified",
    ),
    db: Session = Depends(get_db),
) -> List[StarStoryRead]:
    """Fetch STAR stories, optionally filtered by tag or verification status."""
    stmt = (
        select(StarStory)
        .where(StarStory.account_id == account_id)
        .order_by(StarStory.sort_order, StarStory.created_at.desc())
    )

    if verified_only:
        stmt = stmt.where(StarStory.is_verified == True)

    stories = list(db.scalars(stmt).all())

    # Client-side tag filtering (simple substring match)
    if tag:
        tag_lower = tag.strip().lower()
        stories = [
            s for s in stories
            if tag_lower in (s.good_for_tags or "").lower()
        ]

    return stories


@router.get(
    "/stories/{story_id}",
    response_model=StarStoryRead,
    summary="Get a single STAR story by ID",
)
def get_story(
    story_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> StarStoryRead:
    story = db.scalars(
        select(StarStory).where(
            StarStory.id == story_id,
            StarStory.account_id == account_id,
        )
    ).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found.")
    return story


@router.post(
    "/stories",
    response_model=StarStoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new STAR story",
)
def create_story(
    account_id: str = Query(...),
    payload: StarStoryCreate = ...,
    db: Session = Depends(get_db),
) -> StarStoryRead:
    story = StarStory(account_id=account_id, **payload.model_dump())
    db.add(story)
    db.commit()
    db.refresh(story)
    return story


@router.patch(
    "/stories/{story_id}",
    response_model=StarStoryRead,
    summary="Update a STAR story",
)
def update_story(
    story_id: str,
    account_id: str = Query(...),
    payload: StarStoryUpdate = ...,
    db: Session = Depends(get_db),
) -> StarStoryRead:
    story = db.scalars(
        select(StarStory).where(
            StarStory.id == story_id,
            StarStory.account_id == account_id,
        )
    ).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found.")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(story, field, value)

    db.commit()
    db.refresh(story)
    return story


@router.delete(
    "/stories/{story_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a STAR story",
)
def delete_story(
    story_id: str,
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> None:
    story = db.scalars(
        select(StarStory).where(
            StarStory.id == story_id,
            StarStory.account_id == account_id,
        )
    ).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found.")
    db.delete(story)
    db.commit()


@router.get(
    "/tags",
    response_model=List[str],
    summary="List all unique STAR story tags for an account",
)
def list_tags(
    account_id: str = Query(...),
    db: Session = Depends(get_db),
) -> List[str]:
    """Extract all unique tags across the account's STAR stories."""
    stories = db.scalars(
        select(StarStory).where(StarStory.account_id == account_id)
    ).all()
    tags: set[str] = set()
    for story in stories:
        if story.good_for_tags:
            for tag in story.good_for_tags.split(","):
                cleaned = tag.strip()
                if cleaned:
                    tags.add(cleaned)
    return sorted(tags)
