---
description: Complete GitHub SpecKit workflow overview and command reference
---

# GitHub SpecKit with AntiGravity

This repository integrates the **GitHub SpecKit** methodology with **AntiGravity AI** workflows, making it easy to specify, plan, and implement features using a structured, repeatable process.

## What is SpecKit?

SpecKit is a feature development methodology that separates:
1. **WHAT** you're building (specification) - technology-agnostic requirements
2. **HOW** you'll build it (plan) - technical design and architecture  
3. **EXECUTION** (tasks & implementation) - actionable work items

## Available Workflows

All workflows are available as slash commands in AntiGravity using `/spec.*`:

### 1. `/spec.specify` - Create Feature Specification
**Purpose**: Convert natural language feature descriptions into structured specs

**When to use**: Starting a new feature

**What it does**:
- Generates branch name and creates feature directory
- Creates technology-agnostic specification
- Validates spec quality with requirements checklist
- Handles clarifications interactively

**Output**: `specs/{number}-{name}/spec.md`, quality checklist

**Example**:
> "Create a user authentication system with email/password login"

---

### 2. `/spec.clarify` - Resolve Specification Ambiguities
**Purpose**: Identify and resolve underspecified areas before planning

**When to use**: After `/spec.specify`, before `/spec.plan`

**What it does**:
- Analyzes spec for ambiguities across 8+ dimensions
- Asks up to 5 targeted questions (with recommended answers)
- Updates spec incrementally after each answer
- Provides coverage summary by taxonomy

**Output**: Updated `spec.md` with clarifications section

**Interactive**: Asks questions one at a time, waits for your answers

---

### 3. `/spec.plan` - Create Technical Implementation Plan
**Purpose**: Translate business requirements into technical design

**When to use**: After spec is complete (ideally after `/spec.clarify`)

**What it does**:
- **Phase 0**: Research unknowns and technology choices
- **Phase 1**: Generate data model, API contracts, quickstart guide
- **Phase 2**: Validate against project constitution
- Updates AI agent context with tech stack choices

**Output**: `plan.md`, `research.md`, `data-model.md`, `/contracts/`, `quickstart.md`

**User input**: Tech stack preferences, architecture style, infrastructure

---

### 4. `/spec.tasks` - Generate Task Breakdown
**Purpose**: Convert plan into dependency-ordered, actionable tasks

**When to use**: After `/spec.plan` completes

**What it does**:
- Organizes tasks by user story priority
- Generates phases: Setup → Foundation → User Stories → Polish
- Marks parallelizable tasks with `[P]`
- Labels story tasks with `[US#]`
- Creates dependency graph and execution examples

**Output**: `tasks.md` with complete task breakdown

**Task format**: `- [ ] T001 [P] [US1] Description in path/to/file.ext`

---

### 5. `/spec.checklist` - Generate Quality Checklists
**Purpose**: Create "unit tests for requirements" to validate spec quality

**When to use**: After `/spec.specify`, `/spec.plan`, or `/spec.tasks`

**What it does**:
- Tests requirements quality (NOT implementation)
- Validates: completeness, clarity, consistency, measurability, coverage
- Domain-specific checklists (UX, API, security, performance, etc.)
- Each run creates a new checklist file

**Output**: `checklists/{domain}.md`

**Focus areas**: UX, API, Security, Performance, Accessibility, etc.

