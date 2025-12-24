# Technology Research: Intelligent Research Agent

**Feature**: 001-intelligent-research-agent  
**Date**: 2025-12-24  
**Purpose**: Document technology decisions and rationale for the agentic research workflow

---

## Research Areas

### 1. Agentic Workflow Architecture

**Decision**: Chain-of-Thought pattern with explicit Plan-Execute-Verify-Synthesize stages

**Rationale**:
- **Modularity**: Each stage (Plan, Execute, Verify, Synthesize) can be developed, tested, and optimized independently
- **Observability**: Clear checkpoint between stages allows progress tracking and debugging
- **Extensibility**: Easy to add new stages (e.g., Optimization, Ranking) without refactoring
- **LLM Best Practice**: Explicit reasoning steps improve output quality vs. single-shot prompts
- **Testability**: Each stage has clear inputs/outputs making unit testing straightforward

**Alternatives Considered**:
- **ReAct (Reasoning + Acting)**: More flexible but harder to control recursion depth and can lead to infinite loops
- **Tree of Thoughts**: Explores multiple reasoning paths but too computationally expensive for user-facing research (3-minute target)
- **Single-Shot LLM**: Simple but produces shallow results, exactly what we're trying to avoid

**References**:
- [Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903)
- [ReAct: Synergizing Reasoning and Acting in LLMs](https://arxiv.org/abs/2210.03629)

---

### 2. LLM Strategy: Multi-Model Approach

**Decision**: Use different LLM models for different stages based on task complexity

**Proposed Allocation**:
- **Planning**: GPT-4 or Gemini 1.5 Pro (complex reasoning, generates sub-questions)
- **Information Extraction**: GPT-3.5-turbo or Gemini 1.5 Flash (fast, structured output)
- **Verification**: GPT-4 (cross-referencing requires nuanced reasoning)
- **Synthesis**: GPT-4 or Claude 3 Opus (narrative generation, professional tone)

**Rationale**:
- **Cost Optimization**: GPT-4 is 10-20x more expensive than GPT-3.5-turbo. Use it only where necessary
- **Latency**: Information extraction happens frequently (per search result). Fast models keep workflow under 3-minute target
- **Quality**: Planning and synthesis are one-time operations. Invest in quality here for better overall output

**Alternatives Considered**:
- **Single Model (GPT-4 everywhere)**: Highest quality but 5-10x cost and slower
- **Single Model (GPT-3.5 everywhere)**: Cheapest but insufficient for complex reasoning tasks
- **Open Source (Llama 2, Mistral)**: Free but requires hosting, less reliable structured output

**Implementation Note**: Make LLM backend configurable via environment variables to support swapping models without code changes

---

### 3. Citation Tracking System

**Decision**: Bidirectional mapping using in-memory data structures with unique IDs

**Architecture**:
```python
# Claim to Source (1-to-many)
citations_by_claim = {
    "claim_uuid": ["source_url_1", "source_url_2"]
}

# Source to Claims (1-to-many)
claims_by_source = {
    "source_url": ["claim_uuid_1", "claim_uuid_2"]
}

# Claim details
claims = {
    "claim_uuid": {
        "text": "Elon Musk's net worth is $180B",
        "confidence": 0.85,
        "extraction_timestamp": "2025-12-24T11:56:00Z",
        "section": "Financials"
    }
}

# Source metadata
sources = {
    "source_url": {
        "title": "Bloomberg - Tesla CEO Net Worth",
        "domain": "bloomberg.com",
        "access_timestamp": "2025-12-24T11:55:00Z",
        "credibility_score": 0.95
    }
}
```

**Rationale**:
- **Fast Lookup**: O(1) access for both "show sources for this claim" and "show claims from this source"
- **Memory Efficient**: UUIDs + references instead of duplicating claim/source text
- **Scalability**: Can handle 100+ sources and 500+ claims per report (well within 500MB memory constraint)
- **Future-Proofing**: Easy to migrate to database (SQLite, PostgreSQL) if persistence needed

**Alternatives Considered**:
- **Inline Embedding**: Store citations directly in claim text (e.g., "[1]"). Simple but hard to query bidirectionally
- **Graph Database (Neo4j)**: Powerful for complex queries but overkill for current scale, adds deployment complexity
- **Relational Database (PostgreSQL)**: Better for persistence but unnecessary overhead for MVP (no requirement to save past research)

---

### 4. Recursive Search Management

**Decision**: Depth-limited BFS (Breadth-First Search) with configurable max depth

**Algorithm**:
```
Queue = [original query]
Depth = 0
MaxDepth = 2 (configurable)

while Queue is not empty and Depth <= MaxDepth:
    CurrentQueries = Queue.dequeue_level()  # BFS: process all queries at current depth
    
    for query in CurrentQueries:
        Results = execute_search(query)
        NewTopics = extract_followup_topics(Results)  # LLM identifies relevant mentions
        
        if Depth < MaxDepth:
            Queue.enqueue(NewTopics)
    
    Depth += 1
```

**Rationale**:
- **BFS over DFS**: Ensures we get breadth coverage before going deep. Better for user experience (show partial results early)
- **Depth Limiting**: Prevents infinite loops (e.g., "A mentions B, B mentions A")
- **Configurability**: Users can control depth (quick mode: depth=1, comprehensive: depth=2-3)

**Alternatives Considered**:
- **DFS (Depth-First Search)**: Simpler but can get stuck in rabbit holes before covering main topics
- **No Recursion**: Violates core requirement for "recursive search when search results mention relevant details"
- **Unlimited Recursion with Cycle Detection**: More complex, harder to guarantee 3-minute completion time

**Edge Case Handling**:
- **Cycle Detection**: Track visited topics to avoid re-searching the same thing
- **Duplicate Mentions**: If topic mentioned multiple times, only add to queue once
- **Relevance Filtering**: LLM scores topics 0-1, only follow up if score > 0.6

---

### 5. UI Design System

**Decision**: Google Fonts (Playfair Display + Inter) with CSS custom properties for theming

**Typography**:
- **Headings**: Playfair Display (serif, 400/700 weights)
- **Body**: Inter (sans-serif, 400/500/600 weights)
- **Monospace**: JetBrains Mono (for code/data, 400 weight)

**Color Palette** (Dark Mode Default):
```css
:root {
  /* Primary */
  --navy-900: #0f1729;
  --navy-800: #1a2332;
  --navy-700: #243048;
  
  /* Neutrals */
  --slate-100: #f1f5f9;
  --slate-300: #cbd5e1;
  --slate-500: #64748b;
  --slate-700: #334155;
  
  /* Accents */
  --gold-400: #fbbf24;
  --gold-500: #f59e0b;
  --emerald-400: #34d399;  /* Success */
  --red-400: #f87171;       /* Error */
}
```

**Rationale**:
- **Professional Authority**: Playfair Display is used by Bloomberg, WSJ, FT for headings. Conveys trustworthiness
- **Readability**: Inter is optimized for digital screens, excellent at small sizes
- **Accessibility**: Minimum 4.5:1 contrast ratio (WCAG AA) between text and background
- **Performance**: Google Fonts CDN is globally cached, ~30KB total for all weights

**Alternatives Considered**:
- **System Fonts**: Free but inconsistent across platforms, less premium feel
- **Premium Fonts (Gotham, Proxima Nova)**: Licensing costs prohibitive for open-source project
- **All Serif**: Too traditional, harder to read at small sizes
- **All Sans-Serif**: Lacks the authority/premium feel we need

**Component Framework**:
- **No external library**: Build custom components to avoid bloat (Material-UI is 500KB+)
- **Framer Motion**: Already in dependencies, use for micro-animations (hover effects, tab transitions)
- **CSS Modules**: Scope styles to components, avoid global namespace pollution

---

### 6. State Management

**Decision**: React Context API for global state, local state for components

**Architecture**:
```javascript
// Global contexts
ResearchContext - {currentResearch, setResearch, loading, error}
CitationContext - {citations, showCitation, activeCitation}
ThemeContext - {darkMode, toggleTheme}

// Local state examples
ExecutiveBrief.jsx - {expanded, setExpanded}
ResearchTabs.jsx - {activeTab, setActiveTab}
```

**Rationale**:
- **Simplicity**: Context API is built-in, zero dependencies
- **Sufficient Scale**: 3-5 contexts adequate for this feature scope
- **Performance**: Re-renders manageable with React.memo and useCallback
- **Learning Curve**: Team already familiar with Context from existing codebase

**Alternatives Considered**:
- **Redux**: Overkill for this scale, adds 100KB+ and boilerplate complexity
- **Zustand**: Lightweight but adds dependency, Context API already meets needs
- **Prop Drilling**: Unmaintainable for citation data (needs to be accessible from any claim component)

---

### 7. Testing Strategy

**Decision**: Multi-layer testing with different tools per layer

**Backend Testing**:
```
Unit Tests (pytest):
  - Each agentic module (planner, researcher, verifier, synthesizer)
  - Citation tracker
  - Target: 80%+ coverage

Integration Tests (pytest-asyncio):
  - Full workflow (query → plan → execute → synthesize → report)
  - API endpoints
  - Target: Cover all user stories from spec

Contract Tests:
  - OpenAPI schema validation
  - Ensures frontend/backend stay in sync
```

**Frontend Testing**:
```
Component Tests (Vitest + React Testing Library):
  - ExecutiveBrief rendering
  - CitationTooltip interactions
  - ResearchTabs navigation
  - Target: 70%+ coverage

E2E Tests (Playwright - future):
  - Complete user journey: submit query → view report → click citations
  - Only add if integration tests insufficient
```

**Rationale**:
- **Pytest**: Already in use, excellent async support for LLM/API calls
- **Vitest**: Fast (Vite-native), modern alternative to Jest
- **Contract Tests**: Critical for preventing frontend/backend drift as teams work in parallel

**Alternatives Considered**:
- **TDD (Test-First)**: Ideal but not required by constitution, would slow initial prototyping
- **E2E Only**: Too slow and brittle for primary testing strategy
- **No Frontend Tests**: Risky for complex UI with citations and tabs

---

## Summary of Key Decisions

| Area | Decision | Primary Benefit |
|------|----------|-----------------|
| Workflow | Plan-Execute-Verify-Synthesize | Clear stages, observable, testable |
| LLM Strategy | Multi-model (GPT-4 + GPT-3.5) | Cost optimization + quality where needed |
| Citations | Bidirectional in-memory maps | O(1) lookup, memory efficient |
| Recursion | Depth-limited BFS | Controlled exploration, predictable timing |
| Typography | Playfair Display + Inter | Professional authority + readability |
| Colors | Navy/Slate/Gold dark mode | Premium Bloomberg-like aesthetic |
| State Mgmt | React Context API | Simple, sufficient, zero dependencies |
| Testing | pytest + Vitest multi-layer | Comprehensive coverage, fast feedback |

---

## Open Questions (To Resolve During Implementation)

1. **LLM Fallback**: If GPT-4 unavailable, automatically fall back to GPT-3.5 or return error?
   - **Recommendation**: Fall back with user warning (degraded quality notice)

2. **Citation Display**: Inline tooltips vs. sidebar panel for sources?
   - **Recommendation**: Tooltips for quick reference, sidebar for full bibliography

3. **Depth Default**: Default recursion depth for "standard" queries?
   - **Recommendation**: Depth=1 for speed, with UI toggle for depth=2

4. **Report Persistence**: Save research reports to disk/database or keep in-memory only?
   - **Recommendation**: In-memory for MVP, add optional SQLite persistence in v1.1

These questions have low implementation risk and can be decided during development.
