import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.auth import get_current_account, require_superadmin
from app.db.session import get_db
from app.models.account import Account, AccountRead
from app.models.application import Application
from app.models.cv_template import AccountCvVersion, CvTemplate, CvTemplateRead
from app.models.job import Job, JobRead
from app.models.llm_provider import LLMProviderConfig, LLMProviderRead
from app.services.job_ingestion import JobIngestionService
from app.services.job_sources import get_available_sources
from app.services.llm.service import LLMService



logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])


# --- Schemas ---

class TenantSummary(BaseModel):
    id: str
    email: str
    plan_tier: str
    role: str
    status: str
    account_template_limit: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    jobs_count: int = 0
    applications_count: int = 0
    cv_versions_count: int = 0


class TenantCreateRequest(BaseModel):
    email: str
    plan_tier: str = "free"
    role: str = "tenant"
    status: str = "active"
    account_template_limit: Optional[int] = None


class TenantUpdateRequest(BaseModel):
    email: Optional[str] = None
    plan_tier: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    account_template_limit: Optional[int] = None


class LLMProviderInput(BaseModel):
    provider: str
    model_name: str
    api_key: Optional[str] = None
    is_active: bool = True
    priority: int = 1
    account_id: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class LLMProviderUpdateInput(BaseModel):
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None
    config: Optional[Dict[str, Any]] = None


class JobSourceInfo(BaseModel):
    name: str
    display_name: str
    legal_layer: str
    is_active: bool
    is_restricted: bool
    description: str
    jobs_count: int = 0


class TriggerIngestionRequest(BaseModel):
    account_id: Optional[str] = None
    query: str = "AI Engineer"
    country: str = "gb"


class TriggerIngestionResponse(BaseModel):
    success: bool
    account_id: str
    saved_count: int
    total_fetched: int
    flagged_count: int
    vetoed_count: int
    errors: List[str] = []


class PlatformMetricsResponse(BaseModel):
    total_tenants: int
    active_tenants: int
    total_jobs: int
    clean_jobs: int
    flagged_jobs: int
    vetoed_jobs: int
    total_applications: int
    sent_applications: int
    active_provider: Optional[str] = None
    active_model: Optional[str] = None


class TemplateInput(BaseModel):
    name: str
    description: Optional[str] = None
    latex_source: str
    is_admin_default: bool = True


# --- Endpoints ---

