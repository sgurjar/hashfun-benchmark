rm(list=ls(all=TRUE))

plotmydata <- function(datafile, title, img) {
  u <- read.csv(datafile,header=FALSE, sep=" ", comment.char="@")
  u <- u[c(1,2,3,4,6)] # skip digest
  names(u) <- c('lang','algo','datafile','index','elapsed')

  qplot(x=datafile, y=elapsed, data=subset(u,lang!='perl'), geom='point',
        xlab='Data size in megabytes',
        ylab='Elapsed time in MS',
        color=lang,
        main=title) +
    facet_grid(algo ~ lang ) +
    scale_y_continuous(lim=c(0, 40000), breaks=seq(0,40000,5000)) +
    scale_x_discrete(breaks=c("0002mb.dat", "0008mb.dat", "0032mb.dat",
                              "0128mb.dat", "0640mb.dat", "1024mb.dat"),
                     labels=c("2", "8", "32", "128", "640", "1024")) +
    theme_bw() +
    theme(legend.position="none")

  ggsave(img)
}

setwd("C:/books3/unh/hashfun-benchmark")
library(ggplot2)
plotmydata("ubuntu_results.txt","Ubuntu Benchmark","ubuntu.png")
plotmydata("windows-results.txt","Windows Benchmark","windows.png")
