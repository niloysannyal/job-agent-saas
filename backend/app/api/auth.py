from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, get_current_account
from app.db.session import get_db
from app.models.account import (
    Account,
    AccountCreate,
    AuthMeResponse,
    LoginRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])

DEFAULT_DEV_PASSWORD = "Password123!"


@router.post("/login", response_model=TokenResponse)
def login(
    req: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate user credentials and issue signed JWT bearer token.
    Supports auto-initialization for seeded accounts (sets default password if unset).
    """
    account = db.query(Account).filter_by(email=req.email.strip().lower()).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if account.status == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been suspended by the administrator.",
        )

    # If account was created before password migration, seed password if matches default or set it
    if not account.hashed_password:
        if req.password == DEFAULT_DEV_PASSWORD or req.password == "JobEazy2026!" or req.password:
            account.set_password(req.password)
            db.commit()
            db.refresh(account)
    else:
        if not account.verify_password(req.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

    token = create_access_token(
        data={
            "sub": account.id,
            "email": account.email,
            "role": account.role,
            "plan_tier": account.plan_tier,
        }
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        account_id=account.id,
        email=account.email,
        role=account.role,
        plan_tier=account.plan_tier,
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(
    req: AccountCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new tenant account with email and password.
    Returns authenticated JWT bearer token directly.
    """
    email = req.email.strip().lower()
    existing = db.query(Account).filter_by(email=email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    account = Account(
        email=email,
        plan_tier=req.plan_tier or "free",
        role="tenant",
        status="active",
    )
    if req.password:
        account.set_password(req.password)
    else:
        account.set_password(DEFAULT_DEV_PASSWORD)

    db.add(account)
    db.commit()
    db.refresh(account)

    token = create_access_token(
        data={
            "sub": account.id,
            "email": account.email,
            "role": account.role,
            "plan_tier": account.plan_tier,
        }
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        account_id=account.id,
        email=account.email,
        role=account.role,
        plan_tier=account.plan_tier,
    )


@router.get("/me", response_model=AuthMeResponse)
def get_me(
    current_account: Account = Depends(get_current_account),
):
    """
    Retrieve authenticated account profile and permissions from validated token.
    """
    return current_account

