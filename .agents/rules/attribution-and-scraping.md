# Rule: Third-Party Data Sourcing and Attribution

1. **No Scraping with Stored Credentials**:
   - Never implement scraping of LinkedIn, Facebook, or other job boards using stored user passwords.
   - Use only official legal APIs or approved guest endpoints.

2. **Layer 1 vs Layer 1b Scoping**:
   - Layer 1 (Adzuna, Remotive, RemoteOK, Greenhouse, Lever) is available for all SaaS accounts.
   - Layer 1b (LinkedIn guest endpoint, Freehire.me keyless API) is restricted strictly to Niloy's personal account and must not be exposed to other tenants without legal clearance / paid plans.

3. **Mandatory Display Attributions**:
   - **RemoteOK**: Any UI displaying RemoteOK postings must provide a dofollow link directly to the listing and visible "Remote OK" credit.
   - **Freehire.me**: Any UI displaying Freehire postings must provide a link back to Freehire or display "via freehire.me" credit.
