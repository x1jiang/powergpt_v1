# app.py
# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return render_template("index.html", title="Hello")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import rpy2.robjects as robjects
import uvicorn
from ai_endpoints import ai_router

app = FastAPI(
    title='PowerGPT API - AI-Powered Statistical Power Analysis',
    description='A comprehensive API for statistical power analysis with AI integration',
    version='2.0',
    openapi_url="/api/v1/openapi.json"
)

# Include AI endpoints
app.include_router(ai_router)

# Define the Pydantic model for input parameters
class AddNumbers(BaseModel):
    a: int
    b: int

class TwoSampleTTest(BaseModel):
    delta: float
    sd: float
    power: float

class LogRankTest(BaseModel):
    power: float
    k: float # ratio of participants in experimental/treatment group compared to group C (control group).
    pE: float # probability of failure in treatment group over the maximum time period of the study (t years).
    pC: float # probability of failure in group C (control group) over the maximum time period of the study (t years).
    RR: float # postulated hazard ratio

class PairedTTest(BaseModel):
    d: float
    power: float
    alternative: str

class TwoProportionsTestParams(BaseModel):
    p1: float  
    p2: float
    power: float  # Power of the test
    alternative: str  # Alternative hypothesis: "two.sided", "greater", or "less"

class ChiSquaredTestParams(BaseModel):
    w: float  # Effect size
    df: int  # Degrees of freedom
    power: float  # Power of the test

class OneMeanTTestParams(BaseModel):
    d: float  # Effect size
    power: float  # Power of the test
    alternative: str  # Alternative hypothesis: "two.sided", "greater", or "less"

class OneWayANOVAParams(BaseModel):
    k: int  # Number of groups
    f: float  # Effect size
    power: float  # Power of the test

class SingleProportionTestParams(BaseModel):
    p0: float  
    p1: float
    power: float  # Power of the test
    alternative: str  # Alternative hypothesis: "two.sided", "greater", or "less"

class CoxPhParams(BaseModel):
    power: float  # Power of the test
    theta: float #postulated hazard ratio
    p: float #proportion of subjects taking value one for the covariate of interest (in equal allocation, p = 0.5)
    psi: float #proportion of subjects died of the disease of interest (event rate)
    
class Correlation(BaseModel):
    r: float  # Correlation coefficient
    power: float  # Power of the test

class KruskalWallace(BaseModel):
    k: int  # Number of groups
    f: float  # Effect size
    power: float  # Power of the test

class SimpleLinearRegression(BaseModel):
  u:float=1
  f2:float
  power:float

class MultipleLinearRegression(BaseModel):
    u: float  # degrees of freedom for numerator
    f2: float  # effect size
    power: float  # desired statistical power

class OneMeanWilcoxon(BaseModel):
    d: float  # effect size (Cohen's d)
    power: float  # desired statistical power
    alternative: str = "two.sided"  # type of alternative hypothesis

class MannWhitneyTest(BaseModel):
   d: float
   power: float
   alternative: str = "two.sided"  # type of alternative hypothesis

class PairedWilcoxonTest(BaseModel):
    d: float  # effect size (Cohen's d)
    power: float  # desired statistical power
    alternative: str = "two.sided"  # type of alternative hypothesis    

    
@app.post('/api/v1/add')
def add_two_numbers(add_numbers: AddNumbers):
    '''Add two numbers using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("sum.r")

    print("Getting the add_numbers function from R")
    # Get the add_numbers function from R
    add_numbers_r = robjects.globalenv['add_numbers']

    print(f"Calling the R function with a={add_numbers.a} and b={add_numbers.b}")
    # Call the R function
    result = add_numbers_r(add_numbers.a, add_numbers.b)

    print(f"Returning the result: {result[0]}")
    # Return the result
    return {"result": int(result[0])}

@app.post('/api/v1/two_sample_t_test')
def two_sample_t_test(twosamplettest_n: TwoSampleTTest):
    """
    This function calculates the sample size required to achieve a target power for a two-sample t-test using an R function.
    
    Purpose:
    The task of this function is to determine the number of samples required in each group to detect a specified difference 
    in the means of two independent groups. This is useful when designing studies or experiments that involve comparing 
    two groups using continuous outcomes, where the difference between groups is assumed to be normally distributed.

    Key Considerations for the Agent:
    - Use this function when the problem requires calculating the sample size for a two-sample t-test scenario.
    - This function is ideal for scenarios where the agent knows the user is comparing **means** between two groups and wants to 
      ensure the study is powered to detect a certain effect size (difference in means).
    - If the user provides a specific **difference between means** (referred to as delta), along with the **standard deviation** 
      (sd) of the outcome and a desired level of **power** (probability of detecting the effect), this is the appropriate function to call.

    Parameters:
    - **delta**: The magnitude of the difference in means between the two groups. This is the expected or hypothesized 
      difference that the user wants to detect. For example, this might represent the difference in average treatment 
      effects between a treatment group and a control group.
    - **sd**: The standard deviation of the outcome variable, which reflects the variability of the data across both groups. 
      The higher the variability, the larger the sample size needed to detect a given difference.
    - **power**: The target statistical power (typically 0.80 or 0.90) to detect the difference (delta). Power represents the 
      likelihood of correctly rejecting the null hypothesis when the difference is real. 

    When to Use:
    - Use this function when the task requires determining sample size for studies comparing two independent groups 
      with continuous outcomes.
    - This is relevant when the user needs to design a study or experiment and has specified the desired power, the 
      expected difference between group means (delta), and the expected standard deviation (sd) of the outcome.
    - This function is appropriate when the user asks for a sample size calculation to **compare two groups with continuous outcomes** 
      (e.g., a clinical trial comparing the effectiveness of a drug versus a placebo, where the outcome is a continuous measure 
      like blood pressure or cholesterol levels).

    Example Task for Agent:
    - When the user requests a sample size calculation to detect a difference in means between two groups, and provides 
      parameters like expected difference (delta), standard deviation (sd), and power level, this function should be called. 
    - The agent can also use this function when the problem involves sample size determination for a study design where 
      normally distributed outcomes are assumed.
    """

    '''Calculate sample size for a two-sample t-test using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("twoSampleTTest.R")

    print("Getting the twosamplettest_n function from R")
    # Get the twosamplettest_n function from R
    twosamplettest_n_r = robjects.globalenv['twosamplettest_n']

    print(f"Calling the R function with delta={twosamplettest_n.delta}, sd={twosamplettest_n.sd}, and power={twosamplettest_n.power}")
    # Call the R function
    result = twosamplettest_n_r(twosamplettest_n.delta, twosamplettest_n.sd, twosamplettest_n.power)

    print(f"Returning the result: {result[0]}")
    # Return the result
    return {"result": float(result[0])}
 
