---
description: Generate custom domain-specific quality checklists for requirements validation
---

This workflow creates domain-specific checklists to validate the **quality of your requirements**, not to test implementation. Think of it as "unit tests for English."

## Core Concept: Requirements Quality Testing

**What checklists ARE**:
- ✅ "Are visual hierarchy requirements defined for all card types?" [Completeness]
- ✅ "Is 'prominent display' quantified with specific sizing/positioning?" [Clarity]
- ✅ "Are hover state requirements consistent across all interactive elements?" [Consistency]

**What checklists are NOT**:
- ❌ NOT "Verify the button clicks correctly" (that's implementation testing)
- ❌ NOT "Test error handling works" (that's QA testing)
- ❌ NOT "Confirm the API returns 200" (that's integration testing)

## Prerequisites

- Must have `spec.md` (and ideally `plan.md` and `tasks.md`)
- Run this after `/spec.specify` or `/spec.plan`
- Can be run multiple times for different domains

## What This Does

1. **Clarifies your intent** with up to 3-5 contextual questions:
   - Checklist focus area (UX, API, security, performance, etc.)
   - Depth level (lightweight vs. formal gate)
   - Audience (author, reviewer, QA, release team)
   - Risk priorities
   - Scope boundaries

2. **Analyzes your specs** for requirements quality across dimensions:
   - **Completeness**: Are all necessary requirements present?
   - **Clarity**: Are requirements unambiguous and specific?
   - **Consistency**: Do requirements align without conflicts?
   - **Measurability**: Can requirements be objectively verified?
   - **Coverage**: Are all scenarios/edge cases addressed?

3. **Generates checklist** testing requirement quality:
   - Items numbered sequentially (CHK001, CHK002, ...)
   - Grouped by quality dimension
   - Each item references spec sections or marks gaps
   - ≥80% of items include traceability references

4. **Creates checklist file** at:
   ```
   specs/{feature}/checklists/{domain}.md
   ```
   - Descriptive domain name (e.g., `ux.md`, `api.md`, `security.md`)
   - Each run creates a new file (or appends to existing)
   - Multiple checklists supported per feature

## Quality Dimensions Tested

### Requirement Completeness
"Are error handling requirements defined for all API failure modes? [Gap]"

### Requirement Clarity
"Is 'fast loading' quantified with specific timing thresholds? [Clarity, Spec §NFR-2]"

### Requirement Consistency
"Do navigation requirements align across all pages? [Consistency, Spec §FR-10]"

### Acceptance Criteria Quality
"Can 'visual hierarchy' requirements be objectively measured? [Measurability, Spec §FR-1]"

### Scenario Coverage
"Are requirements defined for zero-state scenarios? [Coverage, Edge Case]"

### Edge Case Coverage
"Are requirements specified for partial data loading failures? [Coverage, Gap]"

### Non-Functional Requirements
"Are performance requirements quantified with specific metrics? [Clarity]"

## Example Checklist Types

**UX Requirements (`/spec.checklist` with focus: UX)**
- Visual hierarchy clarity
- Interaction state consistency
- Accessibility requirement completeness
- Responsive design coverage

**API Requirements (`/spec.checklist` with focus: API)**
- Error response format specification
- Rate limiting clarity
- Authentication consistency
- Versioning strategy documentation

**Security Requirements (`/spec.checklist` with focus: Security)**
- Authentication requirement coverage
- Data protection specification
- Threat model traceability
- Compliance alignment

**Performance Requirements (`/spec.checklist` with focus: Performance)**
- Metric quantification
- Target definition for critical journeys
- Load condition specification
- Degradation requirement coverage

## Usage Examples

**General quality check:**
> "Create a checklist to validate my spec quality"

**Domain-specific:**
> "Generate a security checklist"
> "Create an API requirements checklist"
> "I need a UX/accessibility checklist"

**With parameters:**
> "Create a formal release gate checklist for the security team focusing on data protection and compliance"

## Output

After generation:
- Path to checklist file
- Item count and categories
- Focus areas covered
- Depth level and audience
- Traceability percentage

## Next Steps

After checklist creation:
- Review each item against your spec
- Check boxes for items that pass
- Update spec to address failing items
- Run `/spec.implement` only after checklists pass
- Use checklists during PR reviews

## Important Notes

- Each `/spec.checklist` run creates a new file (use different domains)
- Checklists test REQUIREMENTS quality, not implementation
- Items should be answerable by reading the spec alone
- Focus on gaps, ambiguities, and inconsistencies in what's written
- Minimum 80% traceability to spec sections required
