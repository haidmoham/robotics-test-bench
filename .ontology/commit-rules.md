# Commit ontology contract

Use the installed `commit-boundary` skill before landing commits that change experiment evidence, agent interaction records, queue state, stable IDs, provenance, or C-1N integration claims.

## Blocking invariants

- Preserve existing `AI/Q/R/E/A/O` IDs. Do not reuse, renumber, or silently replace them.
- Keep IDs repository-wide for the date. Parallel work must merge around allocated IDs.
- New agent-log entries must identify source provenance.
- Conversation-derived entries must preserve the explicit before -> after belief update and keep evidence status separate from provenance.
- Do not invent human evaluation, experimental observation, or a resolved outcome.
- If a commit claims an experiment boundary is resolved, its README and `agent-log.md` outcome must agree.
- If a resolved boundary changes the experiment route, re-evaluate `TODO.md`. It must still contain exactly one `NEXT` item.
- Keep GitHub issue numbers as stable concept identity. Do not use issue number as experiment chronology.
- A C-1N hook may describe an integration target. It must not claim a robot capability that the canonical C-1N repository has not demonstrated.

## Librarian state

- Keep `librarian.status` pending until Librarian actually persists the record.
- Preserve stable IDs and provenance when a pending entry is later synced.

## Advisory boundaries

- Implementation-only instrumentation does not require a new semantic record unless it changes a prediction, interpretation, decision, or next action.
- Prefer updating an existing entry when later evidence resolves its pending outcome.
