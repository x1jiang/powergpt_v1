library(pwr)

correlation <- function(r,power){
  result_list <- pwr.r.test(
    r = r,
    sig.level = 0.05,
    power = power
  )
  return(result_list$n) 
}


# r : effect size
# r : correlation coefficient

# Example
# correlation(r=0.5,power = 0.8)
