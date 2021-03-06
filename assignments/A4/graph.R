plotone <- function(data, fname) {
    pdf(fname)
    plot(data, type='o', pch=15, ylim=c(0,1), xlim=c(0,1),
        ylab="Precision", xlab="Recall")
    dev.off()
}
urpgraph <- function(d1, d2, fname) {
    pdf(fname)
    plot(d1, lwd=2, type='o', pch=18, ylim=c(0,1), xlim=c(0,1), col="blue",
        ylab="Precision", xlab="Recall")
    lines(d2, lwd=2, type="o", pch=15, col="red")
    legend(0.8, 1, c('Query 9', 'Query 10'), cex=0.8,
        col=c('blue', 'red'), lty=c(1,1), pch=c(18,15))
    dev.off()
}
iprgraph <- function(d1, d2, id1, id2, fname) {
    pdf(fname)
    plot(d1, lwd=2, type="p", pch=18, ylim=c(0,1), xlim=c(0,1), col="blue",
        ylab="Precision", xlab="Recall")
    lines(id1, lwd=2, type="s", col="blue")
    lines(d2, lwd=2, type="p", pch=15, col="red")
    lines(id2, lwd=2, type="s", col="red")
    legend(0.8, 1, c('Query 9', 'Query 10'), cex=0.8,
        col=c('blue', 'red'), lty=c(1,1), pch=c(18,15))
    dev.off()
}
aipgraph <- function(avg, id1, id2, fname) {
    pdf(fname)
    plot(avg, lwd=2, type="l", ylim=c(0,1), xlim=c(0,1), col="black",
        ylab="Precision", xlab="Recall")
    lines(avg, lwd=2, type="p", pch=17, col="black")
    lines(id1, lwd=2, type="s", col="blue")
    lines(id2, lwd=2, type="s", col="red")
    legend(0.8, 1, c('Query 9', 'Query 10', 'Average'), cex=0.8,
        col=c('blue', 'red', 'black'), lty=c(1,1,1), pch=c(18,15,17))
    dev.off()
}

args = commandArgs(trailingOnly=TRUE)

d1 <- read.table(paste('urpg', args[1], '.dat', sep=''))
d2 <- read.table(paste('urpg', args[2], '.dat', sep=''))

plotone(d1, paste('urpg', args[1], '.pdf', sep=''))
plotone(d2, paste('urpg', args[2], '.pdf', sep=''))
urpgraph(d1, d2, paste('urpg', args[1], '', args[2], '.pdf', sep=''))

id1 <- read.table(paste('ipr', args[1], '.dat', sep=''))
id2 <- read.table(paste('ipr', args[2], '.dat', sep=''))
iprgraph(d1, d2, id1, id2, paste('ipr', args[1], '', args[2], '.pdf', sep=''))

avg <- read.table('avg.dat')
aipgraph(avg, id1, id2, paste('aipr', args[1], args[2], '.pdf', sep=''))

overallavg <- read.table('avgall.dat')
plotone(overallavg, 'avgqall.pdf')