# Workspace Map

This is the routing table. Read this first. It tells you where everything is,
what to load for each task, and what to skip.

## Folder Structure

| Folder | Purpose |
|---|---|
| `context/` | Knowledge and content files — source of truth |
| `context/writing/` | Writing room — drafts, scripts, articles |
| `context/production/` | Production room — specs, builds, outputs |
| `context/research/` | Research room — notes, references, findings |
| `pipelines/` | Pipeline definitions (YAML) — what to execute per room |
| `summaries/` | Auto-generated outputs from pipeline runs |
| `tools/` | Executor scripts — do not modify during pipeline runs |

## Routing Table

| Task | Read | Skip | Notes |
|---|---|---|---|
| Writing | `context/writing/**` | `context/production/**`, `context/research/**` | Focus on current drafts only |
| Production | `context/production/**` | `context/writing/**`, `context/research/**` | Load specs and build rules |
| Research | `context/research/**` | `context/writing/**`, `context/production/**` | Load references and findings |
| Summarize | `context/**` | `summaries/**`, `pipelines/**` | Full context scan |

## Rules

- Each folder is a room. Each room has its own pipeline.
- A pipeline fires when its room's files change.
- Never read files outside your assigned room unless explicitly told to.
- Write outputs to `summaries/` unless the pipeline specifies otherwise.
