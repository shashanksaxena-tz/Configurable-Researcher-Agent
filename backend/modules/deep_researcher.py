"""Deep Researcher Module - Recursive Search with Depth Management.

Per FR-002: System MUST execute independent searches for each sub-question.
Per FR-003: System MUST perform recursive searches when results reference relevant new topics.
Per FR-004: System MUST implement a recursion depth limit (default: 2-3 levels).
"""

import uuid
import asyncio
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from dataclasses import dataclass

from backend.models import (
    SubQuestion, ResearchPlan, DepthLevel, QuestionStatus
)
from backend.utils.llm_utils import get_llm_client, TaskType
from backend.utils.search_utils import get_search_client, SearchResult
from backend.utils.logging_utils import get_logger, StageTimer
from backend.config import settings


logger = get_logger(__name__)


@dataclass
class ResearchFinding:
    """A finding extracted from search results with source tracking.
    
    Per FR-006: System MUST track source URL and timestamp for every fact.
    """
    id: str
    question_id: str
    content: str
    source_url: str
    source_title: str
    extraction_timestamp: datetime
    confidence: float = 0.8
    triggers_recursion: bool = False
    recursion_topics: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "question_id": self.question_id,
            "content": self.content,
            "source_url": self.source_url,
            "source_title": self.source_title,
            "extraction_timestamp": self.extraction_timestamp.isoformat(),
            "confidence": self.confidence,
            "triggers_recursion": self.triggers_recursion,
            "recursion_topics": self.recursion_topics or []
        }


EXTRACTION_PROMPT = """Extract key facts and information from this search result to answer the question.

Question: {question}

Search Result:
Title: {title}
URL: {url}
Content: {content}

Instructions:
1. Extract factual information that answers the question
2. Identify any new topics or entities that should be researched further
3. Rate your confidence in the extracted information (0.0-1.0)

Respond with valid JSON:
{{
  "extracted_facts": [
    "fact 1",
    "fact 2"
  ],
  "confidence": 0.8,
  "new_topics_to_research": ["topic1", "topic2"] or []
}}"""