@app.post('/api/v1/log_rank_test')
def log_rank_test(logranktest_n: LogRankTest):
    """
    This function calculates the sample size required to achieve a target power for a log-rank test using an R function.

    Purpose:
    The task of this function is to determine the number of samples required to achieve a given power when comparing survival curves 
    between two groups using the log-rank test. This test is commonly used to compare the time-to-event data (e.g., time until death 
    or disease recurrence) in clinical trials or studies with censored data.

    Key Considerations for the Agent:
    - Use this function when the user requests sample size calculation for survival analysis involving **time-to-event data**, 
      especially when comparing two groups (e.g., treatment vs. control).
    - The log-rank test is appropriate when the goal is to compare the survival distributions (or time-to-event distributions) 
      of two groups.
    - If the user provides parameters like **power**, **allocation ratio (k)**, **event probabilities (pE and pC)**, and 
      **relative risk (RR)**, this is the function to use.
    - Use this function when there is a need for a **non-parametric comparison of survival curves** between two groups, and 
      assumptions about proportional hazards apply.

    When to Use the Log-Rank Test:
    - The log-rank test is used when the user wants to compare survival times or time-to-event data between two groups and assumes 
      that the hazard ratio is constant over time (i.e., proportional hazards).
    - It is most suitable when the user is not concerned with covariates (other variables that may affect survival time) and simply 
      wants to compare the survival curves between groups.
    - This test is ideal when the task involves comparing overall survival, disease-free survival, or any time-to-event outcome, 
      typically used in clinical trials with two groups (e.g., treatment vs. control).

    When to Use the Cox Proportional Hazards Model Instead:
    - The **Cox proportional hazards model** should be used when the user needs to **adjust for covariates** (other variables that 
      may influence the time to event) and when a more flexible, semi-parametric model is required.
    - Use the Cox model if the task involves assessing how different factors (covariates) impact survival time, not just comparing 
      the survival distributions of two groups.
    - The Cox model is more appropriate when the user is interested in estimating hazard ratios for multiple covariates, 
      while the log-rank test is focused solely on comparing two survival curves.

    Parameters:
    - **power**: The desired power level (e.g., 0.80 or 0.90) to detect a difference in survival curves between the two groups.
    - **k**: The allocation ratio (number of subjects in the experimental group divided by the number of subjects in the control group). 
      A value of 1 means equal sample sizes in both groups.
    - **pE**: The event probability (e.g., probability of death or event occurrence) in the experimental group.
    - **pC**: The event probability in the control group.
    - **RR**: The relative risk (or hazard ratio) that the user expects between the experimental and control groups. This represents 
      the ratio of the hazard rate in the experimental group to the hazard rate in the control group.

    When to Use:
    - This function should be called when the task involves **survival analysis** and the user provides information about the target 
      power, the expected event rates in the two groups, the allocation ratio, and the expected relative risk.
    - The agent should use this function for sample size calculations in studies comparing survival or time-to-event data across 
      two groups where the assumption of proportional hazards holds and covariates do not need to be adjusted for.

    Example Task for Agent:
    - When the user requests a sample size calculation for comparing survival curves (time-to-event data) between two groups, 
      and provides parameters like the event probabilities (pE and pC), relative risk (RR), power level, and allocation ratio (k), 
      this function should be called.
    - The agent can also use this function when the user specifies a comparison of survival data with no need for adjusting for 
      additional covariates or predictors.
    """


    '''Calculate sample size for a log-rank test using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("logRankTest.R")

    print("Getting the logranktest_n function from R")
    # Get the logranktest_n function from R
    logranktest_n_r = robjects.globalenv['logranktest_n']

    print(f"Calling the R function with power={logranktest_n.power}, k={logranktest_n.k}, pE={logranktest_n.pE}, pC={logranktest_n.pC}, and RR={logranktest_n.RR}")
    # Call the R function
    result = logranktest_n_r(
        logranktest_n.power,
        logranktest_n.k,
        logranktest_n.pE,
        logranktest_n.pC,
        logranktest_n.RR
    )

    print(f"Returning the result: {result[0]}, {result[1]}")
    # Return the result
    return {"result": [float(result[0]), float(result[1])]}

@app.post('/api/v1/paired_T_test')
def paired_t_test(paired_t_test_n: PairedTTest):
    """
    This function calculates the sample size required to achieve a target power for a paired t-test using an R function.

    Purpose:
    The task of this function is to determine the number of paired observations required to achieve a desired power when comparing 
    the means of two related (paired) samples. This is useful in situations where measurements are taken on the same subjects 
    (or related subjects) before and after an intervention, or under two different conditions.

    Key Considerations for the Agent:
    - Use this function when the user requests sample size calculation for a **paired t-test**, which is appropriate for comparing 
      **two related groups** (e.g., pre-test and post-test data).
    - The paired t-test is used when the same subjects are measured twice under different conditions, or when two related subjects 
      (e.g., twins) are compared.
    - This test is ideal for detecting the mean difference between paired observations, and it accounts for the correlation 
      between the paired measurements.
    - If the user provides parameters like **effect size (d)**, **power**, and the type of **alternative hypothesis**, 
      this function should be called.

    When to Use the Paired T-Test:
    - The paired t-test is used when the data consists of **paired observations**, meaning that each data point in one group 
      has a corresponding data point in the other group (e.g., pre- and post-treatment measurements on the same subjects).
    - It is particularly useful for within-subject comparisons, where the interest is in determining if there is a mean difference 
      between two conditions for the same subjects.
    - The test should be used when the agent knows the user is comparing **two related groups** and has measurements that are 
      dependent on each other, such as pre- and post-treatment data, or data from matched pairs (e.g., siblings, twins).

    Parameters:
    - **d (effect size)**: This represents the standardized mean difference between the paired observations. It is calculated as:
        - **d = (mean_2 - mean_1) / pooled standard deviation**, where:
            - `mean_2`: The mean of the second set of measurements (e.g., post-treatment).
            - `mean_1`: The mean of the first set of measurements (e.g., pre-treatment).
            - **Pooled standard deviation** = sqrt((sd1^2 + sd2^2) / 2), where `sd1` and `sd2` are the standard deviations 
              of the two sets of measurements.
        - The effect size `d` quantifies the magnitude of the difference between the two means, adjusted for the variability 
          in the data (pooled standard deviation). A larger effect size indicates a more substantial difference between the 
          paired measurements.
    - **power**: The desired power level (e.g., 0.80 or 0.90) to detect the specified effect size.
    - **alternative**: The type of alternative hypothesis, which specifies whether the user is conducting a two-tailed test 
      (the default) or a one-tailed test. A one-tailed test is appropriate when the user expects the difference to occur in a 
      specific direction.

    When to Use:
    - This function should be called when the task involves comparing two related groups or repeated measurements on the same group 
      and the user has provided information about the expected effect size (d), the desired power level, and the alternative hypothesis.
    - This is the correct function to use when the data involves **paired samples** and the user wants to calculate the sample size 
      needed to detect a difference within pairs (e.g., before vs. after treatment comparisons in the same subjects).

    When to Use Other Tests:
    - If the user is comparing **two independent groups** rather than paired observations, the agent should consider using the 
      two-sample t-test instead of the paired t-test.
    - For comparing survival data or time-to-event outcomes, use the log-rank test or Cox model, depending on whether covariates 
      need to be adjusted.

    Output:
    - The function returns the calculated sample size required to achieve the desired power for detecting a mean difference 
      between paired observations.

    Example Task for Agent:
    - When the user asks for a sample size calculation for a paired comparison (e.g., pre- vs. post-treatment measurements on 
      the same subjects), and provides parameters like the expected effect size (d), power, and the alternative hypothesis, 
      this function should be called.
    - This function is particularly relevant when the user is interested in measuring the effect of an intervention or treatment 
      within the same group of subjects at two different time points.
      
    """

    '''Calculate sample size for a paired t-test using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("paired_T_test.R")

    print("Getting the paired_t_test_n function from R")
    # Get the paired_t_test function from R
    paired_t_test_r = robjects.globalenv['paired_t_test_n']

    print(f"Calling the R function with d={paired_t_test_n.d}, power={paired_t_test_n.power}, alternative={paired_t_test_n.alternative}")
    # Call the R function
    result = paired_t_test_r(
        paired_t_test_n.d,
        paired_t_test_n.power,
        paired_t_test_n.alternative
    )

    print(f"Returning the result: {result[0]}")
    # Return the result
    return {"result": float(result[0])}

