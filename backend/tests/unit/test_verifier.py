"""Unit tests for the Verifier module.

Tests:
- FR-005: System MUST cross-reference data from multiple sources
- FR-009: System MUST handle conflicting info with all sources cited
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from backend.modules.verifier import Verifier, VerifiedFact, Discrepancy, verify_findings


class MockFinding:
    """Mock finding for testing."""
    def __init__(self, question_id, content, source_url, source_title, confidence=0.8):
        self.id = f"finding-{question_id}"
        self.question_id = question_id
        self.content = content
        self.source_url = source_url
        self.source_title = source_title
        self.extraction_timestamp = datetime.now()
        self.confidence = confidence


class TestVerifierModule:
    """Tests for the Verifier class."""
    
    @pytest.fixture
    def verifier(self):
        """Create a Verifier with mocked LLM client."""
        v = Verifier()
        v.llm_client = MagicMock()
        return v
    
    @pytest.fixture
    def sample_findings(self):
        """Sample findings from multiple sources."""
        return [
            MockFinding("q1", "Tesla revenue was $25B", "https://source1.com", "Source 1"),
            MockFinding("q1", "Tesla reported $25 billion revenue", "https://source2.com", "Source 2"),
            MockFinding("q2", "Tesla stock rose 10%", "https://source3.com", "Source 3"),
        ]
    
    def test_group_findings_by_topic(self, verifier, sample_findings):
        """Test that findings are grouped by question ID."""
        grouped = verifier._group_findings_by_topic(sample_findings)
        
        assert "q1" in grouped
        assert "q2" in grouped
        assert len(grouped["q1"]) == 2
        assert len(grouped["q2"]) == 1
    
    def test_single_source_fact_has_lower_confidence(self, verifier):
        """Test that single-source facts have reduced confidence."""
        finding = MockFinding("q1", "Test claim", "https://single.com", "Single Source", 0.9)
        
        fact = verifier._create_single_source_fact(finding)
        
        assert fact.confidence < finding.confidence
        assert fact.source_count == 1
        assert "Single source" in fact.verification_notes
    
    @pytest.mark.asyncio
    async def test_verify_findings_returns_facts_and_discrepancies(self, verifier, sample_findings):
        """Test that verify_findings returns both facts and discrepancies."""
        verifier.llm_client.complete_json = AsyncMock(return_value={
            "verified_facts": [
                {"claim": "Tesla revenue was $25B", "confidence": 0.9, "is_consistent": True, "notes": "Confirmed by 2 sources"}
            ],
            "discrepancies": []
        })
        
        facts, discrepancies = await verifier.verify_findings(sample_findings, "req-123")
        
        assert isinstance(facts, list)
        assert isinstance(discrepancies, list)
    
    @pytest.mark.asyncio
    async def test_discrepancy_detection(self, verifier):
        """Test that discrepancies are detected for conflicting claims."""
        conflicting_findings = [
            MockFinding("q1", "Revenue was $25B", "https://a.com", "Source A"),
            MockFinding("q1", "Revenue was $20B", "https://b.com", "Source B"),
        ]
        
        verifier.llm_client.complete_json = AsyncMock(return_value={
            "verified_facts": [],
            "discrepancies": [
                {
                    "topic": "Revenue figures",
                    "description": "Source A says $25B, Source B says $20B",
                    "preferred_claim": "$25B",
                    "resolution_basis": "recency",
                    "resolution_notes": "Source A is more recent"
                }
            ]
        })
        
        facts, discrepancies = await verifier.verify_findings(conflicting_findings, "req-456")
        
        assert len(discrepancies) >= 1


class TestVerifiedFact:
    """Tests for the VerifiedFact dataclass."""
    
    def test_verified_fact_to_dict(self):
        """Test VerifiedFact serialization."""
        fact = VerifiedFact(
            id="vf1",
            claim="Tesla is the top EV manufacturer",
            confidence=0.95,
            source_urls=["https://a.com", "https://b.com"],
            source_count=2,
            is_consistent=True,
            verification_notes="Confirmed by multiple sources"
        )
        
        result = fact.to_dict()
        
        assert result["id"] == "vf1"
        assert result["confidence"] == 0.95
        assert len(result["source_urls"]) == 2


class TestDiscrepancy:
    """Tests for the Discrepancy dataclass."""
    
    def test_discrepancy_to_dict(self):
        """Test Discrepancy serialization."""
        disc = Discrepancy(
            id="d1",
            topic="Revenue figures",
            conflicting_claims=[
                {"claim": "$25B", "source_url": "https://a.com", "timestamp": "2024-01-01"},
                {"claim": "$20B", "source_url": "https://b.com", "timestamp": "2024-01-02"}
            ],
            resolution_notes="Using more recent source",
            preferred_claim="$20B",
            resolution_basis="recency"
        )
        
        result = disc.to_dict()
        
        assert result["topic"] == "Revenue figures"
        assert len(result["conflicting_claims"]) == 2
        assert result["preferred_claim"] == "$20B"


class TestConvenienceFunction:
    """Tests for module-level convenience function."""
    
    @pytest.mark.asyncio
    async def test_verify_findings_function(self):
        """Test the convenience function."""
        findings = []
        
        with patch('backend.modules.verifier.Verifier') as MockVerifier:
            mock_instance = MockVerifier.return_value
            mock_instance.verify_findings = AsyncMock(return_value=([], []))
            
            await verify_findings(findings, "req-test")
            
            mock_instance.verify_findings.assert_called_once()
