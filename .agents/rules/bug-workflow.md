# Bug Workflow Standards (Chrome DevTools MCP & Agentation)

- Runtime bugs: reproduce in the browser with Chrome DevTools MCP, read console and network, find the root cause in source, fix it, reload and re-check the same signals before declaring it fixed.
- Prefer DOM/accessibility snapshots over screenshots. Take screenshots only for purely visual checks.
- When I say "watch mode": call agentation_watch_annotations in a loop. For each annotation: read its thread, agentation_acknowledge, locate the source using elementPath and component info, make the minimal fix, verify it in the browser, then agentation_resolve with a short summary. If an annotation is ambiguous, use agentation_reply to ask. If you decide not to act, use agentation_dismiss with a reason. Never resolve unverified work.
- Do not use Agentation's critique or self-driving modes unless I explicitly ask.
- Use test accounts and fake data only. Never log in with real credentials or real CV/personal data in the agent-controlled browser.