@app.post('/api/v1/two_proportions_test')
def two_proportions_test(two_proportions_test_n: TwoProportionsTestParams):
    """
    This function calculates the sample size required to achieve a target power for a two-proportions z-test using an R function.

    Purpose:
    The task of this function is to determine the sample size needed to detect a difference between the proportions of two groups 
    using a z-test for proportions. This is commonly used in situations where the goal is to compare binary outcomes (e.g., 
    success/failure, yes/no) between two independent groups.

    Key Considerations for the Agent:
    - Use this function when the user requests sample size calculation for comparing **two proportions** between independent groups.
    - The two-proportions z-test is appropriate when the outcome is binary (e.g., presence or absence of an event) and the goal 
      is to compare the proportion of successes (or any binary outcome) between two groups.
    - If the user provides parameters like **effect size (h)**, **power**, and the type of **alternative hypothesis**, 
      this function should be called.

    When to Use the Two-Proportions Test:
    - This test is used when comparing the proportions of a binary outcome between two independent groups. For example, it could be 
      used to compare the success rates of a treatment group versus a control group in a clinical trial.
    - It is particularly useful in studies that assess whether the proportion of individuals experiencing a particular outcome 
      (e.g., a disease or recovery) differs between two groups.
    - Use this function when the user is interested in determining the number of subjects required to detect a difference in proportions 
      between two independent groups, given a specific effect size and power.

    Parameters:
    - **h (effect size)**: This represents the standardized difference in proportions between the two groups. It is calculated using 
      the following formula:
        - **h = 2 * arcsin(sqrt(p1)) - 2 * arcsin(sqrt(p2))**, where `p1` is the proportion in group 1 and `p2` is the proportion in group 2.
        - The effect size `h` is a transformation of the difference in proportions that adjusts for the nonlinear nature of proportion 
          differences, making it easier to standardize the magnitude of the effect.
    - **power**: The desired power level (e.g., 0.80 or 0.90) to detect the specified difference in proportions.
    - **alternative**: The type of alternative hypothesis, which specifies whether the user is conducting a two-tailed test 
      (the default) or a one-tailed test. A one-tailed test is appropriate when the user expects a difference in a specific direction 
      between the two proportions.

    When to Use:
    - This function should be called when the task involves comparing the proportions of a binary outcome between two independent groups, 
      and the user has provided the effect size (h), the desired power, and the alternative hypothesis.
    - It is particularly relevant for clinical trials, survey studies, or experiments where the goal is to compare the proportion 
      of successes, failures, or events between two different groups.

    When to Use Other Tests:
    - If the user is comparing **continuous outcomes** between two groups, the agent should consider using the two-sample t-test instead.
    - If the comparison involves **paired binary data** (e.g., before and after measurements within the same subjects), 
      a McNemar test may be more appropriate.

    Output:
    - The function returns the calculated sample size required for each group to achieve the desired power when detecting 
      a difference in proportions.

    Example Task for Agent:
    - When the user requests a sample size calculation for comparing two proportions (e.g., success rates in two independent groups), 
      and provides parameters like the effect size (h), power, and the alternative hypothesis, this function should be called.
    - This function is particularly relevant when the user is interested in detecting a difference in binary outcomes (e.g., event rates) 
      between two groups in a study or trial.
    """

    '''Calculate sample size for a two-proportions test using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("two_proportions_test.R")

    print("Getting the two_proportions_test function from R")
    # Retrieve the function defined in R
    two_proportions_test_r = robjects.globalenv['two_proportions_test_n']

    print(f"Calling the R function with power={two_proportions_test_n.power}, alternative={two_proportions_test_n.alternative}")
    # Call the R function with the parameters from the input model
    result = two_proportions_test_r(
        two_proportions_test_n.p1,
        two_proportions_test_n.p2,
        two_proportions_test_n.power,
        two_proportions_test_n.alternative
    )

    print(f"Returning the result: {result[0]}")
    # Return the result from the R function call
    return {"result": float(result[0])}

@app.post('/api/v1/chi_squared_test')
def chi_squared_test(chi_squared_test_n: ChiSquaredTestParams):
    """
    This function calculates the sample size required to achieve a target power for a chi-squared test using an R function.

    Purpose:
    The task of this function is to determine the sample size required for a chi-squared test to detect an association or 
    difference between categorical variables in a contingency table. The chi-squared test is used to assess whether there is 
    a significant association between two or more categories.

    Key Considerations for the Agent:
    - Use this function when the user requests a sample size calculation for a **chi-squared test**, which is appropriate 
      for comparing categorical data in a contingency table.
    - The chi-squared test is typically used to evaluate whether the distribution of categorical variables differs significantly 
      between groups or if there is an association between two categorical variables (e.g., gender and treatment response).
    - If the user provides parameters like **effect size (w)**, **degrees of freedom (df)**, and **power**, this function should be called.

    When to Use the Chi-Squared Test:
    - The chi-squared test is used when comparing the observed frequencies in categories of a contingency table to the expected 
      frequencies under the assumption of no association between the variables.
    - It is particularly useful for **categorical data** (e.g., yes/no, success/failure, male/female) and can be used to 
      test for independence between variables or goodness of fit.
    - Use this function when the user wants to compare proportions across more than two categories or groups, or when testing 
      for associations between categorical variables (e.g., disease presence and treatment group).

    Parameters:
    - **w (effect size)**: The effect size for the chi-squared test, typically represented by Cohen’s w. It is a measure of 
      the strength of the association between the categorical variables. Cohen’s w is calculated as:
        - **w = sqrt(Σ[(observed - expected)^2 / expected])**
        - A small effect size (w ≈ 0.10) indicates a weak association, a medium effect size (w ≈ 0.30) indicates a moderate 
          association, and a large effect size (w ≈ 0.50) indicates a strong association.
    - **df (degrees of freedom)**: The degrees of freedom for the test, calculated based on the number of categories or groups 
      in the contingency table. For a 2x2 table, df = 1; for larger tables, df is determined by the number of rows and columns 
      (e.g., for a 3x2 table, df = (3-1)*(2-1) = 2).
    - **power**: The desired power level (e.g., 0.80 or 0.90) to detect an association between the categorical variables. Power 
      reflects the probability of correctly rejecting the null hypothesis when an association exists.

    When to Use:
    - This function should be called when the task involves **categorical data analysis**, and the user has provided the effect size (w), 
      degrees of freedom (df), and the desired power level.
    - It is appropriate for studies involving contingency tables where the user needs to calculate the sample size to detect 
      an association or difference between categories (e.g., in survey research, clinical trials, or epidemiological studies).

    When to Use Other Tests:
    - If the data involves **continuous outcomes**, the agent should consider using t-tests or ANOVA instead of the chi-squared test.
    - If the user is comparing binary outcomes across two independent groups, the two-proportions z-test may be more appropriate.
    - If there is only one categorical variable with several levels, the user might be performing a **goodness-of-fit test** 
      (also based on the chi-squared distribution), which may have different degrees of freedom.

    Output:
    - The function returns the calculated sample size required to achieve the desired power for detecting a difference or 
      association between categorical variables in a chi-squared test.

    Example Task for Agent:
    - When the user asks for a sample size calculation for a chi-squared test (e.g., to detect an association between two categorical variables), 
      and provides parameters like the effect size (w), degrees of freedom (df), and power, this function should be called.
    - This function is particularly relevant for surveys, experimental studies, or observational studies that involve 
      comparing proportions across multiple categories (e.g., disease rates across different demographic groups).
    """

    '''Calculate sample size for a chi-squared test using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("chi_squared_test.R")

    print("Getting the chi_squared_test function from R")
    # Retrieve the function defined in R
    chi_squared_test_r = robjects.globalenv['chi_squared_test_n']

    print(f"Calling the R function with w={chi_squared_test_n.w}, df={chi_squared_test_n.df}, power={chi_squared_test_n.power}")
    # Call the R function with the parameters from the input model
    result = chi_squared_test_r(
        chi_squared_test_n.w,
        chi_squared_test_n.df,
        chi_squared_test_n.power
    )

    print(f"Returning the result: {result[0]}")
    # Return the result from the R function call
    return {"result": float(result[0])}

