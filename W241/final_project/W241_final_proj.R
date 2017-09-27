setwd("MIDS/241")
library(ggplot2)

# load data
rm(list=ls())
data <- read.csv("SurveyTransfer8.csv", header = T)
summary(data)

# remove NA
data2 <- data[!is.na(data$values),]
is.na.id <- is.na(data$values)
data2[is.na.id,c('TimezoneName')]

# remove zero
data3 <- data2[data2$values!=0,]

# only keep 4 US time zones: EST, PST, CST, MST
tz = data3$TimezoneName
keep = tz=='Eastern Standard Time' | tz=='Central Standard Time' | tz=='Pacific Standard Time' | tz=='Mountain Standard Time'
data3 <- data3[keep,]

# remove outliers based on quantils
qt <- rev(as.vector(quantile(data3$values, probs = c(0, 0.005, 0.025, 0.1, 0.25, 0.5, 0.75, 0.90, 0.975, 0.995, 1))))

# remove values less than 20 (2.5%)
data4 <- data3[data3$values>20,]

# evaluate duplicate IP
n_occur <- data.frame(table(data4$IPAddress))
n_occur[n_occur$Freq > 1,]
data5 <- data4[data4$IPAddress %in% n_occur$Var1[n_occur$Freq > 1],]
data5 <- data5[with(data5, order(IPAddress)), ]

# get rid the second entry of any duplicate IP
data4 <- data4[!duplicated(data4$IPAddress), ]

# recode covariates
data4$is.female <- data4$What.is.your.gender. - 1
data4$age <- data4$What.is.your.age.
data4$income <- data4$Indicate.total.household.income.

# model for decimal point treatment & covariates
m <- lm(values ~ is..49.55 + is..49.92 + is..50.08 + is..50.45 + is.female + age + income + is.College + is.Associates + is.Bachelor + is.Graduate + is.Central.Standard.Time + is.Mountain.Standard.Time + is.Pacific.Standard.Time, data=data4)
summary(m)

m2 <- lm(values ~ is..49.55 + is..49.92 + is..50.08 + is..50.45, data=data4)
summary(m2)

# breakdown by covariates
# bar chart: treatment
bar_q <- ggplot(data4, aes(Question, values, fill=gender))
bar_q + stat_summary(fun.y = mean, geom = "bar", position="dodge") + stat_summary(fun.data = mean_cl_normal, geom = "errorbar", position = position_dodge(width=0.90), width = 0.2)
# bar chart: education
bar_e <- ggplot(data4, aes(Education, values, fill=gender))
bar_e + stat_summary(fun.y = mean, geom = "bar", position="dodge") + stat_summary(fun.data = mean_cl_normal, geom = "errorbar", position = position_dodge(width=0.90), width = 0.2)
# bar chart: region
bar_r <- ggplot(data4, aes(TimezoneName, values, fill=gender))
bar_r + stat_summary(fun.y = mean, geom = "bar", position="dodge") + stat_summary(fun.data = mean_cl_normal, geom = "errorbar", position = position_dodge(width=0.90), width = 0.2)
# scatter plot: age
scatter_a <- ggplot(data4, aes(age, values, color=gender))
scatter_a + geom_point() + geom_smooth(method = "lm", aes(fill = gender), alpha = 0.1)
# scatter plot: income
scatter_i <- ggplot(data4, aes(income, values, color=gender))
scatter_i + geom_point() + geom_smooth(method = "lm", aes(fill = gender), alpha = 0.1)

# covariate balance check:
bar_bq <- ggplot(data4, aes(Question))
bar_bq + geom_bar(fill="white", color="black")

bar_be <- ggplot(data4, aes(Education))
bar_be + geom_bar(fill="white", color="black")

bar_bg <- ggplot(data4, aes(gender))
bar_bg + geom_bar(fill="white", color="black")

bar_br <- ggplot(data4, aes(TimezoneName))
bar_br + geom_bar(fill="white", color="black")

