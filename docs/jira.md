# Jira Usage Guide

## Project Setup
- Create a Jira project: Type = Scrum; Key = SPM
- Board: "SPM Agile Board" with columns: Backlog, Selected for Development, In Progress, In Review, Done
- Permissions: Team members added with Developer or Admin roles

## Issue Types
- Epic: Data, Model, API, Dashboard, CI/CD, Deployment
- Story: User-facing increments (e.g., "As an analyst, I want risk predictions")
- Task/Sub-task: Technical work (pipeline steps, refactors)
- Bug: Defects found in testing or review

## Workflow
- Backlog → Selected for Development → In Progress → In Review → Done
- Definition of Done: CI green, code merged, docs updated, demoable

## Sprint Cadence
- 2-week sprints
- Ceremonies: Planning, Daily Scrum, Review, Retrospective (see `docs/scrum.md`)

## Backlog Grooming
- Prioritize by business value and feasibility
- Add acceptance criteria and test notes for each story

## GitHub Mapping
- Branch naming: `feature/SPM-123-description`
- Commits: include issue key in commit message (e.g., `SPM-123: implement predict endpoint`)
- PR title: start with issue key, link PR to Jira issue

## Example Import CSV (Epics & Stories)
Save as `docs/jira_import.csv` and import via Jira CSV import.

Columns: Issue Type, Summary, Description, Epic Link, Priority

- Epic, Data, Synthetic data generation and documentation,, High
- Epic, Model, Baseline risk classifier and evaluation,, High
- Epic, API, FastAPI service and schemas,, High
- Epic, Dashboard, Streamlit GUI for SPM analytics,, Medium
- Epic, CI/CD, Linting, typing, tests, and builds,, Medium
- Epic, Deployment, Containerization and local deploy,, Medium
- Story, Generate synthetic SPM dataset,Create `portfolios.csv` with features, Data, High
- Story, Train RandomForest risk classifier,Save joblib artifact and metrics, Model, High
- Story, Implement /predict endpoint,Swagger docs and Pydantic models, API, High
- Story, Build risk dashboard,EDA and single prediction form, Dashboard, Medium
- Story, Add CI workflow,Ruff+mypy+pytest on push/PR, CI/CD, Medium
- Story, Containerize services,Dockerfile and docker-compose, Deployment, Medium
