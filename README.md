# Configurable Researcher Agent

A highly customizable AI-powered research agent with a modern, animated interface. This application can perform comprehensive research on individuals or companies across multiple dimensions including financial analysis, sentiment analysis, news analysis, and more.

## 🌟 Features

### Research Modules
- **Financial Analysis**: Revenue, market cap, stock performance, profitability metrics
- **Sentiment Analysis**: Public opinion, reviews, social sentiment scoring
- **News Analysis**: Recent news, press releases, media coverage
- **Personality Analysis**: Leadership style, communication patterns, traits
- **Hobbies & Interests**: Personal interests, activities, passions
- **Career Analysis**: Professional background, achievements, education
- **Social Media Presence**: Platform analysis, engagement metrics, influence scores
- **Market Analysis**: Market share, positioning, competitive landscape
- **Competitor Analysis**: Competitive advantages, market positioning
- **Trends Analysis**: Emerging trends, future predictions, opportunities

### Modern UI/UX
- 🎨 Beautiful glassmorphism design
- ✨ Smooth Framer Motion animations
- 🌈 Gradient backgrounds and effects
- 📱 Responsive design for all devices
- 🎭 Interactive particle effects
- 🎯 Real-time loading states and feedback

### Report Generation
- 📄 PDF reports with professional styling
- 🌐 HTML reports for web viewing
- 📊 Data visualization and tables
- 📈 Confidence scores and metrics
- 🎨 Beautiful formatting and colors

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 📖 Usage

1. **Open the Application**: Navigate to `http://localhost:3000` in your browser

2. **Enter Research Target**: 
   - Enter the name of a person or company
   - Select the entity type (Individual or Company)

3. **Select Research Modules**:
   - Click on the modules you want to include in your research
   - You can select multiple modules

4. **Start Research**:
   - Click "Start Research" button
   - Wait for the AI to analyze your request

5. **View Results**:
   - Browse through the analysis results
   - Download the comprehensive PDF report

## 🎨 Customization

### Adding New Research Modules

1. **Create a new module class** in `backend/modules/`:

```python
from .base import BaseResearcher
from typing import Dict, Any

class YourResearcher(BaseResearcher):
    async def research(self) -> Dict[str, Any]:
        # Your research logic here
        return {
            "field1": "value1",
            "field2": "value2"
        }
    
    def generate_summary(self, data: Dict[str, Any]) -> str:
        return f"Summary for {self.entity_name}"
```

2. **Register the module** in `backend/config.py`:

```python
RESEARCH_MODULES["your_module"] = {
    "name": "Your Module Name",
    "description": "Module description",
    "fields": ["field1", "field2"],
    "icon": "🔍",
    "color": "#ff6b6b"
}
```

3. **Add to module manager** in `backend/modules/__init__.py`:

```python
from .your_module import YourResearcher

MODULE_MAP = {
    # ... existing modules
    "your_module": YourResearcher,
}
```

## 🏗️ Architecture

### Backend (FastAPI)
- **main.py**: FastAPI application and API endpoints
- **config.py**: Configuration and module definitions
- **models.py**: Pydantic data models
- **modules/**: Research module implementations
- **utils/**: Utility functions and report generation

### Frontend (React + Vite)
- **App.jsx**: Main application component
- **components/**: Reusable UI components
  - Header: Animated header with branding
  - ModuleSelector: Interactive module selection
  - ResearchForm: Entity input form
  - ResultsDisplay: Animated results display
- **utils/**: API client and utilities

## 📊 API Endpoints

### GET `/api/v1/health`
Health check endpoint

### GET `/api/v1/modules`
Get all available research modules

### POST `/api/v1/research`
Perform research on an entity

**Request Body:**
```json
{
  "entity_name": "Tesla Inc",
  "entity_type": "company",
  "research_types": ["financial", "news", "sentiment"]
}
```

**Response:**
```json
{
  "entity_name": "Tesla Inc",
  "entity_type": "company",
  "results": [...],
  "total_results": 3,
  "report_id": "abc123"
}
```

### POST `/api/v1/generate-report`
Generate a report from research results

## 🎯 Future Enhancements

- [ ] Integration with real APIs (OpenAI, news APIs, financial APIs)
- [ ] User authentication and saved searches
- [ ] Advanced data visualization with charts
- [ ] Export to multiple formats (Excel, Word, etc.)
- [ ] Scheduled/recurring research
- [ ] Collaborative research sharing
- [ ] Custom module builder UI
- [ ] Machine learning insights
- [ ] Real-time updates via WebSocket

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🔧 Troubleshooting

### Backend won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is already in use
- Verify Python version (3.8+)

### Frontend won't start
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 3000 is already in use
- Verify Node.js version (16+)

### API connection errors
- Ensure backend is running on port 8000
- Check CORS settings in `backend/config.py`
- Verify API URL in frontend code

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

Built with ❤️ using FastAPI, React, and Framer Motion