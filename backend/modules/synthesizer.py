"""Synthesizer Module - Narrative Report Generation.

Per FR-007: System MUST generate narrative reports with minimum 300 words per major section.
Per FR-008: System MUST produce reports in professional journalism style (Bloomberg/WSJ tone).
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from backend.utils.llm_utils import get_llm_client, TaskType
from backend.utils.logging_utils import get_logger, StageTimer
from backend.config import settings


logger = get_logger(__name__)


@dataclass
class ReportSection:
    """A section of the narrative report.
    
    Per FR-007: Each major section must have minimum 300 words.
    """
    id: str
    title: str
    content: str
    word_count: int
    citation_ids: List[str]  # References to VerifiedFact IDs
    category: str  # Financials, Legal, Reputation, etc.
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "word_count": self.word_count,
            "citation_ids": self.citation_ids,
            "category": self.category
        }


@dataclass
class NarrativeReport:
    """The complete narrative research report.
    
    Per FR-010: Includes Executive Brief summary.
    Per FR-011: Organized into tabbed sections.
    """
    id: str
    request_id: str
    query: str
    executive_summary: str
    sections: List[ReportSection]
    discrepancy_notes: List[Dict[str, Any]]  # From verifier
    total_word_count: int
    total_sources: int
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "request_id": self.request_id,
            "query": self.query,
            "executive_summary": self.executive_summary,
            "sections": [s.to_dict() for s in self.sections],
            "discrepancy_notes": self.discrepancy_notes,
            "total_word_count": self.total_word_count,
            "total_sources": self.total_sources,
            "created_at": self.created_at.isoformat()
        }


EXECUTIVE_SUMMARY_PROMPT = """You are a Bloomberg/Wall Street Journal editor. Write an executive summary for this research report.

Research Topic: {query}

Key Findings:
{findings_text}

Discrepancies Noted:
{discrepancies_text}

Write a 150-250 word executive summary that:
1. Opens with the most important finding
2. Provides key context and data points
3. Notes any significant conflicting information
4. Maintains professional, authoritative tone
5. Is readable in under 2 minutes

Write only the summary text, no headers or formatting."""


SECTION_PROMPT = """You are a Bloomberg/Wall Street Journal financial journalist. Write a detailed section for a research report.

Section: {section_title}
Category: {category}

Facts to incorporate (include citation markers like [cite:ID]):
{facts_text}

Requirements:
1. MINIMUM 300 words (this is critical - do not go under)
2. Professional journalism style (Bloomberg/WSJ tone)
3. Include specific data points and figures when available
4. Incorporate inline citation markers [cite:FACT_ID] for each fact used
5. Provide context and analysis, not just facts
6. Use clear topic sentences and logical flow

