library(pwr)

paired_t_test_n <- function(d, power,alternative){
  result_list <- pwr.t.test(d=d, sig.level =0.05, power=power, type = "paired", alternative=alternative)
  return(result_list[[1]])}


#d: effect size; d=(mean_2 - mean_1)/pooled standard deviation
#pooled standard deviation = sqrt((sd1^2+sd2^2)/2)

#Example
#paired_t_test_n(d = 0.8, power = 0.8, alternative = "greater")
