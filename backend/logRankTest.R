# logRankTest.R
# Function to calculate the sample size needed to achieve certain power in log rank test

library(powerSurvEpi)

#pE: numeric. probability of failure in group E (experimental/treatment group) over the maximum time period of the study (t years)
#pC: numeric. probability of failure in group C (control group) over the maximum time period of the study (t years).

logranktest_n <- function(power, k, pE, pC,RR,alpha=0.05){
  result <- ssizeCT.default(power=power, k = k, pE = pE, pC = pC, RR = RR, alpha = alpha)
  return(result)
}