**Example items**:
- ✅ "Are visual hierarchy requirements defined with measurable criteria?"
- ✅ "Is 'fast loading' quantified with specific timing thresholds?"
- ❌ NOT "Verify button works" (that's testing, not requirements validation)

---

### 6. `/spec.analyze` - Cross-Artifact Consistency Analysis
**Purpose**: Detect inconsistencies, gaps, and violations across spec/plan/tasks

**When to use**: After `/spec.tasks`, BEFORE `/spec.implement`

**What it does** (READ-ONLY):
- Detects: duplications, ambiguities, coverage gaps, constitution violations
- Assigns severity: CRITICAL, HIGH, MEDIUM, LOW
- Produces findings report with recommendations
- Maps requirements to tasks (coverage %)
- Offers optional remediation suggestions

**Output**: Analysis report (not written to file)

**Blocks implementation if**: CRITICAL issues found

---

### 7. `/spec.implement` - Execute Implementation
**Purpose**: Execute the implementation plan by processing all tasks

**When to use**: After `/spec.tasks` (ideally after `/spec.analyze` passes)

**What it does**:
1. Checks checklist status (blocks if incomplete)
2. Sets up ignore files (.gitignore, .dockerignore, etc.)
3. Loads implementation context
4. Executes tasks phase-by-phase in dependency order
5. Respects parallelization markers `[P]`
6. Marks completed tasks as `[X]` in `tasks.md`
7. Validates completion against spec

**Output**: Implemented feature, updated `tasks.md`

**Auto-setup**: Creates/updates ignore files based on detected tech stack

---

## Recommended Workflow Order

```
1. /spec.specify     → Create spec from description
   ↓
2. /spec.clarify     → Resolve ambiguities (optional but recommended)
   ↓
3. /spec.plan        → Create technical design
   ↓
4. /spec.checklist   → Generate quality checklists (optional)
   ↓
5. /spec.tasks       → Break down into tasks
   ↓
6. /spec.analyze     → Validate consistency (recommended)
   ↓
7. /spec.implement   → Execute implementation
```

## Quick Start Example

### Step 1: Specify
```
/spec.specify "Build a REST API for managing podcast episodes with CRUD operations, 
search, and filtering by category"
```

### Step 2: Clarify (if needed)
```
/spec.clarify
```
*Answer questions interactively*

### Step 3: Plan
```
/spec.plan "Using Node.js with Express, PostgreSQL, and Docker deployment"
```

### Step 4: Generate Tasks
```
/spec.tasks
```

### Step 5: Check Quality (optional)
```
/spec.checklist "Create an API quality checklist"
```

### Step 6: Analyze Consistency
```
/spec.analyze
```

### Step 7: Implement
```
/spec.implement
```

## Key Principles

### Separation of Concerns
- **Spec**: What users need (business requirements, technology-agnostic)
- **Plan**: How to build it (technical design, architecture)
- **Tasks**: Step-by-step execution (actionable work items)

### Iterative Refinement
- Start with `/spec.specify` (rough requirements)
- Refine with `/spec.clarify` (resolve ambiguities)
- Validate with `/spec.analyze` (check consistency)
- Quality gates with `/spec.checklist` (validate requirements)

### Constitution Alignment
- Project constitution (`.specify/memory/constitution.md`) defines non-negotiable principles
- All workflows validate against constitution
- Violations are flagged as CRITICAL

### Progressive Disclosure
- Load only necessary context at each stage
- Avoid token waste with full file dumps
- Incremental updates after each clarification

## File Structure

After running through the workflow, you'll have:

```
specs/{number}-{feature-name}/
├── spec.md                    # Feature specification
├── plan.md                    # Implementation plan
├── tasks.md                   # Task breakdown
├── research.md                # Technology decisions
├── data-model.md              # Entity definitions
├── quickstart.md              # Development guide
├── contracts/                 # API contracts
│   ├── openapi.yaml
│   └── ...
└── checklists/                # Quality checklists
    ├── ux.md
    ├── api.md
    └── security.md
```

## Tips & Best Practices

### For Better Specs
- Focus on **WHAT** and **WHY**, not **HOW**
- Write for non-technical stakeholders
- Keep requirements measurable and testable
- Limit clarifications to 3 critical questions

### For Better Plans
- Be specific about tech stack choices
- Document architecture decisions in `research.md`
- Keep data model focused on entities mentioned in spec
- Generate API contracts from functional requirements

### For Better Tasks
- Organize by user story (enables independent testing)
- Mark parallelizable tasks with `[P]`
- Include exact file paths in task descriptions
- Keep tasks small and focused (single responsibility)

### For Better Implementation
- **Always run `/spec.analyze`** before implementing
- Complete checklists before implementation
- Start with MVP (User Story 1)
- Monitor progress via updated `tasks.md`

## Constitution

Your project constitution lives at `.specify/memory/constitution.md` and defines:
- Non-negotiable principles (MUST statements)
- Recommended practices (SHOULD statements)
- Quality gates and standards
- Technology constraints

All SpecKit workflows validate against the constitution.

## Troubleshooting

**"Prerequisites check failed"**:
- Ensure you're on a feature branch
- Run the prerequisite command first (e.g., `/spec.specify`)

**"Checklists incomplete" blocking implementation**:
- Review incomplete checklist items
- Update spec/plan to address issues
- Or choose to proceed anyway (risky)

**"CRITICAL issues found" in analysis**:
- Must resolve before implementing
- Follow recommended remediation commands
- Re-run `/spec.analyze` to verify

**Tasks failing during implementation**:
- Check error messages for context
- Review task dependencies in `tasks.md`
- Ensure sequential tasks aren't parallelized

## More Information

- SpecKit agents: `.github/agents/speckit.*.agent.md`
- Workflow definitions: `.agent/workflows/spec.*.md`
- Templates: `.specify/templates/`
- Scripts: `.specify/scripts/bash/`

---

**Ready to build?** Start with `/spec.specify "describe your feature here"`
