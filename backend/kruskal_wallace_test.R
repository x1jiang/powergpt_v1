library(pwr)

kruskal_wallace_test <- function(k,f,power){
  result_list <- pwr.anova.test(
    k = k,
    f = f,
    sig.level = 0.05,
    power = power
  )
  return(result_list$n*1.15) 
}


# f : effect size
# f = sqrt(ita^2 / (1-ita^2))
# ita^2 = SS_treat / SS_total
# SS_treat : treatment sum of squares
# SS_total : total sum of squares


# Example
# kruskal_wallace_test(k=3,f=0.25,power = 0.8)
