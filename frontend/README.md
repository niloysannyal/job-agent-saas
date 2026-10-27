# Job Agent SaaS — Frontend

A high-performance React application designed for the Job Application Agent SaaS. Built with an **Obsidian & Cyber Emerald** dark theme, modern typography (Outfit / Inter / JetBrains Mono), radial gauges, glassmorphic surfaces, and responsive controls.

## Features & Views

### 1. Dashboard (`DashboardView.jsx`)
- Executive status metrics (Total Active Postings, Drafts, Sent Applications, Follow-ups Due, Response Rate).
- Match score distribution and pipeline stage breakdowns.
- Quick action jump links to trigger ingestion, tailor applications, or prep for interviews.

### 2. Jobs Queue (`JobsView.jsx`)
- Real-time ranked queue sorted by Qdrant embedding match score.
- Dynamic radial gauges visualizing compatibility percentages.
- Posting guard inspection modal displaying integrity status (`clean`, `flagged`) and raw text preview.
- Mandatory legal attributions for RemoteOK (dofollow link + credit) and Freehire.me.
- Live ingestion modal to trigger crawls across Adzuna, Remotive, RemoteOK, Greenhouse, Lever, and Freehire.

### 3. Application Studio (`ApplicationStudio.jsx`)
- **Quick Fit Evaluator**: Scores profile compatibility against job descriptions before generation, detecting matched skills, missing requirements, and dealbreaker red flags.
- **Two-Pass Drafter + Reviewer Pipeline**: Generates role-tailored LaTeX CV and cover letter adhering to the verified fact ledger.
- **ATS Text-Layer & Budget Audit**: Validates contact info readability, keyword density, and page budgeting.
- **LaTeX Source Editor**: Direct preview and editing of compiled `.tex` source.
- **Multi-Channel Outreach Generator**: Generates customized application emails, form question answers, LinkedIn DMs, or portal submissions.
- **Human Review Gate**: Strictly enforces `Draft -> Human Review -> Send`.

### 4. Pipeline Application Monitor (`PipelineView.jsx`)
- Kanban pipeline tracking application stages: Draft, Sent, Responded, Interview, Offer, Rejected.
- Follow-up tracker identifying applications exceeding the 10-day response threshold.
- AI Follow-Up Drafter with strict human confirmation and max-2-outreach cap enforcement.

### 5. STAR Interview Coach (`InterviewCoachView.jsx`)
- **STAR Story Bank**: CRUD management for Situation-Task-Action-Result stories with tag filtering and truth verification badges.
- **Interview Prep Generator**: Matches relevant STAR stories to specific job posting requirements and generates anticipated technical/behavioral questions.
- **AI Answer Critique**: Evaluates candidate draft answers against the STAR methodology, identifying structure strengths and areas for improvement.

### 6. Profile & Dealbreakers (`ProfileView.jsx`)
- Multi-tenant profile management for Target Designations, Target Locations (EU, remote, local), Compensation Expectations, Spoken Languages, and Hard Dealbreakers.

## Development Setup

```bash
# Install dependencies
npm install

# Start Vite development server
npm run dev
```

Server runs by default at `http://localhost:5173`. Proxies/calls backend API at `http://127.0.0.1:8000/api/v1`.
