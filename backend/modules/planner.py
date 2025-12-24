"""Planner Module - Query Deconstruction into Sub-Questions.

Per FR-001: System MUST deconstruct user research queries into 3-10 structured sub-questions.

The Planner analyzes a user query and generates a research plan with prioritized 
sub-questions that comprehensively cover the topic.
"""

import uuid
from typing import List, Optional
from datetime import datetime

from backend.models import (
    SubQuestion, ResearchPlan, DepthLevel, QuestionStatus, AgenticResearchRequest
)
from backend.utils.llm_utils import get_llm_client, TaskType
from backend.utils.logging_utils import get_logger, StageTimer
from backend.config import settings


logger = get_logger(__name__)


class PlanningError(Exception):
    """Raised when research planning fails."""
    pass


# Depth level to sub-question count mapping (per User Story 4)
DEPTH_CONFIG = {
    DepthLevel.QUICK: {"min_questions": 3, "max_questions": 5, "max_recursion": 1},
    DepthLevel.STANDARD: {"min_questions": 5, "max_questions": 7, "max_recursion": 2},
    DepthLevel.COMPREHENSIVE: {"min_questions": 7, "max_questions": 10, "max_recursion": 3},
}


PLANNING_SYSTEM_PROMPT = """You are an expert research planner. Your task is to analyze a user's research query and decompose it into a comprehensive set of sub-questions that, when answered, will provide thorough coverage of the topic.

Guidelines:
1. Generate between {min_questions} and {max_questions} sub-questions
2. Prioritize questions by importance (1 = most important)
3. Cover different aspects: facts, context, implications, related topics
4. Questions should be specific and searchable
5. Avoid redundant or overlapping questions
6. Consider: who, what, when, where, why, how

Output format - respond with valid JSON only:
{{
  "sub_questions": [
    {{"text": "question text", "priority": 1}},
    {{"text": "question text", "priority": 2}}
  ],
  "estimated_time_seconds": 60
}}
"""


class Planner:
    """Planner module for query deconstruction.
    
    Takes a user research query and generates a structured research plan
    with prioritized sub-questions.
    """
    
    def __init__(self):
        self.llm_client = get_llm_client()
    
    async def create_plan(
        self,
        request: AgenticResearchRequest
    ) -> ResearchPlan:
        """Create a research plan from a user query.
        
        Args:
            request: The agentic research request with query and depth level
            
        Returns:
            ResearchPlan with generated sub-questions
        """
        config = DEPTH_CONFIG.get(request.depth_level, DEPTH_CONFIG[DepthLevel.STANDARD])
        
        with StageTimer("planning", logger, request_id=request.id, query=request.query[:50]):
            try:
                # Call LLM to generate sub-questions
                sub_questions = await self._generate_sub_questions(
                    query=request.query,
                    min_questions=config["min_questions"],
                    max_questions=config["max_questions"]
                )
                
                # Create the research plan
                plan = ResearchPlan(
                    id=str(uuid.uuid4()),
                    request_id=request.id,
                    sub_questions=sub_questions,
                    estimated_time_seconds=self._estimate_time(len(sub_questions), config["max_recursion"]),
                    created_at=datetime.now()
                )
                
                logger.info(
                    "plan_created",
                    request_id=request.id,
                    plan_id=plan.id,
                    num_questions=len(sub_questions)
                )
                
                return plan
                
            except Exception as e:
                logger.error(
                    "planning_failed",
                    request_id=request.id,
                    error=str(e)
                )
                raise
    
    async def _generate_sub_questions(
        self,
        query: str,
        min_questions: int,
        max_questions: int
    ) -> List[SubQuestion]:
        """Generate sub-questions using LLM.
        
        Args:
            query: User's research query
            min_questions: Minimum number of sub-questions
            max_questions: Maximum number of sub-questions
            
        Returns:
            List of SubQuestion objects
        """
        system_prompt = PLANNING_SYSTEM_PROMPT.format(
            min_questions=min_questions,
            max_questions=max_questions
        )
        
        user_prompt = f"""Analyze this research query and generate sub-questions:

Query: {query}

Generate {min_questions}-{max_questions} sub-questions that comprehensively cover this topic."""
        
        try:
            response = await self.llm_client.complete_json(
                prompt=user_prompt,
                task_type=TaskType.PLANNING,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            sub_questions = []
            for i, sq in enumerate(response.get("sub_questions", [])):
                sub_questions.append(SubQuestion(
                    id=str(uuid.uuid4()),
                    text=sq["text"],
                    priority=sq.get("priority", i + 1),
                    parent_id=None,
                    depth=0,
                    status=QuestionStatus.PENDING,
                    created_at=datetime.now()
                ))
            
            # Validate we have sufficient questions
            if len(sub_questions) < min_questions:
                logger.warning(
                    "insufficient_questions_generated",
                    generated=len(sub_questions),
                    minimum=min_questions
                )
                raise PlanningError(
                    f"LLM generated only {len(sub_questions)} questions, minimum required: {min_questions}"
                )
            
            return sub_questions[:max_questions]  # Cap at max
            
        except Exception as e:
            logger.error("sub_question_generation_failed", error=str(e))
            raise PlanningError(f"Failed to generate research plan: {str(e)}") from e
    
    def _generate_fallback_questions(self, query: str, count: int) -> List[SubQuestion]:
        """Generate basic fallback questions if LLM fails.
        
        Args:
            query: Original query
            count: Number of questions to generate
            
        Returns:
            List of basic SubQuestion objects
        """
        basic_aspects = [
            f"What is {query}?",
            f"What are the key facts about {query}?",
            f"What is the recent news about {query}?",
            f"What are the main challenges or controversies related to {query}?",
            f"What is the future outlook for {query}?"
        ]
        
        return [
            SubQuestion(
                id=str(uuid.uuid4()),
                text=basic_aspects[i] if i < len(basic_aspects) else f"Additional information about {query}",
                priority=i + 1,
                parent_id=None,
                depth=0,
                status=QuestionStatus.PENDING,
                created_at=datetime.now()
            )
            for i in range(min(count, len(basic_aspects)))
        ]
    
    def _estimate_time(self, num_questions: int, max_recursion: int) -> int:
        """Estimate total research time in seconds.
        
        Args:
            num_questions: Number of sub-questions
            max_recursion: Maximum recursion depth
            
        Returns:
            Estimated time in seconds
        """
        # Base time per question (search + extraction)
        base_time_per_question = 15  # seconds
        
        # Additional time for verification and synthesis
        verification_time = 10
        synthesis_time = 20
        
        # Recursion multiplier (assume 50% of questions trigger recursion)
        recursion_factor = 1 + (0.5 * max_recursion)
        
        total_time = int(
            (num_questions * base_time_per_question * recursion_factor) +
            verification_time +
            synthesis_time
        )
        
        # Cap at performance target (SC-010: under 3 minutes)
        return min(total_time, settings.MAX_RESEARCH_TIME_SECONDS)


# Module-level convenience function
async def create_research_plan(request: AgenticResearchRequest) -> ResearchPlan:
    """Convenience function to create a research plan.
    
    Args:
        request: The agentic research request
        
    Returns:
        ResearchPlan with generated sub-questions
    """
    planner = Planner()
    return await planner.create_plan(request)
