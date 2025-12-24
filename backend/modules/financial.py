"""Financial analysis researcher module."""

from typing import Dict, Any
from .base import BaseResearcher

class FinancialResearcher(BaseResearcher):
    """Researcher for financial analysis."""
    
    async def research(self) -> Dict[str, Any]:
        """Perform financial research."""
        
        if self.entity_type == "company":
            schema = {
                "revenue": "string",
                "market_cap": "string",
                "stock_price": "string",
                "pe_ratio": "float",
                "debt": "string",
                "profitability": "string",
                "growth_rate": "string",
                "earnings": "string",
            }
            return await self.perform_ai_research("financials revenue stock market cap earnings", schema)
        else:
            schema = {
                "net_worth": "string",
                "income": "string",
                "investments": ["string"],
                "assets": "string",
                "financial_status": "string",
            }
            return await self.perform_ai_research("net worth salary investments assets money", schema)
    
    # Removed the override for generate_summary to use the BaseResearcher's narrative logic.
