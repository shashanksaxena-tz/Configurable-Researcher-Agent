# Adding Custom Research Modules

This guide explains how to add custom research modules to the Configurable Researcher Agent.

## Step 1: Create a New Researcher Class

Create a new file in `backend/modules/` (e.g., `your_module.py`):

```python
"""Your custom researcher module."""

from typing import Dict, Any
from .base import BaseResearcher
import random


class YourResearcher(BaseResearcher):
    """Researcher for your custom analysis."""
    
    async def research(self) -> Dict[str, Any]:
        """Perform your custom research."""
        # Implement your research logic here
        # You can call external APIs, databases, or perform calculations
        
        data = {
            "field1": "value1",
            "field2": "value2",
            "field3": "value3",
        }
        
        return data
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate a summary of your research."""
        return f"Custom analysis completed for {self.entity_name}: {data.get('field1', 'N/A')}"
```

## Step 2: Register the Module

Add your module to `backend/config.py` in the `RESEARCH_MODULES` dictionary:

```python
RESEARCH_MODULES["your_module"] = {
    "name": "Your Module Name",
    "description": "Brief description of what your module does",
    "fields": ["field1", "field2", "field3"],
    "icon": "🔍",  # Choose an emoji icon
    "color": "#ff6b6b"  # Choose a color (hex format)
}
```

## Step 3: Add to Module Manager

Update `backend/modules/__init__.py` to import and register your researcher:

```python
# Add import
from modules.your_module import YourResearcher

# Inside ResearcherManager.__init__, add to MODULE_MAP
ResearcherManager.MODULE_MAP = {
    # ... existing modules
    "your_module": YourResearcher,
}
```

## Step 4: Test Your Module

Test your module through the API:

```bash
curl -X POST http://localhost:8000/api/v1/research \
  -H "Content-Type: application/json" \
  -d '{
    "entity_name": "Test Entity",
    "entity_type": "company",
    "research_types": ["your_module"]
  }'
```

## Advanced Features

### Accessing External APIs

```python
import httpx

async def research(self) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/data?q={self.entity_name}")
        data = response.json()
    return data
```

### Using Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

async def research(self) -> Dict[str, Any]:
    api_key = os.getenv("YOUR_API_KEY")
    # Use the API key in your requests
```

### Custom Confidence Calculation

```python
def calculate_confidence(self, data: Dict[str, Any]) -> float:
    """Calculate confidence based on data quality."""
    # Implement your logic
    data_completeness = len([v for v in data.values() if v]) / len(data)
    return round(data_completeness * 0.9, 2)
```

## Example: Social Media Engagement Module

Here's a complete example of a social media engagement analyzer:

```python
"""Social media engagement analyzer."""

from typing import Dict, Any
from .base import BaseResearcher
import httpx


class SocialEngagementResearcher(BaseResearcher):
    """Researcher for social media engagement metrics."""
    
    async def research(self) -> Dict[str, Any]:
        """Analyze social media engagement."""
        # Simulated data - replace with real API calls
        data = {
            "total_followers": "150K",
            "engagement_rate": "4.2%",
            "avg_likes": "2.5K",
            "avg_comments": "150",
            "posting_frequency": "Daily",
            "best_performing_content": "Product launches",
            "audience_growth": "+12% monthly",
        }
        
        return data
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """Generate engagement summary."""
        return f"{self.entity_name} has {data['total_followers']} followers with {data['engagement_rate']} engagement rate."
```

## Best Practices

1. **Always validate input data** before processing
2. **Handle API failures gracefully** with try-except blocks
3. **Return consistent data structures** for easier processing
4. **Add logging** for debugging
5. **Document your module** with clear docstrings
6. **Test edge cases** (empty data, invalid entities, etc.)
7. **Consider rate limiting** for external API calls
8. **Cache results** when appropriate to improve performance

## Module Configuration Options

Available configuration fields:

- **name**: Display name shown in the UI
- **description**: Brief explanation of module purpose
- **fields**: List of data fields returned by the module
- **icon**: Emoji or icon character
- **color**: Hex color code for UI theming

## Troubleshooting

### Module not appearing in UI
- Check that the module is registered in `config.py`
- Verify the module is added to `MODULE_MAP` in `__init__.py`
- Restart the backend server

### Import errors
- Ensure all imports are correct
- Check for circular dependencies
- Verify the module file is in the correct directory

### Research returning errors
- Check your research logic for exceptions
- Validate data types being returned
- Add error handling in the `research()` method
