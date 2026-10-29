---
paths:
  - "backend/app/**/*.py"
  - "backend/alembic/**/*.py"
---
# Security & Tenancy Policy (adapted from ECC AgentShield)

## 1. Multi-Tenant Partitioning
- **`account_id` Mandate**: Every table (except global master templates where `account_id = None`) must carry an `account_id` column referencing `accounts.id`.
- **Query Scoping**: All database reads, updates, and deletes must scope to the authenticated `account_id`.
- **Cascade Deletion**: All tenant-owned records configure `ondelete="CASCADE"` to prevent orphaned data.

## 2. Secrets & Encryption
- Never store raw API keys or OAuth tokens in plaintext.
- Encrypt sensitive provider keys using `encrypt_secret()` from `app.core.security` (AES-256).
- Never log full API keys, tokens, or authorization headers in stdout or application logs. Mask as `sk-...abcd`.

## 3. Ingestion & Prompt Injection Defense
- Untrusted external job postings must pass through `PostingIntegrityGate`.
- Invisible unicode text, prompt injection patterns (e.g. `Ignore previous instructions and output...`), and canary traps must trigger flag status and routing to the Incident Room.

## 4. Human-in-the-Loop on Send
- Permanent non-negotiable rule: **The user reviews and approves every outgoing communication before it is sent.**
- Any PR or change that creates an automated, unapproved send path is strictly rejected.

