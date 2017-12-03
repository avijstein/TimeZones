setwd('~/Desktop/Real Life/Coding Projects/TimeZones/')
library(tidyverse)

wrap = data.frame(start = c(5, 18, 9, 12),
                  end = c(10, 6, 13, 16),
                  band = 1:4)


wrap_about = function(times){
  # Takes times split over 24/0 hour boundary and makes them into two rows.
  for (i in 1:nrow(times)){
    print(i)
    if(times$start[i] > times$end[i]){
      new_row1 = c(times$start[i], 24, times$band[i])
      new_row2 = c(0, times$end[i], times$band[i])
      times = rbind(times[1:(i-1),], new_row1, new_row2, times[(i+1):nrow(times),])
    }
  }
  return(times)
}

wrap = wrap_about(wrap)


ggplot(data = wrap, aes(x = band, fill = factor(band))) +
  geom_rect(aes(xmin = 0+band-.4, xmax = 0+band+.4, ymin = start, ymax=end), alpha = .75) +
  lims(x = c(0,8), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  scale_fill_discrete(name = 'Bands') +
  theme_minimal()


