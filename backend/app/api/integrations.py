from datetime import datetime, timezone, timedelta
from typing import Optional, List
import json
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.auth import get_current_account
from app.core.crypto import encrypt_secret, decrypt_secret
from app.db.session import get_db
from app.models.account import Account
from app.models.oauth import OAuthConnection
from app.models.application import Application
from app.models.profile import UserProfile
from app.services.integrations.google_service import GoogleIntegrationService

router = APIRouter(prefix="/integrations", tags=["Integrations"])


# --- Pydantic Schemas ---

class GoogleAuthUrlResponse(BaseModel):
    auth_url: str


class GoogleCallbackRequest(BaseModel):
    code: str
    state: Optional[str] = None


class IntegrationStatusResponse(BaseModel):
    connected: bool
    provider: str = "google"
    email: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class CreateGmailDraftRequest(BaseModel):
    application_id: Optional[str] = None
    recipient_email: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject line")
    body_text: str = Field(..., description="Plaintext outreach email body")
    attach_cv: bool = Field(True, description="Whether to attach the tailored PDF CV")


class CreateGmailDraftResponse(BaseModel):
    success: bool
    draft_id: str
    message_id: Optional[str] = None
    web_link: str
    recipient_email: str
    subject: str


class BookmarkletResponse(BaseModel):
    bookmarklet_js: str
    description: str


# --- Endpoints ---

@router.get("/google/auth-url", response_model=GoogleAuthUrlResponse)
def get_google_auth_url(
    state: Optional[str] = "state_oauth_google",
    current_account: Account = Depends(get_current_account),
):
    """
    Generate Google OAuth 2.0 consent URL for Gmail Draft composition.
    Scope is strictly restricted to gmail.compose (no send authority).
    """
    url = GoogleIntegrationService.get_authorization_url(state=f"{current_account.id}:{state}")
    return GoogleAuthUrlResponse(auth_url=url)


