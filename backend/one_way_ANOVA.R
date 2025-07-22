library(pwr)

one_way_ANOVA_n <- function(k, f, power){
  result_list <- pwr.anova.test(k=k, f=f, sig.level =0.05, power=power)
  return(result_list[[2]])}

#k: number of groups
#f: effect size; f = sqrt(eta^2/(1-eta^2)), where
#eta^2 = treatment sum of squares / total sum of squares

#Example
#one_way_ANOVA(k=6, f=0.1, power=0.8)
