---
description: Execute the implementation planning workflow to generate technical design artifacts
---

This workflow creates the technical implementation plan based on your feature specification. It translates business requirements into concrete technical design decisions.

## Prerequisites

- Must have completed `spec.md` (via `/spec.specify`)
- Ideally run `/spec.clarify` first to resolve ambiguities
- Spec should be free of critical ambiguities

## What This Does

The planning workflow executes in phases:

### Phase 0: Outline & Research

1. **Extract unknowns** from technical context:
   - Technology choices needing validation
   - Integration patterns to research
   - Best practices for chosen stack

2. **Generate research findings** in `research.md`:
   - Decision: What was chosen
   - Rationale: Why it was chosen
   - Alternatives considered: What else was evaluated

### Phase 1: Design & Contracts

1. **Data Model** (`data-model.md`):
   - Extract entities from spec
   - Define fields, relationships, validation rules
   - Document state transitions (if applicable)

2. **API Contracts** (`/contracts/`):
   - Generate endpoints from functional requirements
   - Create OpenAPI or GraphQL schema
   - Map user actions to API operations

3. **Quickstart Guide** (`quickstart.md`):
   - Development setup instructions
   - Testing scenarios
   - Integration examples

4. **Agent Context Update**:
   - Updates AI coding assistant context
   - Adds technology choices to agent configuration
   - Preserves manual customizations

### Phase 2: Constitution Validation

- Checks design against project constitution principles
- Flags any violations as CRITICAL
- Ensures quality gates are met

## User Input

When running this workflow, you should provide:
- **Tech stack preferences** (if not already in spec)
- **Architecture style** (monolith, microservices, etc.)
- **Infrastructure constraints** (cloud provider, hosting, etc.)

Example:
> "I'm building with Node.js/Express, PostgreSQL, React frontend, deployed on AWS"

## Outputs

After completion, you'll have:
- `plan.md` - Complete implementation plan
- `research.md` - Technology decisions and rationale
- `data-model.md` - Entity definitions
- `/contracts/` - API specifications
- `quickstart.md` - Development guide
- Updated agent context files

## Next Steps

After planning is complete:
- Review the generated artifacts
- Run `/spec.tasks` to break down into actionable tasks
- Optionally run `/spec.checklist` to generate domain-specific quality checklists

## Common Use Cases

**Full stack web app:**
> "Building with Next.js 14, TypeScript, Prisma ORM, PostgreSQL, deployed on Vercel"

**Microservice:**
> "Go service with gRPC, PostgreSQL, Redis cache, Docker/Kubernetes deployment"

**Mobile app backend:**
> "Node.js REST API, MongoDB, Firebase Auth, deployed on Google Cloud Run"
