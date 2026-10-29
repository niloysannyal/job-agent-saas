# One-Click Development Environment Runner — Job Application Agent SaaS
# Adapted from ECC dev orchestration patterns

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  Job Application Agent SaaS — Local Dev Environment" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Run Doctor Check
Write-Host "`n[1/3] Running Environment Diagnostics..." -ForegroundColor Yellow
python scripts/doctor.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[ERROR] Environment doctor failed. Resolve issues before starting servers." -ForegroundColor Red
    exit 1
}

# 2. Check Background Servers
Write-Host "`n[2/3] Verifying Dev Servers..." -ForegroundColor Yellow
Write-Host "  Backend  -> http://127.0.0.1:8000 (FastAPI Docs: /docs)" -ForegroundColor Cyan
Write-Host "  Frontend -> http://127.0.0.1:5173 (React 19 App)" -ForegroundColor Cyan

# 3. Ready
Write-Host "`n[3/3] Development Environment Online!" -ForegroundColor Green
Write-Host "Tip: Run 'python scripts/verify.py' before committing changes." -ForegroundColor Gray
Write-Host "=================================================================" -ForegroundColor Cyan

