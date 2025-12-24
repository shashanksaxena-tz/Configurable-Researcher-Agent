---
description: Identify underspecified areas in the spec and encode clarification answers
---

This workflow helps identify and resolve ambiguities in your feature specification before planning. It asks targeted questions to reduce downstream rework risk.

## Prerequisites

- Must have an active feature spec (`spec.md`) created via `/spec.specify`
- Should be run BEFORE `/spec.plan`

## What This Does

1. **Analyzes your spec** for ambiguities across multiple dimensions:
   - Functional scope & behavior
   - Domain & data model
   - Interaction & UX flow
   - Non-functional quality attributes
   - Integration & external dependencies
   - Edge cases & failure handling
   - Constraints & tradeoffs

2. **Asks up to 5 targeted questions** (maximum) that materially impact:
   - Architecture decisions
   - Data modeling
   - Task decomposition
   - Test design
   - UX behavior
   - Operational readiness
   - Compliance validation

3. **Each question includes**:
   - **Recommended answer** based on best practices
   - Multiple choice options (or short answer format)
   - Clear implications for each option
   - Answer with option letter, "yes"/"recommended", or custom short answer

4. **Updates the spec incrementally**:
   - Adds a `Clarifications` section with Q&A log
   - Updates relevant sections with clarified requirements
   - Removes ambiguous placeholders
   - Ensures consistency across the spec

## Expected Flow

1. The agent loads your spec and analyzes coverage
2. Questions are asked **ONE AT A TIME** (not all at once)
3. For multiple choice questions, you can:
   - Select an option letter (e.g., "A")
   - Accept the recommendation ("yes" or "recommended")
   - Provide your own short answer
4. After each answer, the spec is immediately updated
5. Process stops when:
   - All critical ambiguities resolved
   - You signal completion ("done", "no more")
   - 5 questions have been asked

## Answer Format

**Multiple choice:**
> Q1: B

**Accept recommendation:**
> yes

**Custom short answer:**
> Custom - real-time pub/sub

**Multiple questions at once:**
> Q1: A, Q2: recommended, Q3: Custom - 100ms latency

## Completion Report

After clarification, you'll receive:
- Number of questions asked & answered
- Path to updated spec
- Sections that were modified
- Coverage summary by taxonomy category
- Recommendation on whether to proceed to planning

## Next Steps

- If all clarifications resolved: Run `/spec.plan`
- If more clarifications needed: Run `/spec.clarify` again
- To review changes: Check the updated `spec.md`
