# Data Model: Intelligent Research Agent

**Feature**: 001-intelligent-research-agent  
**Date**: 2025-12-24  
**Spec Reference**: [spec.md](./spec.md) - Key Entities section

---

## Overview

This document defines the data entities for the agentic research workflow. All entities are initially implemented as Pydantic models (in-memory) with optional persistence layer for future iterations.

---

## Core Entities

### 1. ResearchRequest

**Purpose**: Represents a user's research query with configuration

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `id` | UUID | Yes | Unique identifier | Auto-generated |
| `query` | str | Yes | User's natural language question | 10-500 characters |
| `depth_level` | enum | No | Research depth: quick/standard/comprehensive | Default: standard |
| `user_id` | str | No | User identifier (for multi-user systems) | Optional for MVP |
| `created_at` | datetime | Yes | Request timestamp | Auto-generated |
| `status` | enum | Yes | planning/executing/verifying/synthesizing/completed/failed | Default: planning |
| `completion_time_seconds` | float | No | Total execution time | Set on completion |

**Enums**:
```python
class DepthLevel(str, Enum):
    QUICK = "quick"           # 3-5 sub-questions, depth=1, ~1 min
    STANDARD = "standard"     # 5-7 sub-questions, depth=1, ~3 min
    COMPREHENSIVE = "comprehensive"  # 7-10 sub-questions, depth=2, ~5 min

class ResearchStatus(str, Enum):
    PLANNING = "planning"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    FAILED = "failed"
```

**Relationships**:
- One `ResearchRequest` has one `ResearchPlan`
- One `ResearchRequest` has one `NarrativeReport` (when completed)

**State Transitions**:
```
planning → executing → verifying → synthesizing → completed
   ↓           ↓           ↓            ↓
failed      failed      failed       failed
```

---

### 2. ResearchPlan

**Purpose**: The output of the Planning stage - structured breakdown of research topics

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `id` | UUID | Yes | Unique identifier | Auto-generated |
| `request_id` | UUID | Yes | Parent research request | Foreign key |
| `sub_questions` | List[SubQuestion] | Yes | Generated research questions | 3-10 items |
| `created_at` | datetime | Yes | Plan creation timestamp | Auto-generated |
| `estimated_time_seconds` | int | No | Estimated completion time | Calculated |

**Example**:
```json
{
  "id": "plan-uuid-123",
  "request_id": "req-uuid-456",
  "sub_questions": [
    {
      "id": "sq-uuid-1",
      "text": "What is Elon Musk's current net worth vs last year?",
      "priority": 1,
      "parent_question_id": null
    },
    {
      "id": "sq-uuid-2",
      "text": "What are the major controversies involving Elon Musk in 2023?",
      "priority": 2,
      "parent_question_id": null
    }
  ]
}
```

---

### 3. SubQuestion

**Purpose**: A single research question within a plan (supports recursion)

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `id` | UUID | Yes | Unique identifier | Auto-generated |
| `plan_id` | UUID | Yes | Parent research plan | Foreign key |
| `text` | str | Yes | The actual question | 10-200 characters |
| `priority` | int | Yes | Execution order | 1-10 (1=highest) |
| `parent_question_id` | UUID | No | For recursive questions | Self-referencing |
| `depth` | int | Yes | Recursion depth (0=root) | 0-3 |
| `status` | enum | Yes | pending/searching/completed/failed | Default: pending |
| `search_results` | List[SearchResult] | Yes | Results for this question | 0-10 items |

**Recursive Structure**:
```
SubQuestion (depth=0): "Research Tesla's Q4 performance"
  └─ SubQuestion (depth=1): "Investigate Tesla recall mentioned in Q4 report"
      └─ SubQuestion (depth=2): "Details on battery defect from recall"
```

---

### 4. SearchResult

**Purpose**: Raw data from a single search result (webpage, Wikipedia, etc.)

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `id` | UUID | Yes | Unique identifier | Auto-generated |
| `sub_question_id` | UUID | Yes | Which question this answers | Foreign key |
| `url` | str | Yes | Source URL | Valid URL format |
| `title` | str | Yes | Page/article title | 1-200 characters |
| `content` | str | Yes | Extracted text content | Max 10,000 characters |
| `domain` | str | Yes | Source domain | e.g., "bloomberg.com" |
| `access_timestamp` | datetime | Yes | When we fetched this | Auto-generated |
| `credibility_score` | float | No | 0.0-1.0 source reliability | Domain-based heuristic |
| `extracted_facts` | List[UUID] | Yes | Facts extracted from this | References to Fact.id |

