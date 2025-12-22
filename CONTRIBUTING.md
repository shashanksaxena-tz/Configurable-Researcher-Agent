# Contributing to Configurable Researcher Agent

Thank you for your interest in contributing to the Configurable Researcher Agent! This document provides guidelines for contributing to the project.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Guidelines](#development-guidelines)
5. [Pull Request Process](#pull-request-process)

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions. We're building a welcoming community for everyone.

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/Configurable-Researcher-Agent.git
cd Configurable-Researcher-Agent
```

3. Set up development environment (see README.md)

4. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

## How to Contribute

### Reporting Bugs

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, Node version)

### Suggesting Features

Feature suggestions are welcome! Please:
- Check if the feature already exists
- Describe the use case
- Explain why it would be valuable
- Consider implementation complexity

### Adding Research Modules

See [CUSTOM_MODULES.md](./CUSTOM_MODULES.md) for detailed instructions on creating custom research modules.

## Development Guidelines

### Backend (Python)

**Code Style:**
- Follow PEP 8
- Use type hints
- Write docstrings for all functions and classes
- Keep functions focused and small

**Example:**
```python
async def research(self) -> Dict[str, Any]:
    """
    Perform research and return results.
    
    Returns:
        Dict[str, Any]: Research data with key-value pairs
    """
    data = {}
    return data
```

**Testing:**
```bash
# Run tests (when available)
pytest tests/
```

### Frontend (React)

**Code Style:**
- Use functional components with hooks
- Follow ESLint configuration
- Use meaningful variable names
- Keep components small and reusable

**Example:**
```javascript
const ResearchCard = ({ title, data, icon }) => {
  return (
    <div className="research-card">
      <h3>{icon} {title}</h3>
      <p>{data.summary}</p>
    </div>
  );
};
```

### Commit Messages

Use clear, descriptive commit messages:
```
feat: Add competitor analysis module
fix: Resolve PDF generation encoding issue
docs: Update API documentation
style: Format code with prettier
refactor: Simplify module loader logic
test: Add tests for financial module
```

### Documentation

- Update README.md for major changes
- Add/update docstrings for new functions
- Update API_DOCS.md for API changes
- Include inline comments for complex logic

## Pull Request Process

1. **Update your branch:**
```bash
git fetch upstream
git rebase upstream/main
```

2. **Test your changes:**
- Ensure backend runs without errors
- Ensure frontend builds successfully
- Test new features manually
- Run existing tests

3. **Create Pull Request:**
- Use a clear, descriptive title
- Reference related issues
- Describe what changes were made
- Include screenshots for UI changes
- List any breaking changes

4. **PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] All tests pass
- [ ] Added new tests

## Screenshots
(if applicable)

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No console errors
- [ ] Backward compatible
```

## Project Structure

```
Configurable-Researcher-Agent/
├── backend/
│   ├── modules/          # Research modules
│   ├── utils/            # Utility functions
│   ├── config.py         # Configuration
│   ├── models.py         # Data models
│   └── main.py           # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── utils/        # Frontend utilities
│   └── public/           # Static assets
└── docs/                 # Documentation
```

## Areas for Contribution

### High Priority
- [ ] Real API integrations (OpenAI, news APIs, financial APIs)
- [ ] User authentication system
- [ ] Data visualization with charts
- [ ] Advanced caching mechanisms
- [ ] Comprehensive test suite

### Medium Priority
- [ ] More research modules
- [ ] Improved error handling
- [ ] Performance optimizations
- [ ] Internationalization (i18n)
- [ ] Dark mode support

### Nice to Have
- [ ] Mobile app
- [ ] Browser extension
- [ ] Scheduled research
- [ ] Export to multiple formats
- [ ] Collaborative features

## Development Setup Tips

### Backend Hot Reload
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Hot Reload
```bash
npm run dev
```

### Debug Mode
Set environment variables:
```bash
export DEBUG=True
export LOG_LEVEL=DEBUG
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Framer Motion](https://www.framer.com/motion/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## Questions?

- Open an issue for discussion
- Check existing issues and PRs
- Review documentation files

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
