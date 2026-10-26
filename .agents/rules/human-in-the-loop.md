# Rule: Human-In-The-Loop on Send

All application workflows in this SaaS must strictly terminate at:
`Draft -> Human Reviews -> Send`

- Under no circumstances should an automated, scheduled, or unattended send path be implemented.
- Every email, webform answer, or DM outreach must be placed into a draft state awaiting explicit human review and approval.
- Follow-up messages (Module 3) must also be drafted only, capped at a maximum of 2 follow-ups per application, and never auto-sent.