class DeepResearcher:
    """Deep Researcher module with recursive search capability.
    
    Implements a breadth-first search approach with depth limiting
    to explore topics thoroughly while preventing infinite loops.
    """
    
    def __init__(self, max_depth: int = None):
        self.llm_client = get_llm_client()
        self.search_client = get_search_client()
        self.max_depth = max_depth or settings.MAX_RECURSION_DEPTH
        self.visited_topics: Set[str] = set()  # Prevent duplicate searches
    
    async def execute_research(
        self,
        plan: ResearchPlan,
        depth_level: DepthLevel = DepthLevel.STANDARD
    ) -> List[ResearchFinding]:
        """Execute research for all sub-questions in the plan.
        
        Uses breadth-first search with depth limiting per FR-004.
        
        Args:
            plan: The research plan with sub-questions
            depth_level: Controls recursion depth
            
        Returns:
            List of ResearchFinding objects with source tracking
        """
        # Set max depth based on depth level
        depth_config = {
            DepthLevel.QUICK: 1,
            DepthLevel.STANDARD: 2,
            DepthLevel.COMPREHENSIVE: 3
        }
        self.max_depth = depth_config.get(depth_level, 2)
        
        all_findings: List[ResearchFinding] = []
        
        with StageTimer("executing", logger, request_id=plan.request_id, num_questions=len(plan.sub_questions)):
            # Process questions in priority order
            sorted_questions = sorted(plan.sub_questions, key=lambda q: q.priority)
            
            for question in sorted_questions:
                question.status = QuestionStatus.IN_PROGRESS
                
                try:
                    findings = await self._research_question(question, depth=0)
                    all_findings.extend(findings)
                    question.status = QuestionStatus.COMPLETED
                    
                except Exception as e:
                    logger.error(
                        "question_research_failed",
                        question_id=question.id,
                        error=str(e)
                    )
                    question.status = QuestionStatus.FAILED
            
            logger.info(
                "research_execution_complete",
                request_id=plan.request_id,
                total_findings=len(all_findings),
                questions_completed=sum(1 for q in plan.sub_questions if q.status == QuestionStatus.COMPLETED)
            )
        
        return all_findings
    
    async def _research_question(
        self,
        question: SubQuestion,
        depth: int
    ) -> List[ResearchFinding]:
        """Research a single question with potential recursion.
        
        Args:
            question: The sub-question to research
            depth: Current recursion depth
            
        Returns:
            List of findings for this question
        """
        if depth > self.max_depth:
            logger.debug(
                "max_depth_reached",
                question_id=question.id,
                depth=depth,
                max_depth=self.max_depth
            )
            return []
        
        # Normalize question for deduplication
        normalized_query = question.text.lower().strip()
        if normalized_query in self.visited_topics:
            logger.debug("skipping_duplicate_query", query=question.text[:50])
            return []
        self.visited_topics.add(normalized_query)
        
        findings: List[ResearchFinding] = []
        
        # Execute search
        search_results = await self.search_client.search_all_providers(
            query=question.text,
            max_results_per_provider=settings.MAX_SEARCH_RESULTS_PER_QUERY
        )
        
        if not search_results:
            logger.warning(
                "no_search_results",
                question_id=question.id,
                query=question.text[:50]
            )
            return findings
        
        # Process each search result (limit to avoid rate limits)
        for result in search_results[:settings.MAX_SEARCH_RESULTS_PER_QUERY]:
            try:
                finding = await self._extract_from_result(question, result)
                if finding:
                    findings.append(finding)
                    
                    # Check for recursive topics (per FR-003)
                    if finding.triggers_recursion and depth < self.max_depth:
                        recursive_findings = await self._handle_recursion(
                            finding, question.id, depth + 1
                        )
                        findings.extend(recursive_findings)
                        
            except Exception as e:
                logger.error(
                    "extraction_failed",
                    question_id=question.id,
                    url=result.url,
                    error=str(e)
                )
        
        return findings
    
    async def _extract_from_result(
        self,
        question: SubQuestion,
        result: SearchResult
    ) -> Optional[ResearchFinding]:
        """Extract information from a search result.
        
        Args:
            question: The question being answered
            result: The search result to extract from
            
        Returns:
            ResearchFinding or None if extraction failed
        """
        prompt = EXTRACTION_PROMPT.format(
            question=question.text,
            title=result.title,
            url=result.url,
            content=result.snippet[:1000]  # Limit content length
        )
        
        try:
            response = await self.llm_client.complete_json(
                prompt=prompt,
                task_type=TaskType.EXTRACTION,
                temperature=0.3  # Lower temperature for factual extraction
            )
            
            extracted_facts = response.get("extracted_facts", [])
            if not extracted_facts:
                return None
            
            new_topics = response.get("new_topics_to_research", [])
            
            return ResearchFinding(
                id=str(uuid.uuid4()),
                question_id=question.id,
                content=" ".join(extracted_facts),
                source_url=result.url,
                source_title=result.title,
                extraction_timestamp=datetime.now(),
                confidence=response.get("confidence", 0.7),
                triggers_recursion=len(new_topics) > 0,
                recursion_topics=new_topics[:3]  # Limit recursion topics
            )
            
        except Exception as e:
            logger.error("llm_extraction_failed", error=str(e))
            return None
    
    async def _handle_recursion(
        self,
        finding: ResearchFinding,
        parent_question_id: str,
        new_depth: int
    ) -> List[ResearchFinding]:
        """Handle recursive search for new topics.
        
        Per FR-003: Trigger recursive searches for relevant new topics.
        
        Args:
            finding: The finding with new topics
            parent_question_id: ID of the parent question
            new_depth: Depth level for recursive questions
            
        Returns:
            List of findings from recursive searches
        """
        recursive_findings: List[ResearchFinding] = []
        
        for topic in (finding.recursion_topics or []):
            # Create a new sub-question for the recursive topic
            recursive_question = SubQuestion(
                id=str(uuid.uuid4()),
                text=f"What is {topic}?",
                priority=10,  # Lower priority for recursive questions
                parent_id=parent_question_id,
                depth=new_depth,
                status=QuestionStatus.PENDING,
                created_at=datetime.now()
            )
            
            logger.info(
                "recursive_search_triggered",
                topic=topic,
                parent_question_id=parent_question_id,
                depth=new_depth
            )
            
            # Execute recursive research
            findings = await self._research_question(recursive_question, new_depth)
            recursive_findings.extend(findings)
        
        return recursive_findings


# Module-level convenience function
async def execute_research(plan: ResearchPlan, depth_level: DepthLevel = DepthLevel.STANDARD) -> List[ResearchFinding]:
    """Convenience function to execute research for a plan.
    
    Args:
        plan: The research plan
        depth_level: Research depth setting
        
    Returns:
        List of ResearchFinding objects
    """
    researcher = DeepResearcher()
    return await researcher.execute_research(plan, depth_level)
