# Quickstart Guide: Intelligent Research Agent

**Feature**: 001-intelligent-research-agent  
**Branch**: `001-intelligent-research-agent`  
**Last Updated**: 2025-12-24

---

## Overview

This guide helps developers set up, test, and integrate the Intelligent Research Agent feature. It covers:

1. Development environment setup
2. Running the agentic workflow
3. Testing scenarios
4. Integration examples
5. Debugging tips

---

## Prerequisites

**Required**:
- Python 3.11+
- Node.js 18+ and npm
- Git
- API keys for LLM providers (OpenAI and/or Google Gemini)

**Optional**:
- Docker (for containerized setup)
- VS Code or similar IDE

---

## Development Setup

### 1. Clone and Checkout Feature Branch

```bash
git clone https://github.com/yourusername/Configurable-Researcher-Agent.git
cd Configurable-Researcher-Agent
git checkout 001-intelligent-research-agent
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# Required variables:
#   OPENAI_API_KEY=your-openai-key
#   GOOGLE_API_KEY=your-google-key (optional)
#   LLM_PROVIDER=openai  # or 'google' or 'both'
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Add Vitest for testing (new dependency)
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### 4. Start Backend Server

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.  
API docs (Swagger UI): `http://localhost:8000/docs`

---

## Quick Test: End-to-End Research Flow

### Using the API Directly

```bash
# 1. Generate a research plan
curl -X POST http://localhost:8000/api/research/plan \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Research Tesla Q4 2023 performance",
    "depth_level": "quick"
  }'

# Response example:
# {
#   "id": "plan-uuid-123",
#   "sub_questions": [
#     {"text": "What was Tesla's Q4 2023 revenue?", "priority": 1},
#     {"text": "How did stock price change?", "priority": 2}
#   ],
#   "estimated_time_seconds": 60
# }

# 2. Execute research (async mode)
curl -X POST http://localhost:8000/api/research/execute \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Research Tesla Q4 2023 performance",
    "depth_level": "quick",
    "async": true
  }'

# Response:
# {
#   "request_id": "req-uuid-456",
#   "status": "planning",
#   "estimated_completion_seconds": 60
# }

# 3. Poll for status
curl http://localhost:8000/api/research/req-uuid-456/status

# 4. Get completed report
curl http://localhost:8000/api/research/req-uuid-456/report

# 5. Get all citations
curl http://localhost:8000/api/research/req-uuid-456/citations
```

### Using the Frontend

1. Navigate to `http://localhost:5173`
2. Enter query: "Research Tesla Q4 2023 performance"
3. Select depth level: "Quick"
4. Click "Start Research"
5. Watch progress indicator (will show: Planning → Executing → Verifying → Synthesizing)
6. View the Executive Brief summary
7. Click through tabs: Financials, Legal, Reputation
8. Hover over inline citations to see source tooltips
9. Click "View All Sources" to see bibliography

---

## Testing Scenarios

### Unit Tests (Backend)

```bash
cd backend
pytest tests/unit/ -v

# Run specific module tests
pytest tests/unit/test_planner.py -v
pytest tests/unit/test_deep_researcher.py -v
pytest tests/unit/test_verifier.py -v
pytest tests/unit/test_synthesizer.py -v

# Run with coverage
pytest tests/unit/ --cov=modules --cov-report=html
```

**Key test scenarios**:
- `test_planner.py`: Query deconstruction into 3-10 sub-questions
- `test_deep_researcher.py`: Recursive search triggering, depth limiting
- `test_verifier.py`: Discrepancy detection, source cross-referencing
- `test_synthesizer.py`: Narrative generation, citation embedding

### Integration Tests (Backend)

```bash
cd backend
pytest tests/integration/ -v -s

# This will test the full workflow:
# 1. User query → Research plan
# 2. Plan → Execute searches (may take 1-3 minutes)
# 3. Cross-reference and verify
# 4. Synthesize narrative report
# 5. Validate output quality (word count, citations)
```

### Component Tests (Frontend)

```bash
cd frontend
npm run test

# Run specific component tests
npm run test -- ExecutiveBrief.test.jsx
npm run test -- CitationTooltip.test.jsx
npm run test -- ResearchTabs.test.jsx

# Run with coverage
npm run test -- --coverage
```

**Key component scenarios**:
- **ExecutiveBrief**: Renders summary, expands/collapses
- **CitationTooltip**: Shows source on hover, links to full source
- **ResearchTabs**: Switches between sections, maintains state
- **SourceList**: Displays bibliography, filters by domain

### Manual Testing Checklist

Use these scenarios to validate the feature:

