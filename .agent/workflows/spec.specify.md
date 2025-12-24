---
description: Create or update the feature specification from a natural language feature description
---

This workflow creates a new feature specification using the GitHub SpecKit methodology. It will:
1. Generate a branch name and feature number
2. Check for existing branches to avoid conflicts
3. Create the spec file with proper structure
4. Validate the spec quality
5. Handle clarifications if needed

## Steps

1. **Provide your feature description** - Describe what you want to build in natural language. Be as detailed as possible about:
   - What users should be able to do
   - Why this feature is needed
   - Any specific constraints or requirements

2. **The workflow will automatically**:
   - Generate a concise short name (2-4 words) for the feature
   - Check for existing branches with similar names
   - Create a new branch with format: `{number}-{short-name}`
   - Create the feature directory in `specs/{number}-{short-name}/`
   - Generate a complete specification document

3. **Specification quality validation**:
   - Creates a quality checklist at `checklists/requirements.md`
   - Validates completeness, clarity, and measurability
   - Identifies any areas needing clarification

4. **Handle clarifications** (if any):
   - If unclear aspects exist, you'll be asked up to 3 targeted questions
   - Each question will have suggested answers with implications
   - Answer format: `Q1: A, Q2: Custom - [details], Q3: B`
   - The spec will be updated with your answers

5. **Completion**:
   - Spec file ready at: `specs/{number}-{short-name}/spec.md`
   - Quality checklist at: `specs/{number}-{short-name}/checklists/requirements.md`
   - Ready for next phase: `/spec.clarify` or `/spec.plan`

## Example Usage

**Simple feature:**
> "I want to add user authentication with email and password"

**Complex feature:**
> "Create a dashboard showing real-time analytics with filtering capabilities, export to CSV, and mobile-responsive design"

## Guidelines

- Focus on **WHAT** users need and **WHY**
- Avoid **HOW** to implement (no tech stack, APIs, code structure)
- Think from a business stakeholder perspective, not a developer
- The spec will be technology-agnostic

## Next Steps

After spec creation:
- If clarifications remain: Run `/spec.clarify`
- If spec is complete: Run `/spec.plan` to create technical design
