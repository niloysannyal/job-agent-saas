---
name: job-source-integrator
description: >-
  Standardized procedure for implementing, testing, and wiring new JobSource
  fetch integrations (Adzuna, Remotive, RemoteOK, Greenhouse, Lever, Freehire, Ashby).
---

# Job Source Integrator

Use this skill when implementing a new job board or ATS source under `backend/app/services/job_sources/`.

## Integration Checklist

1. **Implement `JobSource` Interface**:
   ```python
   from app.services.job_sources.base import JobSource
   from app.models.job import JobPosting, JobSearchQuery

   class NewJobSource(JobSource):
       is_per_company: bool = False  # True for ATS sources like Greenhouse/Lever/Ashby

       async def fetch(self, query: Union[JobSearchQuery, str, Dict[str, Any]]) -> List[JobPosting]:
           ...
   ```
2. **DTO Normalization**:
   - Return clean `JobPosting` objects matching the standard schema (`company`, `role`, `description`, `apply_link`, `location`, `salary_min`, `salary_max`, `currency`).
   - Clean up HTML/Markdown formatting in descriptions.

3. **Check ToS & Display Obligations**:
   - Check if the source imposes display constraints (e.g., RemoteOK requires a dofollow link and "Remote OK" credit; Freehire.me keyless API requires "via freehire.me" credit and is restricted to Niloy's account).
   - Document any legal limitations in `docs/ARCHITECTURE.md` §4.

4. **Integration with `JobIngestionService`**:
   - `job_ingestion.py` automatically routes general sources (`is_per_company=False`) with search queries and per-company sources (`is_per_company=True`) with company slugs.
   - Deduplication key `(source, source_job_id)` and `apply_link` is automatically handled.
   - Posting integrity check (`run_posting_guard()`) runs before database persistence.

5. **Unit Tests with Mocks**:
   - Add unit tests in `backend/tests/services/job_sources/test_<source_name>.py` mirroring the implementation.
   - Mock all HTTP requests with `httpx` or `respx`; never hit live external APIs in tests.