@router.post("/google/callback", response_model=IntegrationStatusResponse)
async def google_oauth_callback(
    data: GoogleCallbackRequest,
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Exchange authorization code for tokens, encrypt at rest, and upsert OAuthConnection.
    """
    token_info = await GoogleIntegrationService.exchange_code_for_tokens(data.code)

    expires_in = token_info.get("expires_in", 3600)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    conn = (
        db.query(OAuthConnection)
        .filter_by(account_id=current_account.id, provider="google")
        .first()
    )

    if not conn:
        conn = OAuthConnection(
            account_id=current_account.id,
            provider="google",
            email=token_info.get("email"),
            encrypted_access_token=encrypt_secret(token_info.get("access_token")),
            encrypted_refresh_token=encrypt_secret(token_info.get("refresh_token")),
            token_expires_at=expires_at,
            scope=token_info.get("scope"),
        )
        db.add(conn)
    else:
        conn.email = token_info.get("email") or conn.email
        conn.encrypted_access_token = encrypt_secret(token_info.get("access_token"))
        if token_info.get("refresh_token"):
            conn.encrypted_refresh_token = encrypt_secret(token_info.get("refresh_token"))
        conn.token_expires_at = expires_at
        conn.scope = token_info.get("scope") or conn.scope

    db.commit()
    db.refresh(conn)

    return IntegrationStatusResponse(
        connected=True,
        provider="google",
        email=conn.email,
        token_expires_at=conn.token_expires_at,
    )


@router.get("/google/status", response_model=IntegrationStatusResponse)
def get_google_status(
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Check if the current account has an active Google OAuth integration.
    """
    conn = (
        db.query(OAuthConnection)
        .filter_by(account_id=current_account.id, provider="google")
        .first()
    )

    if not conn or not conn.encrypted_access_token:
        return IntegrationStatusResponse(connected=False, provider="google")

    return IntegrationStatusResponse(
        connected=True,
        provider="google",
        email=conn.email,
        token_expires_at=conn.token_expires_at,
    )


@router.post("/google/disconnect")
def disconnect_google(
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Disconnect and remove Google OAuth credentials for the current account.
    """
    conn = (
        db.query(OAuthConnection)
        .filter_by(account_id=current_account.id, provider="google")
        .first()
    )
    if conn:
        db.delete(conn)
        db.commit()

    return {"success": True, "message": "Google integration successfully disconnected."}


@router.post("/google/create-draft", response_model=CreateGmailDraftResponse)
async def create_gmail_draft(
    data: CreateGmailDraftRequest,
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Create a Draft in the user's Gmail box.
    Non-negotiable: Human-in-the-loop on Send. Never auto-sends.
    """
    conn = (
        db.query(OAuthConnection)
        .filter_by(account_id=current_account.id, provider="google")
        .first()
    )
    if not conn or not conn.encrypted_access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account not connected. Please connect Google in Settings or Application Studio first.",
        )

    # Check token expiry and refresh if needed
    access_token = decrypt_secret(conn.encrypted_access_token)
    now = datetime.now(timezone.utc)
    expires_at = conn.token_expires_at
    if expires_at and expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at and expires_at <= now:
        if conn.encrypted_refresh_token:
            new_token = await GoogleIntegrationService.refresh_access_token(conn.encrypted_refresh_token)
            conn.encrypted_access_token = encrypt_secret(new_token)
            conn.token_expires_at = now + timedelta(seconds=3600)
            db.commit()
            access_token = new_token

    pdf_bytes = None
    pdf_filename = "Tailored_CV.pdf"

    if data.attach_cv and data.application_id:
        app_obj = (
            db.query(Application)
            .filter_by(id=data.application_id, account_id=current_account.id)
            .first()
        )
        if app_obj and app_obj.tailored_cv_pdf_path:
            import os
            if os.path.exists(app_obj.tailored_cv_pdf_path):
                with open(app_obj.tailored_cv_pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                pdf_filename = os.path.basename(app_obj.tailored_cv_pdf_path)

    draft_res = await GoogleIntegrationService.create_gmail_draft(
        access_token=access_token,
        to=data.recipient_email,
        subject=data.subject,
        body_text=data.body_text,
        pdf_bytes=pdf_bytes,
        pdf_filename=pdf_filename,
    )

    return CreateGmailDraftResponse(
        success=True,
        draft_id=draft_res["id"],
        message_id=draft_res.get("message_id"),
        web_link=draft_res.get("web_link", "https://mail.google.com/mail/u/0/#drafts"),
        recipient_email=data.recipient_email,
        subject=data.subject,
    )


@router.get("/autofill/bookmarklet", response_model=BookmarkletResponse)
def get_autofill_bookmarklet(
    job_id: Optional[str] = Query(None, description="Target job UUID to bundle bespoke STAR answers"),
    application_id: Optional[str] = Query(None, description="Target application UUID to bundle bespoke STAR answers"),
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    """
    Generate an intelligent JavaScript bookmarklet code tailored to the current user's profile
    and optionally bundled with tailored STAR answers for a target job application.
    Candidate can drag to browser bookmarks bar or copy.
    Clicking it on any Google Form or ATS portal auto-fills fields matching profile facts and Q&A.
    """
    profile = db.query(UserProfile).filter_by(account_id=current_account.id).first()

    name = profile.full_name if profile else "Candidate"
    name_parts = name.strip().split() if name else ["Candidate"]
    first_name = name_parts[0] if name_parts else "Candidate"
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

    email = current_account.email
    phone = getattr(profile, "phone", "") or ""
    city = getattr(profile, "location_city", "") or ""
    country = getattr(profile, "location_country", "") or ""
    current_role = getattr(profile, "current_role", "") or ""
    current_company = getattr(profile, "current_company", "") or ""
    github = (profile.github_url if profile else "") or ""
    linkedin = (profile.linkedin_url if profile else "") or ""
    portfolio = (profile.portfolio_url if profile else "") or ""

    # Optional bespoke answers for target job/application
    app_record = None
    if application_id:
        app_record = db.query(Application).filter_by(id=application_id, account_id=current_account.id).first()
    elif job_id:
        app_record = db.query(Application).filter_by(job_id=job_id, account_id=current_account.id).first()

    custom_answers = []
    cover_note = ""
    if app_record:
        cover_note = app_record.draft_content or ""
        if app_record.form_answers:
            for fa in app_record.form_answers:
                custom_answers.append({
                    "prompt": fa.question_prompt,
                    "answer": fa.tailored_answer,
                })

    custom_answers_json = json.dumps(custom_answers)

    # Minified intelligent JavaScript bookmarklet
    bookmarklet = f"""javascript:(function(){{
        var data = {{
            name: {repr(name)},
            first_name: {repr(first_name)},
            last_name: {repr(last_name)},
            email: {repr(email)},
            phone: {repr(phone)},
            city: {repr(city)},
            country: {repr(country)},
            role: {repr(current_role)},
            company: {repr(current_company)},
            github: {repr(github)},
            linkedin: {repr(linkedin)},
            portfolio: {repr(portfolio)},
            cover_note: {repr(cover_note)},
            custom_answers: {custom_answers_json}
        }};
        var inputs = document.querySelectorAll('input, textarea');
        var filledCount = 0;
        inputs.forEach(function(el) {{
            if (el.type === 'hidden' || el.type === 'submit' || el.type === 'button') return;
            var label = '';
            var id = el.id || '';
            var nameAttr = el.name || '';
            var placeholder = el.placeholder || '';
            var ariaLabel = el.getAttribute('aria-label') || '';
            
            var labelEl = document.querySelector('label[for="' + id + '"]');
            if (labelEl) label += labelEl.innerText + ' ';
            
            var parent = el.closest('div, .freebirdFormviewerViewNumberedItemContainer, .field, .form-group, [role="listitem"]');
            if (parent) label += parent.innerText + ' ';
            
            var probe = (label + ' ' + nameAttr + ' ' + placeholder + ' ' + ariaLabel).toLowerCase();

            function setVal(val) {{
                if (!val || el.value === val) return;
                el.value = val;
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                filledCount++;
            }}

            if (data.email && (probe.includes('email') || el.type === 'email')) {{
                setVal(data.email);
            }} else if (data.first_name && (probe.includes('first name') || probe.includes('given name') || nameAttr === 'first_name' || id === 'first_name')) {{
                setVal(data.first_name);
            }} else if (data.last_name && (probe.includes('last name') || probe.includes('surname') || probe.includes('family name') || nameAttr === 'last_name' || id === 'last_name')) {{
                setVal(data.last_name);
            }} else if (data.name && (probe.includes('full name') || probe.includes('your name') || probe.includes('candidate name') || probe.includes('name'))) {{
                setVal(data.name);
            }} else if (data.phone && (probe.includes('phone') || probe.includes('mobile') || probe.includes('contact number') || el.type === 'tel')) {{
                setVal(data.phone);
            }} else if (data.city && (probe.includes('city') || probe.includes('location') || probe.includes('address'))) {{
                setVal(data.city);
            }} else if (data.role && (probe.includes('current title') || probe.includes('current role') || probe.includes('job title'))) {{
                setVal(data.role);
            }} else if (data.company && (probe.includes('current company') || probe.includes('current employer') || probe.includes('employer'))) {{
                setVal(data.company);
            }} else if (data.github && (probe.includes('github') || probe.includes('git profile') || probe.includes('repository'))) {{
                setVal(data.github);
            }} else if (data.linkedin && (probe.includes('linkedin') || probe.includes('linked-in'))) {{
                setVal(data.linkedin);
            }} else if (data.portfolio && (probe.includes('portfolio') || probe.includes('website') || probe.includes('personal site') || probe.includes('url'))) {{
                setVal(data.portfolio);
            }} else if (el.tagName === 'TEXTAREA' && data.cover_note && (probe.includes('cover letter') || probe.includes('note') || probe.includes('additional information') || probe.includes('comments'))) {{
                setVal(data.cover_note);
            }} else if (el.tagName === 'TEXTAREA' && data.custom_answers && data.custom_answers.length > 0) {{
                for (var i = 0; i < data.custom_answers.length; i++) {{
                    var ca = data.custom_answers[i];
                    var pWords = ca.prompt.toLowerCase().split(/[^a-z0-9]+/).filter(function(w){{ return w.length > 3; }});
                    var matchScore = 0;
                    pWords.forEach(function(w){{ if (probe.includes(w)) matchScore++; }});
                    if (matchScore >= 2 || (pWords.length > 0 && matchScore / pWords.length >= 0.4)) {{
                        setVal(ca.answer);
                        break;
                    }}
                }}
            }}
        }});
        
        var banner = document.createElement('div');
        banner.style = 'position:fixed;top:20px;right:20px;z-index:9999999;background:#064e3b;color:#a7f3d0;padding:14px 22px;border-radius:8px;font-family:system-ui,-apple-system,sans-serif;font-size:14px;font-weight:600;box-shadow:0 12px 30px rgba(0,0,0,0.35);border:1px solid #10b981;display:flex;align-items:center;gap:10px;';
        banner.innerHTML = '⚡ <span>JobEazy Candidate OS: Autofilled ' + filledCount + ' field(s)!</span>';
        document.body.appendChild(banner);
        setTimeout(function(){{ banner.remove(); }}, 4500);
    }})();"""

    clean_js = " ".join(line.strip() for line in bookmarklet.splitlines() if line.strip())

    return BookmarkletResponse(
        bookmarklet_js=clean_js,
        description="Drag this link to your bookmarks bar. On any Google Form or ATS job application, click it to auto-populate your candidate info.",
    )
