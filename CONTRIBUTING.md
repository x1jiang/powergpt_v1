# Contributing to PowerGPT

Thank you for your interest in contributing to PowerGPT! This document provides guidelines and information for contributors.

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Pull Request Process](#pull-request-process)
7. [Issue Reporting](#issue-reporting)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- R 4.0+
- Git
- Docker (optional)

### Fork and Clone

1. **Fork the repository**
   - Go to [PowerGPT GitHub repository](https://github.com/your-username/powergpt)
   - Click "Fork" button

2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/powergpt.git
   cd powergpt
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/original-username/powergpt.git
   ```

## 🛠️ Development Setup

### Backend Development

1. **Set up environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Install R dependencies**
   ```bash
   R -e "install.packages(c('pwr', 'survival', 'stats'), repos='https://cran.rstudio.com/')"
   ```

3. **Run development server**
   ```bash
   python app.py
   ```

### Frontend Development

1. **Set up environment**
   ```bash
   cd frontend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run development server**
   ```bash
   python main.py
   ```

### Docker Development

```bash
cd deployment
docker-compose up --build
```

## 📝 Code Style

### Python Code Style

We follow PEP 8 guidelines with some modifications:

- **Line length**: 88 characters (Black formatter)
- **Indentation**: 4 spaces
- **Docstrings**: Google style
- **Type hints**: Required for all functions

### Example Code Style

```python
from typing import Dict, List, Optional
import numpy as np


def calculate_sample_size(
    effect_size: float,
    power: float,
    alpha: float = 0.05
) -> int:
    """Calculate required sample size for statistical test.
    
    Args:
        effect_size: The expected effect size (Cohen's d).
        power: Desired statistical power (0.8 or 0.9).
        alpha: Significance level (default: 0.05).
        
    Returns:
        Required sample size per group.
        
    Raises:
        ValueError: If parameters are invalid.
    """
    if not 0 < power < 1:
        raise ValueError("Power must be between 0 and 1")
    
    # Calculate sample size using R
    result = call_r_function(effect_size, power, alpha)
    
    return int(np.ceil(result))
```

### R Code Style

- **Line length**: 80 characters
- **Indentation**: 2 spaces
- **Naming**: snake_case for functions, camelCase for variables
- **Comments**: Use `#` for comments

### Example R Code Style

```r
# Calculate sample size for two-sample t-test
two_sample_t_test_n <- function(delta, sd, power) {
  # Validate inputs
  if (delta <= 0 || sd <= 0 || power <= 0 || power >= 1) {
    stop("Invalid parameters provided")
  }
  
  # Calculate sample size using pwr package
  result <- pwr.t.test(
    n = NULL,
    d = delta / sd,
    sig.level = 0.05,
    power = power,
    type = "two.sample",
    alternative = "two.sided"
  )
  
  return(ceiling(result$n))
}
```

## 🧪 Testing

### Running Tests

1. **Install test dependencies**
   ```bash
   pip install pytest pytest-cov pytest-asyncio
   ```

2. **Run backend tests**
   ```bash
   cd backend
   pytest tests/ -v --cov=app --cov-report=html
   ```

3. **Run frontend tests**
   ```bash
   cd frontend
   pytest tests/ -v --cov=main --cov-report=html
   ```

### Writing Tests

Create tests in the `tests/` directory:

```python
# tests/test_statistical_tests.py
import pytest
from app import two_sample_t_test


class TestTwoSampleTTest:
    """Test cases for two-sample t-test endpoint."""
    
    def test_valid_parameters(self):
        """Test with valid parameters."""
        params = {
            "delta": 0.5,
            "sd": 1.0,
            "power": 0.8
        }
        
        result = two_sample_t_test(params)
        
        assert result["result"] > 0
        assert isinstance(result["result"], float)
    
    def test_invalid_power(self):
        """Test with invalid power parameter."""
        params = {
            "delta": 0.5,
            "sd": 1.0,
            "power": 1.5  # Invalid power > 1
        }
        
        with pytest.raises(ValueError):
            two_sample_t_test(params)
```

### Test Coverage

We aim for at least 80% test coverage. Run coverage report:

```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View coverage report
```

## 📚 Documentation

### Code Documentation

- **Functions**: Include docstrings with Google style
- **Classes**: Document purpose and methods
- **Modules**: Add module-level docstrings

### API Documentation

- Update API documentation in `docs/api.md`
- Include new endpoints with examples
- Update parameter descriptions

### User Documentation

- Update relevant sections in `docs/`
- Add examples for new features
- Update deployment guides if needed

## 🔄 Pull Request Process

### Before Submitting

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes**
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation

3. **Test your changes**
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Check code style
   black .
   flake8 .
   
   # Run type checking
   mypy .
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new statistical test endpoint"
   ```

### Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tool changes

**Examples:**
```
feat(api): add chi-squared test endpoint
fix(backend): resolve R package installation issue
docs(readme): update deployment instructions
```

### Submitting PR

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create pull request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out PR template

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Other (specify)
   
   ## Testing
   - [ ] Tests pass
   - [ ] Manual testing completed
   - [ ] Documentation updated
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Tests added/updated
   - [ ] Documentation updated
   ```

## 🐛 Issue Reporting

### Before Reporting

1. **Check existing issues**
   - Search for similar issues
   - Check if issue is already reported

2. **Try to reproduce**
   - Test on different environments
   - Check if issue is environment-specific

### Issue Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- R: [e.g., 4.1.2]
- PowerGPT version: [e.g., 1.0.0]

## Additional Information
- Error messages
- Screenshots
- Logs
```

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow project guidelines

### Communication

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Discord**: For real-time chat and support

### Recognition

Contributors will be recognized in:
- GitHub contributors list
- Project documentation
- Release notes

## 📋 Development Workflow

### Feature Development

1. **Create issue** for feature request
2. **Fork repository** and create feature branch
3. **Implement feature** with tests and documentation
4. **Submit pull request** with detailed description
5. **Code review** and address feedback
6. **Merge** when approved

### Bug Fixes

1. **Create issue** with reproduction steps
2. **Create fix branch** from main
3. **Implement fix** with regression tests
4. **Submit pull request** with fix description
5. **Review and merge**

### Release Process

1. **Version bump** in appropriate files
2. **Update changelog** with new features/fixes
3. **Create release tag**
4. **Deploy to production**
5. **Announce release**

## 🔧 Development Tools

### Recommended Tools

- **IDE**: VS Code, PyCharm, or Vim
- **Linting**: flake8, pylint
- **Formatting**: Black, isort
- **Type Checking**: mypy
- **Testing**: pytest
- **Documentation**: Sphinx

### VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-python.mypy-type-checker",
    "ms-vscode.vscode-r"
  ]
}
```

---

Thank you for contributing to PowerGPT! Your contributions help make statistical analysis more accessible to researchers worldwide. 