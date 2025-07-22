#!/usr/bin/env python3
"""
PowerGPT AI Endpoints
=====================
FastAPI endpoints that integrate OpenAI GPT with statistical APIs.
Provides natural language interface for statistical power analysis.
"""

import os
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from ai_coordinator import PowerGPTCoordinator, StatisticalQuery, AIResponse

# Create router for AI endpoints
ai_router = APIRouter(prefix="/ai", tags=["AI Integration"])

# Models for AI endpoints
class AIQueryRequest(BaseModel):
    """Request model for AI-powered queries"""
    query: str = Field(..., description="Natural language query for statistical analysis")
    include_educational_content: bool = Field(True, description="Include educational explanations")
    response_format: str = Field("detailed", description="Response format: 'detailed' or 'simple'")

class AIQueryResponse(BaseModel):
    """Response model for AI-powered queries"""
    success: bool = Field(..., description="Whether the query was processed successfully")
    user_query: str = Field(..., description="Original user query")
    extracted_query: Optional[StatisticalQuery] = Field(None, description="Extracted parameters")
    statistical_result: Optional[Dict[str, Any]] = Field(None, description="Statistical calculation result")
    ai_response: Optional[AIResponse] = Field(None, description="AI-generated educational response")
    processing_time: Optional[str] = Field(None, description="Processing time")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    ai_enabled: bool = Field(..., description="Whether AI features are enabled")

class TestInfoRequest(BaseModel):
    """Request model for getting test information"""
    test_type: str = Field(..., description="Type of statistical test")

class TestInfoResponse(BaseModel):
    """Response model for test information"""
    test_type: str = Field(..., description="Type of statistical test")
    description: str = Field(..., description="Description of the test")
    parameters: Dict[str, str] = Field(..., description="Required parameters and descriptions")
    example_query: str = Field(..., description="Example natural language query")
    use_cases: list = Field(..., description="Common use cases")

# Global coordinator instance
_ai_coordinator = None

def get_ai_coordinator() -> PowerGPTCoordinator:
    """Get AI coordinator instance (singleton pattern)"""
    global _ai_coordinator
    if _ai_coordinator is None:
        _ai_coordinator = PowerGPTCoordinator()
    return _ai_coordinator

# AI-powered query endpoint
@ai_router.post("/query", response_model=AIQueryResponse)
async def process_ai_query(
    request: AIQueryRequest
) -> AIQueryResponse:
    """
    Process natural language query for statistical power analysis
    
    This endpoint uses OpenAI GPT to:
    1. Extract statistical parameters from natural language
    2. Call the appropriate statistical API
    3. Generate educational response with interpretation
    
    Example queries:
    - "I need sample size for comparing two groups with 0.5 difference, SD of 1.0, and 80% power"
    - "What sample size do I need for a chi-squared test with effect size 0.3, 1 degree of freedom, and 90% power?"
    - "Help me design a survival analysis study with 80% power, equal allocation, 30% events in treatment, 50% in control, hazard ratio 0.6"
    """
    try:
        coordinator = get_ai_coordinator()
        
        # Process the query through AI coordinator
        result = coordinator.process_query(request.query)
        
        # Check if AI is enabled
        if not result.get("ai_enabled", False):
            return AIQueryResponse(
                success=False,
                user_query=request.query,
                error_message=result.get("error", "AI features are disabled"),
                ai_enabled=False
            )
        
        # Format response based on user preference
        if request.response_format == "simple":
            # Return simplified response
            return AIQueryResponse(
                success=True,
                user_query=request.query,
                statistical_result=result.get("statistical_result"),
                processing_time=result.get("processing_time"),
                ai_enabled=True
            )
        else:
            # Return detailed response with educational content
            return AIQueryResponse(
                success=True,
                user_query=result.get("user_query"),
                extracted_query=StatisticalQuery(**result.get("extracted_query", {})),
                statistical_result=result.get("statistical_result"),
                ai_response=AIResponse(**result.get("ai_response", {})) if request.include_educational_content else None,
                processing_time=result.get("processing_time"),
                ai_enabled=True
            )
            
    except Exception as e:
        coordinator = get_ai_coordinator()
        return AIQueryResponse(
            success=False,
            user_query=request.query,
            error_message=str(e),
            ai_enabled=coordinator.is_ai_enabled()
        )