**Credibility Scoring**:
```python
# Heuristic based on domain reputation
CREDIBILITY_MAP = {
    "bloomberg.com": 0.95,
    "wsj.com": 0.95,
    "reuters.com": 0.93,
    "wikipedia.org": 0.85,
    "forbes.com": 0.80,
    # ... configurable
}
```

---

### 5. Fact (Claim)

**Purpose**: A single piece of information extracted from a search result

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `id` | UUID | Yes | Unique identifier | Auto-generated |
| `text` | str | Yes | The actual claim | 10-500 characters |
| `source_url` | str | Yes | Where this came from | Valid URL |
| `source_id` | UUID | Yes | SearchResult reference | Foreign key |
| `confidence` | float | Yes | 0.0-1.0 extraction confidence | LLM-provided score |
| `section` | str | No | Report section (Financials/Legal/etc.) | Optional categorization |
| `extraction_timestamp` | datetime | Yes | When extracted | Auto-generated |
| `verified` | bool | Yes | Cross-referenced with other sources | Default: false |
| `discrepancy_id` | UUID | No | If conflicts with another fact | References Discrepancy.id |

**Example**:
```json
{
  "id": "fact-uuid-789",
  "text": "Elon Musk's net worth was estimated at $180B in December 2023",
  "source_url": "https://bloomberg.com/...",
  "source_id": "search-result-uuid-101",
  "confidence": 0.92,
  "section": "Financials",
  "verified": true,
  "discrepancy_id": null
}
```

---

### 6. Discrepancy

**Purpose**: Tracks conflicting facts from different sources

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `id` | UUID | Yes | Unique identifier | Auto-generated |
| `fact_ids` | List[UUID] | Yes | All conflicting facts | 2+ items |
| `topic` | str | Yes | What the conflict is about | e.g., "Net worth estimate" |
| `resolution` | str | No | How to resolve (recency/credibility/both) | LLM-generated |
| `resolution_confidence` | float | No | 0.0-1.0 confidence in resolution | LLM-provided |
| `created_at` | datetime | Yes | When discrepancy detected | Auto-generated |

**Example**:
```json
{
  "id": "disc-uuid-202",
  "fact_ids": ["fact-uuid-789", "fact-uuid-790"],
  "topic": "Elon Musk net worth December 2023",
  "resolution": "Bloomberg source ($180B) is more recent (Dec 20) than Wikipedia ($200B, updated Nov 15). Prefer Bloomberg.",
  "resolution_confidence": 0.88,
  "created_at": "2025-12-24T11:56:00Z"
}
```

**Resolution Strategies**:
- **Recency**: Prefer newer source
- **Credibility**: Prefer higher credibility score
- **Consensus**: If 3+ sources agree on value A and 1 source says B, prefer A
- **Uncertainty**: If irresolvable, present both with context

---

### 7. NarrativeReport

**Purpose**: The final synthesized research output

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `id` | UUID | Yes | Unique identifier | Auto-generated |
| `request_id` | UUID | Yes | Parent research request | Foreign key |
| `executive_summary` | str | Yes | 1-minute read overview | 200-500 words |
| `sections` | List[ReportSection] | Yes | Detailed sections (Financials/Legal/etc.) | 1-10 sections |
| `total_word_count` | int | Yes | Full report word count | Min 300 words/section |
| `total_sources` | int | Yes | Unique sources cited | Min 3/section target |
| `generated_at` | datetime | Yes | Report creation timestamp | Auto-generated |
| `quality_score` | float | No | 0.0-1.0 quality metric | Based on word count, sources, verification rate |

---

### 8. ReportSection

**Purpose**: A single thematic section of the narrative report

**Fields**:
| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|-----------|
| `id` | UUID | Yes | Unique identifier | Auto-generated |
| `report_id` | UUID | Yes | Parent report | Foreign key |
| `title` | str | Yes | Section name | e.g., "Financial Overview" |
| `content` | str | Yes | Narrative text with inline citation markers | Min 300 words |
| `fact_ids` | List[UUID] | Yes | Facts used in this section | References Fact.id |
| `order` | int | Yes | Display order | 1-10 |

**Content Format** (Markdown with citation markers):
```markdown
Elon Musk's net worth was estimated at $180B in December 2023 [cite:fact-uuid-789], 
a decrease from $200B earlier in the year [cite:fact-uuid-790]. This decline was 
primarily attributed to Tesla's stock performance [cite:fact-uuid-791].
```

