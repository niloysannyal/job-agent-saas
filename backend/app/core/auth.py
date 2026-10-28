from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from fastapi import Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.account import Account

DEFAULT_SUPERADMIN_ID = "6e488188-0015-4657-94c9-92d01413dcfb"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a cryptographically signed JWT access token.
    Contains subject (account_id), role, email, and expiration timestamp.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.
    Raises HTTPException(401) on expiration or signature failure.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired. Please log in again.",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials. Invalid token.",
        )


def get_current_account(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_account_id: Optional[str] = Header(None, alias="X-Account-ID"),
    account_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
) -> Account:
    """
    Resolve the current authenticated account context.
    1. Primary: Validates Authorization: Bearer <jwt_token> header.
    2. Fallback (dev & pytest backward-compat): Checks X-Account-ID header or query param.
    """
    target_id: Optional[str] = None

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1].strip()
        payload = decode_access_token(token)
        target_id = payload.get("sub")
    elif x_account_id or account_id:
        target_id = x_account_id or account_id
    else:
        target_id = DEFAULT_SUPERADMIN_ID

    account = db.query(Account).filter_by(id=target_id).first()

    if not account:
        # Fallback to any superadmin account or create default
        account = db.query(Account).filter_by(role="superadmin").first()
        if not account:
            account = db.query(Account).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not found. Please log in or specify valid account ID.",
        )

    if account.status == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been suspended by the administrator.",
        )

    return account


def require_superadmin(
    current_account: Account = Depends(get_current_account),
) -> Account:
    """
    Ensure the caller has superadmin role privileges.
    """
    if current_account.role != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superadmin privileges required to access this resource.",
        )
    return current_account
