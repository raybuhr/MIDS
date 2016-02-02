# W203 - Lab 3, Part 3
# Ray Buhr, 10/20/2014

# ------------------------------------------------------------- #
# 1. Data Import and Error Checking
# Load the GSS R data file
load("C:/Users/Public/Documents/MIDS/Exploring and Analyzing Data/Assignments/Lab2/GSS.Rdata")
# Examine the agewed variable
# First will look at the summary of the variable
summary(GSS$agewed)
# Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
# 0.00   18.00   21.00   19.06   24.00   99.00 
# Looks like 0 and 99 are probably wrong, though I guess 99 could be legit.
# Let's try running a histogram on the variable with a bunch of bins
hist(GSS$agewed, breaks = 100)
# See Figure1 for image of histogram
# From the graph, 0 and 99 seem like the only weird data points.
# Recode 0 and 99 as NA for agewed
GSS$agewed <- ifelse(GSS$agewed == 0 | GSS$agewed == 99, NA, GSS$agewed)
# Redo the summary for agewed
summary(GSS$agewed)
# Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's 
# 13.00   19.00   22.00   22.79   25.00   58.00     298 
# Mean of agewed is 22.79

# ------------------------------------------------------------- #

# 2. Checking assumptions
# Produce a QQ plot of agewed, so import ggplot2
library(ggplot2)
qqagewed <- qplot(sample = GSS$agewed, stat = "qq")
qqagewed
# Looking at the QQ plot - see Figure2 - the distribution of agewed
# does not look particularly normal.
# The variable seems positively skewed. Instead of the straight line
# relationship one would expect, the line leans to the right. 
# This skew occurs due to most people marrying in their twenties.

# Perform a Shapiro-Wilk test on agewed
shapiro.test(GSS$agewed)
#Shapiro-Wilk normality test
# data:  GSS$agewed
# W = 0.8896, p-value < 2.2e-16
# The Null hypothesis is that the variable is normally distributed, where
# the Alternative hypothesis would be that it is not normally distributed.
# Since the p-value was incredibly small, close to 0, I reject the Null 
# hypothesis and conclude the variable is not normally distributed.

# What is the variance of agewed for Men?
var(GSS$agewed[GSS$sex == "Male"], na.rm = T)
# [1] 23.6843
# What is the variance of agewed for Women?
var(GSS$agewed[GSS$sex == "Female"], na.rm = T)
# [1] 24.29948

# Perform a Levene's test for agewed grouped by sex.
# Have to import car package to run Levene's test
library(car)
leveneTest(GSS$agewed, GSS$sex)
# Levene's Test for Homogeneity of Variance (center = median)
# Df F value Pr(>F)
# group    1  0.9609 0.3272
# 1200 

# What is the null and alternative hypothesis?
# The Null hypothesis for Levene's Test is that the assumption of 
# homogeneity of variance is true, thus the Alternative hypothesis is 
# that the assumption of homogeneity of variance is not true. 

# What is your p-value and specific conclusion?
# p-value = Pr(>F) = 0.3272, so thus I accept the null hypothesis
# and conclude that homogeneity of variance is tenable. 

# ------------------------------------------------------------- #

# 3. More hypothesis testing
# Suppose mean = 23, sd = 5, H0 = 23 and Ha != 23
# Perform a z-test
# First calculate standard error, SE = sd /  sqrt(n)
# N is the sample size, but since we have 298 NA's due to throwing
# out the 0 and 99 scores, n = 1500 - 298 = 1202
SE <- 5 / sqrt(1202)
SE
# [1] 0.1442174 
# Now to calculate the z-score of mean of 23
# Z = (M - m) / SE
z_agewed <- (23 - mean(GSS$agewed, na.rm = T)) / SE
z_agewed
# [1] 1.442174

# What are the null and alternative hypotheses?
# The null hypothesis would be that population mean = 23, where the 
# alternative hypothesis would be that the population mean != 23.

# What is your p-value and specific conclusion?
# p = 0.14984 for a 2-sided test with the z-score reached above ~ 1.44
# From that probability, there is not enough to reject the null hypotheis
# and so we would accept the null hypothesis that the mean = 23.

# ------------------------------------------------------------- #

