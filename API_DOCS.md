# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required. Future versions will include API key authentication.

## Endpoints

### Health Check

**GET** `/api/v1/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Configurable Researcher Agent",
  "version": "1.0.0",
  "timestamp": "2025-12-22T18:25:45.048764"
}
```

---

### List Available Modules

**GET** `/api/v1/modules`

Get all available research modules with their configurations.

**Response:**
```json
[
  {
    "id": "financial",
    "name": "Financial Analysis",
    "description": "Analyze financial data, stock performance, revenue, and market cap",
    "fields": ["revenue", "market_cap", "stock_price", "pe_ratio", "debt", "profitability"],
    "icon": "💰",
    "color": "#10b981"
  }
]
```

---

### Perform Research

**POST** `/api/v1/research`

Perform comprehensive research on an entity using selected modules.

**Request Body:**
```json
{
  "entity_name": "Tesla Inc",
  "entity_type": "company",
  "research_types": ["financial", "sentiment", "news"]
}
```

**Parameters:**
- `entity_name` (string, required): Name of the person or company to research
- `entity_type` (string, required): Type of entity - "company" or "individual"
- `research_types` (array, required): List of research module IDs to execute

**Response:**
```json
{
  "entity_name": "Tesla Inc",
  "entity_type": "company",
  "results": [
    {
      "research_type": "financial",
      "title": "Financial Analysis",
      "data": {
        "revenue": "$100B",
        "market_cap": "$301B",
        "stock_price": "$100",
        "pe_ratio": 13.47,
        "debt": "$33B",
        "profitability": "12% profit margin"
      },
      "summary": "Tesla Inc shows strong financial performance...",
      "confidence": 0.86,
      "timestamp": "2025-12-22T18:25:55.909650"
    }
  ],
  "total_results": 3,
  "report_id": "abc123",
  "timestamp": "2025-12-22T18:25:55.910000"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid request (bad entity type, invalid research types)
- `500`: Internal server error

---

### Generate Report

**POST** `/api/v1/generate-report`

Generate a downloadable report from research results.

**Request Body:**
```json
{
  "entity_name": "Tesla Inc",
  "entity_type": "company",
  "results": [...],
  "format": "pdf"
}
```

**Parameters:**
- `entity_name` (string, required): Entity name
- `entity_type` (string, required): "company" or "individual"
- `results` (array, required): Array of research results
- `format` (string, optional): Report format - "pdf" (default) or "html"

**Response:**
```json
{
  "report_id": "abc123",
  "filename": "abc123_Tesla_Inc_report.pdf",
  "url": "/reports/abc123_Tesla_Inc_report.pdf",
  "format": "pdf"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid format or missing data
- `500`: Report generation failed

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. This will be added in future versions.

## Examples

### cURL Examples

**Get available modules:**
```bash
curl http://localhost:8000/api/v1/modules
```

**Perform research:**
```bash
curl -X POST http://localhost:8000/api/v1/research \
  -H "Content-Type: application/json" \
  -d '{
    "entity_name": "Apple Inc",
    "entity_type": "company",
    "research_types": ["financial", "sentiment", "news"]
  }'
```

### Python Example

```python
import requests

# Perform research
response = requests.post(
    'http://localhost:8000/api/v1/research',
    json={
        'entity_name': 'Apple Inc',
        'entity_type': 'company',
        'research_types': ['financial', 'sentiment', 'news']
    }
)

data = response.json()
print(f"Research completed with {data['total_results']} results")
print(f"Report ID: {data['report_id']}")
```

### JavaScript Example

```javascript
const response = await fetch('http://localhost:8000/api/v1/research', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    entity_name: 'Apple Inc',
    entity_type: 'company',
    research_types: ['financial', 'sentiment', 'news']
  })
});

const data = await response.json();
console.log(`Research completed with ${data.total_results} results`);
```

## Interactive API Documentation

Visit `/docs` for interactive Swagger UI documentation where you can test all endpoints directly in your browser.

Visit `/redoc` for alternative ReDoc documentation.