#### Scenario 1: Basic Research Flow (Happy Path)
1. Query: "Research Apple Inc financial performance"
2. Expected: 5-7 sub-questions generated
3. Expected: Report completed in <3 minutes
4. Expected: Executive summary 200-500 words
5. Expected: At least 3 sections (Financials, Market, etc.)
6. Expected: Minimum 300 words per section
7. Expected: At least 3 unique sources per section
8. Expected: All claims have clickable citations

#### Scenario 2: Recursive Search Trigger
1. Query: "Research Tesla recall in Q4 2023"
2. Expected: Initial sub-questions about the recall
3. Expected: If search mentions "battery defect", system triggers recursive search for "Tesla battery defect details"
4. Expected: Depth=1 sub-questions generated from depth=0 results
5. Validate: Check report cites both original article AND follow-up sources

#### Scenario 3: Discrepancy Handling
1. Query: "Research Elon Musk net worth 2023"
2. Expected: Multiple sources with different values (e.g., $180B vs $200B)
3. Expected: Discrepancy detected in verification stage
4. Validate: Report notes the conflict with explanation: "Sources disagree: Bloomberg ($180B, Dec 20) vs Wikipedia ($200B, Nov 15). Preferring Bloomberg due to recency."
5. Validate: Hover over conflicting claims shows discrepancy note

#### Scenario 4: Premium UI Validation
1. Load any completed report
2. Validate Typography:
   - Headings use Playfair Display (serif)
   - Body text uses Inter (sans-serif)
