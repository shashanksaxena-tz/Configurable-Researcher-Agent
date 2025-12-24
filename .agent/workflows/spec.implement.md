---
description: Execute the implementation plan by processing all tasks from tasks.md
---

This workflow executes your feature implementation by processing tasks in the correct dependency order with proper parallelization.

## Prerequisites

- **REQUIRED**: `tasks.md` (from `/spec.tasks`)
- **REQUIRED**: `plan.md` (from `/spec.plan`)
- **OPTIONAL**: `data-model.md`, `/contracts/`, `research.md`, `quickstart.md`
- **RECOMMENDED**: Run `/spec.analyze` first to validate consistency

## What This Does

1. **Checks checklist status** (if checklists exist):
   - Scans all checklist files in `checklists/` directory
   - Counts total, completed, and incomplete items
   - **BLOCKS if incomplete** and asks for confirmation
   - Displays status table:
     ```
     | Checklist    | Total | Completed | Incomplete | Status |
     |--------------|-------|-----------|------------|--------|
     | ux.md        | 12    | 12        | 0          | ✓ PASS |
     | security.md  | 8     | 5         | 3          | ✗ FAIL |
     ```

2. **Project setup verification**:
   - Auto-detects project type (git, Docker, Node, Python, etc.)
   - Creates/verifies appropriate ignore files:
     - `.gitignore` (if git repo)
     - `.dockerignore` (if Docker present)
     - `.eslintignore` or `eslint.config.js` ignores
     - `.prettierignore` (if Prettier present)
     - Language-specific ignores
   - Adds essential patterns for detected technologies
   - Preserves existing patterns, appends only missing critical ones

3. **Loads implementation context**:
   - Parses `tasks.md` for phases, dependencies, parallel markers
   - Reads `plan.md` for tech stack and architecture
   - Loads optional design artifacts as available

4. **Executes tasks phase-by-phase**:
   - **Phase 1**: Setup (project initialization)
   - **Phase 2**: Foundational (blocking prerequisites)
   - **Phase 3+**: User Stories (in priority order)
   - **Final Phase**: Polish & cross-cutting concerns

5. **Respects execution rules**:
   - Sequential tasks run in order
   - Parallel tasks `[P]` can run together (different files, no deps)
   - File-based coordination (same file → sequential)
   - TDD approach: Tests before implementation (if tests exist)
   - Halts on non-parallel task failure

6. **Tracks progress**:
   - Reports after each completed task
   - **Marks completed tasks** as `[X]` in `tasks.md`
   - Provides clear error messages with context
   - Suggests next steps if blocked

7. **Validates completion**:
   - Verifies all tasks completed
   - Checks features match specification
   - Validates tests pass (if tests exist)
   - Confirms plan compliance

## Execution Flow

```
1. Check checklists → PASS or ask user confirmation
2. Setup .gitignore and other ignore files
3. Parse tasks.md structure
4. Phase 1: Setup
   ├─ Create project structure
   ├─ Initialize dependencies
   └─ Configure build tools
5. Phase 2: Foundational
   ├─ Setup database
   ├─ Configure middleware
   └─ Create shared utilities
6. Phase 3: User Story 1 (MVP)
   ├─ Models
   ├─ Services
   ├─ Endpoints/UI
   └─ Tests (if present)
7. Phase 4+: Additional User Stories
8. Final Phase: Polish
   └─ Documentation, optimization, etc.
9. Completion validation
```

## Checklist Behavior

**If all checklists PASS**:
- Automatically proceeds to implementation

**If any checklist FAILS**:
- Shows incomplete item count
- Asks: "Some checklists are incomplete. Proceed anyway?"
- User responses:
  - "yes"/"proceed"/"continue" → Continues with implementation
  - "no"/"wait"/"stop" → Halts execution

## Progress Tracking

Tasks in `tasks.md` are automatically updated:
```diff
- - [ ] T001 Create project structure
+ - [X] T001 Create project structure
```

## Error Handling

**Non-parallel task fails**:
- Halts execution immediately
- Reports error with context
- Suggests remediation steps

**Parallel task `[P]` fails**:
- Continues with successful parallel tasks
- Reports failed tasks
- Continues to next phase if possible

## Ignore Files Auto-Detection

The workflow automatically creates/updates:

**Language Detection** (from `plan.md`):
- Node.js → `node_modules/`, `dist/`, `.env*`
- Python → `__pycache__/`, `venv/`, `*.pyc`
- Java → `target/`, `*.class`
- Go → `vendor/`, `*.exe`
- Rust → `target/`, `debug/`, `release/`
- And many more...

**Tool Detection**:
- Git repo → `.gitignore`
- Dockerfile* → `.dockerignore`
- ESLint config → `.eslintignore` or config ignores
- Prettier config → `.prettierignore`
- Terraform files → `.terraformignore`

## Completion Report

After implementation:
- Total tasks completed
- Features implemented
- Tests passed (if applicable)
- Spec compliance status
- Plan adherence confirmation

## Next Steps

After implementation:
- Manual testing of implemented features
- Review code quality and architecture
- Deploy to staging/production
- Generate documentation if needed

## Tips

- **Always run `/spec.analyze`** before implementing to catch issues early
- **Complete checklists first** to ensure spec quality
- **Start with MVP** (User Story 1) for faster feedback
- **Monitor parallel tasks** for potential conflicts
- **Review ignore files** after first run to add project-specific patterns
