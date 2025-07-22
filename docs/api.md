# PowerGPT API Documentation

This document provides comprehensive documentation for the PowerGPT backend API, including all statistical analysis endpoints, request/response formats, and usage examples.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL](#base-url)
4. [Statistical Test Endpoints](#statistical-test-endpoints)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Examples](#examples)

## 🔍 Overview

The PowerGPT API provides RESTful endpoints for statistical power analysis calculations. Each endpoint accepts JSON parameters and returns calculated sample sizes or other statistical results.

### Key Features

- **R-Python Integration**: Leverages R's statistical packages through Python
- **Comprehensive Coverage**: 15+ statistical test types
- **JSON API**: Standard REST API with JSON request/response
- **Detailed Documentation**: Each endpoint includes comprehensive parameter descriptions
- **Error Handling**: Robust error responses with helpful messages

## 🔐 Authentication

Currently, the API operates without authentication for development purposes. For production deployment, implement authentication using:

```python
# Example authentication header
Authorization: Bearer your-api-token
```

## 🌐 Base URL

```
Development: http://localhost:5000
Production: https://your-domain.com
```

## 📊 Statistical Test Endpoints

### 1. Two-Sample T-Test

**Endpoint:** `POST /api/v1/two_sample_t_test`

**Description:** Calculates sample size for comparing means between two independent groups.

**Parameters:**
```json
{
  "delta": 0.5,    // Difference between group means
  "sd": 1.0,       // Standard deviation
  "power": 0.8     // Desired statistical power
}
```

**Response:**
```json
{
  "result": 64.0
}
```

**Example:**
```bash
curl -X POST "http://localhost:5000/api/v1/two_sample_t_test" \
  -H "Content-Type: application/json" \
  -d '{"delta": 0.5, "sd": 1.0, "power": 0.8}'
```

### 2. Paired T-Test

**Endpoint:** `POST /api/v1/paired_T_test`

**Description:** Calculates sample size for comparing means between paired observations.

**Parameters:**
```json
{
  "d": 0.5,                    // Effect size (Cohen's d)
  "power": 0.8,               // Desired statistical power
  "alternative": "two.sided"  // Alternative hypothesis type
}
```

**Response:**
```json
{
  "result": 34.0
}
```

### 3. One-Sample T-Test

**Endpoint:** `POST /api/v1/one_mean_T_test`

**Description:** Calculates sample size for comparing a sample mean to a population mean.

**Parameters:**
```json
{
  "d": 0.5,                    // Effect size (Cohen's d)
  "power": 0.8,               // Desired statistical power
  "alternative": "two.sided"  // Alternative hypothesis type
}
```

**Response:**
```json
{
  "result": 26.0
}
```

### 4. One-Way ANOVA

**Endpoint:** `POST /api/v1/one_way_ANOVA`

**Description:** Calculates sample size for comparing means across multiple groups.

**Parameters:**
```json
{
  "k": 3,        // Number of groups
  "f": 0.25,     // Effect size (Cohen's f)
  "power": 0.8   // Desired statistical power
}
```

**Response:**
```json
{
  "result": 45.0
}
```

### 5. Log-Rank Test

**Endpoint:** `POST /api/v1/log_rank_test`

**Description:** Calculates sample size for survival analysis comparing two groups.

**Parameters:**
```json
{
  "power": 0.8,  // Desired statistical power
  "k": 1.0,      // Allocation ratio (experimental/control)
  "pE": 0.3,     // Event probability in experimental group
  "pC": 0.5,     // Event probability in control group
  "RR": 0.6      // Relative risk (hazard ratio)
}
```

**Response:**
```json
{
  "result": [156.0, 156.0]
}
```

### 6. Chi-Squared Test

**Endpoint:** `POST /api/v1/chi_squared_test`

**Description:** Calculates sample size for chi-squared test of independence.

**Parameters:**
```json
{
  "w": 0.3,      // Effect size (Cohen's w)
  "df": 1,       // Degrees of freedom
  "power": 0.8   // Desired statistical power
}
```

**Response:**
```json
{
  "result": 88.0
}
```

### 7. Two-Proportions Test

**Endpoint:** `POST /api/v1/two_proportions_test`

**Description:** Calculates sample size for comparing proportions between two groups.

**Parameters:**
```json
{
  "p1": 0.3,                   // Proportion in group 1
  "p2": 0.5,                   // Proportion in group 2
  "power": 0.8,                // Desired statistical power
  "alternative": "two.sided"   // Alternative hypothesis type
}
```

**Response:**
```json
{
  "result": 89.0
}
```

### 8. Single Proportion Test

**Endpoint:** `POST /api/v1/single_proportion_test`

**Description:** Calculates sample size for comparing a sample proportion to a population proportion.

**Parameters:**
```json
{
  "p0": 0.5,                   // Hypothesized population proportion
  "p1": 0.6,                   // Expected sample proportion
  "power": 0.8,                // Desired statistical power
  "alternative": "two.sided"   // Alternative hypothesis type
}
```

**Response:**
```json
{
  "result": 194.0
}
```

### 9. Cox Proportional Hazards

**Endpoint:** `POST /api/v1/cox_ph`

**Description:** Calculates sample size for Cox proportional hazards regression.

**Parameters:**
```json
{
  "power": 0.8,  // Desired statistical power
  "theta": 0.7,  // Hazard ratio
  "p": 0.5,      // Proportion of subjects with covariate = 1
  "psi": 0.3     // Event rate (proportion of subjects with events)
}
```

**Response:**
```json
{
  "result": 234.0
}
```

### 10. Correlation Analysis

**Endpoint:** `POST /api/v1/correlation`

**Description:** Calculates sample size for correlation analysis.

**Parameters:**
```json
{
  "r": 0.5,      // Expected correlation coefficient
  "power": 0.8   // Desired statistical power
}
```

**Response:**
```json
{
  "result": 29.0
}
```

### 11. Kruskal-Wallis Test

**Endpoint:** `POST /api/v1/kruskal-wallace`

**Description:** Calculates sample size for non-parametric multiple group comparison.

**Parameters:**
```json
{
  "k": 3,        // Number of groups
  "f": 0.25,     // Effect size
  "power": 0.8   // Desired statistical power
}
```

**Response:**
```json
{
  "result": 45.0
}
```

### 12. Simple Linear Regression

**Endpoint:** `POST /api/v1/simple_linear_regression`

**Description:** Calculates sample size for simple linear regression analysis.

**Parameters:**
```json
{
  "u": 1,        // Numerator degrees of freedom
  "f2": 0.15,    // Effect size
  "power": 0.8   // Desired statistical power
}
```

**Response:**
```json
{
  "result": 55.0
}
```

### 13. Multiple Linear Regression

**Endpoint:** `POST /api/v1/multiple_linear_regression`

**Description:** Calculates sample size for multiple linear regression analysis.

**Parameters:**
```json
{
  "u": 3,        // Degrees of freedom for numerator
  "f2": 0.15,    // Effect size
  "power": 0.8   // Desired statistical power
}
```

**Response:**
```json
{
  "result": 77.0
}
```

### 14. One-Sample Wilcoxon Test

**Endpoint:** `POST /api/v1/one_mean_wilcoxon`

**Description:** Calculates sample size for non-parametric one-sample test.

**Parameters:**
```json
{
  "d": 0.5,                    // Effect size (Cohen's d)
  "power": 0.8,               // Desired statistical power
  "alternative": "two.sided"  // Alternative hypothesis type
}
```

**Response:**
```json
{
  "result": 26.0
}
```

### 15. Mann-Whitney U Test

**Endpoint:** `POST /api/v1/mann_whitney_test`

**Description:** Calculates sample size for non-parametric two-group comparison.

**Parameters:**
```json
{
  "d": 0.5,                    // Effect size (Cohen's d)
  "power": 0.8,               // Desired statistical power
  "alternative": "two.sided"  // Alternative hypothesis type
}
```

**Response:**
```json
{
  "result": 64.0
}
```

### 16. Paired Wilcoxon Test

**Endpoint:** `POST /api/v1/paired_wilcoxon_test`

**Description:** Calculates sample size for non-parametric paired comparison.

**Parameters:**
```json
{
  "d": 0.5,                    // Effect size (Cohen's d)
  "power": 0.8,               // Desired statistical power
  "alternative": "two.sided"  // Alternative hypothesis type
}
```

**Response:**
```json
{
  "result": 34.0
}
```

## ⚠️ Error Handling

The API returns standard HTTP status codes and detailed error messages:

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Invalid parameters provided"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "power"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "R computation error occurred"
}
```

### Error Codes Reference

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 422 | Validation Error - Missing required fields |
| 500 | Internal Server Error - R computation error |
| 503 | Service Unavailable - R packages not available |

## 🚦 Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider implementing:

```python
# Example rate limiting configuration
RATE_LIMIT = "100/minute"
RATE_LIMIT_STORAGE_URL = "redis://localhost:6379"
```

## 💡 Examples

### Python Client Example

```python
import requests
import json

def calculate_sample_size(test_type, parameters):
    """Calculate sample size using PowerGPT API"""
    
    base_url = "http://localhost:5000"
    endpoint = f"/api/v1/{test_type}"
    
    try:
        response = requests.post(
            f"{base_url}{endpoint}",
            headers={"Content-Type": "application/json"},
            json=parameters
        )
        response.raise_for_status()
        return response.json()["result"]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage
params = {
    "delta": 0.5,
    "sd": 1.0,
    "power": 0.8
}

sample_size = calculate_sample_size("two_sample_t_test", params)
print(f"Required sample size: {sample_size}")
```

### JavaScript Client Example

```javascript
async function calculateSampleSize(testType, parameters) {
    const baseUrl = 'http://localhost:5000';
    const endpoint = `/api/v1/${testType}`;
    
    try {
        const response = await fetch(`${baseUrl}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(parameters)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.result;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Example usage
const params = {
    delta: 0.5,
    sd: 1.0,
    power: 0.8
};

calculateSampleSize('two_sample_t_test', params)
    .then(sampleSize => console.log(`Required sample size: ${sampleSize}`));
```

### R Client Example

```r
library(httr)
library(jsonlite)

calculate_sample_size <- function(test_type, parameters) {
    base_url <- "http://localhost:5000"
    endpoint <- paste0("/api/v1/", test_type)
    
    tryCatch({
        response <- POST(
            url = paste0(base_url, endpoint),
            add_headers("Content-Type" = "application/json"),
            body = toJSON(parameters, auto_unbox = TRUE)
        )
        
        if (status_code(response) == 200) {
            result <- fromJSON(rawToChar(response$content))
            return(result$result)
        } else {
            stop(paste("HTTP error:", status_code(response)))
        }
    }, error = function(e) {
        cat("Error:", e$message, "\n")
        return(NULL)
    })
}

# Example usage
params <- list(delta = 0.5, sd = 1.0, power = 0.8)
sample_size <- calculate_sample_size("two_sample_t_test", params)
cat("Required sample size:", sample_size, "\n")
```

## 📚 Additional Resources

- [Statistical Methods Guide](statistical-methods.md)
- [Deployment Guide](deployment.md)
- [Dify Integration Guide](ai-integration.md)
- [GitHub Repository](https://github.com/your-username/powergpt)

## 🤝 Support

For API support and questions:
- 📧 Email: api-support@powergpt.com
- 📖 Documentation: [docs.powergpt.com/api](https://docs.powergpt.com/api)
- 💬 Discord: [PowerGPT Community](https://discord.gg/powergpt) 