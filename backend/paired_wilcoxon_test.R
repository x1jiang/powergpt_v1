library(pwr)

paired_wilcoxon_test <- function(d,power,alternative){
  result_list <- pwr.t.test(
    d = d,
    sig.level = 0.05,
    power = power,
    type = "paired",
    alternative = alternative
  )
  return(result_list$n*1.15) 
}


# Cohen's D : effect size
# Cohen's D = Mean_diff/Sd_diff; 


# Example
# paired_wilcoxon_test(d=0.8,power = 0.8,alternative = 'greater')


