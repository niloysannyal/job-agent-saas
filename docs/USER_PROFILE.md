# User Profile — Niloy Sannyal

This file covers what MASTER_CV.tex doesn't: the human context the agent needs to write
authentic emails, DMs, form answers, and interview prep. Facts below are either stated
directly by Niloy or carried over from his existing context file; anything still marked
[fill in] has no confirmed answer yet and must not be invented by the agent.

## Basic info
- Name: Niloy Sannyal
- Current role: AI Engineer, Betopia Limited
- Education: B.Sc. in Information and Communication Engineering, University of Rajshahi
- Location: Dhaka, Bangladesh
- Links: see MASTER_CV.tex header (Portfolio, LinkedIn, GitHub, LeetCode, Codeforces)

## Job search logistics
- Target roles: AI Engineering, Machine Learning Engineering, Generative AI, LLM
  Engineering, Agentic AI, Applied AI, Computer Vision, AI Backend Engineering,
  MLOps/AI Infrastructure, Production AI systems; Robotics/Robotic AI as a longer-term
  direction (see "Robotics & long-term direction" below)
- Target locations: open to relocating anywhere in the EU; also open to strong on-site
  roles in Dhaka/Bangladesh (e.g. the Inverse.AI Robotics Engineer role, Mohakhali DOHS)
- Work authorization / visa needs for EU relocation: [fill in — sponsorship required?]
- Notice period: [fill in]
- Salary expectation: [fill in — treat as sensitive, don't put a figure in outbound
  messages unless Niloy provides one for that specific application]
- Dealbreakers: generic/low-substance roles that don't involve real production systems

## Positioning & narrative
Core narrative to reuse across CVs, summaries, and outreach:
> Niloy builds real AI systems, integrates them with business software, deploys them,
> and takes responsibility for keeping them working.

- Primary identity: AI/ML Engineer focused on production AI systems — Agentic AI, LLM
  applications, RAG, backend/API engineering, MLOps, applied ML — not someone who only
  experiments with models.
- Representative one-liner: "AI/ML Engineer building and deploying scalable AI-powered
  systems using Python, FastAPI, LLMs, RAG, Agentic AI, and MLOps."
- Recurring engineering principle to echo in interviews/writing: the model is only one
  component — a useful AI product needs data, retrieval, state, orchestration, APIs,
  infrastructure, monitoring, and a reliable user workflow around the model.
- Avoid: "passionate AI enthusiast" framing, generic claims with no engineering evidence,
  keyword stuffing, fabricated technologies, inflated metrics, fake leadership claims.

## Robotics & long-term direction
- Has loved robotics since childhood and has built what he could learn and afford;
  robotics/physical AI is his ultimate long-term goal, not a side interest.
- Trajectory he frames his career around: LLM -> Agent -> Autonomous system ->
  Physical/robotic intelligence.
- Cites physical problem-solving and visualization as personal strengths relevant to
  robotics.
- Currently pursuing this direction partly through the Inverse.AI Robotics Engineer
  role (Mohakhali DOHS, Dhaka; on-site; 60k+ BDT; apply by email to
  career@inverseai.com) — positioned as an AI Engineer moving toward robotics/physical
  AI. Do not claim ROS, kinematics, or other hands-on robotics-engineering experience he
  hasn't done — frame this honestly as a deliberate pivot, not existing expertise.
- Related long-term interests to draw on for "why this role" answers: robot perception,
  vision-language-action models, reinforcement learning, robot planning, sim-to-real
  learning, autonomous navigation, manipulation, embodied AI, human-robot interaction.

## Working style & soft skills
- Hands-on, curious, self-directed, comfortable taking ownership, execution-oriented;
  learns by building and debugging real systems rather than staying theoretical.
- Moves fluidly across business requirements, AI architecture, Python code, API design,
  Docker, Linux servers, Git, database/state layers, and frontend/backend integration.
- Leadership example: led the Betopia Sales Agent largely solo ("one man army"),
  covering requirement gathering, visiting SBUs and talking to salespeople, knowledge
  collection, AI/RAG development, agent development, UI/backend integration, CEO-level
  updates, salesperson reviews, deployment, CI/CD, monitoring, Odoo integration, and
  production debugging — with help from colleagues Asif and Zohora apu.
