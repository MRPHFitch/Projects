#' ntickets
#'
#' @param N size
#' @param gamma gamma
#' @param p Probability
#'
#' @return the number of tickets needed to sell to not overbook
#' @export
#' @import graphics
#' @import stats
#' @examples
#' ntickets(200, .02,.95)
ntickets<-function(N, gamma, p){

  #First do Discrete
  #The function needed to solve
  findn<-function(n){
    1-gamma-pbinom(N, n, p)
  }
  #Set a vector with all possible numbers
  v<-seq(N,2*N, by=1)
  test<-sapply(v,findn)
  test<-abs(test)
  #Find the index point
  index<-which.min(test)
  #Find what value in the vector that the index points to
  nd<-v[index]

  #Now do Approximation
  #Establish what q is
  q<-1-p
  #Set up the function to solve
  approxn<-function(n){
    pnorm(N+0.5, n*p, sqrt(n*p*q))-1+gamma
  }

  #Find the roots of the function
  aproot<-uniroot(approxn, c(0,2*N))
  #Round the roots to a whole number
  nc<-round(aproot$root)

  #Return the values in a list
  result<-(list(nd=nd,nc=nc,N=N,gamma=gamma,p=p))

  # Plot the objective function
  par(mfrow = c(2, 1))

  # Discrete case
  lim<-N*1.1
  n_values<-seq(N, 2*N, by=1)
  discrete<-1-gamma-pbinom(N, n_values, p)
  plot(n_values, discrete, type="l", col="magenta",lwd=3, main="Discrete Case", xlim=c(N,lim),
       ylim=c(0, 1.2), xlab="n", ylab="Objective Function")
  points(n_values, discrete, pch=19, col="black", cex=0.5)
  abline(v=nd, col="cyan", lwd=3)
  text(201, 0.5, paste("nd =", nd))

  # Continuous case
  n_values<-seq(N, 2*N)
  continuous<-1-gamma-pnorm(N, n_values*p, sqrt(n_values*p*q))
  plot(n_values, continuous, type="l", lwd=3, col="cyan", main="Continuous Case", xlim=c(N,lim),
       ylim=c(0, 1.2), xlab="n", ylab="Objective Function")
  points(n_values, continuous, pch=19, col="black", cex=0.5)
  abline(v=nc, col="magenta", lwd=3)
  text(201, 0.5, paste("nc =", nc))

  return(result)
}
