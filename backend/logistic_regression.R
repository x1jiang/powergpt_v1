library(WebPower)

logistic_regression <- function(p0,p1,power,alternative,family,parameter){
  result_list <- wp.logistic(
    p0 = p0,
    p1 = p1,
    alpha = 0.05,
    power = power,
    alternative = alternative,
    family = family,
    parameter = parameter
  )
  return(result_list$n) 
}

# effect size : NA

# Example
# logistic_regression(p0=0.15,p1=0.25,power=0.8,alternative='two.sided',family='normal',parameter=NULL)