3. Validate Color Scheme:
   - Background is navy-900 (#0f1729)
   - Accent colors are gold-400/500
4. Validate Dark Mode:
   - Toggle light/dark mode
   - Contrast ratio >4.5:1 (use browser DevTools accessibility checker)
5. Validate Information Density:
   - Can see Executive Brief + Key Insights without scrolling
   - Tabs clearly visible for navigation

#### Scenario 5: Citation Interaction
1. Find a claim with inline citation marker (e.g., "Revenue was $25B [cite]")
2. Hover over marker
3. Expected: Tooltip shows source title, domain, access date
4. Click citation
5. Expected: Opens full source view or bibliography panel
6. Expected: Shows all claims from that source

#### Scenario 6: Error Handling
1. Query: "" (empty)
2. Expected: Validation error "Query must be 10-500 characters"
3. Query: "Research XYZ123" (nonsense topic with no search results)
4. Expected: Graceful handling, report states "Limited information available"
5. Simulate LLM API failure (disable API key)
6. Expected: User-friendly error message, not stack trace

---

## Integration Examples

### Example 1: Embedding Research Agent in Another App

```python
# your_app.py
import httpx
import asyncio

async def get_research_report(query: str) -> dict:
    """
    Integrate research agent into your application
    """
    async with httpx.AsyncClient() as client:
        # Start research
        response = await client.post(
            "http://localhost:8000/api/research/execute",
            json={"query": query, "async": True}
        )
        request_id = response.json()["request_id"]
        
        # Poll for completion
        while True:
            status_response = await client.get(
                f"http://localhost:8000/api/research/{request_id}/status"
            )
            status_data = status_response.json()
            
            if status_data["status"] == "completed":
                break
            elif status_data["status"] == "failed":
                raise Exception(status_data["error"])
            
            await asyncio.sleep(5)  # Poll every 5 seconds
        
        # Get final report
        report_response = await client.get(
            f"http://localhost:8000/api/research/{request_id}/report"
        )
        return report_response.json()

# Usage
report = asyncio.run(get_research_report("Research blockchain technology"))
print(report["executive_summary"])
```

### Example 2: Custom Frontend Component

```jsx
// CustomResearchWidget.jsx
import { useState } from 'react';
import axios from 'axios';

function CustomResearchWidget() {
  const [query, setQuery] = useState('');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleResearch = async () => {
    setLoading(true);
    try {
      // Start research
      const { data } = await axios.post('/api/research/execute', {
        query,
        async: true
      });
      
      const requestId = data.request_id;
      
      // Poll for completion
      const pollInterval = setInterval(async () => {
        const statusRes = await axios.get(`/api/research/${requestId}/status`);
        
        if (statusRes.data.status === 'completed') {
          clearInterval(pollInterval);
          
          // Fetch report
          const reportRes = await axios.get(`/api/research/${requestId}/report`);
          setReport(reportRes.data);
          setLoading(false);
        }
      }, 5000);  // Poll every 5 seconds
      
    } catch (error) {
      console.error('Research failed:', error);
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        value={query} 
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter research query..."
      />
      <button onClick={handleResearch} disabled={loading}>
        {loading ? 'Researching...' : 'Start Research'}
      </button>
      
      {report && (
        <div>
          <h2>Executive Summary</h2>
          <p>{report.executive_summary}</p>
          
          {report.sections.map(section => (
            <div key={section.id}>
              <h3>{section.title}</h3>
              <div dangerouslySetInnerHTML={{ __html: section.content }} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## Debugging Tips

### Backend Issues

**Problem**: Research takes longer than 3 minutes  
**Debug**:
```python
# Add logging to track stage durations
import logging
logger = logging.getLogger(__name__)

# In each module (planner, researcher, etc.)
start_time = time.time()
# ... do work
logger.info(f"[{stage_name}] Duration: {time.time() - start_time:.2f}s")
```

**Problem**: LLM returns malformed JSON  
**Debug**:
```python
# Enable verbose LLM logging in config.py
LLM_VERBOSE = True  # Logs all prompts and responses

# Add retry logic with exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call_llm(prompt: str) -> dict:
    # ... LLM call
```

**Problem**: Search results not triggering recursive search  
**Debug**:
```bash
# Check the LLM's extraction output
grep "Extracted topics" backend_log.txt

# Verify relevance scoring threshold
# In deep_researcher.py, lower threshold temporarily:
if relevance_score > 0.4:  # Was 0.6, now 0.4 for debugging
```

### Frontend Issues

**Problem**: Citations not rendering  
**Debug**:
```javascript
// In browser console
console.log('[cite:uuid]' regex matches)

const content = "...[cite:550e8400-e29b-41d4-a716-446655440000]...";
const matches = content.matchAll(/\[cite:([a-f0-9-]+)\]/g);
console.log([...matches]);  // Should find UUIDs
```

**Problem**: Dark mode colors not applying  
**Debug**:
```javascript
// Check CSS custom properties in DevTools
getComputedStyle(document.documentElement).getPropertyValue('--navy-900');

// Verify theme context
const themeContext = useContext(ThemeContext);
console.log('Dark mode enabled:', themeContext.darkMode);
```

**Problem**: Tabs not switching  
**Debug**:
```jsx
// Add console logs to ResearchTabs.jsx
const handleTabClick = (tabId) => {
  console.log('Tab clicked:', tabId);
  console.log('Current active:', activeTab);
  setActiveTab(tabId);
};
```

### Performance Profiling

**Backend** (using cProfile):
```bash
python -m cProfile -o profile.stats main.py
python -m pstats profile.stats
> sort cumulative
> stats 20  # Show top 20 slowest functions
```

**Frontend** (using React DevTools Profiler):
1. Install React DevTools browser extension
2. Open DevTools → Profiler tab
3. Click "Record"
4. Interact with research report
5. Stop recording
6. Analyze which components render most frequently

---

## Environment Variables Reference

### Backend (.env)

```bash
# LLM Provider Configuration
LLM_PROVIDER=openai              # 'openai', 'google', or 'both'
OPENAI_API_KEY=sk-...            # Required if LLM_PROVIDER includes 'openai'
GOOGLE_API_KEY=AIza...           # Required if LLM_PROVIDER includes 'google'

# Model Selection
PLANNING_MODEL=gpt-4             # Model for query deconstruction
EXTRACTION_MODEL=gpt-3.5-turbo   # Model for information extraction
VERIFICATION_MODEL=gpt-4         # Model for cross-referencing
SYNTHESIS_MODEL=gpt-4            # Model for narrative generation

# Research Configuration
MAX_RECURSION_DEPTH=2            # Maximum depth for followup searches
DEFAULT_DEPTH_LEVEL=standard     # 'quick', 'standard', or 'comprehensive'
SEARCH_TIMEOUT_SECONDS=30        # Timeout per search request
MAX_SEARCH_RESULTS_PER_QUERY=5   # Number of results to process

# Performance
MAX_CONCURRENT_SEARCHES=3        # Parallel searches (balance speed vs rate limits)
LLM_RATE_LIMIT_RPM=60           # Requests per minute for LLM API

# Logging
LOG_LEVEL=INFO                   # DEBUG, INFO, WARNING, ERROR
LOG_TO_FILE=true                 # Log to backend_log.txt
```

### Frontend (.env or vite.config.js)

```javascript
// vite.config.js
export default {
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
}
```

---

## Next Steps

After completing local testing:

1. **Run `/spec.tasks`** to generate implementation task breakdown
2. **Review task priorities** and assign to team members
3. **Set up CI/CD pipeline** for automated testing
4. **Deploy to staging environment** for stakeholder review
5. **Collect feedback** and iterate

---

## Support

For questions or issues:
- Check the [spec.md](./spec.md) for requirements clarification
- Review [data-model.md](./data-model.md) for entity definitions
- Consult [research.md](./research.md) for technology decisions
- Open an issue on the GitHub repository

**Happy researching!** 🎯
