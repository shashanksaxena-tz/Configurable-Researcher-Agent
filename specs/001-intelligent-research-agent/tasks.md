# Tasks: Intelligent Research Agent

**Input**: Design documents from `/specs/001-intelligent-research-agent/`  
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓

**Organization**: Tasks are grouped by user story (P1-P3) to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Paths follow web app convention: `backend/`, `frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic configuration

- [x] T001 Create agentic module directory structure at `backend/modules/` (planner, researcher, verifier, synthesizer, citation_tracker)
- [x] T002 [P] Add new Python dependencies to `backend/requirements.txt` (tenacity for retries, structlog for logging)
- [x] T003 [P] Create frontend premium styles directory at `frontend/src/styles/` (typography.css, colors.css, dark-mode.css)
- [x] T004 [P] Add Google Fonts (Playfair Display, Inter) to `frontend/index.html`
- [x] T005 [P] Install Vitest and React Testing Library via `frontend/package.json`
- [x] T006 Update `backend/config.py` with agentic workflow configuration (LLM models, timeouts, depth settings)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can proceed

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create base Pydantic models in `backend/models.py` for ResearchRequest, ResearchPlan, SubQuestion (extend existing models)
- [x] T008 [P] Create structured logging utility in `backend/utils/logging_utils.py` (JSON format, stage durations per NFR-003 to NFR-006)
- [x] T009 [P] Create LLM abstraction layer in `backend/utils/llm_utils.py` (multi-model support, retry with backoff)
- [x] T010 [P] Create search abstraction in `backend/utils/search_utils.py` (DuckDuckGo, Wikipedia, English-only filter per NFR-008)
- [x] T011 Create API router skeleton in `backend/main.py` for `/api/research/*` endpoints
- [x] T012 [P] Create frontend theme context in `frontend/src/contexts/ThemeContext.jsx` (dark mode default per FR-016)
- [x] T013 [P] Create research context in `frontend/src/contexts/ResearchContext.jsx` (current research, loading state)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Deep Research with Multi-Step Reasoning (Priority: P1) 🎯 MVP

**Goal**: Transform the agent from a shallow search wrapper into an intelligent research system that deconstructs queries, performs recursive searches, cross-references data, and synthesizes narrative reports.

**Independent Test**: Submit query "Research Tesla's Q4 2023 performance" → Receive research plan with 5+ sub-questions → View narrative report with 300+ words per section → Verify all claims have source citations.

### Implementation for User Story 1

#### Backend Agentic Modules

- [x] T014 [P] [US1] Create Planner module in `backend/modules/planner.py` (query deconstruction into 3-10 sub-questions per FR-001)
- [x] T015 [P] [US1] Create DeepResearcher module in `backend/modules/deep_researcher.py` (recursive search with depth limit per FR-003, FR-004)
- [x] T016 [P] [US1] Create Verifier module in `backend/modules/verifier.py` (cross-reference data, detect discrepancies per FR-005, FR-009)
- [x] T017 [P] [US1] Create Synthesizer module in `backend/modules/synthesizer.py` (narrative generation per FR-007, FR-008)
- [x] T018 [US1] Create workflow orchestrator in `backend/modules/agentic_workflow.py` (coordinates Plan-Execute-Verify-Synthesize stages)

#### Backend Data Models

- [x] T019 [P] [US1] Extend models in `backend/models.py` with SearchResult, Fact, Discrepancy, NarrativeReport, ReportSection entities
- [x] T020 [US1] Add Pydantic validators for word count minimums (300 words) and source requirements (3+ per section)

#### Backend API Endpoints

- [x] T021 [US1] Implement `POST /api/research/plan` endpoint in `backend/main.py` (returns structured research plan)
- [x] T022 [US1] Implement `POST /api/research/execute` endpoint in `backend/main.py` (async workflow execution)
- [x] T023 [US1] Implement `GET /api/research/{id}/status` endpoint in `backend/main.py` (progress polling)
- [x] T024 [US1] Implement `GET /api/research/{id}/report` endpoint in `backend/main.py` (retrieve completed report)
- [x] T025 [US1] Add structured logging to all endpoints per NFR-003 to NFR-006

#### Backend Tests

- [x] T026 [US1] Write unit tests for Planner module in `backend/tests/unit/test_planner.py`
- [x] T027 [US1] Write unit tests for DeepResearcher module in `backend/tests/unit/test_deep_researcher.py`
- [x] T028 [US1] Write unit tests for Verifier module in `backend/tests/unit/test_verifier.py`
- [x] T029 [US1] Write unit tests for Synthesizer module in `backend/tests/unit/test_synthesizer.py`
- [x] T030 [US1] Integration test for full workflow in `backend/tests/integration/test_agentic_workflow.py`

**Checkpoint**: User Story 1 (Core Intelligence) should be fully functional and testable via API

---

## Phase 4: User Story 2 - Executive Intelligence Dashboard UI (Priority: P1) 🎯 MVP

**Goal**: Create a premium, trustworthy interface with Bloomberg Terminal-level quality featuring professional typography, high information density, and dark mode.

**Independent Test**: View any completed research report → See Executive Brief at top → Navigate via tabbed sections → Verify premium typography (Playfair + Inter) → Confirm dark mode and navy/slate/gold palette.

### Implementation for User Story 2

#### Frontend Premium Design System

- [ ] T031 [P] [US2] Create typography CSS in `frontend/src/styles/typography.css` (Playfair Display headings, Inter body per FR-014)
- [ ] T032 [P] [US2] Create color palette CSS in `frontend/src/styles/colors.css` (navy-900, slate, gold per FR-015)
- [ ] T033 [P] [US2] Create dark mode CSS in `frontend/src/styles/dark-mode.css` (default dark, optional light per FR-016)
- [ ] T034 [P] [US2] Create premium card component in `frontend/src/components/PremiumCard.jsx` (high information density per FR-018)

#### Frontend Core Components

- [ ] T035 [P] [US2] Create ExecutiveBrief component in `frontend/src/components/ExecutiveBrief.jsx` (1-minute summary per FR-010)
- [ ] T036 [P] [US2] Create ResearchTabs component in `frontend/src/components/ResearchTabs.jsx` (Financials/Legal/Reputation tabs per FR-011)
- [ ] T037 [P] [US2] Create MetricDisplay component in `frontend/src/components/MetricDisplay.jsx` (contextual metrics per FR-017)
- [ ] T038 [US2] Create ResearchReport page in `frontend/src/pages/ResearchReport.jsx` (integrates all components)

#### Frontend Dashboard

- [ ] T039 [US2] Update Dashboard in `frontend/src/pages/Dashboard.jsx` (replace card grid with executive layout)
- [ ] T040 [US2] Update App.jsx with routing for new report pages in `frontend/src/App.jsx`
- [ ] T041 [US2] Update API service in `frontend/src/services/api.js` (add new endpoint calls)

#### Frontend Tests

- [ ] T042 [P] [US2] Create component test for ExecutiveBrief in `frontend/tests/components/ExecutiveBrief.test.jsx`
- [ ] T043 [P] [US2] Create component test for ResearchTabs in `frontend/tests/components/ResearchTabs.test.jsx`
- [ ] T044 [P] [US2] Create component test for MetricDisplay in `frontend/tests/components/MetricDisplay.test.jsx`

**Checkpoint**: User Story 2 (Premium UI) should render reports with premium design, complete with US1

---

## Phase 5: User Story 3 - Source Transparency and Verification (Priority: P2)

**Goal**: Enable users to verify every claim by clicking to view original sources with citation metadata.

**Independent Test**: Click any claim in a report → See source URL, extraction timestamp, excerpt → Access complete bibliography → View discrepancy notes for conflicting sources.

### Implementation for User Story 3

#### Backend Citation System

- [ ] T045 [P] [US3] Create CitationTracker module in `backend/modules/citation_tracker.py` (bidirectional mapping per data-model.md)
- [ ] T046 [US3] Implement `GET /api/research/{id}/citations` endpoint in `backend/main.py` (returns bibliography)
- [ ] T047 [US3] Implement `GET /api/citations/fact/{id}` endpoint in `backend/main.py` (source details for specific claim)
- [ ] T048 [US3] Integrate CitationTracker with Synthesizer to embed `[cite:uuid]` markers in report content

#### Frontend Citation Components

- [ ] T049 [P] [US3] Create CitationTooltip component in `frontend/src/components/CitationTooltip.jsx` (hover/click source display per FR-012)
- [ ] T050 [P] [US3] Create SourceList component in `frontend/src/components/SourceList.jsx` (bibliography per FR-013)
- [ ] T051 [US3] Create citation context in `frontend/src/contexts/CitationContext.jsx` (active citation state)
- [ ] T052 [US3] Add citation parser utility to replace `[cite:uuid]` markers with interactive components
- [ ] T053 [US3] Update ReportSection in `frontend/src/components/ReportSection.jsx` to render inline citations

#### Tests for User Story 3

- [ ] T054 [P] [US3] Create unit test for CitationTracker in `backend/tests/unit/test_citation_tracker.py`
- [ ] T055 [P] [US3] Create component test for CitationTooltip in `frontend/tests/components/CitationTooltip.test.jsx`
- [ ] T056 [P] [US3] Create component test for SourceList in `frontend/tests/components/SourceList.test.jsx`

**Checkpoint**: User Story 3 (Source Transparency) should be complete; all claims verifiable

---

## Phase 6: User Story 4 - Adaptive Research Depth (Priority: P3)

**Goal**: Allow users to control research depth (quick/standard/comprehensive) for different query needs.

**Independent Test**: Submit same query with "quick" vs "comprehensive" depth → Verify quick generates 3-5 sub-questions, comprehensive generates 7-10 → Confirm different completion times.

### Implementation for User Story 4

#### Backend Depth Configuration

- [ ] T057 [US4] Update ResearchRequest model in `backend/models.py` with depth_level enum (quick/standard/comprehensive)
- [ ] T058 [US4] Update Planner to adjust sub-question count based on depth_level in `backend/modules/planner.py`
- [ ] T059 [US4] Update DeepResearcher to adjust recursion depth based on depth_level in `backend/modules/deep_researcher.py`
- [ ] T060 [US4] Add depth_level parameter to `/api/research/execute` endpoint in `backend/main.py`

#### Frontend Depth Controls

- [ ] T061 [P] [US4] Create DepthSelector component in `frontend/src/components/DepthSelector.jsx` (quick/standard/comprehensive toggle)
- [ ] T062 [US4] Update research input form to include DepthSelector in `frontend/src/pages/Dashboard.jsx`
- [ ] T063 [US4] Update API service to pass depth_level parameter in `frontend/src/services/api.js`

#### Tests for User Story 4

- [ ] T064 [US4] Create test for depth-aware planning in `backend/tests/unit/test_planner.py` (add test cases)
- [ ] T065 [US4] Create component test for DepthSelector in `frontend/tests/components/DepthSelector.test.jsx`

**Checkpoint**: User Story 4 (Adaptive Depth) complete; all user stories functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Quality improvements, documentation, and production readiness

- [ ] T066 [P] Run and verify all backend tests with `pytest backend/tests/ -v`
- [ ] T067 [P] Run and verify all frontend tests with `cd frontend && npm run test`
- [ ] T068 [P] Update README.md with new feature documentation
- [ ] T069 [P] Add health check endpoint `GET /api/health` in `backend/main.py` (LLM and search provider status)
- [ ] T070 Code cleanup: remove unused imports and dead code across `backend/` and `frontend/`
- [ ] T071 Performance review: verify research completes in <3 minutes per SC-010
- [ ] T072 Accessibility audit: verify WCAG 2.1 AA contrast ratios in frontend components
- [ ] T073 Run quickstart.md validation scenarios (all 6 manual test scenarios)
- [ ] T074 Security review: verify no API keys exposed in frontend code

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ─────────────────┐
                                │
Phase 2: Foundational ←─────────┘
         │
         ├─→ Phase 3: US1 (Core Intelligence) ─→ [MVP Ready!]
         │           │
         │           └─→ Phase 4: US2 (Premium UI) ─→ [Full MVP!]
         │                       │
         │                       └─→ Phase 5: US3 (Citations)
         │                                   │
         │                                   └─→ Phase 6: US4 (Depth)
         │
         └─→ Phase 7: Polish (after all desired stories complete)
```

### User Story Dependencies

| Story | Depends On | Can Parallelize With |
|-------|------------|----------------------|
| US1 (Core Intelligence) | Phase 2 only | None (foundational) |
| US2 (Premium UI) | US1 (needs reports to display) | - |
| US3 (Citations) | US1 + US2 (needs reports and UI) | - |
| US4 (Adaptive Depth) | US1 (needs planner/researcher) | US2, US3 |

### Within Each User Story

1. Models before services
2. Services before endpoints
3. Backend before frontend (need API to call)
4. Core implementation before tests
5. All tests pass before checkpoint

### Parallel Opportunities

**Phase 1 (Setup)**: T002, T003, T004, T005 can run in parallel  
**Phase 2 (Foundational)**: T008, T009, T010, T012, T013 can run in parallel  
**Phase 3 (US1)**: T014-T017 (modules), T026-T029 (tests) can run in parallel  
**Phase 4 (US2)**: T031-T037 (components) can run in parallel  
**Phase 5 (US3)**: T049-T050 (components), T054-T056 (tests) can run in parallel  
**Phase 7 (Polish)**: T066, T067, T068, T069 can run in parallel

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup (6 tasks)
2. Complete Phase 2: Foundational (7 tasks)
3. Complete Phase 3: User Story 1 - Core Intelligence (17 tasks)
4. **MVP CHECKPOINT**: Test via API - verify research workflow works
5. Complete Phase 4: User Story 2 - Premium UI (14 tasks)
6. **FULL MVP**: Test via browser - verify premium dashboard works
7. Deploy/demo if ready

### Incremental Delivery

| Milestone | Tasks | Cumulative Value |
|-----------|-------|------------------|
| Foundation Ready | T001-T013 (13) | Infrastructure complete |
| Core Intelligence | T014-T030 (17) | Backend research API works |
| Premium UI | T031-T044 (14) | Full MVP with beautiful UI |
| Source Transparency | T045-T056 (12) | Citations and verification |
| Adaptive Depth | T057-T065 (9) | User control over research |
| Production Ready | T066-T074 (9) | Polish and documentation |

**Total Tasks: 74**

---

## Task Summary

| Phase | User Story | Task Count | Parallel Tasks |
|-------|------------|------------|----------------|
| 1 | Setup | 6 | 4 |
| 2 | Foundational | 7 | 5 |
| 3 | US1: Core Intelligence | 17 | 8 |
| 4 | US2: Premium UI | 14 | 10 |
| 5 | US3: Source Transparency | 12 | 6 |
| 6 | US4: Adaptive Depth | 9 | 1 |
| 7 | Polish | 9 | 4 |
| **Total** | | **74** | **38** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = Phase 1 + Phase 2 + Phase 3 + Phase 4 (44 tasks)
