# Implementation Plan: Intelligent Research Agent

**Branch**: `001-intelligent-research-agent` | **Date**: 2025-12-24 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-intelligent-research-agent/spec.md`

## Summary

Transform the Configurable Researcher Agent from a shallow search wrapper into a true intelligent research system. The implementation will:

1. **Backend AI Engine**: Replace linear search flow with a Plan-Execute-Verify-Synthesize workflow that includes recursive search, cross-referencing, and narrative synthesis
2. **Premium UI Redesign**: Create an Executive Intelligence Dashboard with Bloomberg Terminal-level quality, featuring serif/sans-serif typography, dark mode, tabbed navigation, and inline citations
3. **Source Transparency**: Implement comprehensive citation tracking and verification system

**Technical Approach**: Extend existing FastAPI backend with new agentic workflow modules. Redesign React frontend with premium component library and citation system. No database changes required initially (extend in-memory models).

## Technical Context

**Language/Version**: Python 3.11+ (backend), JavaScript ES2022+ (frontend)  
**Primary Dependencies**:
- Backend: FastAPI 0.104.1, Pydantic 2.5.0, HTTPX 0.25.1, BeautifulSoup4, Google Generative AI, OpenAI
- Frontend: React 18.2, Vite 5.0, Framer Motion 10.16, React Markdown 10.1, Axios 1.6
**Storage**: In-memory data structures (extend existing models.py), with optional SQLite for persistence in future iterations  
**Testing**: pytest + pytest-asyncio (backend), Vitest (frontend - to be added)  
**Target Platform**: Linux/macOS server (backend), Modern browsers (Chrome/Firefox/Safari latest)  
**Project Type**: Web application (separate backend/frontend)  
**Performance Goals**: 
- Research completion under 3 minutes for standard queries (5 sub-questions, 1 recursion level)
- Dashboard render under 2 seconds
- Citation lookup under 1 second
**Constraints**:
- LLM API rate limits (managed through backoff/retry)
- Search provider rate limits (DuckDuckGo, Wikipedia)
- Memory constraints for large research reports (target: <500MB per session)
**Scale/Scope**:
- Support 10-20 concurrent research sessions
- Reports with 10-50 sources per topic
- 5-10 sub-questions per research plan
- 2-3 levels of recursive search depth

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: No formal constitution file exists yet for this project. Applying general best practices:

### Design Principles (Inferred)

✅ **Modularity**: New agentic workflow will be implemented as separate modules (`modules/planner`, `modules/researcher`, `modules/verifier`, `modules/synthesizer`)  
✅ **Testability**: Each module will have unit tests, integration tests for the full workflow  
✅ **Extensibility**: Plugin architecture for new search providers and LLM backends  
✅ **User-Centric**: All changes driven by user value (deep research, trust, premium UX)  

### Quality Gates

- [ ] All new backend modules must have >80% test coverage
- [ ] Frontend components must pass accessibility audit (WCAG 2.1 AA)
- [ ] No regression in existing functionality
- [ ] Performance targets met (3min research, 2sec render, 1sec citation)

**Status**: PASSED - No violations. Proceeding to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-intelligent-research-agent/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output (technology research)
├── data-model.md        # Phase 1 output (entity definitions)
├── quickstart.md        # Phase 1 output (development guide)
├── contracts/           # Phase 1 output (API specifications)
│   ├── research-api.yaml
│   └── citation-api.yaml
├── checklists/          # Quality validation
│   └── requirements.md
└── tasks.md             # Phase 2 output (from /spec.tasks)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI app entry point (MODIFY)
├── config.py            # Configuration (MODIFY - add agentic settings)
├── models.py            # Data models (EXTEND)
├── modules/
│   ├── base_researcher.py       # Existing (MODIFY)
│   ├── planner.py               # NEW - Deconstructs queries into sub-questions
│   ├── deep_researcher.py       # NEW - Executes recursive searches
│   ├── verifier.py              # NEW - Cross-references and validates data
│   ├── synthesizer.py           # NEW - Generates narrative reports
│   └── citation_tracker.py      # NEW - Tracks sources and claims
├── utils/
│   ├── llm_utils.py             # Existing LLM helpers (EXTEND)
│   └── search_utils.py          # Existing search helpers (EXTEND)
└── tests/
    ├── unit/
    │   ├── test_planner.py
    │   ├── test_deep_researcher.py
    │   ├── test_verifier.py
    │   └── test_synthesizer.py
    └── integration/
        └── test_agentic_workflow.py

frontend/
├── src/
│   ├── components/
│   │   ├── ExecutiveBrief.jsx       # NEW - Top-level summary component
│   │   ├── ResearchTabs.jsx         # NEW - Tabbed navigation (Financials/Legal/Reputation)
│   │   ├── CitationTooltip.jsx      # NEW - Inline citation display
│   │   ├── SourceList.jsx           # NEW - Bibliography component
│   │   └── PremiumCard.jsx          # NEW - Premium UI card component
│   ├── pages/
│   │   ├── Dashboard.jsx            # MODIFY - New executive dashboard layout
│   │   └── ResearchReport.jsx       # NEW - Full report view
│   ├── services/
│   │   └── api.js                   # MODIFY - Add new endpoint calls
│   ├── styles/
│   │   ├── typography.css           # NEW - Serif/sans-serif setup
│   │   ├── colors.css               # NEW - Navy/slate/gold palette
│   │   └── dark-mode.css            # NEW - Dark mode styles
│   └── App.jsx                      # MODIFY - Route new pages
└── tests/
    └── components/                   # NEW - Component tests
```