@app.post('/api/v1/one_mean_T_test')
def one_mean_T_test(one_mean_T_test_n: OneMeanTTestParams):
    """
    This function calculates the sample size required to achieve a target power for a one-mean t-test using an R function.

    Purpose:
    The task of this function is to determine the sample size required to detect a difference between a sample mean and a known population mean using a one-sample t-test. This test is used when comparing the mean of a single group to a known or hypothesized value.

    Key Considerations for the Agent:
    - Use this function when the user requests a sample size calculation for a **one-mean t-test**, which is appropriate for testing whether the mean of a single group is significantly different from a known or hypothesized population mean.
    - The one-sample t-test is used when the goal is to compare the observed mean of a single sample to a theoretical mean, under the assumption that the data is normally distributed.
    - If the user provides parameters like **effect size (d)**, **power**, and the type of **alternative hypothesis**, this function should be called.

    When to Use the One-Mean T-Test:
    - The one-sample t-test is used when the user wants to compare the mean of a single sample to a known or hypothesized value (e.g., comparing the average blood pressure of a group to a known population mean).
    - It is particularly useful for determining whether the observed sample mean differs significantly from a reference mean (e.g., testing if a new treatment changes a health metric compared to the population average).
    - Use this function when the task involves calculating the sample size required to detect a difference between the sample mean and a known population mean, given a specific effect size and power.

    Parameters:
    - **d (effect size)**: This represents the standardized mean difference between the sample mean and the population mean. It is calculated as:
        - **d = (mean_sample - mean_population) / standard deviation**.
        - The effect size `d` quantifies the magnitude of the difference between the sample mean and the known population mean. A larger effect size indicates a more substantial difference between the two means.
    - **power**: The desired power level (e.g., 0.80 or 0.90) to detect the specified mean difference.
    - **alternative**: The type of alternative hypothesis, which specifies whether the user is conducting a two-tailed test (the default) or a one-tailed test. A one-tailed test is appropriate when the user expects the mean difference to occur in a specific direction.

    When to Use:
    - This function should be called when the task involves testing the difference between a sample mean and a known or hypothesized population mean, and the user has provided the effect size (d), the desired power level, and the alternative hypothesis.
    - This is particularly relevant for research scenarios where the user wants to determine if the observed mean of a sample significantly deviates from a standard or reference mean (e.g., comparing a test score average to a national average).

    When to Use Other Tests:
    - If the user is comparing **two independent means** (e.g., comparing two separate groups), the agent should consider using the two-sample t-test instead.
    - If the data involves **paired observations** (e.g., before and after measurements on the same subjects), the paired t-test should be used.

    Output:
    - The function returns the calculated sample size required to achieve the desired power for detecting a difference between the sample mean and the population mean.

    Example Task for Agent:
    - When the user requests a sample size calculation for comparing a sample mean to a known or hypothesized population mean, and provides parameters like the effect size (d), power, and the alternative hypothesis, this function should be called.
    - This function is relevant when the user wants to test whether the mean of a group differs from a known or hypothesized value, such as in quality control studies or when testing for changes against a benchmark.
    """

    '''Calculate sample size for a one-mean t-test using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("one_mean_T_test.R")

    print("Getting the one_mean_T_test function from R")
    # Retrieve the function defined in R
    one_mean_T_test_r = robjects.globalenv['one_mean_T_test_n']

    print(f"Calling the R function with d={one_mean_T_test_n.d}, power={one_mean_T_test_n.power}, alternative={one_mean_T_test_n.alternative}")
    # Call the R function with the parameters from the input model
    result = one_mean_T_test_r(
        one_mean_T_test_n.d,
        one_mean_T_test_n.power,
        one_mean_T_test_n.alternative
    )

    print(f"Returning the result: {result[0]}")
    # Return the result from the R function call
    return {"result": float(result[0])}

@app.post('/api/v1/one_way_ANOVA')
def one_way_ANOVA(one_way_ANOVA_n: OneWayANOVAParams):
    """
    This function calculates the sample size required to achieve a target power for a one-way ANOVA using an R function.

    Purpose:
    The task of this function is to determine the sample size required for a one-way analysis of variance (ANOVA) to detect 
    differences between the means of multiple independent groups. This test is used when comparing the means of three or more groups 
    to determine if at least one group differs significantly from the others.

    Key Considerations for the Agent:
    - Use this function when the user requests a sample size calculation for a **one-way ANOVA**, which is appropriate for comparing 
      the means of three or more independent groups.
    - The one-way ANOVA tests the null hypothesis that the means of all groups are equal. If the test is significant, it suggests 
      that at least one group’s mean differs from the others.
    - If the user provides parameters like the **number of groups (k)**, **effect size (f)**, and **power**, this function should be called.

    When to Use the One-Way ANOVA:
    - The one-way ANOVA is used when comparing the means of three or more independent groups. It is commonly applied in experiments 
      or studies where the user wants to test whether there is a significant difference in a continuous outcome variable between groups 
      defined by a single categorical factor (e.g., different treatment groups, different levels of a factor like dosage or diet type).
    - It is particularly useful for understanding whether differences exist across multiple groups, but it does not specify which groups 
      differ—additional post-hoc tests (e.g., Tukey’s test) may be required for that purpose.
    - Use this function when the user is determining the sample size required to detect differences between group means, given a 
      specific effect size and power.

    Parameters:
    - **k (number of groups)**: The number of independent groups being compared. The more groups there are, the larger the 
      required sample size to maintain statistical power.
    - **f (effect size)**: The effect size for the one-way ANOVA, typically represented as Cohen’s f. It quantifies the 
      strength of the difference between group means and is calculated as:
        - **f = sqrt(η² / (1 - η²))**, where η² (eta-squared) represents the proportion of variance explained by the group differences.
        - A small effect size (f ≈ 0.10) suggests minor differences between group means, while a large effect size (f ≈ 0.40) 
          suggests more substantial differences.
    - **power**: The desired power level (e.g., 0.80 or 0.90) to detect a difference between the group means. Power refers 
      to the likelihood of correctly rejecting the null hypothesis if group differences exist.

    When to Use:
    - This function should be called when the task involves comparing the means of three or more independent groups and the user has 
      provided the number of groups (k), effect size (f), and desired power level.
    - It is particularly relevant for studies that involve multiple groups with a single factor of interest, such as clinical trials, 
      educational experiments, or studies comparing different treatment levels or conditions.

    When to Use Other Tests:
    - If the user is comparing **two independent groups**, the agent should consider using the two-sample t-test instead of one-way ANOVA.
    - If the user is comparing more than one factor (e.g., two-way ANOVA), this function is not appropriate, and the agent should 
      consider more complex ANOVA models.

    Output:
    - The function returns the calculated sample size required to achieve the desired power for detecting a difference between 
      the means of multiple independent groups.

    Example Task for Agent:
    - When the user requests a sample size calculation for comparing the means of three or more groups (e.g., different treatment groups), 
      and provides parameters like the number of groups (k), effect size (f), and power, this function should be called.
    - This function is relevant when the user wants to determine if there are significant differences across multiple groups, 
      such as in studies comparing different interventions or treatment levels.
    """
    '''Calculate sample size for a one-way ANOVA using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("one_way_ANOVA.R")

    print("Getting the one_way_ANOVA function from R")
    # Retrieve the function defined in R
    one_way_ANOVA_r = robjects.globalenv['one_way_ANOVA_n']

    print(f"Calling the R function with k={one_way_ANOVA_n.k}, f={one_way_ANOVA_n.f}, power={one_way_ANOVA_n.power}")
    # Call the R function with the parameters from the input model
    result = one_way_ANOVA_r(
        one_way_ANOVA_n.k,
        one_way_ANOVA_n.f,
        one_way_ANOVA_n.power
    )

    print(f"Returning the result: {result[0]}")
    # Return the result from the R function call
    return {"result": float(result[0])}

