# Agent Interaction: <short title>

```yaml
id: AI-YYYYMMDD-NNN
date: YYYY-MM-DD
agent: Codex
status: open # open | acted | resolved | abandoned
evaluation: unconfirmed # unconfirmed | confirmed
repo_state:
  repository: robotics-test-bench
  branch:
  commit:
  changed_files: []
related:
  experiment:
  hypotheses: []
  experiments: []
  claims: []
  decisions: []
  issues: []
  files: []
objects:
  question: Q-YYYYMMDD-NNN
  response: R-YYYYMMDD-NNN
  evaluation: E-YYYYMMDD-NNN
  action: A-YYYYMMDD-NNN
  outcome: O-YYYYMMDD-NNN
librarian:
  status: pending # pending | synced | not-needed
  record_ids: []
```

## Q — Question

State the decision-relevant question.

### Human prediction

Record Iteration 0 before the agent reveals a non-trivial mechanism or result when learning is the target.

### Purpose

Explain why the question matters to the experiment or implementation.

### Context supplied

List only the files, constraints, observations, data, or prior claims that shaped the interaction.

## R — Response summary

Summarize the useful claims, options, warnings, or proposed tests. Do not paste the full response by default.

## E — Human evaluation

### Accepted

- Useful or correct item accepted by the human.

### Rejected

- Item rejected and why.

### Unresolved

- Item that still needs evidence or a decision.

### Verification required

- Code, data, documentation, inspection, or experiment required before treating the response as evidence.

## A — Action

Record the test, inspection, decision, code change, or commit caused by the interaction. Link repository-relative files and other evidence.

If the action changes code, use the commit message as the translation layer between reasoning and implementation: state why the current belief, evidence, or decision justified the change. Leave exact implementation detail to the diff.

## O — Outcome

Record the observed result, or write `Pending` until it is known.

### Effect on current belief

State which prediction, hypothesis, claim, interpretation, or decision became stronger, weaker, rejected, or superseded.

## Librarian update

Pass this compact payload during the next Librarian invocation. Preserve the stable IDs when updating the entry.

```yaml
source:
  repository: robotics-test-bench
  path: experiments/<date-question>/agent-log.md
  commit:
objects:
  - id: Q-YYYYMMDD-NNN
    type: Question
    summary:
    status:
  - id: R-YYYYMMDD-NNN
    type: Response
    summary:
    status:
  - id: E-YYYYMMDD-NNN
    type: Evaluation
    summary:
    status:
  - id: A-YYYYMMDD-NNN
    type: Action
    summary:
    status:
  - id: O-YYYYMMDD-NNN
    type: Outcome
    summary:
    status:
relations:
  - subject: Q-YYYYMMDD-NNN
    predicate: receives
    object: R-YYYYMMDD-NNN
  - subject: R-YYYYMMDD-NNN
    predicate: receives
    object: E-YYYYMMDD-NNN
  - subject: E-YYYYMMDD-NNN
    predicate: causes
    object: A-YYYYMMDD-NNN
  - subject: A-YYYYMMDD-NNN
    predicate: produces
    object: O-YYYYMMDD-NNN
unresolved_questions: []
superseded_claims: []
```

Do not include secrets, hidden reasoning, full chat transcripts, or unsupported conclusions presented as verified facts.
