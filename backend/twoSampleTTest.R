# twoSampleTTest.R
# Function to calculate the sample size needed to achive certain power in two-sample t-test

twosamplettest_n <- function(delta, sd, power){
    result_list <- power.t.test(n = NULL, delta = delta, sd = sd, sig.level = 0.05,
             power = power,
             type = c("two.sample"),
             alternative = c("two.sided"),
             strict = FALSE, tol = .Machine$double.eps^0.25)
   return(as.numeric(result_list[1]))
}

