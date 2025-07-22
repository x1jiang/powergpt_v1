# PowerGPT AI Integration Guide

This guide provides comprehensive instructions for integrating PowerGPT with AI platforms, particularly OpenAI GPT, to create powerful AI-driven statistical consulting applications.

## 📋 Table of Contents

1. [Overview](#overview)
2. [AI Functional Calling Layer](#ai-functional-calling-layer)
3. [OpenAI GPT Integration](#openai-gpt-integration)
4. [Dify Platform Integration](#dify-platform-integration)
5. [Custom AI Integration](#custom-ai-integration)
6. [Workflow Examples](#workflow-examples)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## 🔍 Overview

PowerGPT is designed to seamlessly integrate with AI platforms, enabling intelligent statistical consulting through natural language interactions. The platform provides RESTful APIs that can be easily integrated with any AI chatbot or conversational AI system.

### Key Integration Features

- **Natural Language Processing**: Convert user queries to statistical parameters
- **Real-time Calculations**: Instant power analysis results
- **Educational Responses**: Detailed explanations of statistical concepts
- **Multi-modal Support**: Text, voice, and visual interactions
- **Institutional Customization**: Branded experiences for different organizations

## 🤖 AI Functional Calling Layer

### Core Components

PowerGPT now includes a comprehensive AI functional calling layer that integrates OpenAI GPT with statistical APIs:

#### 1. **AI Coordinator (`ai_coordinator.py`)**
- **Parameter Extraction**: Uses GPT to extract statistical parameters from natural language
- **API Orchestration**: Coordinates calls between GPT and statistical APIs
- **Response Generation**: Creates educational responses with interpretations
- **Error Handling**: Robust error handling and validation

#### 2. **AI Endpoints (`ai_endpoints.py`)**
- **Natural Language Queries**: `/ai/query` endpoint for processing natural language
- **Test Information**: `/ai/tests` and `/ai/test-info` for educational content
- **Health Monitoring**: `/ai/health` for service status

#### 3. **Chat Interface (`ai_chat_interface.html`)**
- **Interactive Chat**: Beautiful web-based chat interface
- **Real-time Responses**: Live statistical analysis with educational content
- **Example Queries**: Pre-built examples for easy testing

### Architecture

```
User Query → AI Coordinator → OpenAI GPT → Parameter Extraction → 
Statistical API → Result Processing → Educational Response → User
```

### Key Features

1. **Intelligent Parameter Extraction**
   - Automatically identifies statistical test type from natural language
   - Extracts required parameters with confidence scoring
   - Handles missing parameters with reasonable defaults

2. **Educational Response Generation**
   - Provides detailed interpretations of results
   - Lists statistical assumptions and requirements
   - Offers study design recommendations
   - Includes educational context about statistical concepts

3. **Comprehensive Test Coverage**
   - All 16 statistical methods supported
   - Parameter validation and error handling
   - Example queries and use cases for each test

## 🚀 OpenAI GPT Integration

### Setup

1. **Install Dependencies**
   ```bash
   pip install openai>=1.0.0 requests>=2.31.0 python-dotenv>=1.0.0
   ```

2. **Configure Environment Variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   export POWERGPT_BASE_URL="http://localhost:5000"
   ```

3. **Start the Backend**
   ```bash
   cd backend
   python -c "import uvicorn; uvicorn.run('app:app', host='0.0.0.0', port=5000)"
   ```

### API Usage

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
    "assumptions": [
      "Independent observations",
      "Normal distribution",
      "Equal variances"
    ],
    "recommendations": [
      "Consider using 64 participants per group",
      "Plan for potential dropout rates"
    ],
    "educational_context": "The two-sample t-test is used to compare..."
  }
}
```

### Web Interface

Access the interactive chat interface at: `http://localhost:8000/ai-chat`

Features:
- Real-time natural language processing
- Beautiful chat interface with typing indicators
- Example queries for easy testing
- Detailed result display with educational content

## 🤖 Dify Platform Integration

### What is Dify?

Dify is an open-source LLM app development platform that enables developers to create AI applications with visual workflows. PowerGPT is specifically optimized for Dify integration.

### Integration Architecture

```
User Query → Dify Workflow → PowerGPT API → Statistical Result → AI Response
```

### Step-by-Step Dify Setup

#### 1. Dify Account Setup

1. **Create Account**
   - Visit [dify.ai](https://dify.ai)
   - Sign up for a free account
   - Create a new workspace

2. **Configure API Keys**
   - Go to Settings → API Keys
   - Generate a new API key
   - Note down the key for PowerGPT configuration

#### 2. PowerGPT Backend Deployment

Before integrating with Dify, deploy your PowerGPT backend:

```bash
# Deploy to Google Cloud Run (recommended)
gcloud run deploy powergpt-backend \
  --source backend/ \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2 \
  --allow-unauthenticated

# Note the service URL for Dify configuration
```

#### 3. Create Dify Application

1. **Create New Workflow**
   - Name: "PowerGPT Statistical Analysis"
   - Type: Chat Application

2. **Configure System Prompt**
   ```
   You are PowerGPT, an AI-powered statistical consultant. You can perform power analysis for various statistical tests including:
   
   - T-tests (one-sample, two-sample, paired)
   - ANOVA and regression analysis
   - Non-parametric tests
   - Survival analysis
   - Proportion tests
   
   When users ask for power analysis, use the PowerGPT API to calculate sample sizes and provide detailed explanations.
   ```

3. **Add API Integration**
   - Method: POST
   - URL: `https://your-backend-url.com/ai/query`
   - Headers: `Content-Type: application/json`
   - Body: 
   ```json
   {
     "query": "{{user_query}}",
     "include_educational_content": true,
     "response_format": "detailed"
   }
   ```

#### 4. API Endpoint Mapping

| Statistical Test | Dify API Endpoint | Parameters |
|------------------|-------------------|------------|
| Two-Sample T-Test | `/ai/query` | Natural language query |
| Log-Rank Test | `/ai/query` | Natural language query |
| Chi-Squared Test | `/ai/query` | Natural language query |
| All Tests | `/ai/query` | Natural language query |

### Advanced Dify Configuration

#### 1. Conditional Logic

Add conditional nodes to handle different scenarios:

```yaml
# Parameter Validation Node
Condition: {{api_response.success}} == true
Action: Continue to response generation
Else: Ask for clarification

# Error Handling Node
Condition: {{api_response.error_message}} is not null
Action: Provide helpful error message
Else: Continue to response generation
```

#### 2. Multi-step Workflows

For complex queries, create multi-step workflows:

```
User Input → Query Classification → AI Processing → 
Result Validation → Response Generation
```

#### 3. Context Memory

Enable conversation memory in Dify settings:

```yaml
Memory Type: Conversation
Max Tokens: 4000
Include: Previous statistical calculations and explanations
```

## 🔧 Custom AI Integration

### OpenAI Integration

```python
import openai
import requests
import json

class PowerGPTClient:
    def __init__(self, openai_api_key, powergpt_url):
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.powergpt_url = powergpt_url
    
    def analyze_query(self, user_query):
        # Use PowerGPT's AI endpoint directly
        response = requests.post(
            f"{self.powergpt_url}/ai/query",
            json={
                "query": user_query,
                "include_educational_content": True,
                "response_format": "detailed"
            }
        )
        
        return response.json()
```

### LangChain Integration

```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import requests

class PowerGPTLangChain:
    def __init__(self, openai_api_key, powergpt_url):
        self.llm = OpenAI(api_key=openai_api_key)
        self.powergpt_url = powergpt_url
        
    def process_query(self, query):
        # Use PowerGPT's AI endpoint
        response = requests.post(
            f"{self.powergpt_url}/ai/query",
            json={
                "query": query,
                "include_educational_content": True,
                "response_format": "detailed"
            }
        )
        
        return response.json()
```

### Custom Chatbot Integration

```javascript
// Node.js example
const axios = require('axios');

class PowerGPTChatbot {
    constructor(powergptUrl) {
        this.powergptUrl = powergptUrl;
    }
    
    async processMessage(message) {
        try {
            const result = await axios.post(
                `${this.powergptUrl}/ai/query`,
                {
                    query: message,
                    include_educational_content: true,
                    response_format: "detailed"
                }
            );
            
            return result.data;
            
        } catch (error) {
            return {
                success: false,
                error_message: "I'm sorry, I couldn't process your request. Please try again."
            };
        }
    }
}
```

## 📊 Workflow Examples

### Example 1: Simple T-Test Query

**User Input:** "I need sample size for comparing two groups with 0.5 difference, SD of 1.0, and 80% power"

**AI Processing:**
1. **Parameter Extraction:**
   ```json
   {
     "test_type": "two_sample_t_test",
     "parameters": {
       "delta": 0.5,
       "sd": 1.0,
       "power": 0.8
     },
     "confidence": 0.95
   }
   ```

2. **Statistical Calculation:**
   ```json
   {"result": 63.76576371427719}
   ```

3. **Educational Response:**
   ```
   For your two-sample t-test comparing two independent groups, you'll need 64 participants per group (128 total) to detect a difference of 0.5 with 80% power, assuming a standard deviation of 1.0.
   
   This test is appropriate when comparing means between two independent groups, such as treatment vs. control in a randomized trial. The effect size (delta = 0.5) represents a medium effect according to Cohen's guidelines.
   ```

### Example 2: Survival Analysis Query

**User Input:** "Design a survival study with 80% power, equal groups, 30% events in treatment, 50% in control, hazard ratio 0.6"

**AI Processing:**
1. **Parameter Extraction:**
   ```json
   {
     "test_type": "log_rank_test",
     "parameters": {
       "power": 0.8,
       "k": 1.0,
       "pE": 0.3,
       "pC": 0.5,
       "RR": 0.6
     },
     "confidence": 0.92
   }
   ```

2. **Statistical Calculation:**
   ```json
   {"result": [156.0, 156.0]}
   ```

3. **Educational Response:**
   ```
   For your log-rank test comparing survival curves between two groups, you'll need 156 participants per group (312 total) to detect a hazard ratio of 0.6 with 80% power.
   
   This test is appropriate for survival analysis studies where you're comparing time-to-event outcomes between groups. The hazard ratio of 0.6 indicates that the treatment group has a 40% reduction in the hazard rate compared to the control group.
   ```

## 🔍 Troubleshooting

### Common Issues

#### 1. OpenAI API Key Issues

**Problem:** "OpenAI API key not configured"
**Solution:**
```bash
# Set environment variable
export OPENAI_API_KEY="your-api-key-here"

# Or create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

#### 2. API Connection Errors

**Problem:** Cannot connect to PowerGPT API
**Solution:**
```bash
# Check if backend is running
curl http://localhost:5000/health

# Check AI service health
curl http://localhost:5000/ai/health

# Verify URL configuration
echo $POWERGPT_BASE_URL
```

#### 3. Parameter Extraction Failures

**Problem:** AI fails to extract correct parameters
**Solution:**
- Check the query format and clarity
- Ensure the statistical test is supported
- Review the confidence score in the response
- Try rephrasing the query

#### 4. Response Generation Issues

**Problem:** AI generates unclear or incorrect responses
**Solution:**
- Check if educational content is enabled
- Verify the response format setting
- Review the API response structure

### Debug Mode

Enable debug mode for troubleshooting:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

def debug_integration(user_query, extracted_params, api_result):
    """Debug integration workflow"""
    
    logging.debug(f"User Query: {user_query}")
    logging.debug(f"Extracted Parameters: {extracted_params}")
    logging.debug(f"API Result: {api_result}")
    
    # Add your debug logic here
```

### Performance Monitoring

Monitor integration performance:

```python
import time
from functools import wraps

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logging.info(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@monitor_performance
def process_user_query(query):
    # Your integration logic here
    pass
```

## 🎯 Best Practices

### 1. Query Formulation
- Be specific about the statistical test you want to use
- Include all required parameters clearly
- Use standard statistical terminology
- Provide context about your research question

### 2. Error Handling
- Always check the `success` field in responses
- Handle API errors gracefully
- Provide helpful error messages to users
- Log errors for debugging

### 3. Performance Optimization
- Cache frequently used results
- Use appropriate response formats
- Monitor API response times
- Implement rate limiting if needed

### 4. User Experience
- Provide clear examples and templates
- Include educational content in responses
- Offer multiple response formats
- Implement progressive disclosure

---

For additional support with AI integration, please refer to our [Support Documentation](support.md) or contact our team. 