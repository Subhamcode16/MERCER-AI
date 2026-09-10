# Phase 26: Workforce API Contract Specification

## 1. Overview
The Workforce API provides RESTful endpoints under the `/workforce` prefix for managing persistent workers, skills, campaign rooms, handoffs, routines, activity streams, and system health.

## 2. Endpoints Summary
| Method | Path | Purpose |
|---|---|---|
| `POST` | `/workforce/workers` | Register new persistent digital coworker |
| `GET` | `/workforce/workers` | List coworkers scoped to tenant |
| `GET` | `/workforce/workers/{id}` | Get coworker profile and status |
| `PATCH` | `/workforce/workers/{id}/status` | Transition coworker lifecycle status |
| `POST` | `/workforce/skills` | Register immutable versioned skill |
| `GET` | `/workforce/skills` | List registered skills |
| `POST` | `/workforce/campaign-rooms` | Create collaborative Campaign Room |
| `GET` | `/workforce/campaign-rooms/{id}` | Inspect Campaign Room state and artifacts |
| `POST` | `/workforce/campaign-rooms/{id}/handoffs` | Create cryptographic worker handoff |
| `POST` | `/workforce/routines` | Register workforce routine |
| `POST` | `/workforce/routines/{id}/run` | Trigger routine in advisory dry-run mode |
| `GET` | `/workforce/activity` | Query sanitized workforce activity stream |
| `GET` | `/workforce/health` | System health check |
