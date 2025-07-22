library(pwr)

#p0: hypothesized proportion
#p1: observed proportion

# Define function
single_proportion_test_n <- function(p0,p1, power, alternative) {
  h = 2*asin(sqrt(p1))-2*asin(sqrt(p0))
  # Automatically map "one.sided" to either "greater" or "less" based on the sign of h
  if (alternative == "one.sided") {
    if (h > 0) {
      alternative <- "greater"
    } else if (h < 0) {
      alternative <- "less"
    } else {
      stop("For 'one.sided', the effect size 'h' cannot be 0. It must be non-zero.")
    }
  }
  # Validate the 'alternative' argument based on h
  if (h > 0) {
    if (!alternative %in% c("greater", "two.sided")) {
      stop("For h > 0, 'alternative' must be 'greater' or 'two.sided'.")
    }
  } else if (h < 0) {
    if (!alternative %in% c("less", "two.sided")) {
      stop("For h < 0, 'alternative' must be 'less' or 'two.sided'.")
    }
  } else { # h == 0
      stop("Ensure that the effect size is non-zero!")
  }
  
  # Perform the power analysis
  result_list <- pwr.p.test(h = h, sig.level = 0.05, power = power, alternative = alternative)
  
  # Print the results
  print(result_list)
  
  # Return the sample size estimate (n)
  return(result_list$n)
}

#Example:
#p1 <- 0.65
#p0 <- 0.7
#single_proportion_test_n(p0, p1, power=0.8, alternative = "less")
