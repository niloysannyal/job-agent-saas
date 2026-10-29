# QA & Validation Context — Job Application Agent SaaS

Mode: QA Dogfooding & Integration Validation
Focus: Personal validation (Niloy's real job search) and multi-tenant QA simulation.

## Validation Scenarios

### 1. SuperAdmin Ops Center & Tenant Management
- **Dashboard Telemetry**: Bento metric cards reflect live counts (tenants, clean jobs, incidents, LLM provider).
- **Tenant Provisioning**: Add Tenant modal creates isolated partition with proper tier and quota.
- **QA Impersonation ("Test As Tenant")**: One-click impersonation switches workspace context without logging out.

### 2. Job Radar Ingestion & Integrity Shield
- **Multi-Source Fetching**: Fetch jobs via official adapters (Adzuna, Remotive, RemoteOK, Freehire, Greenhouse, Lever).
- **Prompt Injection Defense**: Ingested descriptions pass through `PostingIntegrityGate`. Flagged postings show in Incident Room.

### 3. Dynamic LLM Failover Engine
- **Priority Cascade**: Active models route requests according to priority rank.
- **Bedrock Backup**: If database models rate-limit or fail, the system automatically falls back to `.env` fallback key (`gpt-4o-mini`).
- **Ping Testing**: Live "Test Ping" button pings providers and reports live model latency.

### 4. CV Tailoring & Application Studio
- **Master CV Fact Consistency**: Tailored LaTeX CV output matches source truth.
- **Overleaf Editor & PDF Preview**: In-browser compiler generates valid PDF download.
- **Human-in-the-Loop Send Gate**: Final outreach email/DM draft requires explicit human review and click to Send.

