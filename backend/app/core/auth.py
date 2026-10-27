from typing import Optional
from fastapi import Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.account import Account

DEFAULT_SUPERADMIN_ID = "6e488188-0015-4657-94c9-92d01413dcfb"


def get_current_account(
    x_account_id: Optional[str] = Header(None, alias="X-Account-ID"),
    account_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
) -> Account:
    """
    Resolve the current authenticated account context.
    Checks X-Account-ID header first, then account_id query param,
    and falls back to Niloy's default account for single-user dev testing.
    """
    target_id = x_account_id or account_id or DEFAULT_SUPERADMIN_ID
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
