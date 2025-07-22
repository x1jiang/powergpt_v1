# PowerGPT Statistical Methods Guide

This comprehensive guide explains all statistical methods supported by PowerGPT, including their applications, assumptions, and practical considerations for study design.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Parametric Tests](#parametric-tests)
3. [Non-Parametric Tests](#non-parametric-tests)
4. [Survival Analysis](#survival-analysis)
5. [Proportion Tests](#proportion-tests)
6. [Regression Analysis](#regression-analysis)
7. [Correlation Analysis](#correlation-analysis)
8. [Effect Size Guidelines](#effect-size-guidelines)
9. [Study Design Considerations](#study-design-considerations)

## 🔍 Overview

PowerGPT supports 16 different statistical methods for power analysis, covering the most common research scenarios in clinical trials, observational studies, and experimental research. Each method is implemented using R's statistical packages and provides accurate sample size calculations.

### Key Features

- **Comprehensive Coverage**: From basic t-tests to complex survival analysis
- **Educational Content**: Detailed explanations of each method
- **Practical Guidance**: Real-world applications and considerations
- **Effect Size Support**: Built-in effect size calculators and guidelines
- **Assumption Checking**: Clear documentation of test assumptions

## 📊 Parametric Tests

### 1. Two-Sample T-Test

**Purpose**: Compare means between two independent groups

**When to Use**:
- Comparing treatment vs. control groups
- Assessing differences between two populations
- Clinical trials with continuous outcomes

**Parameters**:
- `delta`: Difference between group means
- `sd`: Standard deviation (assumed equal in both groups)
- `power`: Desired statistical power (typically 0.8 or 0.9)

**Assumptions**:
- Normally distributed data
- Equal variances (homoscedasticity)
- Independent observations
- Random sampling

**Example Application**:
```
Clinical trial comparing blood pressure reduction between drug A and placebo
- Expected difference: 5 mmHg
- Standard deviation: 10 mmHg
- Desired power: 80%
- Result: 64 participants per group
```

### 2. Paired T-Test

**Purpose**: Compare means between related observations (before/after, matched pairs)

**When to Use**:
- Pre-post intervention studies
- Crossover trials
- Matched case-control studies
- Repeated measures on same subjects

**Parameters**:
- `d`: Effect size (Cohen's d)
- `power`: Desired statistical power
- `alternative`: "two.sided", "greater", or "less"

**Assumptions**:
- Normally distributed differences
- Independent pairs
- Random sampling

**Example Application**:
```
Weight loss program evaluation
- Pre-post weight measurements
- Expected effect size: 0.5 (medium effect)
- Desired power: 80%
- Result: 34 participants
```

### 3. One-Sample T-Test

**Purpose**: Compare a sample mean to a known or hypothesized population mean

**When to Use**:
- Quality control studies
- Comparing to historical data
- Testing against theoretical values
- Single-group intervention studies

**Parameters**:
- `d`: Effect size (Cohen's d)
- `power`: Desired statistical power
- `alternative`: "two.sided", "greater", or "less"

**Assumptions**:
- Normally distributed data
- Independent observations
- Random sampling

**Example Application**:
```
Comparing student test scores to national average
- Expected difference: 0.5 standard deviations
- Desired power: 80%
- Result: 26 participants
```

### 4. One-Way ANOVA

**Purpose**: Compare means across three or more independent groups

**When to Use**:
- Multi-arm clinical trials
- Comparing multiple treatments
- Experimental designs with multiple conditions
- Survey research with multiple groups

**Parameters**:
- `k`: Number of groups
- `f`: Effect size (Cohen's f)
- `power`: Desired statistical power

**Assumptions**:
- Normally distributed data in each group
- Equal variances across groups
- Independent observations
- Random sampling

**Example Application**:
```
Three-arm clinical trial (placebo, low dose, high dose)
- Number of groups: 3
- Expected effect size: 0.25 (medium)
- Desired power: 80%
- Result: 45 participants per group
```

## 🔄 Non-Parametric Tests

### 5. Mann-Whitney U Test

**Purpose**: Non-parametric alternative to two-sample t-test

**When to Use**:
- Non-normally distributed data
- Ordinal data
- Small sample sizes
- When parametric assumptions are violated

**Parameters**:
- `d`: Effect size (Cohen's d)
- `power`: Desired statistical power
- `alternative`: "two.sided", "greater", or "less"

**Assumptions**:
- Independent observations
- Ordinal or continuous data
- Random sampling

**Example Application**:
```
Comparing pain scores between treatment groups
- Non-normally distributed pain scale data
- Expected effect size: 0.5
- Desired power: 80%
- Result: 64 participants per group
```

### 6. Wilcoxon Signed-Rank Test

**Purpose**: Non-parametric alternative to paired t-test

**When to Use**:
- Non-normally distributed paired data
- Ordinal paired measurements
- Small sample sizes with paired observations

**Parameters**:
- `d`: Effect size (Cohen's d)
- `power`: Desired statistical power
- `alternative`: "two.sided", "greater", or "less"

**Assumptions**:
- Paired observations
- Ordinal or continuous data
- Random sampling

**Example Application**:
```
Patient satisfaction scores before/after intervention
- Non-normally distributed satisfaction data
- Expected effect size: 0.5
- Desired power: 80%
- Result: 34 participants
```

### 7. Kruskal-Wallis Test

**Purpose**: Non-parametric alternative to one-way ANOVA

**When to Use**:
- Non-normally distributed data across multiple groups
- Ordinal data with multiple groups
- When ANOVA assumptions are violated

**Parameters**:
- `k`: Number of groups
- `f`: Effect size
- `power`: Desired statistical power

**Assumptions**:
- Independent observations
- Ordinal or continuous data
- Random sampling

**Example Application**:
```
Comparing quality of life scores across four treatment groups
- Non-normally distributed QoL data
- Number of groups: 4
- Expected effect size: 0.25
- Desired power: 80%
- Result: 45 participants per group
```

## ⏰ Survival Analysis

### 8. Log-Rank Test

**Purpose**: Compare survival curves between two groups

**When to Use**:
- Time-to-event outcomes
- Clinical trials with survival endpoints
- Cancer research
- Any study with censored data

**Parameters**:
- `power`: Desired statistical power
- `k`: Allocation ratio (experimental/control)
- `pE`: Event probability in experimental group
- `pC`: Event probability in control group
- `RR`: Relative risk (hazard ratio)

**Assumptions**:
- Proportional hazards
- Independent observations
- Random sampling
- Non-informative censoring

**Example Application**:
```
Cancer treatment trial
- 5-year survival comparison
- Equal allocation (k = 1.0)
- 30% survival in treatment group
- 50% survival in control group
- Hazard ratio: 0.6
- Desired power: 80%
- Result: 156 participants per group
```

### 9. Cox Proportional Hazards

**Purpose**: Multivariate survival analysis with covariates

**When to Use**:
- Survival analysis with multiple predictors
- Adjusting for confounding variables
- Complex survival models
- When covariates affect survival time

**Parameters**:
- `power`: Desired statistical power
- `theta`: Hazard ratio
- `p`: Proportion with covariate = 1
- `psi`: Event rate

**Assumptions**:
- Proportional hazards
- Independent observations
- Random sampling
- Non-informative censoring

**Example Application**:
```
Survival analysis adjusting for age and gender
- Hazard ratio of interest: 0.7
- 50% of subjects have covariate = 1
- Event rate: 30%
- Desired power: 80%
- Result: 234 participants
```

## 📈 Proportion Tests

### 10. Single Proportion Test

**Purpose**: Compare a sample proportion to a known population proportion

**When to Use**:
- Survey research
- Quality control
- Comparing to historical rates
- Single-group studies with binary outcomes

**Parameters**:
- `p0`: Hypothesized population proportion
- `p1`: Expected sample proportion
- `power`: Desired statistical power
- `alternative`: "two.sided", "greater", or "less"

**Assumptions**:
- Independent observations
- Random sampling
- Large enough sample for normal approximation

**Example Application**:
```
Vaccination rate survey
- Hypothesized rate: 50%
- Expected rate: 60%
- Desired power: 80%
- Result: 194 participants
```

### 11. Two-Proportions Test

**Purpose**: Compare proportions between two independent groups

**When to Use**:
- Clinical trials with binary outcomes
- Survey comparisons
- A/B testing
- Comparing success rates

**Parameters**:
- `p1`: Proportion in group 1
- `p2`: Proportion in group 2
- `power`: Desired statistical power
- `alternative`: "two.sided", "greater", or "less"

**Assumptions**:
- Independent observations
- Random sampling
- Large enough samples for normal approximation

**Example Application**:
```
Drug efficacy trial
- Success rate in treatment: 70%
- Success rate in control: 50%
- Desired power: 80%
- Result: 89 participants per group
```

### 12. Chi-Squared Test

**Purpose**: Test for association between categorical variables

**When to Use**:
- Contingency table analysis
- Testing independence
- Goodness-of-fit tests
- Categorical data analysis

**Parameters**:
- `w`: Effect size (Cohen's w)
- `df`: Degrees of freedom
- `power`: Desired statistical power

**Assumptions**:
- Independent observations
- Random sampling
- Expected frequencies ≥ 5

**Example Application**:
```
Disease association study
- Effect size: 0.3 (medium)
- Degrees of freedom: 1 (2x2 table)
- Desired power: 80%
- Result: 88 participants
```

## 📊 Regression Analysis

### 13. Simple Linear Regression

**Purpose**: Analyze relationship between two continuous variables

**When to Use**:
- Predicting continuous outcomes
- Assessing linear relationships
- Correlation analysis
- Simple predictive modeling

**Parameters**:
- `u`: Numerator degrees of freedom (1 for simple regression)
- `f2`: Effect size
- `power`: Desired statistical power

**Assumptions**:
- Linear relationship
- Independent observations
- Normally distributed residuals
- Homoscedasticity

**Example Application**:
```
Predicting blood pressure from age
- Effect size: 0.15 (medium)
- Desired power: 80%
- Result: 55 participants
```

### 14. Multiple Linear Regression

**Purpose**: Analyze relationships with multiple predictors

**When to Use**:
- Complex predictive modeling
- Adjusting for confounders
- Multivariate analysis
- Complex study designs

**Parameters**:
- `u`: Degrees of freedom for numerator
- `f2`: Effect size
- `power`: Desired statistical power

**Assumptions**:
- Linear relationships
- Independent observations
- Normally distributed residuals
- Homoscedasticity
- No multicollinearity

**Example Application**:
```
Predicting outcomes with 3 predictors
- Effect size: 0.15
- Degrees of freedom: 3
- Desired power: 80%
- Result: 77 participants
```

## 🔗 Correlation Analysis

### 15. Pearson Correlation

**Purpose**: Measure strength and direction of linear relationship

**When to Use**:
- Assessing associations
- Exploratory data analysis
- Psychometric studies
- Relationship analysis

**Parameters**:
- `r`: Expected correlation coefficient
- `power`: Desired statistical power

**Assumptions**:
- Linear relationship
- Bivariate normal distribution
- Independent observations

**Example Application**:
```
Correlation between height and weight
- Expected correlation: 0.5
- Desired power: 80%
- Result: 29 participants
```

## 📏 Effect Size Guidelines

### Cohen's Effect Size Standards

| Effect Size | Small | Medium | Large |
|-------------|-------|--------|-------|
| **Cohen's d** | 0.2 | 0.5 | 0.8 |
| **Cohen's f** | 0.1 | 0.25 | 0.4 |
| **Cohen's w** | 0.1 | 0.3 | 0.5 |
| **Correlation r** | 0.1 | 0.3 | 0.5 |

### Practical Interpretation

**Small Effects (0.1-0.3)**:
- Subtle differences
- May require large sample sizes
- Often clinically meaningful despite small magnitude

**Medium Effects (0.3-0.5)**:
- Moderate differences
- Balance between detectability and practical significance
- Most common target in research

**Large Effects (0.5+)**:
- Substantial differences
- Easier to detect with smaller samples
- May indicate strong interventions or clear relationships

## 🎯 Study Design Considerations

### Sample Size Planning

1. **Primary Outcome**: Base sample size on primary endpoint
2. **Multiple Comparisons**: Adjust for multiple testing
3. **Attrition**: Plan for expected dropout rates
4. **Subgroup Analysis**: Ensure adequate power for subgroups

### Power Analysis Strategy

1. **Define Effect Size**: Use literature, pilot data, or clinical judgment
2. **Set Alpha Level**: Typically 0.05 (adjust for multiple comparisons)
3. **Choose Power**: 80% minimum, 90% preferred for important studies
4. **Consider Practical Constraints**: Budget, time, participant availability

### Common Pitfalls

1. **Underpowered Studies**: Insufficient sample size for meaningful effects
2. **Overpowered Studies**: Unnecessarily large samples for trivial effects
3. **Ignoring Assumptions**: Failing to verify test assumptions
4. **Multiple Testing**: Not adjusting for multiple comparisons

### Best Practices

1. **Pilot Studies**: Use pilot data to estimate effect sizes
2. **Literature Review**: Base effect sizes on similar studies
3. **Clinical Input**: Consult with clinical experts on meaningful differences
4. **Sensitivity Analysis**: Test sample size across range of effect sizes
5. **Documentation**: Clearly document power analysis assumptions

## 🔧 Practical Examples

### Clinical Trial Design

```
Phase II Clinical Trial
- Primary outcome: Change in symptom score
- Expected difference: 2 points (SD = 4)
- Desired power: 80%
- Alpha: 0.05
- Result: 64 participants per group
- Plan for 20% attrition: 80 participants per group
```

### Survey Research

```
Customer Satisfaction Survey
- Comparing satisfaction between two products
- Expected difference: 10% (70% vs 60%)
- Desired power: 80%
- Alpha: 0.05
- Result: 89 participants per group
```

### Observational Study

```
Epidemiological Study
- Association between exposure and disease
- Expected odds ratio: 2.0
- Exposure prevalence: 30%
- Desired power: 80%
- Result: 156 participants
```

---

For specific implementation details and API usage, please refer to our [API Documentation](api.md). For deployment and integration guidance, see our [Deployment Guide](deployment.md). 