one <- function(data, outfile, title) {
  pdf(outfile)
  max_x <- length(data$V1)
  x <- c(1:max_x)
  y <- data$V1 / sum(data$V1)
  plot(x,y, type='l', log='xy', main=title, 
       ylab='Frequency', xlab='Rank', col="blue")
  
  fr <- data$V1
  
  p <- fr/sum(fr)
  
  lzipf <- function(s,N) -s*log(1:N)-log(sum(1/(1:N)^s))
  
  opt.f <- function(s) sum((log(p)-lzipf(s,length(p)))^2)
  
  opt <- optimize(opt.f,c(p[1],max_x))
  
  library(stats4)
  ll <- function(s) sum(fr*(s*log(1:max_x)+log(sum(1/(1:max_x)^s))))
  
  fit <- mle(ll,start=list(s=1))
  
  summary(fit)
  s.sq <- opt$minimum
  s.ll <- coef(fit)
  
  lines(1:max_x,exp(lzipf(s.sq,max_x)),col='red')
}

both <- function(d1, d2, outfile, title) {
  pdf(outfile)
  d1 <- d1["V1"]
  d2 <- d2["V1"]
  combined <- rbind(d2, d1)
  newdata <- combined[order(-combined$V1),]

  max_x <- length(newdata)
    x <- c(1:max_x)
    y <- newdata / (sum(d1$V1) + sum(d2$V1))
    plot(x,y, type='l', log='xy', main=title, 
       ylab='Frequency', xlab='Rank', col="blue")

    fr <- newdata
    p <- y

    lzipf <- function(s, N) -s*log(1:N)-log(sum(1/(1:N)^s))
    opt.f <- function(s) sum((log(p)-lzipf(s,length(p)))^2)
    opt <- optimize(opt.f,c(p[1],max_x))

    library(stats4)
    ll <- function(s) sum(fr*(s*log(1:max_x)+log(sum(1/(1:max_x)^s))))
    fit <- mle(ll,start=list(s=1))
    summary(fit)

    s.sq <- opt$minimum
    s.ll <- coef(fit)
    lines(1:max_x,exp(lzipf(s.sq,max_x)),col=2)
}

d1 <- read.table('wordcount.dat')
d2 <- read.table('bigramcount.dat')
one(d1, 'wordcount.pdf', 'Word Counts')
one(d2, 'bigram.pdf', 'Bigram Counts')
both(d1,d2,'word_bigram.pdf', 'Combined Counts')