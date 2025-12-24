# Comprehensive Review & Redesign Proposal

## Executive Summary

The current "Configurable Researcher Agent" suffers from a lack of depth in both its AI reasoning capabilities and its User Interface. It functions as a shallow search wrapper rather than a true intelligent agent. This review outlines the necessary steps to transform the service into a high-value tool suitable for High Net Worth Individuals (HNWIs) and professional use.

---

## 1. AI Expert Review: The Intelligence Flow

### Critique of Current Architecture
*   **Linear & Shallow:** The current flow (`Search -> Extract JSON`) is too simple. It accepts the first 5 search results as truth without verification.
*   **No Reasoning:** The agent does not "think" about what it needs to find. It just dumps a generic query into a search engine.
*   **Hallucination Risk:** Without cross-referencing, the agent blindly trusts scraping results.
*   **Output Quality:** The "One Line Insight" is unacceptable. It reduces complex topics (Sentiment, Finance) to meaningless numbers (e.g., "6/10 sentiment").

### Proposed "Agentic" Workflow
To create a true Researcher Agent, we must move to a **Plan-Execute-Verify-Synthesize** model:

1.  **Planner (The Brain):**
    *   *Input:* User request (e.g., "Research Elon Musk").
    *   *Action:* Deconstruct into sub-questions.
        *   "What is his current net worth vs last year?"
        *   "What are the major controversies?"
        *   "What is the market sentiment for his companies?"
    *   *Output:* A research plan.

2.  **Deep Researcher (The Worker):**
    *   Executes searches for *each* sub-question.
    *   **Recursive Search:** If a search result mentions a "new lawsuit," the agent triggers a *new* search specifically for that lawsuit.

3.  **Verifier (The Judge):**
    *   Cross-references data points.
    *   *Rule:* If Wikipedia says Net Worth is $200B and a recent News Article says $180B, the agent notes the discrepancy and cites the recency of the news.

4.  **Synthesizer (The Author):**
    *   Instead of filling a JSON schema, the LLM writes a **Narrative Report**.
    *   *Output:* A "Wall Street Journal" style briefing.

---

## 2. UI/UX Expert Review: The User Experience

### Critique of Current Interface
*   **"Admin Panel" Aesthetic:** The current card grid looks like a debugger or a developer tool, not a consumer product.
*   **Low Information Density:** HNWIs are used to Bloomberg Terminals or Private Banking dashboards. They want density, hierarchy, and clarity.
*   **Arbitrary Metrics:** "Sentiment: 6/10" is useless. "Market Confidence: Volatile (Negative Trend)" is useful.
*   **Lack of Trust:** No source links or citations makes the data unverifiable.

### Proposed "Executive Intelligence Dashboard"
The new UI should feel like a high-end briefing document.

1.  **Visual Language:**
    *   **Typography:** Serif headings (Merriweather/Playfair) for authority; clean Sans-Serif (Inter/Roboto) for data.
    *   **Color:** Deep Navy, Slate, and Gold/muted accents. Dark mode by default or high-contrast light mode.

2.  **Key Components:**
    *   **The Executive Brief:** A top-level summary written in natural language. This is the "1 minute read".
    *   **Key Insights Rail:** A sidebar highlighting critical stats (Net Worth, Risk Score) but backed by context.
    *   **Deep Dive Tabs:** Instead of scrolling cards, use tabs for "Financials", "Legal", "Reputation".
    *   **Source Truth:** Every claim in the text should be clickable to see the source URL.

---

## 3. Functional Requirements & Deliverables

### Backend Deliverables
1.  **Multi-Step Agent Loop:** Refactor `BaseResearcher` to support planning and synthesis.
2.  **Narrative Generation:** Switch LLM prompts to produce Markdown reports, not just JSON.
3.  **Citation System:** logic to track which URL provided which fact.

### Frontend Deliverables
1.  **`ExecutiveSummary` Component:** Renders Markdown with citation tooltips.
2.  **`SourceList` Component:** A transparent bibliography.
3.  **`Dashboard` Layout:** Replaces the generic grid.

### Success Metrics
*   **Depth:** Reports must be at least 300 words of narrative text per module, not 1 sentence.
*   **Accuracy:** Users must be able to click a source to verify a claim.
*   **Perception:** UI must score high on "Trustworthiness" and "Professionalism".
