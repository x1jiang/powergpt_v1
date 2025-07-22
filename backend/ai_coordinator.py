#!/usr/bin/env python3
"""
PowerGPT AI Coordinator
=======================
AI-powered functional calling layer that integrates OpenAI GPT with statistical APIs.
This module provides intelligent parameter extraction, query understanding, and 
educational response generation for statistical power analysis.
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from fastapi import HTTPException
import openai
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StatisticalQuery(BaseModel):
    """Model for statistical query processing"""
    user_query: str = Field(..., description="Natural language query from user")
    test_type: Optional[str] = Field(None, description="Identified statistical test type")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Extracted parameters")
    confidence: Optional[float] = Field(None, description="Confidence in parameter extraction")

class AIResponse(BaseModel):
    """Model for AI-generated responses"""
    sample_size: Optional[float] = Field(None, description="Calculated sample size")
    interpretation: str = Field(..., description="Educational interpretation")
    assumptions: List[str] = Field(default_factory=list, description="Statistical assumptions")
    recommendations: List[str] = Field(default_factory=list, description="Study design recommendations")
    educational_context: str = Field(..., description="Educational explanation")

class PowerGPTCoordinator:
    """
    AI Coordinator for PowerGPT - Integrates OpenAI GPT with statistical APIs
    """
    
    def __init__(self, openai_api_key: Optional[str] = None, powergpt_base_url: str = "http://localhost:5001"):
        """
        Initialize the AI Coordinator
        
        Args:
            openai_api_key: OpenAI API key (if None, will try to get from environment)
            powergpt_base_url: Base URL for PowerGPT API
        """
        # Get OpenAI API key from parameter, environment, or prompt user
        self.openai_api_key = self._get_openai_api_key(openai_api_key)
        self.powergpt_base_url = powergpt_base_url
        self.available_tests = [
            "two_sample_t_test", "paired_T_test", "one_mean_T_test",
            "one_way_ANOVA", "log_rank_test", "chi_squared_test",
            "two_proportions_test", "single_proportion_test", "cox_ph",
            "correlation", "kruskal-wallace", "simple_linear_regression",
            "multiple_linear_regression", "one_mean_wilcoxon",
            "mann_whitney_test", "paired_wilcoxon_test"
        ]
        
        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
        
        logger.info("PowerGPT AI Coordinator initialized")
    
    def _get_openai_api_key(self, api_key: Optional[str] = None) -> str:
        """
        Get OpenAI API key from various sources
        
        Args:
            api_key: Directly provided API key
            
        Returns:
            OpenAI API key string
        """
        # First, try the provided API key
        if api_key:
            return api_key
        
        # Second, try environment variable
        env_key = os.getenv("OPENAI_API_KEY")
        if env_key:
            logger.info("Using OpenAI API key from environment variable")
            return env_key
        
        # Third, try .env file (already loaded by load_dotenv())
        env_file_key = os.getenv("OPENAI_API_KEY")
        if env_file_key:
            logger.info("Using OpenAI API key from .env file")
            return env_file_key
        
        # Finally, prompt user for API key
        logger.warning("OpenAI API key not found in environment or .env file")
        print("\n" + "="*60)
        print("🤖 PowerGPT AI Integration Setup")
        print("="*60)
        print("To use AI-powered natural language queries, you need an OpenAI API key.")
        print("You can:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Add OPENAI_API_KEY=your-key to .env file")
        print("3. Enter your API key now (it will be used for this session only)")
        print("="*60)
        
        user_key = input("Enter your OpenAI API key (or press Enter to skip AI features): ").strip()
        
        if user_key:
            logger.info("Using OpenAI API key from user input")
            return user_key
        else:
            logger.warning("No OpenAI API key provided - AI features will be disabled")
            return ""
    
    def is_ai_enabled(self) -> bool:
        """Check if AI features are enabled"""
        return bool(self.openai_api_key)
    
    def extract_parameters(self, user_query: str) -> StatisticalQuery:
        """
        Extract statistical parameters from natural language query using GPT
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            StatisticalQuery with extracted parameters
        """
        if not self.is_ai_enabled():
            raise HTTPException(
                status_code=503, 
                detail="AI features are disabled. Please provide an OpenAI API key."
            )
        
        try:
            # Create system prompt for parameter extraction
            system_prompt = f"""
            You are an expert statistical consultant specializing in power analysis.
            
            Extract statistical parameters from user queries and identify the appropriate test type.
            
            Available statistical tests: {', '.join(self.available_tests)}
            
            Return a JSON object with:
            - test_type: the appropriate statistical test from the available list
            - parameters: object with required parameters for the test
            - confidence: confidence score (0-1) in your extraction
            - explanation: brief explanation of what the user wants
            
            Parameter requirements for each test:
            - two_sample_t_test: {{"delta": float, "sd": float, "power": float}}
            - paired_T_test: {{"d": float, "power": float, "alternative": "two.sided"}}
            - one_mean_T_test: {{"d": float, "power": float, "alternative": "two.sided"}}
            - one_way_ANOVA: {{"k": int, "f": float, "power": float}}
            - log_rank_test: {{"power": float, "k": float, "pE": float, "pC": float, "RR": float}}
            - chi_squared_test: {{"w": float, "df": int, "power": float}}
            - two_proportions_test: {{"p1": float, "p2": float, "power": float, "alternative": "two.sided"}}
            - single_proportion_test: {{"p0": float, "p1": float, "power": float, "alternative": "two.sided"}}
            - cox_ph: {{"power": float, "theta": float, "p": float, "psi": float}}
            - correlation: {{"r": float, "power": float}}
            - kruskal-wallace: {{"k": int, "f": float, "power": float}}
            - simple_linear_regression: {{"u": int, "f2": float, "power": float}}
            - multiple_linear_regression: {{"u": int, "f2": float, "power": float}}
            - one_mean_wilcoxon: {{"d": float, "power": float, "alternative": "two.sided"}}
            - mann_whitney_test: {{"d": float, "power": float}}
            - paired_wilcoxon_test: {{"d": float, "power": float, "alternative": "two.sided"}}
            
            Be precise and extract all required parameters. If parameters are missing, estimate reasonable defaults.
            """
            
            # Call OpenAI for parameter extraction
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=500
            )
            
            # Parse the response
            content = response.choices[0].message.content
            extracted_data = json.loads(content)
            
            return StatisticalQuery(
                user_query=user_query,
                test_type=extracted_data.get("test_type"),
                parameters=extracted_data.get("parameters"),
                confidence=extracted_data.get("confidence", 0.0)
            )
            
        except Exception as e:
            logger.error(f"Error extracting parameters: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Parameter extraction failed: {str(e)}")
    
    def call_statistical_api(self, test_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the PowerGPT statistical functions directly
        
        Args:
            test_type: Type of statistical test
            parameters: Parameters for the test
            
        Returns:
            API response with results
        """
        try:
            # Import the app module to access statistical functions
            import app
            
            # Map test types to function names
            test_function_map = {
                "two_sample_t_test": app.two_sample_t_test,
                "paired_T_test": app.paired_t_test,
                "one_mean_T_test": app.one_mean_T_test,
                "one_way_ANOVA": app.one_way_ANOVA,
                "log_rank_test": app.log_rank_test,
                "chi_squared_test": app.chi_squared_test,
                "two_proportions_test": app.two_proportions_test,
                "single_proportion_test": app.single_proportion_test,
                "cox_ph": app.cox_ph,
                "correlation": app.correlation,
                "kruskal-wallace": app.kruskal_wallace,
                "simple_linear_regression": app.simple_linear_regression,
                "multiple_linear_regression": app.multiple_linear_regression,
                "one_mean_wilcoxon": app.one_mean_wilcoxon,
                "mann_whitney_test": app.mann_whitney_test_n,
                "paired_wilcoxon_test": app.paired_wilcoxon_test
            }
            
            if test_type not in test_function_map:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unknown test type: {test_type}"
                )
            
            # Create the appropriate model instance
            model_class_map = {
                "two_sample_t_test": app.TwoSampleTTest,
                "paired_T_test": app.PairedTTest,
                "one_mean_T_test": app.OneMeanTTestParams,
                "one_way_ANOVA": app.OneWayANOVAParams,
                "log_rank_test": app.LogRankTest,
                "chi_squared_test": app.ChiSquaredTestParams,
                "two_proportions_test": app.TwoProportionsTestParams,
                "single_proportion_test": app.SingleProportionTestParams,
                "cox_ph": app.CoxPhParams,
                "correlation": app.Correlation,
                "kruskal-wallace": app.KruskalWallace,
                "simple_linear_regression": app.SimpleLinearRegression,
                "multiple_linear_regression": app.MultipleLinearRegression,
                "one_mean_wilcoxon": app.OneMeanWilcoxon,
                "mann_whitney_test": app.MannWhitneyTest,
                "paired_wilcoxon_test": app.PairedWilcoxonTest
            }
            
            model_class = model_class_map[test_type]
            model_instance = model_class(**parameters)
            
            # Call the function directly
            result = test_function_map[test_type](model_instance)
            
            return result
                
        except Exception as e:
            logger.error(f"Statistical function call failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Statistical function call failed: {str(e)}")
    
    def generate_educational_response(
        self, 
        user_query: str, 
        test_type: str, 
        parameters: Dict[str, Any], 
        api_result: Dict[str, Any]
    ) -> AIResponse:
        """
        Generate educational response using GPT
        
        Args:
            user_query: Original user query
            test_type: Statistical test type
            parameters: Parameters used
            api_result: Results from statistical API
            
        Returns:
            AIResponse with educational content
        """
        if not self.is_ai_enabled():
            # Return a basic response without AI
            return AIResponse(
                sample_size=api_result.get("result"),
                interpretation=f"Sample size calculation completed for {test_type}",
                assumptions=["Please consult statistical literature for assumptions"],
                recommendations=["Consider consulting with a statistician"],
                educational_context=f"This is a {test_type} power analysis result."
            )
        
        try:
            # Create system prompt for response generation
            system_prompt = f"""
            You are PowerGPT, an AI-powered statistical consultant specializing in power analysis.
            
            Generate a comprehensive, educational response that includes:
            
            1. Clear explanation of the statistical test and its purpose
            2. Interpretation of the sample size result
            3. Statistical assumptions that should be met
            4. Practical recommendations for study design
            5. Educational context about power analysis
            
            Be conversational, educational, and helpful. Use clear language that researchers can understand.
            Include practical advice and explain the implications of the results.
            
            Return a JSON object with:
            - sample_size: the calculated sample size
            - interpretation: detailed interpretation of results
            - assumptions: list of statistical assumptions
            - recommendations: list of study design recommendations
            - educational_context: educational explanation of the test
            """
            
            # Prepare context for GPT
            context = f"""
            User Query: {user_query}
            Statistical Test: {test_type}
            Parameters Used: {json.dumps(parameters, indent=2)}
            API Result: {json.dumps(api_result, indent=2)}
            """
            
            # Call OpenAI for response generation
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,  # Higher temperature for creative responses
                max_tokens=1000
            )
            
            # Parse the response
            content = response.choices[0].message.content
            response_data = json.loads(content)
            
            return AIResponse(
                sample_size=response_data.get("sample_size"),
                interpretation=response_data.get("interpretation", ""),
                assumptions=response_data.get("assumptions", []),
                recommendations=response_data.get("recommendations", []),
                educational_context=response_data.get("educational_context", "")
            )
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            # Return a basic response on error
            return AIResponse(
                sample_size=api_result.get("result"),
                interpretation=f"Sample size calculation completed for {test_type}",
                assumptions=["Please consult statistical literature for assumptions"],
                recommendations=["Consider consulting with a statistician"],
                educational_context=f"This is a {test_type} power analysis result."
            )
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Complete AI-powered query processing pipeline
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Complete response with statistical results and educational content
        """
        try:
            logger.info(f"Processing query: {user_query}")
            
            # Step 1: Extract parameters using GPT (if AI is enabled)
            if self.is_ai_enabled():
                extracted_query = self.extract_parameters(user_query)
                logger.info(f"Extracted parameters: {extracted_query}")
                
                # Step 2: Call statistical API
                api_result = self.call_statistical_api(
                    extracted_query.test_type, 
                    extracted_query.parameters
                )
                logger.info(f"API result: {api_result}")
                
                # Step 3: Generate educational response
                ai_response = self.generate_educational_response(
                    user_query,
                    extracted_query.test_type,
                    extracted_query.parameters,
                    api_result
                )
                
                # Step 4: Compile complete response
                complete_response = {
                    "timestamp": datetime.now().isoformat(),
                    "user_query": user_query,
                    "extracted_query": extracted_query.dict(),
                    "statistical_result": api_result,
                    "ai_response": ai_response.dict(),
                    "processing_time": "real-time",
                    "ai_enabled": True
                }
            else:
                # Fallback: return error message
                complete_response = {
                    "timestamp": datetime.now().isoformat(),
                    "user_query": user_query,
                    "error": "AI features are disabled. Please provide an OpenAI API key.",
                    "ai_enabled": False
                }
            
            logger.info("Query processing completed successfully")
            return complete_response
            
        except Exception as e:
            logger.error(f"Query processing failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")
    
    def get_available_tests(self) -> List[str]:
        """Get list of available statistical tests"""
        return self.available_tests
    
    def get_test_parameters(self, test_type: str) -> Dict[str, Any]:
        """Get parameter requirements for a specific test"""
        parameter_requirements = {
            "two_sample_t_test": {
                "delta": "Effect size (difference between groups)",
                "sd": "Standard deviation",
                "power": "Desired power (0-1)"
            },
            "paired_T_test": {
                "d": "Effect size (Cohen's d)",
                "power": "Desired power (0-1)",
                "alternative": "Alternative hypothesis ('two.sided', 'greater', 'less')"
            },
            "one_mean_T_test": {
                "d": "Effect size (Cohen's d)",
                "power": "Desired power (0-1)",
                "alternative": "Alternative hypothesis"
            },
            "one_way_ANOVA": {
                "k": "Number of groups",
                "f": "Effect size (Cohen's f)",
                "power": "Desired power (0-1)"
            },
            "log_rank_test": {
                "power": "Desired power (0-1)",
                "k": "Allocation ratio",
                "pE": "Event rate in experimental group",
                "pC": "Event rate in control group",
                "RR": "Risk ratio"
            },
            "chi_squared_test": {
                "w": "Effect size (Cohen's w)",
                "df": "Degrees of freedom",
                "power": "Desired power (0-1)"
            },
            "two_proportions_test": {
                "p1": "Proportion in group 1",
                "p2": "Proportion in group 2",
                "power": "Desired power (0-1)",
                "alternative": "Alternative hypothesis"
            },
            "single_proportion_test": {
                "p0": "Null proportion",
                "p1": "Alternative proportion",
                "power": "Desired power (0-1)",
                "alternative": "Alternative hypothesis"
            },
            "cox_ph": {
                "power": "Desired power (0-1)",
                "theta": "Hazard ratio",
                "p": "Proportion of events",
                "psi": "Proportion of subjects in experimental group"
            },
            "correlation": {
                "r": "Correlation coefficient",
                "power": "Desired power (0-1)"
            },
            "kruskal-wallace": {
                "k": "Number of groups",
                "f": "Effect size",
                "power": "Desired power (0-1)"
            },
            "simple_linear_regression": {
                "u": "Number of predictors",
                "f2": "Effect size (f²)",
                "power": "Desired power (0-1)"
            },
            "multiple_linear_regression": {
                "u": "Number of predictors",
                "f2": "Effect size (f²)",
                "power": "Desired power (0-1)"
            },
            "one_mean_wilcoxon": {
                "d": "Effect size (Cohen's d)",
                "power": "Desired power (0-1)",
                "alternative": "Alternative hypothesis"
            },
            "mann_whitney_test": {
                "d": "Effect size (Cohen's d)",
                "power": "Desired power (0-1)"
            },
            "paired_wilcoxon_test": {
                "d": "Effect size (Cohen's d)",
                "power": "Desired power (0-1)",
                "alternative": "Alternative hypothesis"
            }
        }
        
        return parameter_requirements.get(test_type, {})

# Example usage and testing
if __name__ == "__main__":
    # Initialize coordinator (will prompt for API key if not found)
    coordinator = PowerGPTCoordinator()
    
    # Test query processing
    test_query = "I need to calculate sample size for a two-group comparison with expected difference of 0.5, standard deviation of 1.0, and 80% power"
    
    try:
        result = coordinator.process_query(test_query)
        print("Test Result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Test failed: {str(e)}") 