table <- matrix(0, ncol = 0, nrow=400)
table <- data.frame(table)
table$ReceivedReply <- c(rep(1, 52), rep(0, 48), rep(1,29), rep(0,71), rep(1,37), rep(0,63), rep(1,34), rep(0,66)) 
table$Colin <- c(rep(1, 200), rep(0, 200))
table$Jose <- c(rep(0, 200), rep(1, 200))
table$GoodGrammar <- c(rep(1,100), rep(0,100), rep(1,100), rep(0,100))
table$BadGrammar <- c(rep(0,100), rep(1,100), rep(0,100), rep(1,100))
summary(table)

linreg <- lm(table$ReceivedReply ~ table$Colin + table$Jose + table$GoodGrammar + table$BadGrammar)
summary(linreg)


outcome=c(rep(1,52),rep(0,48),rep(1,29),rep(0,71),rep(1,37),rep(0,63),rep(1,34),rep(0,66))
is.jose =c(rep(0,200),rep(1,200))
good.grammar = c(rep(0,100), rep(1,100), rep(0,100), rep(1,100)) 
#should be called bad.grammar
both = c(rep(0,100), rep(0,100), rep(0,100), rep(1,100))

data <- data.frame(  po = outcome,  jose = is.jose,  good_grammar = good.grammar, both = both)

lm <- lm(data$po ~ data$jose + data$good_grammar + data$both)
lm
summary(lm)
plot(lm)
