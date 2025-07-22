library(pwr)

simple_linear_regression <- function(u,f2,power){
  result_list <- pwr.f2.test(
    u = u,
    f2 = f2,
    sig.level = 0.05,
    power = power
  )
  return(result_list$v + 2) 
}


# f2 : effect size
# f2 = R = sqrt(R^2)
# R : correlation coefficient
# R^2 = goodness-of-fit (Use adjusted R^2)

# Example
# simple_linear_regression(u=1,f2=0.35,power = 0.8)
