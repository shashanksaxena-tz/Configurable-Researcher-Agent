"""Verifier Module - Cross-Reference and Discrepancy Detection.

Per FR-005: System MUST cross-reference data points from multiple sources to identify discrepancies.
Per FR-009: System MUST handle conflicting information by citing all sources and noting discrepancies.
"""

import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from collections import defaultdict

from backend.utils.llm_utils import get_llm_client, TaskType
from backend.utils.logging_utils import get_logger, StageTimer
from backend.config import settings


logger = get_logger(__name__)


@dataclass
class VerifiedFact:
    """A fact that has been verified against multiple sources.
    
    Per FR-005: Cross-referenced data points from multiple sources.
    """
    id: str
    claim: str
    confidence: float
    source_urls: List[str]
    source_count: int
    is_consistent: bool
    verification_notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "claim": self.claim,
            "confidence": self.confidence,
            "source_urls": self.source_urls,
            "source_count": self.source_count,
            "is_consistent": self.is_consistent,
            "verification_notes": self.verification_notes
        }


@dataclass
class Discrepancy:
    """A detected discrepancy between sources.
    
    Per FR-009: Handle conflicting information with source citations and context.
    """
    id: str
    topic: str
    conflicting_claims: List[Dict[str, Any]]  # [{claim, source_url, timestamp}]
    resolution_notes: str
    preferred_claim: Optional[str] = None
    resolution_basis: str = ""  # recency, credibility, consensus
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "topic": self.topic,
            "conflicting_claims": self.conflicting_claims,
            "resolution_notes": self.resolution_notes,
            "preferred_claim": self.preferred_claim,
            "resolution_basis": self.resolution_basis
        }


VERIFICATION_PROMPT = """You are a fact-checker. Analyze these claims from different sources and determine:
1. Which claims are consistent across sources
2. Which claims conflict with each other
3. For conflicts, suggest which claim is most reliable and why

Topic: {topic}

Claims from sources:
{claims_text}

Respond with valid JSON:
{{
  "verified_facts": [
    {{
      "claim": "the verified claim text",
      "confidence": 0.9,
      "is_consistent": true,
      "notes": "Found in 3 sources with matching data"
    }}
  ],
  "discrepancies": [
    {{
      "topic": "specific topic of conflict",
      "description": "Source A says X, Source B says Y",
      "preferred_claim": "the more reliable claim",
      "resolution_basis": "recency|credibility|consensus",
      "resolution_notes": "Preferring Source A because..."
    }}
  ]
}}"""


