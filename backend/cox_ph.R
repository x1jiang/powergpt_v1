# cox_ph.R
# Function to calculate the sample size needed to achieve certain power in cox proportional hazard

library(powerSurvEpi)

cox_ph_n <- function(power, theta, p, psi, rho2 = 0, alpha = 0.05){
  result <- ssizeEpi.default(power=power, theta=theta, p, psi, rho2 = 0, alpha = 0.05)
  return(result)
}

#theta: postulated hazard ratio
#p: proportion of subjects taking value one for the covariate of interest (in equal allocation, p=0.5)
#psi: proportion of subjects died of the disease of interest (event rate)
#Example: cox_ph_n(power = 0.80, theta = 2, p = 0.56, psi = 0.57)
