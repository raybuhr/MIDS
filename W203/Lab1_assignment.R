# W203: Exploring and Analyzing Data
# Fall 2014
# Lab 1
# Raymond Buhr

# Part 1: Multiple Choice
# 1. e
# 2. e 
# 3. b 
# 4. b 
# 5. d 
# 6. a 
# 7. f 
# 8. d 
# 9. b 

# Part 2: Data Analysis and Short Answer

# 1. Variable Manipulation
# a. Load the data found in the file, GDP_World_Bank.csv into a new dataframe.

gdp_wb <- read.csv("C:/Users/Public/Documents/MIDS/Exploring and Analyzing Data/Assignments/Lab1/GDP_World_Bank.csv")

# Create a new variable, gdp_growth, that equals the increase in GDP from 
# 2011 to 2012

gdp_wb$gdp_growth <- gdp_wb$gdp2012 - gdp_wb$gdp2011

# What is the mean of your new variable?

mean_growth <- mean(gdp_wb$gdp_growth, na.rm = T)
print(mean_growth)
# I found a mean of +$7,172,376,796

# b. Create a histogram of your new variable from part a.

hist(gdp_wb$gdp_growth)

# Describe its shape in terms of the distribution properties from class.

# The histogram is positively skewed and leptokurtotic. It also seems to
# have a few very large and very small outliers.

# c. Create a new Boolean variable, high_growth, that equals TRUE if a 
# country’s gdp growth is higher than the mean.

gdp_wb$high_growth <- ifelse(gdp_wb$gdp_growth > mean_growth, TRUE, FALSE)

# How many countries have above average growth, and how many have 
# below average growth?

summary(gdp_wb$high_growth)

# 31 countries have high growth and 142 have below average growth.
# 39 countries do not have data to determine growth.

# Explain this result in terms of the shape of the gdp_growth distribution.

# In the gdp_growth distribution plotted earlier, the mean was also in the
# most frequent bin. Countries higher than average would generally be to
# the right of that bin, where countries lower than average would to the left.
# Since R makes it easy to visualize this, let's scale the values and then 
# add the mean to the histogram.
# SCALING
z_gdp_growth <- scale(gdp_wb$gdp_growth, center = T, scale = T)
# hist of scaled GDP growth
hist(z_gdp_growth, breaks = 30)
# I think this is a better depiction of the data as you can see the peakiness 
# and the extreme positive outliers.
# Now adding in the mean as a blue line on the histogram:
abline(v = mean(z_gdp_growth, na.rm = T), col = "blue", lwd = 2)
# Now we can clearly see most of the countries are to the left of the mean line. 

# 2. Data Import
# a. Find one new metric country-level variable from some public source and merge
# it into your dataset.

# I chose to use data from the World Resources Institute Climate Analysis Indicators Tool
# http://cait2.wri.org/
# The variables I selected included total green house gases (GHG) emissions, GHG
# for just  ]the energy sector and total methane emissions, all for 2011.
# Since the first line of the csv file is source info, I did not choose a header.

WRI_cait <- read.csv("C:/Users/Public/Documents/MIDS/Exploring and Analyzing Data/Assignments/Lab1/WorldResourcesInstituteCAIT.csv", header=FALSE)

# I want to create a data frame with the 2nd row as the headers and remove the 1st row
# To do this, I need to know how many rows there are.
nrow(WRI_cait)
# I find there are 190 rows, so I subset WRI_cait into rows 2 through 190.
WRI_df <- WRI_cait[2:190,]
# I now want to change the names of the columns to something useable.
names(WRI_df) <- c("Country", "year", "total.GHG", "energy.GHG", "methane")
# Now I want to create a new dataframe that merges 2011 GDP with the 2011 emissions.
gwb_wri <- merge(gdp_wb, WRI_df, by = "Country")
# How many countries matched up?
nrow(gwb_wri)
# I got 161 countries with data in both sets.

# Once you have successfully merged your dataframes, create one more 
# graph that you think is interesting that involves your new variable.

# After playing with the data for a while, I settled on plotting 2011 GDP
# against 2011 methane emissions while grouping by our previous variable high_growth.
# In order for the graph to make sense, I normalized the 2011 GDP using log10,
# as well as rounded methane emissions to the nearest integer.
# Creating new variable that uses log10 of 2011 GDP.
gwb_wri$log_gdp2011 <- log10(gwb_wri$gdp2011)
# Creating new variable that rounds methane emissions.
gwb_wri$rd.methane <- as.numeric(levels(gwb_wri$methane))[gwb_wri$methane]

# To create the scatter plot graph or both High Growth countries 
# and non-High Growth countries, I used ggplot2.

cool_plot <- qplot(log_gdp2011, rd.methane, data = gwb_wri, 
                   shape = high_growth, color = high_growth, 
                   xlab = "log of 2011 GDP", 
                   ylab = "2011 Methane Emissions")
# Also want to linear trend models to each group, a chart title, and
# for good measure label a few out the outliers.
cool_plot + geom_smooth(method = lm, se = F) + 
  ggtitle("2011 GDP compared to\n2011 Methane Emissions") +
  geom_text(aes(label= (ifelse(((log_gdp2011 > 12)&(rd.methane > 200)), 
                               as.character(gwb_wri$Country), ""))), 
            hjust = 1.1, vjust = 1.1)

# Write a few sentences about what the graph shows.

# The new graph shows that countries that did not experience high-growth
# in GDP from 2011 to 2012 have generally low levels of methane emissions,
# though there were a few outliers. For the countries that did experience
# high-growth of GDP, the graph shows a considerable increasing trend as GDP 
# increases. While the fit of the model for this trend does not seem to be 
# particularly strong, I think we can reasonably estimate that most countries
# with high-growth GDP will emit more methane than countries with low-growth GDP.
