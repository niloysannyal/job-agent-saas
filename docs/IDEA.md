# Job Application Agent — Original Idea (transcribed from notebook)

## General flow (manual, today)
1. Browse websites, newsfeeds, LinkedIn, etc. and select job posts.
2. Copy the job post and send it to ChatGPT/Claude.
3. Give it the current CV (LaTeX/Overleaf).
4. Ask it to make a personalized CV tailored to the job description.
5. Ask it to generate a professional email to apply, or answer application-form questions.
6. Fill forms, send emails/DMs, and apply.

## The solution: 3 major tasks
1. **Find Job Opportunity**
2. **Apply for the Job**
3. **Monitor Job Applications**

---

## Step 1 — Find Job Opportunity

**Sources:** LinkedIn, Facebook, company websites, other job-search websites.

**Note (original plan):** store IDs/passwords for these sites so the agent can search automatically. *(Flagged in ARCHITECTURE.md as a legal/security risk to redesign — see "Open risks.")*

**Behavior:**
- Fetch all matching job opportunities, save them, and show them in a dashboard.
- Categorize fetched jobs by:
  - **On-site** → Own country / Other country → (if other country) Visa opportunity / No visa
  - **Remote** → Own country / Other country
  - **Target company** — user selects/adds companies of interest (with their website, LinkedIn profile, etc.)
  - **General scraping** — broader, non-targeted matches

**Dashboard mock (jobs list view):**
- Summary tiles: On-site (12), Remote (8), Target Company (5), Well Aligned (7)
- Table columns: Company | Role | Salary | Deadline | Apply
  - Example rows: Optimizely / AI-ML / 55000 / 2 Oct 26 / Apply; Pathao / SWE / negotiable / 8 Oct 26 / Apply; Inverse AI / Robotics / 65000 / 7 Oct 26 / Apply; Raco IT / GenAI / 50000 / 10 Oct 26 / Apply
- "Add Sources and Credentials" section: Sources (links), Credentials (username, password)
- "Applied Jobs" list below

**Target companies (example from notebook):** Optimizely (2 openings tracked), Therap (1), Pathao (2).

**"Well Aligned" example:** AI/ML Engineer — 92% match.

---

## Step 2 — Apply for the Job

**Flow:**
```
Job Opportunity (extracted)
   ↓
Get User Context (User.md + MasterCV.tex)
   ↓
Tailor CV → Export as PDF
   ↓
Application Method?
 ├─ Is Mail?  → yes → Generate Professional Mail (attach CV) ─┐
 ├─ Is Form?  → yes → Generate Form Answers (attach CV) ──────┤→ Draft
 └─ Is DM?    → yes → Generate Professional Message (attach CV)┘
   ↓
Get Credentials & OAuth (for sending)
   ↓
Draft  →  User reviews  →  Send
```
Key point from the original sketch: **CV tailoring happens once per job**, then branches into whichever channel (mail / form / DM) the job actually requires, all three reusing the same tailored CV attachment.

**"Get User Contexts" (source files for tailoring):**
- `User.md` — all about the user: basic info, hobbies, soft skills, technical skills, leadership, adaptability, etc.
- `MasterCV.tex` — covers the user's full technical background (this is `01_MASTER_CV.tex`, already built).

---

## Step 3 — Monitor Job Applications

**Status report mock (e.g. a weekly/on-demand summary):**
> "Hi, Niloy Sannyal — here is your Job Application status:
> Total: 35 | Responded: 21 | Interview Call: 8 | Upcoming Interviews: 3"

**Dashboard sections (app-level mock):**
- **About Me** — profile summary
- **Master CV** — PDF / Latex source
- **Custom Instruction** — editable agent instructions
- **Role-wise CV** — separate tailored CVs kept per target, e.g. AI/ML @ Optimizely, GenAI @ Therap, Robotics @ Sellec
- **Drafts**, split by channel:
  - **Mails** — list with View / Send per row
  - **Forms** — list with Form link / Answers per row
  - **DMs** — list with Edit / Send per row

---

## Open questions from the original sketch (carried into ARCHITECTURE.md)
- How are credentials for LinkedIn/Facebook/company sites actually meant to be stored and used? (flagged as a risk — see ARCHITECTURE.md)
- What counts as a "match" for the Well-Aligned % score, and who/what computes it?
- Is "Draft → User Send" always human-in-the-loop, or is auto-send ever intended? (original flow shows "User" explicitly gating "Send," suggesting human-in-the-loop by design — keep this.)
