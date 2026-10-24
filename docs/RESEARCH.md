# Research — Competitors, APIs, and Legal Notes

Last updated: 2026-09-24. Re-run these searches every few months — this market moves fast.

## Competitor landscape (auto-apply / job-search AI tools)

| Tool | Approach | Auto-apply? | Pricing (as found) | Notes |
|---|---|---|---|---|
| LazyApply | High-volume browser automation across LinkedIn, Indeed, ZipRecruiter, Glassdoor | Yes, up to ~750/day on top tiers | ~$99-149/yr | Cheapest per-application; reviews report a low Trustpilot score and recurring complaints about form-filling errors and generic, poorly targeted applications. Optimizes for volume over quality. |
| JobCopilot | Selective, more curated auto-apply | Yes | ~$24-35/mo | Positioned as more targeted than LazyApply, at a higher price. |
| Sonara AI | Finds jobs, tailors resume, applies automatically based on saved preferences | Yes, continuous | Paid | Runs unattended once preferences are set — no per-job confirmation, which is the opposite of the human-in-the-loop "Send" step in our own design. |
| AIApply | Auto-apply plus an "Interview Buddy" real-time coaching feature and a resume translator (50+ languages) | Yes (credit-based) | ~$29/mo + credits | Interview-prep add-on is a differentiator worth noting. |
| Scoutify | Real-time job alerts plus auto-apply, aimed at being first to apply | Yes | From ~$5/week | Speed-to-apply as the core pitch, similar to our "apply within 24-48h" guidance. |
| Teal | Resume builder + application tracker, no auto-apply | No | Free / ~$29/mo | Quality/organization-focused, not volume. Closest to our Module 3 (Monitor) alone. |
| Jobright | AI copilot for tailoring + autofill (not full auto-submit) + networking features | Autofill only | Free / $29-59/mo | Middle ground between full auto-apply and manual. |
| LoopCV | Automated job search + apply | Yes | Paid | Marketed as "fully automated." |
| Huntr / Simplify Jobs | Application tracking (Kanban-style pipelines) | No | Free / paid tiers | Pure tracking tools — comparable to our Module 3 dashboard concept. |

## What this means for our positioning
- The market splits into two camps: **volume auto-apply** (LazyApply, Sonara, LoopCV —
  optimize for quantity, criticized for generic/low-quality applications) and **quality
  tracking/tailoring tools** (Teal, Huntr, Simplify — no auto-apply, safer but more manual).
- Very few tools combine **real per-job CV tailoring** (not just keyword-stuffing) **with**
  a **mandatory human-review step before sending** — most either fully automate sending
  (Sonara) or don't automate at all (Teal). Our design's "Draft → User reviews → Send" gate
  plus the tagged master-CV tailoring system is a plausible gap to target: quality-focused
  semi-automation, not blind volume.
- Interview prep (AIApply) and networking (Jobright) are adjacent features worth watching,
  not core to our MVP.

## Legal / ToS notes (OPEN — verify current terms before building)
- LinkedIn's and Facebook's terms have historically prohibited automated scraping and
  bot-driven actions on their platforms; several of the tools above (LazyApply in
  particular) operate in this gray area via browser automation rather than official APIs,
  and user reviews suggest this correlates with reliability problems (forms filled wrong,
  accounts flagged). This is a real business risk these competitors are already absorbing —
  worth deciding deliberately rather than copying by default.
- Recommended research task: check LinkedIn's and Facebook's current developer/ToS pages
  directly, and look at whether any of the above competitors have had public account-ban
  complaints, before deciding how far to push browser automation on those specific sites.

## Legal job-data API options to evaluate
- Indeed Publisher Program
- Adzuna API
- USAJobs API (US government roles)
- RemoteOK API
- Greenhouse and Lever public job-board APIs (many companies expose these per-company)
- Company-specific career-page feeds (often simpler than a general scraper, since each
  target company is known in our "Target Company" list)

## Open research tasks
- [ ] Read LinkedIn's and Facebook's current automation/ToS terms directly
- [ ] Test whether Claude in Chrome (or similar) can extract/apply within ToS bounds for a
      single user's own session
- [ ] Estimate LLM cost per application (CV tailoring + email/DM + form answers) to model
      SaaS unit economics
- [ ] Talk to 3-5 people actively job hunting about what LazyApply/Teal/Simplify get wrong
      for them — direct signal beats reading reviews

---

## Addendum (2026-10-04): Job sourcing & payments research

### Job data sourcing — legal layering (feeds ARCHITECTURE.md §4)
- **Adzuna, Remotive, RemoteOK**: official, direct APIs — no ToS risk, no
  scraping. Adzuna covers 19 countries including on-site roles; Remotive/RemoteOK
  are remote-specific. These are the MVP's only sources.
- **Greenhouse / Lever / Ashby**: most companies using these ATS platforms expose
  a public job-listing API per company — ideal for the user's "Target Company"
  list specifically, and fully legal since it's the company's own published feed.
- **JSearch (via RapidAPI, built by OpenWeb Ninja)**: a third-party aggregator
  that pulls from Google for Jobs and re-publishes LinkedIn/Indeed/Glassdoor/
  ZipRecruiter/Dice listings in one normalized API. Using it makes *us* a paying
  API customer of a vendor's product, not a direct scraper of LinkedIn — the
  scraping-ToS exposure sits with the vendor's business model, not ours directly.
  This is the realistic way most "AI job search" competitors get LinkedIn/Indeed
  coverage without running their own scrapers. Known downside: duplicate listings
  across boards, and a RapidAPI markup on top of the base price. Recommended as a
  Phase 2 addition once the product needs broader coverage than the official APIs
  provide — not a Phase 0 default.
- **Direct LinkedIn/Facebook scraping with stored credentials**: ruled out
  entirely for the SaaS (see ARCHITECTURE.md §4). Still only viable, if at all,
  for Niloy's own personal use via his own authenticated browser session — never
  as a product feature for other users' accounts.

### Payments — why Stripe is off the table (feeds ARCHITECTURE.md §12)
- Stripe does not accept businesses registered in Bangladesh (nor Pakistan, Nepal,
  or Sri Lanka) as of 2026. This isn't a settings issue — it's a hard geographic
  restriction on Stripe's side.
- **Paddle** and **Dodo Payments** both operate as Merchant of Record and
  explicitly list Bangladesh as a supported seller country — they become your
  legal seller of record, collecting and remitting VAT/GST/sales tax across every
  country a subscriber lives in. This matters immediately once an EU user
  subscribes, since EU VAT obligations apply regardless of where the company is
  based.
- **Lemon Squeezy** also works today, but Stripe acquired it in 2024 and is
  actively migrating it toward "Stripe Managed Payments" — building fresh on it
  in 2026 means building on a product mid-transition, with the original team on
  record saying the MoR product is the future and Lemon Squeezy itself less so.
- Both Paddle and Dodo charge roughly the same MoR fee (~5% + $0.50/transaction).
  Worth a direct side-by-side on fee structure and payout speed to Bangladesh
  bank accounts specifically before committing, since that detail wasn't
  confirmed in this research pass.
