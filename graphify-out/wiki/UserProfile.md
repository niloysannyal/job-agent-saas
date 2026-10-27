# UserProfile

> God node · 28 connections · `backend/app/models/profile.py`

**Community:** [models/__init__.py](models-__init__.py.md)

## Connections by Relation

### calls
- seed_initial_data() `EXTRACTED`
- test_user_profile_and_relations() `EXTRACTED`

### contains
- models/profile.py `EXTRACTED`

### imports
- [models/__init__.py](models-__init__.py.md) `EXTRACTED`
- [test_models.py](test_models.py.md) `EXTRACTED`
- [applications.py](applications.py.md) `EXTRACTED`
- api/profile.py `EXTRACTED`
- account.py `EXTRACTED`
- tailor_service.py `EXTRACTED`
- [test_profile.py](test_profile.py.md) `EXTRACTED`
- [api/interview.py](api-interview.py.md) `EXTRACTED`
- seed.py `EXTRACTED`

### inherits
- [Base](Base.md) `EXTRACTED`

### rationale_for
- Core profile for a user (one-to-one with Account). Stores identity, narrative,… `EXTRACTED`

### uses
- CVTailorService `INFERRED`
- generate_interview_prep() `INFERRED`
- test_seed_initial_data() `INFERRED`
- evaluate_job_fit() `INFERRED`
- add_designation() `INFERRED`
- add_language() `INFERRED`
- add_location() `INFERRED`
- create_profile() `INFERRED`
- update_profile() `INFERRED`
- upsert_compensation() `INFERRED`
- get_profile() `INFERRED`
- list_designations() `INFERRED`
- list_languages() `INFERRED`
- list_locations() `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*