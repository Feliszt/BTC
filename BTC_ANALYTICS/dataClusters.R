#!/usr/bin/env Rscript

# load file
fileName <- "data/analytics01.txt"
btcData <- read.table(fileName, header=TRUE, sep="-")

# display non scientific numbers
options("scipen"=100, "digits"=4)

# get times and transactions value
btcTimes <- data.matrix(btcData[2])
btcTrans <- data.matrix(btcData[3]) / 100000000

# get quantiles
q <- quantile(btcTrans, prob = seq(0, 1, length = 101))

# show histogram
for(histLimit in c(0.001, 0.01, 0.1, 0.5, 1, 5, 10, 100)) {
  nextStep = FALSE
  for(i in 1:length(q)) {
    if(nextStep) next
    if(unname(q[i]) >= histLimit) {
      resultFileName = sprintf("results/analytics01-hist%d",i)
      png(filename=resultFileName)

      histTitle = sprintf("%s of transactions are less than %f BTC",labels(q[i]), histLimit)
      hist(btcTrans[which(btcTrans > unname(q[1]) & btcTrans < unname(q[i]))], breaks=100, main = histTitle)
      dev.off()
      nextStep = TRUE
    }
  }
}

# get min, max, mean, var
minBtc <- min(btcTrans)
maxBtc <- max(btcTrans)
meanBtc <- mean(btcTrans)
medianBtc <- median(btcTrans)

# write stats to file
textFile <- file("results/analytics01-stats.txt")

write(sprintf("min\t%f\nmax\t%f\nmean\t%f\nmedian\t%f\n", minBtc, maxBtc, meanBtc, medianBtc), textFile, append=TRUE)

close(textFile)