# Get available tests endpoint
@ai_router.get("/tests", response_model=Dict[str, Any])
async def get_available_tests() -> Dict[str, Any]:
    """
    Get list of available statistical tests and their descriptions
    
    Returns information about all 16 statistical tests supported by PowerGPT
    """
    try:
        coordinator = get_ai_coordinator()
        tests = coordinator.get_available_tests()
        test_info = {}
        
        for test in tests:
            parameters = coordinator.get_test_parameters(test)
            test_info[test] = {
                "description": get_test_description(test),
                "parameters": parameters,
                "example_query": get_example_query(test),
                "use_cases": get_use_cases(test)
            }
        
        return {
            "total_tests": len(tests),
            "available_tests": tests,
            "test_details": test_info,
            "ai_enabled": coordinator.is_ai_enabled()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get test information: {str(e)}")

# Get specific test information endpoint
@ai_router.post("/test-info", response_model=TestInfoResponse)
async def get_test_info(
    request: TestInfoRequest
) -> TestInfoResponse:
    """
    Get detailed information about a specific statistical test
    
    Returns parameter requirements, example queries, and use cases for the specified test
    """
    try:
        coordinator = get_ai_coordinator()
        test_type = request.test_type
        parameters = coordinator.get_test_parameters(test_type)
        
        if not parameters:
            raise HTTPException(status_code=404, detail=f"Test type '{test_type}' not found")
        
        return TestInfoResponse(
            test_type=test_type,
            description=get_test_description(test_type),
            parameters=parameters,
            example_query=get_example_query(test_type),
            use_cases=get_use_cases(test_type)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get test information: {str(e)}")

# Health check endpoint for AI service
@ai_router.get("/health")
async def ai_health_check() -> Dict[str, Any]:
    """
    Health check for AI integration service
    
    Checks if OpenAI API key is configured and service is ready
    """
    try:
        coordinator = get_ai_coordinator()
        ai_enabled = coordinator.is_ai_enabled()
        
        if ai_enabled:
            return {
                "status": "healthy",
                "message": "AI integration service is ready",
                "openai_configured": True,
                "available_tests": 16,
                "ai_enabled": True,
                "timestamp": "2025-07-22T09:42:00Z"
            }
        else:
            return {
                "status": "degraded",
                "message": "AI features are disabled - statistical APIs still available",
                "openai_configured": False,
                "available_tests": 16,
                "ai_enabled": False,
                "timestamp": "2025-07-22T09:42:00Z"
            }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Health check failed: {str(e)}",
            "ai_enabled": False,
            "timestamp": "2025-07-22T09:42:00Z"
        }

# Helper functions for test information
def get_test_description(test_type: str) -> str:
    """Get description for a statistical test"""
    descriptions = {
        "two_sample_t_test": "Compare means between two independent groups",
        "paired_T_test": "Compare means between two related groups (before/after)",
        "one_mean_T_test": "Compare a single group mean to a known value",
        "one_way_ANOVA": "Compare means across three or more independent groups",
        "log_rank_test": "Compare survival curves between groups",
        "chi_squared_test": "Test association between categorical variables",
        "two_proportions_test": "Compare proportions between two groups",
        "single_proportion_test": "Compare a single proportion to a known value",
        "cox_ph": "Analyze survival data with covariates",
        "correlation": "Test correlation between two continuous variables",
        "kruskal-wallace": "Non-parametric alternative to one-way ANOVA",
        "simple_linear_regression": "Test relationship between one predictor and outcome",
        "multiple_linear_regression": "Test relationship between multiple predictors and outcome",
        "one_mean_wilcoxon": "Non-parametric one-sample test",
        "mann_whitney_test": "Non-parametric alternative to two-sample t-test",
        "paired_wilcoxon_test": "Non-parametric alternative to paired t-test"
    }
    return descriptions.get(test_type, "Statistical test for power analysis")

def get_example_query(test_type: str) -> str:
    """Get example natural language query for a test"""
    examples = {
        "two_sample_t_test": "I need sample size for comparing two groups with 0.5 difference, SD of 1.0, and 80% power",
        "paired_T_test": "What sample size do I need for a paired t-test with effect size 0.4 and 80% power?",
        "one_mean_T_test": "Calculate sample size for comparing a group mean to 100 with effect size 0.3 and 90% power",
        "one_way_ANOVA": "I need sample size for ANOVA with 3 groups, effect size 0.25, and 80% power",
        "log_rank_test": "Design a survival study with 80% power, equal groups, 30% events in treatment, 50% in control, hazard ratio 0.6",
        "chi_squared_test": "What sample size do I need for a chi-squared test with effect size 0.3, 1 degree of freedom, and 90% power?",
        "two_proportions_test": "Compare two proportions: 0.3 vs 0.5 with 80% power",
        "single_proportion_test": "Test if proportion differs from 0.5, alternative proportion 0.7, 80% power",
        "cox_ph": "Cox regression with hazard ratio 1.5, 50% events, 50% in experimental group, 80% power",
        "correlation": "Test correlation of 0.5 with 80% power",
        "kruskal-wallace": "Non-parametric ANOVA with 3 groups, effect size 0.25, 80% power",
        "simple_linear_regression": "Simple regression with 1 predictor, effect size 0.15, 80% power",
        "multiple_linear_regression": "Multiple regression with 3 predictors, effect size 0.15, 80% power",
        "one_mean_wilcoxon": "Non-parametric one-sample test with effect size 0.3, 80% power",
        "mann_whitney_test": "Non-parametric two-group comparison with effect size 0.5, 80% power",
        "paired_wilcoxon_test": "Non-parametric paired test with effect size 0.4, 80% power"
    }
    return examples.get(test_type, "Natural language query for statistical power analysis")

def get_use_cases(test_type: str) -> list:
    """Get common use cases for a statistical test"""
    use_cases = {
        "two_sample_t_test": [
            "Clinical trials comparing treatment vs. control",
            "Educational studies comparing teaching methods",
            "Marketing studies comparing product preferences"
        ],
        "paired_T_test": [
            "Before/after intervention studies",
            "Repeated measures designs",
            "Matched case-control studies"
        ],
        "one_mean_T_test": [
            "Quality control testing",
            "Benchmark comparisons",
            "Standard value validation"
        ],
        "one_way_ANOVA": [
            "Multi-arm clinical trials",
            "Educational program comparisons",
            "Product testing across multiple variants"
        ],
        "log_rank_test": [
            "Clinical trials with survival endpoints",
            "Cancer treatment studies",
            "Equipment reliability studies"
        ],
        "chi_squared_test": [
            "Survey response analysis",
            "Disease association studies",
            "Market preference analysis"
        ],
        "two_proportions_test": [
            "Voting preference studies",
            "Disease prevalence comparisons",
            "Success rate comparisons"
        ],
        "single_proportion_test": [
            "Survey response validation",
            "Quality control testing",
            "Prevalence studies"
        ],
        "cox_ph": [
            "Clinical trials with covariates",
            "Risk factor analysis",
            "Prognostic factor studies"
        ],
        "correlation": [
            "Relationship studies",
            "Predictor validation",
            "Association analysis"
        ],
        "kruskal-wallace": [
            "Non-parametric group comparisons",
            "Ordinal data analysis",
            "Robust statistical testing"
        ],
        "simple_linear_regression": [
            "Predictor-outcome relationships",
            "Trend analysis",
            "Forecasting studies"
        ],
        "multiple_linear_regression": [
            "Multivariate analysis",
            "Confounding control",
            "Predictive modeling"
        ],
        "one_mean_wilcoxon": [
            "Non-parametric one-sample testing",
            "Robust mean comparisons",
            "Ordinal data analysis"
        ],
        "mann_whitney_test": [
            "Non-parametric group comparisons",
            "Robust statistical testing",
            "Ordinal data analysis"
        ],
        "paired_wilcoxon_test": [
            "Non-parametric paired comparisons",
            "Robust before/after analysis",
            "Ordinal paired data"
        ]
    }
    return use_cases.get(test_type, ["Statistical power analysis"])

# Example usage and testing
if __name__ == "__main__":
    import uvicorn
    
    # Test the AI endpoints
    print("Testing AI endpoints...")
    
    # This would be integrated into the main FastAPI app
    # For testing, you can run this file directly
    uvicorn.run("ai_endpoints:ai_router", host="0.0.0.0", port=5002, reload=True) 