Frontend will parse `[cite:uuid]` markers and replace with clickable citation components.

---

## Supporting Entities

### 9. CitationLink

**Purpose**: Bidirectional mapping between facts and sources (for O(1) lookups)

**Fields**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `fact_id` | UUID | Yes | The claim |
| `source_url` | str | Yes | The source |
| `source_title` | str | Yes | For display in tooltips |
| `access_timestamp` | datetime | Yes | When source was accessed |

**Indexes** (for fast lookup):
```python
# In-memory dictionaries
citations_by_fact: Dict[UUID, List[CitationLink]]
citations_by_source: Dict[str, List[CitationLink]]
```

---

## Database Schema (Optional Future Persistence)

If moving from in-memory to SQLite/PostgreSQL:

```sql
-- Core tables
CREATE TABLE research_requests (...);
CREATE TABLE research_plans (...);
CREATE TABLE sub_questions (...);
CREATE TABLE search_results (...);
CREATE TABLE facts (...);
CREATE TABLE discrepancies (...);
CREATE TABLE narrative_reports (...);
CREATE TABLE report_sections (...);

-- Junction tables
CREATE TABLE fact_discrepancies (
    fact_id UUID REFERENCES facts(id),
    discrepancy_id UUID REFERENCES discrepancies(id),
    PRIMARY KEY (fact_id, discrepancy_id)
);

CREATE TABLE section_facts (
    section_id UUID REFERENCES report_sections(id),
    fact_id UUID REFERENCES facts(id),
    citation_order INT,
    PRIMARY KEY (section_id, fact_id)
);

-- Indexes for performance
CREATE INDEX idx_facts_source ON facts(source_url);
CREATE INDEX idx_sub_questions_parent ON sub_questions(parent_question_id);
CREATE INDEX idx_search_results_domain ON search_results(domain);
```

---

## Validation Rules

### ResearchRequest
- `query` must not be empty or only whitespace
- `depth_level` must be one of: quick, standard, comprehensive

### ResearchPlan
- Must have 3-10 `sub_questions` based on depth level
- All sub-questions must have unique priorities

### SubQuestion
- `depth` must not exceed MAX_DEPTH (default: 3)
- `parent_question_id` must reference existing SubQuestion if not null
- Circular references not allowed (detect during insertion)

### Fact
- `confidence` must be between 0.0 and 1.0
- `source_url` must be valid URL format
- `text` must not be empty

### NarrativeReport
- Each section must have minimum 300 words
- Must cite at least 3 unique sources per section
- Total word count must be calculated from all sections

---

## Example Complete Data Flow

```
User Query: "Research Elon Musk"

1. ResearchRequest created:
   - id: req-001
   - query: "Research Elon Musk"
   - depth_level: standard
   - status: planning

2. ResearchPlan generated:
   - id: plan-001
   - sub_questions: [
       {id: sq-001, text: "What is his net worth?", priority: 1, depth: 0},
       {id: sq-002, text: "Major controversies?", priority: 2, depth: 0}
     ]

3. SubQuestion sq-001 executed:
   - SearchResult: {id: sr-001, url: "bloomberg.com/...", content: "..."}
   - Fact extracted: {id: fact-001, text: "Net worth $180B", source_id: sr-001}
   - Recursive SubQuestion: {id: sq-003, text: "Why did net worth decrease?", parent_id: sq-001, depth: 1}

4. Verification stage:
   - Discrepancy found: {id: disc-001, fact_ids: [fact-001, fact-002], resolution: "Prefer Bloomberg (more recent)"}

5. NarrativeReport synthesized:
   - id: report-001
   - executive_summary: "Elon Musk, CEO of Tesla and SpaceX..."
   - sections: [
       {title: "Financial Overview", content: "...[cite:fact-001]...", fact_ids: [fact-001, fact-002]}
     ]
```

---

## Implementation Notes

**Pydantic Models** (backend/models.py):
```python
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from enum import Enum
from typing import List, Optional

class ResearchRequest(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    query: str = Field(min_length=10, max_length=500)
    depth_level: DepthLevel = DepthLevel.STANDARD
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: ResearchStatus = ResearchStatus.PLANNING
    # ... other fields

class ResearchPlan(BaseModel):
    # ... fields

# ... other models
```

**Migration Path**:
1. MVP: Pure Pydantic in-memory
2. v1.1: Add SQLAlchemy ORM models alongside Pydantic
3. v1.2: Implement repository pattern for swappable persistence