**Structure Decision**: Extending existing web application structure (backend/ + frontend/). New agentic modules will live in `backend/modules/` alongside existing researchers. Frontend components will be added to `src/components/` with new premium styling system.

## Complexity Tracking

> No Constitution violations to justify. All changes align with extensibility and modularity principles.

---

## Phase 0: Research & Technology Decisions

See [research.md](./research.md) for detailed technology research and decision rationale.

### Key Decisions

1. **Agentic Workflow Pattern**: Chain-of-Thought with explicit Plan-Execute-Verify-Synthesize stages
2. **LLM Strategy**: Multi-model approach (GPT-4 for planning/synthesis, faster models for extraction)
3. **Citation Tracking**: Bidirectional mapping (claim → source, source → claims)
4. **UI Framework**: Enhance existing React with premium design system
5. **Typography**: Google Fonts (Playfair Display + Inter)
6. **State Management**: React Context API (sufficient for current scale)

---

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Key Entities**:
- `ResearchRequest` - User query with depth settings
- `ResearchPlan` - Generated sub-questions and priorities
- `SearchResult` - Raw search data with metadata
- `Fact` - Extracted claims with citations
- `Discrepancy` - Conflicting facts with resolution
- `NarrativeReport` - Final synthesized output

### API Contracts

See [contracts/](./contracts/) for OpenAPI specifications.

**New Endpoints**:
- `POST /api/research/plan` - Generate research plan
- `POST /api/research/execute` - Execute agentic workflow
- `GET /api/research/{id}/report` - Retrieve narrative report
- `GET /api/research/{id}/citations` - Get all sources
- `GET /api/research/{id}/status` - Check progress

### Development Guide

See [quickstart.md](./quickstart.md) for setup and testing instructions.

---

## Phase 2: Implementation Tasks

To be generated via `/spec.tasks` command.

**Expected Task Categories**:
1. Backend agentic modules (4-5 tasks)
2. Citation tracking system (2-3 tasks)
3. Frontend premium UI components (5-7 tasks)
4. API endpoint implementation (3-4 tasks)
5. Testing and validation (4-5 tasks)
6. Documentation and deployment (2-3 tasks)

**Total Estimated Tasks**: 20-27 tasks
