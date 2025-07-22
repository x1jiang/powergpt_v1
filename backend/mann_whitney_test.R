library(pwr)

mann_whitney_test <- function(d,power,alternative){
  result_list <- pwr.t.test(
    d = d,
    sig.level = 0.05,
    power = power,
    type = "two.sample",
    alternative = alternative
  )
  return(result_list$n*1.15) 
}


# Cohen's D : effect size
# Cohen's D = (M2-M1)/Sd_pooled; 


# Example
 mann_whitney_test(d=0.2,power = 0.8,alternative = 'two.sided')


