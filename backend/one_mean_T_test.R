library(pwr)

one_mean_T_test_n <- function(d, power, alternative){
  result_list <- pwr.t.test(d=d, sig.level =0.05, power=power, type = "one.sample", alternative=alternative)
  return(result_list$n)  # Returning the sample size (n)
}

# Example
one_mean_T_test_n(d = 0.5, power = 0.8, alternative = "two.sided")