Write only the section content, no headers."""


class Synthesizer:
    """Synthesizer module for generating narrative reports.
    
    Takes verified facts and discrepancies and produces a professional
    narrative report with executive summary and detailed sections.
    """
    
    def __init__(self):
        self.llm_client = get_llm_client()
        self.min_words_per_section = settings.MIN_WORDS_PER_SECTION
    
    async def generate_report(
        self,
        request_id: str,
        query: str,
        verified_facts: List[Any],  # VerifiedFact objects
        discrepancies: List[Any],   # Discrepancy objects
    ) -> NarrativeReport:
        """Generate a complete narrative report from verified facts.
        
        Args:
            request_id: The research request ID
            query: Original user query
            verified_facts: List of verified facts from verifier
            discrepancies: List of discrepancies from verifier
            
        Returns:
            NarrativeReport with executive summary and sections
        """
        with StageTimer("synthesizing", logger, request_id=request_id, num_facts=len(verified_facts)):
            # Group facts by category for sections
            categorized_facts = self._categorize_facts(verified_facts, query)
            
            # Generate executive summary
            executive_summary = await self._generate_executive_summary(
                query, verified_facts, discrepancies
            )
            
            # Generate sections for each category
            sections = []
            for category, facts in categorized_facts.items():
                section = await self._generate_section(category, facts)
                sections.append(section)
            
            # Calculate totals
            total_word_count = len(executive_summary.split()) + sum(s.word_count for s in sections)
            total_sources = len(set(url for f in verified_facts for url in f.source_urls))
            
            # Create discrepancy notes for the report
            discrepancy_notes = [d.to_dict() for d in discrepancies]
            
            report = NarrativeReport(
                id=str(uuid.uuid4()),
                request_id=request_id,
                query=query,
                executive_summary=executive_summary,
                sections=sections,
                discrepancy_notes=discrepancy_notes,
                total_word_count=total_word_count,
                total_sources=total_sources,
                created_at=datetime.now()
            )
            
            logger.info(
                "report_generated",
                request_id=request_id,
                report_id=report.id,
                sections=len(sections),
                word_count=total_word_count,
                sources=total_sources
            )
            
            return report
    
    def _categorize_facts(
        self,
        facts: List[Any],
        query: str
    ) -> Dict[str, List[Any]]:
        """Categorize facts into report sections.
        
        Categories: Financials, Legal, Reputation, Market, Operations, Other
        
        Args:
            facts: List of verified facts
            query: Original query for context
            
        Returns:
            Dictionary mapping category to list of facts
        """
        categories = {
            "Overview": [],
            "Key Findings": [],
            "Analysis": []
        }
        
        # Simple categorization - split facts into sections
        third = len(facts) // 3 or 1
        
        for i, fact in enumerate(facts):
            if i < third:
                categories["Overview"].append(fact)
            elif i < 2 * third:
                categories["Key Findings"].append(fact)
            else:
                categories["Analysis"].append(fact)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    async def _generate_executive_summary(
        self,
        query: str,
        facts: List[Any],
        discrepancies: List[Any]
    ) -> str:
        """Generate the executive summary.
        
        Per FR-010: 1-minute natural language summary.
        
        Args:
            query: Original research query
            facts: Verified facts
            discrepancies: Detected discrepancies
            
        Returns:
            Executive summary text
        """
        # Prepare findings text
        findings_text = "\n".join([
            f"- {f.claim} (confidence: {f.confidence:.0%})"
            for f in facts[:10]  # Top 10 facts
        ])
        
        # Prepare discrepancies text
        if discrepancies:
            discrepancies_text = "\n".join([
                f"- {d.topic}: {d.resolution_notes}"
                for d in discrepancies[:3]
            ])
        else:
            discrepancies_text = "No significant discrepancies found."
        
        prompt = EXECUTIVE_SUMMARY_PROMPT.format(
            query=query,
            findings_text=findings_text,
            discrepancies_text=discrepancies_text
        )
        
        try:
            summary = await self.llm_client.complete(
                prompt=prompt,
                task_type=TaskType.SYNTHESIS,
                temperature=0.6
            )
            return summary.strip()
        except Exception as e:
            logger.error("executive_summary_generation_failed", error=str(e))
            return f"Research on {query} has been completed. Please see the detailed sections below for findings."
    
    async def _generate_section(
        self,
        category: str,
        facts: List[Any]
    ) -> ReportSection:
        """Generate a single report section.
        
        Per FR-007: Minimum 300 words per section.
        Per FR-008: Professional journalism style.
        
        Args:
            category: Section category name
            facts: Facts to include in this section
            
        Returns:
            ReportSection with generated content
        """
        # Prepare facts with citation markers
        facts_text = "\n".join([
            f"[cite:{f.id}] {f.claim} (Sources: {f.source_count})"
            for f in facts
        ])
        
        prompt = SECTION_PROMPT.format(
            section_title=category,
            category=category,
            facts_text=facts_text
        )
        
        try:
            content = await self.llm_client.complete(
                prompt=prompt,
                task_type=TaskType.SYNTHESIS,
                max_tokens=1500,  # Allow for 300+ words
                temperature=0.7
            )
            
            content = content.strip()
            word_count = len(content.split())
            
            # Validate minimum word count (FR-007)
            if word_count < self.min_words_per_section:
                logger.warning(
                    "section_under_minimum_words",
                    category=category,
                    word_count=word_count,
                    minimum=self.min_words_per_section
                )
            
            return ReportSection(
                id=str(uuid.uuid4()),
                title=category,
                content=content,
                word_count=word_count,
                citation_ids=[f.id for f in facts],
                category=category
            )
            
        except Exception as e:
            logger.error("section_generation_failed", category=category, error=str(e))
            # Return placeholder section
            return ReportSection(
                id=str(uuid.uuid4()),
                title=category,
                content=f"Information about {category} is being compiled.",
                word_count=6,
                citation_ids=[],
                category=category
            )


# Module-level convenience function
async def generate_report(
    request_id: str,
    query: str,
    verified_facts: List[Any],
    discrepancies: List[Any]
) -> NarrativeReport:
    """Convenience function to generate a narrative report.
    
    Args:
        request_id: Research request ID
        query: Original user query
        verified_facts: Verified facts from verifier
        discrepancies: Discrepancies from verifier
        
    Returns:
        NarrativeReport object
    """
    synthesizer = Synthesizer()
    return await synthesizer.generate_report(request_id, query, verified_facts, discrepancies)
