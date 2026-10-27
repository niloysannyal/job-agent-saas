# Application

> God node · 28 connections · `backend/app/models/application.py`

**Community:** [applications.py](applications.py.md)

## Connections by Relation

### calls
- .tailor_for_job() `EXTRACTED`
- test_multi_tenant_cascade_deletes() `EXTRACTED`
- test_application_status_update() `EXTRACTED`
- test_follow_up_draft_and_cap_enforcement() `EXTRACTED`
- test_monitor_summary_view() `EXTRACTED`
- test_application_model_and_human_in_the_loop_gate() `EXTRACTED`

### contains
- application.py `EXTRACTED`

### imports
- [models/__init__.py](models-__init__.py.md) `EXTRACTED`
- [test_models.py](test_models.py.md) `EXTRACTED`
- [job.py](job.py.md) `EXTRACTED`
- [applications.py](applications.py.md) `EXTRACTED`
- account.py `EXTRACTED`
- tailor_service.py `EXTRACTED`
- [test_applications.py](test_applications.py.md) `EXTRACTED`
- cv_template.py `EXTRACTED`

### inherits
- [Base](Base.md) `EXTRACTED`

### method
- .job_company() `EXTRACTED`
- .job_role() `EXTRACTED`

### rationale_for
- Multi-tenant Application model matching ARCHITECTURE.md §6 & §7: (job_id,… `EXTRACTED`

### references
- .__init__() `EXTRACTED`

### uses
- CVTailorService `INFERRED`
- draft_follow_up() `INFERRED`
- update_application_status() `INFERRED`
- get_monitor_summary() `INFERRED`
- mark_application_sent() `INFERRED`
- CVTailorResult `INFERRED`
- list_applications() `INFERRED`
- mark_follow_up_sent() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*