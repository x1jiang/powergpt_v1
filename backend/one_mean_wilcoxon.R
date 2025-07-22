library(pwr)

one_mean_wilcoxon <- function(d,power,alternative){
  result_list <- pwr.t.test(
    d = d,
    sig.level = 0.05,
    power = power,
    type = "one.sample",
    alternative = alternative
  )
  return(result_list$n*1.15) 
}


# Cohen's D : effect size
# Cohen's D = (M2-M1)/SD; 


# Example
# one_mean_wilcoxon(d=0.5,power = 0.8,alternative = 'greater')