class Verifier:
    """Verifier module for cross-referencing and discrepancy detection.
    
    Analyzes findings from multiple sources to identify consistent facts
    and detect conflicting information.
    """
    
    def __init__(self):
        self.llm_client = get_llm_client()
    
    async def verify_findings(
        self,
        findings: List[Any],  # ResearchFinding objects from deep_researcher
        request_id: str
    ) -> Tuple[List[VerifiedFact], List[Discrepancy]]:
        """Verify findings by cross-referencing sources.
        
        Args:
            findings: List of ResearchFinding objects
            request_id: The research request ID for logging
            
        Returns:
            Tuple of (verified_facts, discrepancies)
        """
        with StageTimer("verifying", logger, request_id=request_id, num_findings=len(findings)):
            # Group findings by question/topic for cross-referencing
            grouped_findings = self._group_findings_by_topic(findings)
            
            all_verified_facts: List[VerifiedFact] = []
            all_discrepancies: List[Discrepancy] = []
            
            # Process each topic group
            for topic, topic_findings in grouped_findings.items():
                if len(topic_findings) < 2:
                    # Single source - add as low-confidence fact
                    fact = self._create_single_source_fact(topic_findings[0])
                    all_verified_facts.append(fact)
                else:
                    # Multiple sources - cross-reference
                    facts, discrepancies = await self._cross_reference(topic, topic_findings)
                    all_verified_facts.extend(facts)
                    all_discrepancies.extend(discrepancies)
            
            logger.info(
                "verification_complete",
                request_id=request_id,
                verified_facts=len(all_verified_facts),
                discrepancies=len(all_discrepancies)
            )
            
            return all_verified_facts, all_discrepancies
    
    def _group_findings_by_topic(self, findings: List[Any]) -> Dict[str, List[Any]]:
        """Group findings by their question ID (topic).
        
        Args:
            findings: List of ResearchFinding objects
            
        Returns:
            Dictionary mapping question_id to list of findings
        """
        grouped = defaultdict(list)
        for finding in findings:
            grouped[finding.question_id].append(finding)
        return dict(grouped)
    
    def _create_single_source_fact(self, finding: Any) -> VerifiedFact:
        """Create a verified fact from a single source (lower confidence).
        
        Args:
            finding: A single ResearchFinding object
            
        Returns:
            VerifiedFact with lower confidence
        """
        return VerifiedFact(
            id=str(uuid.uuid4()),
            claim=finding.content,
            confidence=min(finding.confidence * 0.7, 0.6),  # Reduce confidence for single source
            source_urls=[finding.source_url],
            source_count=1,
            is_consistent=True,
            verification_notes="Single source - not cross-verified"
        )
    
    async def _cross_reference(
        self,
        topic: str,
        findings: List[Any]
    ) -> Tuple[List[VerifiedFact], List[Discrepancy]]:
        """Cross-reference multiple findings for a topic.
        
        Per FR-005: Cross-reference data points from multiple sources.
        
        Args:
            topic: The topic/question being verified
            findings: List of findings from different sources
            
        Returns:
            Tuple of (verified_facts, discrepancies)
        """
        # Prepare claims text for LLM
        claims_text = "\n".join([
            f"Source: {f.source_title} ({f.source_url})\n"
            f"Claim: {f.content}\n"
            f"Timestamp: {f.extraction_timestamp.isoformat()}\n"
            for f in findings
        ])
        
        prompt = VERIFICATION_PROMPT.format(
            topic=topic,
            claims_text=claims_text
        )
        
        try:
            response = await self.llm_client.complete_json(
                prompt=prompt,
                task_type=TaskType.VERIFICATION,
                temperature=0.3  # Low temperature for factual analysis
            )
            
            verified_facts = []
            discrepancies = []
            
            # Process verified facts
            for vf in response.get("verified_facts", []):
                # Find which sources support this fact
                supporting_sources = [f.source_url for f in findings]
                
                verified_facts.append(VerifiedFact(
                    id=str(uuid.uuid4()),
                    claim=vf["claim"],
                    confidence=vf.get("confidence", 0.8),
                    source_urls=supporting_sources[:3],  # Limit sources shown
                    source_count=len(findings),
                    is_consistent=vf.get("is_consistent", True),
                    verification_notes=vf.get("notes", "")
                ))
            
            # Process discrepancies
            for disc in response.get("discrepancies", []):
                # Build conflicting claims list
                conflicting = [
                    {
                        "claim": f.content[:200],
                        "source_url": f.source_url,
                        "timestamp": f.extraction_timestamp.isoformat()
                    }
                    for f in findings
                ]
                
                discrepancies.append(Discrepancy(
                    id=str(uuid.uuid4()),
                    topic=disc.get("topic", topic),
                    conflicting_claims=conflicting,
                    resolution_notes=disc.get("resolution_notes", ""),
                    preferred_claim=disc.get("preferred_claim"),
                    resolution_basis=disc.get("resolution_basis", "unknown")
                ))
            
            return verified_facts, discrepancies
            
        except Exception as e:
            logger.error("cross_reference_failed", topic=topic, error=str(e))
            # Return basic facts without cross-referencing
            return [self._create_single_source_fact(f) for f in findings], []


# Module-level convenience function
async def verify_findings(findings: List[Any], request_id: str) -> Tuple[List[VerifiedFact], List[Discrepancy]]:
    """Convenience function to verify findings.
    
    Args:
        findings: List of ResearchFinding objects
        request_id: Research request ID
        
    Returns:
        Tuple of (verified_facts, discrepancies)
    """
    verifier = Verifier()
    return await verifier.verify_findings(findings, request_id)
