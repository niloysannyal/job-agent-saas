from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, get_current_account
from app.core.config import settings
from app.db.session import get_db
from app.models.account import (
    Account,
    AccountCreate,
    AuthMeResponse,
    EmailVerification,
    LoginRequest,
    SendOtpRequest,
    SendOtpResponse,
    TokenResponse,
    VerifyOtpSignupRequest,
)
from app.models.profile import UserProfile
from app.models.subscription import Entitlement
from app.services.email.email_service import generate_otp, send_otp_email, is_smtp_configured

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
        is_new_user=False,
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
    db.flush()

    # Create default entitlement
    entitlement = Entitlement(
        account_id=account.id,
        plan_tier="free",
        all_access=True,
    )
    db.add(entitlement)

    # Create profile if full_name is provided
    if req.full_name:
        profile = UserProfile(
            account_id=account.id,
            full_name=req.full_name.strip(),
        )
        db.add(profile)

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
        is_new_user=True,
    )


@router.post("/signup/send-otp", response_model=SendOtpResponse)
def send_signup_otp(
    req: SendOtpRequest,
    db: Session = Depends(get_db),
):
    """
    Generate and dispatch a 6-digit OTP verification code to candidate's email.
    Enforces a 60-second rate-limit cooldown between OTP requests for the same address.
    """
    email = req.email.strip().lower()
    if not email or "@" not in email or "." not in email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A valid email address is required.",
        )

    # Check if account already registered
    existing_account = db.query(Account).filter_by(email=email).first()
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists. Please sign in instead.",
        )

    now = datetime.now(timezone.utc)

    # Rate limiting: 60 seconds cooldown between OTP requests
    recent_otp = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.email == email,
            EmailVerification.created_at >= now - timedelta(seconds=60),
        )
        .first()
    )
    if recent_otp:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="A verification code was recently sent. Please wait 60 seconds before requesting another.",
        )

    # Generate 6-digit OTP
    otp_code = generate_otp()
    expires_at = now + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

    verification = EmailVerification(
        email=email,
        otp_code=otp_code,
        expires_at=expires_at,
        attempts=0,
        is_verified=False,
    )
    db.add(verification)
    db.commit()

    # Dispatch email
    sent = send_otp_email(email, otp_code)
    if not sent and is_smtp_configured():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email. Please try again later.",
        )

    # In dev/test mode where SMTP is not configured, provide dev_otp for developer ease
    dev_otp = otp_code if not is_smtp_configured() else None

    return SendOtpResponse(
        status="success",
        email=email,
        message=f"Verification code sent to {email}. Valid for {settings.OTP_EXPIRE_MINUTES} minutes.",
        dev_otp=dev_otp,
    )


@router.post("/signup/verify-otp", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def verify_signup_otp(
    req: VerifyOtpSignupRequest,
    db: Session = Depends(get_db),
):
    """
    Verify 6-digit OTP code, create tenant account with full name and profile,
    and return an authenticated JWT token.
    """
    email = req.email.strip().lower()
    otp_code = req.otp_code.strip()
    full_name = req.full_name.strip()
    password = req.password

    if not full_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Full Name is required.",
        )

    if not password or len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 6 characters long.",
        )

    # Check for existing account
    existing_account = db.query(Account).filter_by(email=email).first()
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists. Please sign in instead.",
        )

    now = datetime.now(timezone.utc)

    # Find the latest pending verification for this email
    verification = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.email == email,
            EmailVerification.is_verified.is_(False),
        )
        .order_by(EmailVerification.created_at.desc())
        .first()
    )

    if not verification:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No verification request found for this email. Please request a new code.",
        )

    # Check expiration
    exp = verification.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if exp < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code has expired. Please request a new code.",
        )

    # Check maximum attempts (max 5)
    if verification.attempts >= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum verification attempts exceeded. Please request a new code.",
        )

    # Verify code
    if verification.otp_code != otp_code:
        verification.attempts += 1
        db.commit()
        attempts_left = 5 - verification.attempts
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid verification code. {attempts_left} attempt{'s' if attempts_left != 1 else ''} remaining.",
        )

    # Mark as verified
    verification.is_verified = True

    # Create Account
    account = Account(
        email=email,
        plan_tier="free",
        role="tenant",
        status="active",
    )
    account.set_password(password)
    db.add(account)
    db.flush()  # populate account.id

    # Create Entitlement
    entitlement = Entitlement(
        account_id=account.id,
        plan_tier="free",
        all_access=True,
    )
    db.add(entitlement)

    # Auto-initialize UserProfile with full_name and headline
    profile = UserProfile(
        account_id=account.id,
        full_name=full_name,
        headline=req.headline.strip() if req.headline else None,
    )
    db.add(profile)

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
        is_new_user=True,
    )


@router.get("/me", response_model=AuthMeResponse)
def get_me(
    current_account: Account = Depends(get_current_account),
):
    """
    Retrieve authenticated account profile and permissions from validated token.
    """
    return current_account


# --- Google OAuth Aliases ---

@router.get("/google/authorize", summary="Google OAuth authorization URL redirect or link")
def auth_google_authorize(
    state: Optional[str] = "state_oauth_google",
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    from app.services.integrations.google_service import GoogleIntegrationService
    creds = GoogleIntegrationService.resolve_platform_credentials(db=db, account_id=current_account.id)
    client_id = creds.get("client_id")
    if not client_id and getattr(settings, "ENVIRONMENT", "development").lower() in ("production", "staging"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google OAuth application is not configured on this platform.",
        )
    url = GoogleIntegrationService.get_authorization_url(
        state=f"{current_account.id}:{state}",
        db=db,
        account_id=current_account.id,
    )
    return {"auth_url": url}


@router.get("/google/callback", summary="Google OAuth browser redirect callback")
async def auth_google_callback_get(
    code: str = Query(...),
    state: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    from app.api.integrations import google_oauth_get_callback
    return await google_oauth_get_callback(code=code, state=state, db=db)


@router.post("/google/callback", summary="Google OAuth code exchange callback")
async def auth_google_callback_post(
    data: dict,
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    from app.api.integrations import google_oauth_callback, GoogleCallbackRequest
    req = GoogleCallbackRequest(code=data.get("code", ""), state=data.get("state"))
    return await google_oauth_callback(data=req, current_account=current_account, db=db)

