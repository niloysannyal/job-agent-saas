---
name: database-migrations
description: Reversible database migration patterns for PostgreSQL and SQLite — forward-only production changes, Alembic linear revisions, foreign key cascade safety, and zero-downtime schema evolution.
---
# Database Migrations Skill — Job Application Agent SaaS

Safe, multi-tenant schema evolution and migration patterns using Alembic and SQLAlchemy 2.0.

## Core Rules
1. **Every Schema Change is a Migration**: Never execute manual `ALTER TABLE` in production. Always generate a tracked Alembic revision.
2. **Multi-Tenant `account_id` Mandate**: Every table (except global master templates) must include:
   ```python
   account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
   ```
3. **Foreign Keys Must Have Indexes & Cascades**: Every foreign key must configure an index and appropriate cascade delete behavior to prevent orphaned data.
4. **Reversible Operations**: Every migration must define both `upgrade()` and `downgrade()`.
5. **No Data Mix**: Schema changes (DDL) and data backfills (DML) must be distinct migrations.

## Verification
Run the database audit script:
```bash
python scripts/check_migrations.py
```