@app.post('/api/v1/single_proportion_test')
def single_proportion_test(single_proportion_test_n: SingleProportionTestParams):
    """
    This function calculates the sample size required to achieve a target power for a single-proportion z-test using an R function.

    Purpose:
    The task of this function is to determine the sample size required to detect a significant difference between a sample proportion 
    and a hypothesized population proportion. The single-proportion test is used when testing whether the proportion of a binary outcome 
    in a sample is significantly different from a known or hypothesized proportion.

    Key Considerations for the Agent:
    - Use this function when the user requests a sample size calculation for a **single-proportion test**, which is appropriate 
      for comparing a sample proportion to a known or expected population proportion.
    - This test is commonly used in studies or surveys where the user wants to test whether the observed proportion of an event 
      (e.g., success/failure, yes/no) in a sample differs from a specific value.
    - If the user provides parameters like **effect size (h)**, **power**, and the type of **alternative hypothesis**, this function should be called.

    When to Use the Single-Proportion Test:
    - The single-proportion test is used when comparing the observed proportion of a binary outcome in a sample to a hypothesized proportion in the population.
    - It is particularly useful for evaluating whether the proportion of individuals with a certain characteristic in a sample differs 
      from a known or hypothesized population proportion (e.g., determining if the proportion of voters in a sample differs from 
      an expected national proportion).
    - Use this function when the user is determining the sample size required to detect a difference between the sample proportion and a known proportion, 
      given a specific effect size and power.

    Parameters:
    - **h (effect size)**: This represents the standardized difference between the observed sample proportion and the hypothesized population proportion. 
      It is calculated using the following formula:
        - **h = 2 * arcsin(sqrt(p)) - 2 * arcsin(sqrt(p0))**, where `p` is the observed sample proportion and `p0` is the hypothesized population proportion.
        - The effect size `h` adjusts for the nonlinear nature of proportion differences and standardizes the difference between the sample and population proportions.
    - **power**: The desired power level (e.g., 0.80 or 0.90) to detect the specified difference in proportions. Power refers to the likelihood of correctly rejecting the null hypothesis when there is a true difference.
    - **alternative**: The type of alternative hypothesis, which specifies whether the user is conducting a two-tailed test 
      (the default) or a one-tailed test. A one-tailed test is appropriate when the user expects the sample proportion to differ in a specific direction.

    When to Use:
    - This function should be called when the task involves comparing a sample proportion to a known or hypothesized population proportion, 
      and the user has provided the effect size (h), the desired power level, and the alternative hypothesis.
    - It is particularly relevant for studies that involve comparing observed proportions in a sample (e.g., survey responses) 
      to a standard or expected proportion (e.g., national average, historical data).

    When to Use Other Tests:
    - If the user is comparing **two proportions** between two independent groups, the agent should consider using the two-proportions z-test instead.
    - If the data involves **multiple categories** of proportions, consider using a chi-squared test.

    Output:
    - The function returns the calculated sample size required to achieve the desired power for detecting a difference between 
      the sample proportion and the hypothesized population proportion.

    Example Task for Agent:
    - When the user requests a sample size calculation for comparing a sample proportion to a hypothesized population proportion, 
      and provides parameters like the effect size (h), power, and alternative hypothesis, this function should be called.
    - This function is particularly relevant for studies where the user is testing whether the observed proportion of a sample 
      (e.g., proportion of smokers in a population) differs from a known or expected proportion.
    """
    '''Calculate sample size for a single-proportion test using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("single_proportion_test.R")

    print("Getting the single_proportion_test function from R")
    # Retrieve the function defined in R
    single_proportion_test_r = robjects.globalenv['single_proportion_test_n']

    print(f"Calling the R function with power={single_proportion_test_n.power}, alternative={single_proportion_test_n.alternative}")
    # Call the R function with the parameters from the input model
    result = single_proportion_test_r(
        single_proportion_test_n.p0,
         single_proportion_test_n.p1,
        single_proportion_test_n.power,
        single_proportion_test_n.alternative
    )

    print(f"Returning the result: {result[0]}")
    # Return the result from the R function call
    return {"result": float(result[0])}

@app.post('/api/v1/cox_ph')
def cox_ph(cox_ph_n: CoxPhParams):
    """
    This function calculates the sample size required to achieve a target power for a Cox proportional hazards model using an R function.

    Purpose:
    The task of this function is to determine the sample size required for survival analysis using the Cox proportional hazards (Cox PH) model.
    The Cox PH model is a regression method used to examine the effect of several variables on the time a specified event takes to happen,
    commonly used in medical research for analyzing patient survival times.

    Key Considerations for the Agent:
    - Use this function when the user requests a sample size calculation for survival analysis involving the Cox proportional hazards model,
      particularly when the analysis involves covariates.
    - The Cox PH model is appropriate when the user wants to assess the impact of one or more predictor variables on survival time,
      and when the proportional hazards assumption holds (i.e., the effect of the covariates on the hazard rate is constant over time).
    - If the user provides parameters such as **power**, **hazard ratio (theta)**, **proportion of events (p)**, and **variance of the covariate (psi)**,
      this function should be called.
    - This function is suitable when the analysis involves continuous or categorical covariates and when adjusting for confounding variables is necessary.

    When to Use the Cox Proportional Hazards Model:
    - Use this function when the user is interested in modeling the relationship between survival time and one or more predictor variables,
      and requires a sample size calculation that accounts for covariates.
    - The Cox PH model is used when the goal is to estimate hazard ratios for covariates and when adjusting for other variables is important.
    - This function is appropriate when the user wants to perform multivariate survival analysis, unlike the log-rank test which is univariate and does not adjust for covariates.

    When to Use Other Tests:
    - If the user is comparing survival curves between two groups without adjusting for covariates, the **log-rank test** may be more appropriate.
    - Use the log-rank test for sample size calculation when covariates are not considered, and the primary interest is in the difference between two survival curves.

    Parameters:
    - **power**: The desired statistical power (e.g., 0.80 or 0.90) to detect a significant effect of the covariate on survival time.
   #theta: postulated hazard ratio
   #p: proportion of subjects taking value one for the covariate of interest (in equal allocation, p=0.5)
   #psi: proportion of subjects died of the disease of interest (event rate)

    When to Use:
    - This function should be called when the task involves calculating the sample size for a survival analysis using the Cox PH model,
      and the user provides the hazard ratio, proportion of events, covariate variance, and desired power.
    - It is particularly relevant when the study aims to assess the effect of one or more covariates on survival time while adjusting for other factors.

    Output:
    - The function returns the calculated sample size required to achieve the desired power for detecting an effect of the covariate(s) in the Cox PH model.

    Example Task for Agent:
    - When the user requests a sample size calculation for a Cox proportional hazards model, providing parameters like power, hazard ratio, proportion of events,
      and covariate variance, this function should be called.
    - This function is especially useful in clinical trials or cohort studies where survival time is the outcome, and there is a need to adjust for multiple covariates.
    """
    '''Calculate sample size for a cox_ph using an R function'''
    print("Loading the R script")
    # Load the R script
    robjects.r.source("cox_ph.R")

    print("Getting the cox_ph function from R")
    # Retrieve the function defined in R
    cox_ph_r = robjects.globalenv['cox_ph_n']

    print(f"Calling the R function with power={cox_ph_n.power}, theta={cox_ph_n.theta}, p={cox_ph_n.p}, psi={cox_ph_n.psi}")
    # Call the R function with the parameters from the input model
    result = cox_ph_r(
        cox_ph_n.power,
        cox_ph_n.theta,
        cox_ph_n.p,
        cox_ph_n.psi
    )

    print(f"Returning the result: {result[0]}")
    # Return the result from the R function call
    return {"result": float(result[0])}



@app.post('/api/v1/correlation')
def correlation(correlation: Correlation):
    """
    This function calculates the sample size required to achieve a target power for correlation analysis using an R function.

    Purpose:
    The task of this function is to determine the sample size needed for correlation analysis when examining the relationship 
    between two continuous variables. This is commonly used in research where the strength of association between variables 
    needs to be measured.

    Key Considerations for the Agent:
    - Use this function when the user requests sample size calculation for **correlation analysis**.
    - Correlation analysis is appropriate when measuring the strength and direction of association between two continuous variables.
    - If the user provides parameters like **correlation coefficient (r)** and **power**, 
      this function should be called.

    When to Use Correlation Analysis:
    - Use this test when both variables are continuous.
    - When you need to measure the strength and direction of a linear relationship.
    - When you want to determine if there is a significant association between two variables.

    Parameters:
    - **r**: The expected correlation coefficient (between -1 and 1).
    - **power**: The desired power level (e.g., 0.80 or 0.90) to detect the specified correlation.

    When to Use:
    - This function should be called when the task involves measuring correlation between continuous variables.
    - It's particularly useful in research where the strength of relationship between variables needs to be quantified.

    When to Use Other Tests:
    - For categorical variables, consider using chi-square tests.
    - For cause-effect relationships, consider regression analysis.
    - For binary outcomes, consider logistic regression.

    Output:
    - The function returns the calculated sample size required to achieve the desired power for detecting 
      the specified correlation coefficient.

    Example Task for Agent:
    - When the user requests a sample size calculation for a study examining correlation between two variables 
      (e.g., height and weight) and provides the expected correlation coefficient, power, and alternative hypothesis type.
    """

    print("Loading the R script")
    # Load the R script
    robjects.r.source("correlation.R")

    print("Getting the correlation function from R")
    # Retrieve the function defined in R
    correlation_r = robjects.globalenv['correlation']

    print(f"Calling the R function with r={correlation.r}, power={correlation.power}")
    # Call the R function with the parameters from the input model
    result = correlation_r(
        correlation.r,
        correlation.power,
    )

    print(f"Returning the result: {result[0]}")
    # Return the result from the R function call
    return {"result": float(result[0])}



@app.post('/api/v1/kruskal-wallace')
def kruskal_wallace(kruskal_wallace_test: KruskalWallace):
    """
    This function calculates the sample size required for a Kruskal-Wallace test using an R function.

    Purpose:
    The task of this function is to determine the sample size needed for a Kruskal-Wallace test, which is 
    a non-parametric method for comparing two or more independent samples. It's the non-parametric 
    equivalent of one-way ANOVA.

    Key Considerations for the Agent:
    - Use this function when the user requests sample size calculation for **Kruskal-Wallace test**.
    - This test is appropriate when comparing multiple independent groups and the data doesn't meet 
      the normality assumption of ANOVA.
    - If the user provides parameters like **number of groups (k)**, **effect size (f)**, and **power**, 
      this function should be called.

    When to Use Kruskal-Wallace Test:
    - When comparing three or more independent groups
    - When the data doesn't meet normality assumptions
    - When working with ordinal data or ranked measurements

    Parameters:
    - **k**: Number of groups being compared
    - **f**: Effect size (calculated as sqrt(eta^2 / (1-eta^2)))
    - **power**: The desired power level (e.g., 0.80 or 0.90)

    When to Use:
    - When comparing multiple groups and data is not normally distributed
    - When working with ordinal data
    - When sample sizes are small

    When to Use Other Tests:
    - For normally distributed data, consider one-way ANOVA
    - For two groups only, consider Mann-Whitney U test
    - For paired samples, consider Friedman test

    Output:
    - The function returns the calculated sample size required per group to achieve the desired power

    Example Task for Agent:
    - When the user needs to calculate sample size for comparing multiple groups using a non-parametric 
      approach and provides the number of groups, expected effect size, and desired power.
    """

    print("Loading the R script")
    # Load the R script
    robjects.r.source("kruskal_wallace_test.R")

    print("Getting the kruskal_wallace_test function from R")
    # Retrieve the function defined in R
    kruskal_wallace_test_r = robjects.globalenv['kruskal_wallace_test']

    print(f"Calling the R function with k={kruskal_wallace_test.k}, f={kruskal_wallace_test.f}, power={kruskal_wallace_test.power}")
    # Call the R function with the parameters from the input model
    result = kruskal_wallace_test_r(
        kruskal_wallace_test.k,
        kruskal_wallace_test.f,
        kruskal_wallace_test.power
    )

    print(f"Returning the result: {result[0]}")
    # Return the result from the R function call
    return {"result": float(result[0])}


@app.post('/api/v1/simple_linear_regression')
def simple_linear_regression(simple_linear_regression: SimpleLinearRegression):
    """
    This function calculates the sample size required to achieve a target power for a simple linear regression analysis using an 
    R function.
    
    Purpose:
    The task of this function is to determine the number of samples required to detect a specified relationship between two normally
    distributed numerical variables. This is useful when designing studies or experiments that involve measuring the relationship 
    between two continuous variables, where the relationship is assumed to be linear.

    Key Considerations for the Agent:
    - Use this function when the problem requires determining sample size for a simple linear regression analysis scenario.
    - The function is ideal for scenarios where the agent knows the user is measuring the relationship between two continuous variables, 
      where the relationship is assumed to be linear and wants to ensure the study is powered to detect a certain effect size. 
    - If the user provides a specific **effect size** (referred to as f2), along with the **numerator degrees of freedom** (referred to as u), 
      and a desired level of **power** (probability of detecting the effect), this is the appropriate function to call.

    Parameters:
    - **u**: The numerator degrees of freedom. Defaults to 1. For simple linear regression, the numerator degrees of freedom is 1 
      as there is only one predictor. 
    - **f2**: The expected effect size. This is the expected or hypothesized relationship between the predictor and outcome variables 
      that the user wants to detect.
    - **power**: The target statistical power (typically 0.80 or 0.90) to detect the difference (delta). Power represents the 
      likelihood of correctly rejecting the null hypothesis when the difference is real.

    When to Use:
    - Use this function when the task requires determining sample size for studies examining relationships between two continuous 
      variables.
    - This is relevant when the user needs to design a study or experiment and has specified the desired power, the expected effect 
      size (f2), and the numerator degrees of freedom (u).
    - This function is appropriate when the user asks for sample size calculation to measure the relationship between two normally 
      distributed variables.

    Example Task for Agent:
    - When the user requests a sample size calculation to detect a relationship between two continuous variables, and provides parameters 
      like the expected effect size (f2), the numerator degrees of freedom (u), and the desired power level, this function should be called.
    - The agent can also use this function when the problem involves sample size determination for a study design where predictor and 
      outcome variables are assumed to be normally distributed.
    """
    """Calculate sample size for a simple linear regression using an R function"""
    print("Loading the R script")
    # Load the R script
    robjects.r.source("simple_linear_regression.R")

    print("Getting the simple_linear_regression function from R")
    # Get the simple_linear_regression_n function from R
    simple_linear_regression_n_r = robjects.globalenv['simple_linear_regression']

    print(f"Calling the R function with u={simple_linear_regression.u}, "
          f"f2={simple_linear_regression.f2}, "
          f"power={simple_linear_regression.power}")
          
    # Call the R function
    result = simple_linear_regression_n_r(
        simple_linear_regression.u,
        simple_linear_regression.f2,
        simple_linear_regression.power
    )


    print(f"Returning the result: {result[0]}")
    # Return the result
    return {"result": float(result[0])}



@app.post('/api/v1/multiple_linear_regression')
def multiple_linear_regression(multiple_linear_regression: MultipleLinearRegression):
    """
    This function calculates the required sample size for multiple linear regression using an R function.

    Purpose:
    The task of this function is to determine the sample size needed to achieve desired statistical power 
    in multiple linear regression analysis. This is useful when designing studies that involve predicting 
    a continuous outcome using multiple predictor variables.

    Key Considerations for the Agent:
    - Use this function when the problem involves calculating sample size for multiple linear regression analysis.
    - This function is ideal for scenarios where the agent knows the user is examining relationships between 
      multiple predictors and a continuous outcome variable.
    - If the user provides the **degrees of freedom** (u), **effect size** (f2), and desired level of 
      **power**, this is the appropriate function to call.

    Parameters:
    - **u**: The degrees of freedom for numerator, which equals the number of predictor variables in the model. 
      This represents how many independent variables are being used in the regression analysis.
    - **f2**: The effect size, calculated as R/(1-R^2) where R is the correlation coefficient and R^2 is the 
      coefficient of determination (use adjusted R^2). This represents the strength of the relationship between 
      the predictors and the outcome.
    - **power**: The target statistical power (typically 0.80 or 0.90) to detect the specified effect size. 
      Power represents the probability of detecting a true relationship when it exists.

    When to Use:
    - Use this function when designing studies that involve multiple linear regression analysis.
    - This is relevant when the user needs to determine the required sample size to detect specific effect 
      sizes in regression models.
    - This function is particularly appropriate for research involving:
      * Multiple predictor variables
      * Continuous outcome variables
      * Need to account for effect size and desired power

    Example Task for Agent:
    - When the user requests sample size calculations for a multiple regression study and provides parameters 
      like degrees of freedom (u), effect size (f2), and desired power level.
    - The agent should use this function for study designs where:
      1. Multiple predictor variables are being analyzed
      2. The outcome variable is continuous
      3. The focus is on detecting relationships between predictors and the outcome
    """
    print("Loading the R script")
    # Load the R script
    robjects.r.source("multiple_linear_regression.R")

    print("Getting the multiple_linear_regression function from R")
    # Get the MLR function from R
    multiple_linear_regression_r = robjects.globalenv['multiple_linear_regression']

    print(f"Calling the R function with u={multiple_linear_regression.u}, f2={multiple_linear_regression.f2}, power={multiple_linear_regression.power}")
    # Call the R function
    result = multiple_linear_regression_r(multiple_linear_regression.u, multiple_linear_regression.f2, multiple_linear_regression.power)

    print(f"Returning the result: {result[0]}")
    # Return the result (required sample size)
    return {"result": float(result[0])}


@app.post('/api/v1/one_mean_wilcoxon')
def one_mean_wilcoxon(one_mean_wilcoxon: OneMeanWilcoxon):
    """
    This function calculates the required sample size for a one-sample Wilcoxon test using an R function.

    Purpose:
    The task of this function is to determine the sample size needed to achieve desired statistical power 
    in a one-sample Wilcoxon test. This is useful when designing studies that compare a single sample to 
    a hypothesized median under non-parametric conditions.

    Key Considerations for the Agent:
    - Use this function when the problem involves calculating sample size for one-sample Wilcoxon tests.
    - This function is ideal for scenarios where the agent knows the user is comparing a single group to 
      a reference value and wants to use a non-parametric approach.
    - If the user provides the **effect size** (Cohen's d), desired level of **power**, and **alternative** 
      hypothesis type, this is the appropriate function to call.

    Parameters:
    - **d**: Cohen's d effect size, calculated as (M2-M1)/SD, where:
      * M2 is the sample mean
      * M1 is the hypothesized population mean
      * SD is the standard deviation
      This represents the standardized magnitude of the difference.
    - **power**: The target statistical power (typically 0.80 or 0.90) to detect the specified effect size. 
      Power represents the probability of detecting a true difference when it exists.
    - **alternative**: The type of alternative hypothesis to test, must be one of:
      * "two.sided" (default) - testing for any difference
      * "greater" - testing for an increase
      * "less" - testing for a decrease

    When to Use:
    - Use this function when designing studies that involve comparing a single sample to a reference value.
    - This is relevant when the user needs non-parametric analysis and wants to determine the required 
      sample size.
    - This function is particularly appropriate for:
      * Non-normally distributed data
      * Ordinal measurements
      * Small sample sizes where normality cannot be assumed

    Example Task for Agent:
    - When the user requests sample size calculations for a one-sample Wilcoxon test and provides parameters 
      like effect size (d), desired power, and alternative hypothesis type.
    - The agent should use this function for study designs where:
      1. A single group is being compared to a reference value
      2. Non-parametric analysis is preferred
      3. The focus is on detecting differences from a hypothesized value
    """
    print("Loading the R script")
    # Load the R script
    robjects.r.source("one_mean_wilcoxon.R")

    print("Getting the one_mean_wilcoxon function from R")
    # Get the Wilcoxon test function from R
    one_mean_wilcoxon_r = robjects.globalenv['one_mean_wilcoxon']

    print(f"Calling the R function with d={one_mean_wilcoxon.d}, power={one_mean_wilcoxon.power}, alternative={one_mean_wilcoxon.alternative}")
    # Call the R function
    result = one_mean_wilcoxon_r(one_mean_wilcoxon.d, one_mean_wilcoxon.power, one_mean_wilcoxon.alternative)

    print(f"Returning the result: {result[0]}")
    # Return the result (required sample size)
    return {"result": float(result[0])}


@app.post('/api/v1/mann_whitney_test')
def mann_whitney_test_n(mann_whitney_test: MannWhitneyTest):
    """
    This function calculates the required sample size for a Mann-Whitney test based on the specified effect size, desired power, and alternative hypothesis using an R function.
   Purpose:
   The task of this function is to determine the number of samples required in each group to detect a specified difference 
   in the distributions of two independent groups. This is useful when designing studies or experiments that involve comparing 
   two groups using non-parametric methods, where the difference between groups need not be normally distributed.
   Key Considerations for the Agent:
   - Use this function when the problem requires calculating the sample size for a Mann-Whitney test scenario.
   - This function is ideal for scenarios where the agent knows the user is comparing distributions between two groups and wants to 
     ensure the study is powered to detect a certain effect size (difference in distributions).
   - If the user provides a specific effect size (d), along with the desired level of power (probability of detecting the effect), 
     and the type of alternative hypothesis (alternative), this is the appropriate function to call.
     
   Parameters:
    - **d**: The effect size, which represents the magnitude of the difference in distributions between the two groups. This is the expected or hypothesized difference that the user wants to detect.
    - **power**: The target statistical power (typically 0.80 or 0.90) to detect the effect size (d). Power represents the likelihood of correctly rejecting the null hypothesis when the difference is real.
    - **alternative**: The type of alternative hypothesis. It can be one of the following values: "two.sided", "less", or "greater". This specifies the direction of the test.
    
     When to Use:
    - Use this function when the task requires determining sample size for studies comparing two independent groups 
      with non-parametric methods.
    - This is relevant when the user needs to design a study or experiment and has specified the desired power, the 
      expected effect size (d), and the type of alternative hypothesis (alternative).
    - This function is appropriate when the user asks for a sample size calculation to compare two groups with non-parametric outcomes 
      (e.g., a clinical trial comparing the effectiveness of a drug versus a placebo, where the outcome is not assumed to be normally distributed).

      Example Task for Agent:
    - When the user requests a sample size calculation to detect a difference in distributions between two groups, and provides 
      parameters like expected effect size (d), power level, and type of alternative hypothesis (alternative), this function should be called.
    - The agent can also use this function when the problem involves sample size determination for a study design where 
      non-parametric outcomes are assumed.
    """
    print("Loading the R script")
    # Load the R script
    robjects.r.source("mann_whitney_test.R")

    print("Getting the mann_whitney_test function from R")
    # Get the mann_whitney_test function from R
    mann_whitney_test_n_r = robjects.globalenv['mann_whitney_test']

    print(f"Calling the R function with delta={mann_whitney_test.d}, sd={mann_whitney_test.power}, and power={mann_whitney_test.alternative}")
    # Call the R function
    result = mann_whitney_test_n_r(mann_whitney_test.d, mann_whitney_test.power, mann_whitney_test.alternative)

    print(f"Returning the result: {result[0]}")
    # Return the result
    return {"result": float(result[0])}

@app.post('/api/v1/paired_wilcoxon_test')
def paired_wilcoxon_test(paired_wilcoxon_test: PairedWilcoxonTest):
    """
    This function calculates the required sample size for a paired Wilcoxon test using an R function.

    Purpose:
    The task of this function is to determine the sample size needed to achieve desired statistical power 
    in a paired Wilcoxon test. This is useful when designing studies that compare paired measurements 
    under non-parametric conditions.

    Key Considerations for the Agent:
    - Use this function when the problem involves calculating sample size for paired Wilcoxon tests.
    - This function is ideal for scenarios where the agent knows the user is comparing matched pairs 
      of observations and wants to use a non-parametric approach.
    - If the user provides the **effect size** (Cohen's d), desired level of **power**, and **alternative** 
      hypothesis type, this is the appropriate function to call.

    Parameters:
    - **d**: Cohen's d effect size, calculated as Mean_diff/Sd_diff, where:
      * Mean_diff is the mean of the differences between pairs
      * Sd_diff is the standard deviation of the differences between pairs
      This represents the standardized magnitude of the difference between paired observations.
    - **power**: The target statistical power (typically 0.80 or 0.90) to detect the specified effect size. 
      Power represents the probability of detecting a true difference when it exists.
    - **alternative**: The type of alternative hypothesis to test, must be one of:
      * "two.sided" (default) - testing for any difference
      * "greater" - testing for an increase
      * "less" - testing for a decrease

    When to Use:
    - Use this function when designing studies that involve comparing paired or matched observations.
    - This is relevant when the user needs non-parametric analysis and wants to determine the required 
      sample size.
    - This function is particularly appropriate for:
      * Before-after studies
      * Matched pairs designs
      * Repeated measurements on the same subjects
      * Non-normally distributed paired data

    Example Task for Agent:
    - When the user requests sample size calculations for a paired Wilcoxon test and provides parameters 
      like effect size (d), desired power, and alternative hypothesis type.
    - The agent should use this function for study designs where:
      1. Observations are naturally paired or matched
      2. Non-parametric analysis is preferred
      3. The focus is on detecting differences within pairs
    """
    print("Loading the R script")
    # Load the R script
    robjects.r.source("paired_wilcoxon_test.R")

    print("Getting the paired_wilcoxon_test function from R")
    # Get the paired Wilcoxon test function from R
    paired_wilcoxon_test_r = robjects.globalenv['paired_wilcoxon_test']

    print(f"Calling the R function with d={paired_wilcoxon_test.d}, power={paired_wilcoxon_test.power}, alternative={paired_wilcoxon_test.alternative}")
    # Call the R function
    result = paired_wilcoxon_test_r(paired_wilcoxon_test.d, paired_wilcoxon_test.power, paired_wilcoxon_test.alternative)

    print(f"Returning the result: {result[0]}")
    # Return the result (required sample size)
    return {"result": float(result[0])}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
