library(pwr)

chi_squared_test_n <- function(w, df, power){
  result_list <- pwr.chisq.test(w = w, df=df, sig.level = 0.05, power = power)
  return(result_list[[2]])}

#w: effect size
#w = sqrt(X^2/(n*df)), where
#df: degree of freedom
#n = number of samples
#X^2 = sum of ((observed - expected)^2 / expected)

#Example
#chi_squared_test(w=0.3, df=3, power=0.8)
