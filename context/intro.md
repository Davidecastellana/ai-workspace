---
title: Project Introduction
description: Overview of this AI workspace infrastructure
---

# AI Workspace

This is a Git-native AI workspace where the folder structure is the application.

## Architecture

- **context/** — Knowledge and documentation files. Claude reads these to understand the project.
- **pipelines/** — YAML workflow definitions. Each file describes a sequence of steps to execute.
- **summaries/** — Auto-generated outputs produced by pipeline runs.
- **tools/** — Scripts used by the pipeline executor.

## How It Works

1. Edit content via TinaCMS (localhost:3000/admin) or directly in files
2. Commit and push to GitHub
3. GitHub Actions detects changes and sends the job to the self-hosted runner (this Mac)
4. The pipeline executor runs `claude -p` for each AI step
5. Results are committed back automatically

## Philosophy

The folder structure is the app. Pipelines are strict YAML — parsed and executed by Python, not interpreted by an LLM. Claude Code is the AI worker within the pipeline, not the orchestrator.
