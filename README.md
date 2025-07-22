# PowerGPT: AI-Powered Statistical Power Analysis Platform  

PowerGPT is an innovative AI-powered statistical power analysis platform that bridges R statistical computing with Python web services. It provides comprehensive power analysis for 16 statistical methods with a beautiful web interface and seamless AI integration.

### 🏆 **Excellence Highlights**

- **🚀 High Performance**: Sub-second response times (< 0.01s average)
- **🎨 Beautiful Interface**: Professional web design with university branding
- **📚 Educational Value**: Comprehensive tutorials and explanations
- **🤖 AI Integration**: OpenAI GPT functional calling layer for natural language queries
- **🔗 Dify Platform**: Seamless integration with AI development platforms
- **🐳 Production Ready**: Docker deployment with microservices
- **📖 Complete Documentation**: Comprehensive guides and examples

### 🤖 **AI Functional Calling Layer**

PowerGPT now includes a comprehensive AI functional calling layer that integrates OpenAI GPT with statistical APIs:

#### **Core AI Features**
- **Natural Language Processing**: Convert user queries to statistical parameters using GPT
- **Intelligent Parameter Extraction**: Automatically identify test types and extract parameters
- **Educational Response Generation**: Create detailed interpretations with statistical context
- **Interactive Chat Interface**: Beautiful web-based chat for real-time statistical consulting

#### **AI Architecture**
```
User Query → AI Coordinator → OpenAI GPT → Parameter Extraction → 
Statistical API → Result Processing → Educational Response → User
```

#### **Example AI Queries**
- "I need sample size for comparing two groups with 0.5 difference, SD of 1.0, and 80% power"
- "What sample size do I need for a chi-squared test with effect size 0.3, 1 degree of freedom, and 90% power?"
- "Help me design a survival analysis study with 80% power, equal allocation, 30% events in treatment, 50% in control, hazard ratio 0.6"

#### **AI Endpoints**
- **`/ai/query`**: Process natural language queries
- **`/ai/tests`**: Get information about available statistical tests
- **`/ai/test-info`**: Get detailed test information and examples
- **`/ai/health`**: Check AI service status

### 📊 **Statistical Methods Supported**
- **T-Tests**: Two-Sample, One-Mean, Paired
- **Proportions**: Two Proportions, Single Proportion
- **ANOVA & Regression**: One-Way ANOVA, Simple/Multiple Linear Regression
- **Non-Parametric**: Kruskal-Wallace, Wilcoxon Tests, Mann-Whitney
- **Survival Analysis**: Cox Proportional Hazards, Log-Rank Test
- **Other**: Chi-Squared Test, Correlation Analysis

### 🏗️ **Architecture**

```
powergpt_v1/
├── backend/           # FastAPI + R statistical engine + AI coordinator
├── frontend/          # Web interface with university pages + AI chat
├── deployment/        # Docker & microservices setup
├── docs/             # Comprehensive documentation
└── README.md         # This file
```

### 🚀 **Quick Start**

#### Prerequisites
- Python 3.9+
- R 4.4.2+
- OpenAI API key (for AI features)
- Docker (optional)

#### Installation
```bash
# Clone repository
git clone https://github.com/your-username/powergpt.git
cd powergpt

# Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Install R packages
R -e "install.packages(c('pwr', 'survival', 'stats', 'MASS'), repos='https://cran.rstudio.com/')"

# Set OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Start services
cd backend && python -c "import uvicorn; uvicorn.run('app:app', host='0.0.0.0', port=5000)" &
cd frontend && python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000)" &

# Access application
open http://localhost:8000
```

#### AI Chat Interface
```bash
# Access the AI chat interface
open http://localhost:8000/ai-chat
```



### 🤖 **AI Integration Examples**

#### Natural Language Query
```bash
curl -X POST "http://localhost:5000/ai/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I need sample size for comparing two groups with 0.5 difference, SD of 1.0, and 80% power",
    "include_educational_content": true,
    "response_format": "detailed"
  }'
```

#### Response Format
```json
{
  "success": true,
  "user_query": "I need sample size for comparing two groups...",
  "extracted_query": {
    "test_type": "two_sample_t_test",
    "parameters": {
      "delta": 0.5,
      "sd": 1.0,
      "power": 0.8
    },
    "confidence": 0.95
  },
  "statistical_result": {
    "result": 63.76576371427719
  },
  "ai_response": {
    "sample_size": 63.77,
    "interpretation": "For your two-sample t-test...",
    "assumptions": ["Independent observations", "Normal distribution"],
    "recommendations": ["Consider using 64 participants per group"],
    "educational_context": "The two-sample t-test is used to compare..."
  }
}
```

### 📚 **Documentation**

- **[📖 Complete Documentation](docs/)** - API, deployment, statistical methods
- **[🚀 Deployment Guide](docs/deployment.md)** - Production deployment
- **[🤖 AI Integration](docs/ai-integration.md)** - OpenAI GPT and Dify platform setup
- **[📊 Statistical Methods](docs/statistical-methods.md)** - Educational guide



### 🌟 **Innovation Highlights**

1. **R-Python Bridge**: Novel statistical computing integration
2. **AI Functional Calling**: OpenAI GPT integration for natural language queries
3. **Educational AI Responses**: Detailed interpretations and statistical context
4. **Multi-Institution**: Scalable architecture for universities
5. **Educational Excellence**: Comprehensive tutorials
6. **Production Ready**: Modern microservices architecture

### 📈 **Performance Metrics**

- **API Response Time**: < 0.01 seconds average
- **Reliability**: Consistent results
- **Scalability**: Docker microservices ready
- **AI Integration**: Real-time natural language processing

### 🤝 **Contributing**

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

### 📄 **License**

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

### 🙏 **Acknowledgments**

- R statistical computing community
- FastAPI framework developers
- OpenAI for GPT integration capabilities
- University partners and collaborators
- Open source community contributors

---
