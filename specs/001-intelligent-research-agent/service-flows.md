# Service Flow Diagrams

## Individual Service Flows

### Planner Service Flow

```mermaid
flowchart TD
    Start([create_plan]) --> ValidateInput{Validate Input}
    ValidateInput -->|Invalid| Error400[Return 400]
    ValidateInput -->|Valid| GetConfig[Get Depth Config]
    GetConfig --> BuildPrompt[Build System Prompt]
    BuildPrompt --> CallLLM[LLM: complete_json]
    
    CallLLM -->|Success| ParseResponse[Parse JSON Response]
    CallLLM -->|Failure| RaiseError[Raise PlanningError]
    
    ParseResponse --> ValidateCount{questions >= min?}
    ValidateCount -->|No| RaiseError
    ValidateCount -->|Yes| CreateSubQuestions[Create SubQuestion objects]
    
    CreateSubQuestions --> BuildPlan[Build ResearchPlan]
    BuildPlan --> LogSuccess[Log plan_created]
    LogSuccess --> Return([Return Plan])
```

### DeepResearcher Service Flow

```mermaid
flowchart TD
    Start([execute_research]) --> SetDepth[Set max_depth from level]
    SetDepth --> SortQuestions[Sort by priority]
    SortQuestions --> LoopQ{For each question}
    
    LoopQ --> SetInProgress[status = IN_PROGRESS]
    SetInProgress --> CheckDepth{depth > max?}
    CheckDepth -->|Yes| SkipQ[Skip - depth exceeded]
    CheckDepth -->|No| CheckVisited{Topic visited?}
    
    CheckVisited -->|Yes| SkipQ
    CheckVisited -->|No| AddVisited[Add to visited]
    AddVisited --> Search[search_all_providers]
    
    Search -->|No results| LogWarn[Log no_search_results]
    Search -->|Results| LoopR{For each result}
    
    LoopR --> Extract[LLM: extract_facts]
    Extract -->|Success| CreateFinding[Create ResearchFinding]
    Extract -->|Failure| LogError[Log extraction_failed]
    
    CreateFinding --> CheckRecurse{triggers_recursion?}
    CheckRecurse -->|Yes| Recurse[Handle recursion]
    CheckRecurse -->|No| NextResult
    
    Recurse --> NextResult{More results?}
    NextResult -->|Yes| LoopR
    NextResult -->|No| SetComplete[status = COMPLETED]
    
    LogWarn --> SetComplete
    SkipQ --> NextQ{More questions?}
    SetComplete --> NextQ
    NextQ -->|Yes| LoopQ
    NextQ -->|No| Return([Return findings])
```

### Verifier Service Flow

```mermaid
flowchart TD
    Start([verify_findings]) --> GroupByTopic[Group findings by question_id]
    GroupByTopic --> LoopG{For each group}
    
    LoopG --> CheckSources{Multiple sources?}
    CheckSources -->|No| CreateSingleFact[Create low-confidence fact]
    CheckSources -->|Yes| CrossRef[LLM: cross-reference claims]
    
    CrossRef -->|Consistent| CreateVerifiedFact[Create VerifiedFact]
    CrossRef -->|Conflict| CreateDiscrepancy[Create Discrepancy]
    
    CreateSingleFact --> Next{More groups?}
    CreateVerifiedFact --> Next
    CreateDiscrepancy --> Next
    
    Next -->|Yes| LoopG
    Next -->|No| Return([Return facts, discrepancies])
```

### Synthesizer Service Flow

```mermaid
flowchart TD
    Start([generate_report]) --> Categorize[Categorize facts by topic]
    Categorize --> GenerateSummary[LLM: executive summary]
    
    GenerateSummary --> LoopS{For each section}
    LoopS --> GenerateSection[LLM: section content]
    GenerateSection --> ValidateWords{words >= 300?}
    
    ValidateWords -->|No| Expand[Expand section]
    ValidateWords -->|Yes| AddSection[Add to report]
    
    Expand --> ValidateWords
    AddSection --> NextS{More sections?}
    NextS -->|Yes| LoopS
    NextS -->|No| BuildReport[Build NarrativeReport]
    
    BuildReport --> Return([Return report])
```

---

## Orchestrator Coordination

```mermaid
stateDiagram-v2
    [*] --> PENDING: Request received
    PENDING --> PLANNING: Start workflow
    
    PLANNING --> EXECUTING: Plan created
    PLANNING --> FAILED: Planning error
    
    EXECUTING --> VERIFYING: Findings collected
    EXECUTING --> FAILED: Research error
    
    VERIFYING --> SYNTHESIZING: Facts verified
    VERIFYING --> FAILED: Verification error
    
    SYNTHESIZING --> COMPLETED: Report generated
    SYNTHESIZING --> FAILED: Synthesis error
    
    COMPLETED --> [*]
    FAILED --> [*]
```

---

## LLM Client Flow

```mermaid
flowchart TD
    Start([complete_json]) --> SelectModel[Select model for task type]
    SelectModel --> CheckProvider{Provider configured?}
    
    CheckProvider -->|No| RaiseError[Raise LLMConfigError]
    CheckProvider -->|Yes| PrepareRequest[Prepare API request]
    
    PrepareRequest --> CallAPI[Call LLM API]
    CallAPI -->|429| Wait[Exponential backoff]
    Wait --> CallAPI
    
    CallAPI -->|Timeout| Retry{Retries left?}
    Retry -->|Yes| CallAPI
    Retry -->|No| RaiseTimeout[Raise TimeoutError]
    
    CallAPI -->|Success| ParseJSON[Parse JSON response]
    ParseJSON -->|Invalid| RaiseParseError[Raise JSONDecodeError]
    ParseJSON -->|Valid| Return([Return response])
```

---

## Search Client Flow

```mermaid
flowchart TD
    Start([search_all_providers]) --> LoopP{For each provider}
    
    LoopP --> CheckEnabled{Provider enabled?}
    CheckEnabled -->|No| NextP
    CheckEnabled -->|Yes| ExecuteSearch[Search provider]
    
    ExecuteSearch -->|Timeout| LogTimeout[Log timeout]
    ExecuteSearch -->|Error| LogError[Log error]
    ExecuteSearch -->|Success| FilterEnglish{English only?}
    
    FilterEnglish -->|Yes| ApplyFilter[Remove non-English]
    FilterEnglish -->|No| AddResults[Add to results]
    ApplyFilter --> AddResults
    
    LogTimeout --> NextP{More providers?}
    LogError --> NextP
    AddResults --> NextP
    
    NextP -->|Yes| LoopP
    NextP -->|No| Combine[Combine and deduplicate]
    Combine --> Return([Return SearchResults])
```
