cl <- function(fm, cluster){
	require(sandwich, quietly = TRUE)
	require(lmtest, quietly = TRUE)
	M <- length(unique(cluster))
	N <- length(cluster)
	K <- fm$rank
	dfc <- (M/(M-1))*((N-1)/(N-K))
	uj <- apply(estfun(fm),2, function(x) tapply(x, cluster, sum));
	vcovCL <- dfc*sandwich(fm, meat=crossprod(uj)/N)
	coeftest(fm, vcovCL)
}