- Prefers practical solutions over theoretical complexity, clear architecture over
  clever abstractions, explicit interfaces, and real business impact over demos.

## Adaptability
- Rapidly self-onboarded onto Odoo, Redis, Qdrant, and Next.js for the Betopia Sales
  Agent — none were prior hands-on experience.
- Actively experiments across AI providers and tooling rather than sticking to one:
  OpenAI, Anthropic, Gemini, Qwen, Ollama, self-hosted/open-weight models, OpenClaw,
  OpenCode — evaluated for where each fits in a production architecture (accuracy,
  latency, cost, context length, tool use, self-hosting, deployment constraints).
- Has evaluated vision models (e.g. Qwen 3.x vision, including self-hosted deployments)
  for document/screenshot information extraction.

## Hobbies & personal interests
- Football, including playing on artificial turf; follows football analytics/tech
  (e.g. his FIFA World Cup 2026 analytics project).
- Technology/corporate stories tied to engineering, entrepreneurship, career growth,
  and ambition.
- Broad technology enthusiasm — trying new AI tools and models as they appear.

## Reasons for leaving current role
Keep this consistent across every application — growth, scope, and ambition. Do not
mention compensation dissatisfaction or criticize the current employer in any outbound
material.
- Standard framing to reuse: looking for a role with broader ownership and scale,
  ideally one that also moves his trajectory toward robotics/physical AI.

## Tone & writing preferences
(See /preferences.md for the full standing communication rules — summarized here for
anything drafting outbound text.)
- Direct, technically precise, no corporate fluff, no excessive motivational language.
- Concise and credible; avoid exaggerated claims and buzzwords.
- Every statement must be defensible if asked about in an interview.
- Prefer natural, non-AI-sounding professional English over overly polished phrasing.
- Keep short-form applications/messages short.
- Never say: "passionate AI enthusiast," inflated metrics, fabricated technologies or
  certifications, fake leadership claims, or generic descriptions that could describe
  any AI engineer.

## Facts that require confirmation before use (never invent these)
Exact years of experience; exact employment dates beyond what's in MASTER_CV.tex; exact
salary or compensation figures; exact academic GPA; exact project revenue; exact
performance percentages beyond the verified ones in MASTER_CV.tex; exact model
names/versions used in production beyond OpenAI/Anthropic/Gemini as providers;
application or user counts for any project other than the verified 700+ salespersons on
Betopia Sales Agent; certifications or awards not explicitly listed in MASTER_CV.tex.

## Interview story bank (STAR format)
### Story: Betopia Sales Agent — end-to-end ownership
- Situation/Task: Betopia needed a production AI sales assistant embedded in Odoo CRM,
  with no existing team or infrastructure for it.
- Action: owned the project solo end-to-end — requirement gathering, visiting SBUs and
  salespeople, collecting won/lost cases and objection-handling knowledge, building the
  RAG/LLM pipeline, multi-provider routing with failover, the agent itself, backend and
  admin frontend, CI/CD, deployment, and ongoing production operation.
- Result: production system used by 700+ salespersons across Betopia Group.
- Good for: ownership, ambiguity, end-to-end execution, working solo.

### Story: Self-onboarding onto an unfamiliar stack
- Situation/Task: the Sales Agent required Odoo, Redis, Qdrant, and Next.js — none used
  hands-on before.
- Action: learned and integrated all four directly inside a live production build,
  rather than deferring the project or staying in familiar tools.
- Result: all four are now core, reliable parts of the production system.
- Good for: learning speed, adaptability, comfort with the unfamiliar.

### Story: Vision/document information extraction
- Situation/Task: the Sales Agent needed to read Fiverr inbox screenshots, PDFs, and
  other documents and extract structured information reliably.
- Action: evaluated vision-capable models (including self-hosted options) for
  extraction accuracy, structured output, and cost/latency trade-offs, and built the
  extraction pipeline into the agent.
- Result: working document/image understanding inside the production agent.
- Good for: multimodal AI, practical model evaluation, production trade-offs.

### Story: [add more as they come up — e.g. HA-MEEM factory digitization consulting]
- Situation/Task:
- Action:
- Result:
- Good for:
