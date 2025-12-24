
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.utils.report_generator import ReportGenerator
from backend.models import ResearchResult, EntityType

def generate_sample_report():
    print("Generating sample report...")
    
    # Create dummy data
    results = [
        ResearchResult(
            title="Financial Performance Q1 2024",
            summary="Tesla reported strong earnings with a 15% increase in revenue year-over-year. Margins remained healthy despite price cuts.",
            confidence=0.95,
            research_type="financial_analysis",
            data={
                "revenue": "$25.5 Billion",
                "net_income": "$3.2 Billion",
                "deliveries": "450,000 units",
                "margin": "18.5%"
            }
        ),
        ResearchResult(
            title="New Model Launch",
            summary="The company announced the upcoming release of the Model 2, a budget-friendly electric vehicle aimed at the mass market.",
            confidence=0.88,
            research_type="product_analysis",
            data={
                "model_name": "Model 2",
                "expected_price": "$25,000",
                "release_date": "Late 2025"
            }
        ),
        ResearchResult(
            title="Gigafactory Expansion",
            summary="Expansion plans for Gigafactory Texas are underway to support Cybertruck production scaling.",
            confidence=0.92,
            research_type="operational_analysis",
            data={
                "location": "Austin, Texas",
                "investment": "$10 Billion",
                "jobs_created": "5,000+"
            }
        )
    ]
    
    generator = ReportGenerator(reports_dir="./test_reports")
    report_id = generator.generate_pdf_report(
        entity_name="Tesla Inc",
        entity_type=EntityType.COMPANY,
        results=results
    )
    
    print(f"Report generated: ./test_reports/*{report_id}*.pdf")

if __name__ == "__main__":
    generate_sample_report()