@router.get("/metrics", response_model=PlatformMetricsResponse, summary="Get global SaaS platform metrics")
def get_platform_metrics(
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> PlatformMetricsResponse:
    total_tenants = db.query(Account).count()
    active_tenants = db.query(Account).filter_by(status="active").count()
    total_jobs = db.query(Job).count()
    clean_jobs = db.query(Job).filter(Job.integrity_status == "clean", Job.vetoed == False).count()
    flagged_jobs = db.query(Job).filter(Job.integrity_status == "flagged").count()
    vetoed_jobs = db.query(Job).filter(Job.vetoed == True).count()
    total_apps = db.query(Application).count()
    sent_apps = db.query(Application).filter(Application.sent_at.isnot(None)).count()

    active_provider_cfg = (
        db.query(LLMProviderConfig)
        .filter_by(is_active=True, account_id=None)
        .order_by(LLMProviderConfig.priority.asc())
        .first()
    )

    return PlatformMetricsResponse(
        total_tenants=total_tenants,
        active_tenants=active_tenants,
        total_jobs=total_jobs,
        clean_jobs=clean_jobs,
        flagged_jobs=flagged_jobs,
        vetoed_jobs=vetoed_jobs,
        total_applications=total_apps,
        sent_applications=sent_apps,
        active_provider=active_provider_cfg.provider if active_provider_cfg else "openai",
        active_model=active_provider_cfg.model_name if active_provider_cfg else "gpt-4o-mini",
    )


# --- Tenant Management ---

@router.get("/tenants", response_model=List[TenantSummary], summary="List all tenants and quotas")
def list_tenants(
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> List[TenantSummary]:
    accounts = db.query(Account).order_by(Account.created_at.desc()).all()
    summaries = []
    for acc in accounts:
        jobs_count = db.query(Job).filter_by(account_id=acc.id).count()
        apps_count = (
            db.query(Application)
            .join(Job, Application.job_id == Job.id)
            .filter(Job.account_id == acc.id)
            .count()
        )
        cvs_count = db.query(AccountCvVersion).filter_by(account_id=acc.id).count()

        summaries.append(
            TenantSummary(
                id=acc.id,
                email=acc.email,
                plan_tier=acc.plan_tier,
                role=acc.role,
                status=acc.status,
                account_template_limit=acc.account_template_limit,
                created_at=acc.created_at,
                updated_at=acc.updated_at,
                jobs_count=jobs_count,
                applications_count=apps_count,
                cv_versions_count=cvs_count,
            )
        )
    return summaries


@router.post("/tenants", response_model=TenantSummary, summary="Create or invite a new tenant")
def create_tenant(
    data: TenantCreateRequest,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> TenantSummary:
    existing = db.query(Account).filter_by(email=data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account with this email already exists")

    new_acc = Account(
        email=data.email,
        plan_tier=data.plan_tier,
        role=data.role,
        status=data.status,
        account_template_limit=data.account_template_limit,
    )
    db.add(new_acc)
    db.commit()
    db.refresh(new_acc)

    return TenantSummary(
        id=new_acc.id,
        email=new_acc.email,
        plan_tier=new_acc.plan_tier,
        role=new_acc.role,
        status=new_acc.status,
        account_template_limit=new_acc.account_template_limit,
        created_at=new_acc.created_at,
        updated_at=new_acc.updated_at,
        jobs_count=0,
        applications_count=0,
        cv_versions_count=0,
    )


@router.patch("/tenants/{tenant_id}", response_model=TenantSummary, summary="Update tenant tier, role, or status")
def update_tenant(
    tenant_id: str,
    data: TenantUpdateRequest,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> TenantSummary:
    acc = db.query(Account).filter_by(id=tenant_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Tenant not found")

    if data.email is not None:
        acc.email = data.email
    if data.plan_tier is not None:
        acc.plan_tier = data.plan_tier
    if data.role is not None:
        acc.role = data.role
    if data.status is not None:
        acc.status = data.status
    if data.account_template_limit is not None:
        acc.account_template_limit = data.account_template_limit

    acc.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(acc)

    jobs_count = db.query(Job).filter_by(account_id=acc.id).count()
    apps_count = (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .filter(Job.account_id == acc.id)
        .count()
    )
    cvs_count = db.query(AccountCvVersion).filter_by(account_id=acc.id).count()

    return TenantSummary(
        id=acc.id,
        email=acc.email,
        plan_tier=acc.plan_tier,
        role=acc.role,
        status=acc.status,
        account_template_limit=acc.account_template_limit,
        created_at=acc.created_at,
        updated_at=acc.updated_at,
        jobs_count=jobs_count,
        applications_count=apps_count,
        cv_versions_count=cvs_count,
    )


@router.delete("/tenants/{tenant_id}", summary="Delete tenant and all associated data")
def delete_tenant(
    tenant_id: str,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
):
    acc = db.query(Account).filter_by(id=tenant_id).first()
    if not acc:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if acc.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own superadmin account")

    db.delete(acc)
    db.commit()
    return {"status": "deleted", "tenant_id": tenant_id}


@router.post("/tenants/{tenant_id}/impersonate", summary="Generate impersonation context for QA and testing")
def impersonate_tenant(
    tenant_id: str,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
):
    target = db.query(Account).filter_by(id=tenant_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return {
        "impersonating": True,
        "superadmin_id": admin.id,
        "tenant_id": target.id,
        "email": target.email,
        "plan_tier": target.plan_tier,
        "role": target.role,
    }


# --- LLM Providers Management ---

@router.get("/llm-providers", response_model=List[LLMProviderRead], summary="List all configured LLM providers")
def list_llm_providers(
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> List[LLMProviderRead]:
    providers = db.query(LLMProviderConfig).order_by(LLMProviderConfig.priority.asc()).all()
    results = []
    for p in providers:
        results.append(
            LLMProviderRead(
                id=p.id,
                provider=p.provider,
                model_name=p.model_name,
                account_id=p.account_id,
                is_active=p.is_active,
                priority=p.priority,
                config=p.config or {},
                has_api_key=bool(p.encrypted_api_key),
                created_at=p.created_at,
                updated_at=p.updated_at,
            )
        )
    return results


@router.post("/llm-providers", response_model=LLMProviderRead, summary="Register a new LLM provider")
def create_llm_provider(
    data: LLMProviderInput,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> LLMProviderRead:
    new_provider = LLMProviderConfig(
        provider=data.provider,
        model_name=data.model_name,
        account_id=data.account_id,
        is_active=data.is_active,
        priority=data.priority,
        config=data.config or {},
        encrypted_api_key=data.api_key,  # In production, encrypt with secret key
    )
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)

    return LLMProviderRead(
        id=new_provider.id,
        provider=new_provider.provider,
        model_name=new_provider.model_name,
        account_id=new_provider.account_id,
        is_active=new_provider.is_active,
        priority=new_provider.priority,
        config=new_provider.config or {},
        has_api_key=bool(new_provider.encrypted_api_key),
        created_at=new_provider.created_at,
        updated_at=new_provider.updated_at,
    )


@router.patch("/llm-providers/{provider_id}", response_model=LLMProviderRead, summary="Update provider priority or active status")
def update_llm_provider(
    provider_id: str,
    data: LLMProviderUpdateInput,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> LLMProviderRead:
    p = db.query(LLMProviderConfig).filter_by(id=provider_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Provider config not found")

    if data.model_name is not None:
        p.model_name = data.model_name
    if data.is_active is not None:
        p.is_active = data.is_active
    if data.priority is not None:
        p.priority = data.priority
    if data.api_key is not None:
        p.encrypted_api_key = data.api_key
    if data.config is not None:
        p.config = data.config

    p.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(p)

    return LLMProviderRead(
        id=p.id,
        provider=p.provider,
        model_name=p.model_name,
        account_id=p.account_id,
        is_active=p.is_active,
        priority=p.priority,
        config=p.config or {},
        has_api_key=bool(p.encrypted_api_key),
        created_at=p.created_at,
        updated_at=p.updated_at,
    )


@router.delete("/llm-providers/{provider_id}", summary="Delete an LLM provider configuration")
def delete_llm_provider(
    provider_id: str,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
):
    p = db.query(LLMProviderConfig).filter_by(id=provider_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Provider config not found")

    db.delete(p)
    db.commit()
    return {"status": "deleted", "provider_id": provider_id}


@router.post("/llm-providers/{provider_id}/test", summary="Test live connectivity of an LLM provider")
def test_llm_provider(
    provider_id: str,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
):
    p = db.query(LLMProviderConfig).filter_by(id=provider_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Provider config not found")

    try:
        service = LLMService(db_session=db)
        test_reply = service.generate(
            prompt="Respond with 'OK' if you can read this.",
            context="System health check",
        )
        return {
            "status": "connected",
            "provider": p.provider,
            "model": p.model_name,
            "response": test_reply.strip(),
        }

    except Exception as e:
        return {
            "status": "error",
            "provider": p.provider,
            "model": p.model_name,
            "error": str(e),
        }


# --- Job Sourcing & Ingestion Controls ---

@router.get("/jobs/sources", response_model=List[JobSourceInfo], summary="List all integrated job sources and status")
def get_job_sources(
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> List[JobSourceInfo]:
    sources_catalog = [
        {
            "name": "adzuna",
            "display_name": "Adzuna API",
            "legal_layer": "Layer 1 (Official / Legal)",
            "is_active": True,
            "is_restricted": False,
            "description": "Broad international coverage across 19 countries.",
        },
        {
            "name": "remotive",
            "display_name": "Remotive API",
            "legal_layer": "Layer 1 (Official / Legal)",
            "is_active": True,
            "is_restricted": False,
            "description": "Curated remote tech & software engineering jobs.",
        },
        {
            "name": "remoteok",
            "display_name": "RemoteOK API",
            "legal_layer": "Layer 1 (Attribution Required)",
            "is_active": True,
            "is_restricted": False,
            "description": "Remote tech positions with mandatory source attribution.",
        },
        {
            "name": "greenhouse",
            "display_name": "Greenhouse Board API",
            "legal_layer": "Layer 1 (Official / Legal)",
            "is_active": True,
            "is_restricted": False,
            "description": "Target company board feeder via public Greenhouse API.",
        },
        {
            "name": "lever",
            "display_name": "Lever Postings API",
            "legal_layer": "Layer 1 (Official / Legal)",
            "is_active": True,
            "is_restricted": False,
            "description": "Target company board feeder via public Lever API.",
        },
        {
            "name": "freehire",
            "display_name": "Freehire Aggregator",
            "legal_layer": "Layer 1b (Restricted / QA Only)",
            "is_active": True,
            "is_restricted": True,
            "description": "Tech aggregator for Niloy personal validation.",
        },
    ]

    results = []
    for src in sources_catalog:
        count = db.query(Job).filter(Job.source.ilike(f"%{src['name']}%")).count()
        results.append(
            JobSourceInfo(
                name=src["name"],
                display_name=src["display_name"],
                legal_layer=src["legal_layer"],
                is_active=src["is_active"],
                is_restricted=src["is_restricted"],
                description=src["description"],
                jobs_count=count,
            )
        )
    return results


@router.post("/jobs/trigger", response_model=TriggerIngestionResponse, summary="Trigger manual job ingestion")
async def trigger_ingestion(
    req: TriggerIngestionRequest,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> TriggerIngestionResponse:
    target_account_id = req.account_id or admin.id
    target_acc = db.query(Account).filter_by(id=target_account_id).first()
    if not target_acc:
        raise HTTPException(status_code=404, detail="Target account for ingestion not found")

    job_sources = get_available_sources()
    service = JobIngestionService(db=db)
    result = await service.ingest(
        account_id=target_acc.id,
        sources=job_sources,
        search_queries=[req.query or "AI Engineer"],
    )

    scored = result.matching_result.scored_count if result.matching_result else 0
    vetoed = result.matching_result.vetoed_count if result.matching_result else 0


    return TriggerIngestionResponse(
        success=True,
        account_id=target_acc.id,
        saved_count=len(result.saved_jobs),
        total_fetched=result.total_fetched,
        flagged_count=result.flagged_count,
        vetoed_count=vetoed,
        errors=result.errors,
    )


@router.get("/jobs/flagged", response_model=List[JobRead], summary="Inspect flagged postings caught by integrity guard")
def list_flagged_jobs(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> List[JobRead]:
    flagged = (
        db.query(Job)
        .filter(Job.integrity_status == "flagged")
        .order_by(Job.created_at.desc())
        .limit(limit)
        .all()
    )
    return list(flagged)


# --- Global CV Template Management ---

@router.get("/templates", response_model=List[CvTemplateRead], summary="List admin-curated LaTeX templates")
def list_admin_templates(
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> List[CvTemplateRead]:
    templates = (
        db.query(CvTemplate)
        .filter(CvTemplate.account_id.is_(None))
        .order_by(CvTemplate.created_at.desc())
        .all()
    )
    return list(templates)


@router.post("/templates", response_model=CvTemplateRead, summary="Create a new global LaTeX template")
def create_admin_template(
    data: TemplateInput,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> CvTemplateRead:
    tmpl = CvTemplate(
        account_id=None,
        name=data.name,
        description=data.description,
        latex_source=data.latex_source,
        is_admin_default=data.is_admin_default,
    )
    db.add(tmpl)
    db.commit()
    db.refresh(tmpl)
    return tmpl


@router.patch("/templates/{template_id}", response_model=CvTemplateRead, summary="Update global LaTeX template")
def update_admin_template(
    template_id: str,
    data: TemplateInput,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
) -> CvTemplateRead:
    tmpl = db.query(CvTemplate).filter(CvTemplate.id == template_id, CvTemplate.account_id.is_(None)).first()
    if not tmpl:
        raise HTTPException(status_code=404, detail="Template not found")

    tmpl.name = data.name
    tmpl.description = data.description
    tmpl.latex_source = data.latex_source
    tmpl.is_admin_default = data.is_admin_default
    tmpl.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(tmpl)
    return tmpl


@router.delete("/templates/{template_id}", summary="Delete a global LaTeX template")
def delete_admin_template(
    template_id: str,
    db: Session = Depends(get_db),
    admin: Account = Depends(require_superadmin),
):
    tmpl = db.query(CvTemplate).filter(CvTemplate.id == template_id, CvTemplate.account_id.is_(None)).first()
    if not tmpl:
        raise HTTPException(status_code=404, detail="Template not found")

    db.delete(tmpl)
    db.commit()
    return {"status": "deleted", "template_id": template_id}
