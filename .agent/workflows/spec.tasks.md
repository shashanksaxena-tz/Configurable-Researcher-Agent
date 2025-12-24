---
description: Generate dependency-ordered tasks.md for feature implementation
---

This workflow converts your implementation plan into a detailed, actionable task breakdown organized by user story priority.

## Prerequisites

- Must have `plan.md` (from `/spec.plan`)
- Must have `spec.md` with user stories
- Optional: `data-model.md`, `/contracts/`, `research.md`

## What This Does

1. **Loads design documents**:
   - Required: `plan.md` (tech stack, architecture)
   - Required: `spec.md` (user stories with priorities)
   - Optional: `data-model.md` (entities)
   - Optional: `/contracts/` (API endpoints)
   - Optional: `research.md` (technical decisions)

2. **Generates structured tasks** organized by:
   - **Phase 1**: Setup (project initialization)
   - **Phase 2**: Foundational (blocking prerequisites)
   - **Phase 3+**: One phase per user story (in priority order)
   - **Final Phase**: Polish & cross-cutting concerns

3. **Each task follows strict format**:
   ```
   - [ ] T001 [P] [US1] Description with file/path/to/file.ext
   ```
   - Checkbox for tracking
   - Sequential task ID (T001, T002, ...)
   - `[P]` marker for parallelizable tasks
   - `[US#]` story label for user story tasks
   - Clear file path for implementation

4. **Provides execution guidance**:
   - Dependency graph showing story completion order
   - Parallel execution opportunities
   - Independent test criteria per story
   - MVP scope recommendation (typically User Story 1)

## Task Organization Principles

**User Story-Centric**:
- Each user story from `spec.md` gets its own phase
- All related components grouped together:
  - Models needed for that story
  - Services needed for that story
  - Endpoints/UI needed for that story
  - Tests (if requested) for that story

**Parallelization**:
- Tasks marked `[P]` can run in parallel
- Different files, no dependencies = parallelizable
- Same file or sequential dependency = must run in order

**Test-Driven** (if requested):
- Tests generated only if spec requests them or user wants TDD
- Tests appear before implementation in each phase
- Contract tests → Models → Services → Integration

## Output Format

The generated `tasks.md` includes:
- Feature overview and goals
- Complete task list by phase
- Dependency section (story completion order)
- Parallel execution examples
- Implementation strategy (MVP-first, incremental)
- Format validation confirmation

## Example Task Breakdown

**Setup Phase:**
```
- [ ] T001 Create project structure per plan
- [ ] T002 Initialize package.json with dependencies
- [ ] T003 Configure TypeScript and build tools
```

**User Story Phase (US1: User Registration):**
```
- [ ] T010 [P] [US1] Create User model in src/models/user.ts
- [ ] T011 [P] [US1] Create UserService in src/services/user.service.ts
- [ ] T012 [US1] Implement POST /api/users endpoint in src/routes/users.ts
- [ ] T013 [US1] Add validation middleware in src/middleware/validation.ts
```

## Completion Report

After generation, you'll see:
- Path to `tasks.md`
- Total task count
- Task count per user story
- Parallel opportunities identified
- Independent test criteria per story
- Suggested MVP scope
- Format validation status

## Next Steps

After task generation:
- Review `tasks.md` for completeness
- Run `/spec.analyze` to check consistency across spec/plan/tasks
- Run `/spec.implement` to execute the tasks
- Optionally run `/spec.checklist` for quality validation

## Tips

- Keep user stories small and independent for better parallelization
- Review the dependency graph to understand story order
- MVP = User Story 1 typically gives you a working baseline
- Parallel tasks can significantly speed up development
