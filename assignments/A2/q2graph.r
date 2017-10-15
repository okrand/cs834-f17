data <- read.table('vocab.dat')
pdf("vocabulary.pdf")
plot(data$V2, data$V1, type="l", col="blue", main="Vocabulary Growth",
    ylab="Words in Vocabulary", xlab="Total Words")
dev.off()