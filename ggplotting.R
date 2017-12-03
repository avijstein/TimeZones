setwd('~/Desktop/Real Life/Coding Projects/TimeZones/')
library(tidyverse)

wrap = data.frame(start = c(5, 18, 18, 0),
                  end = c(10, 6, 24, 6),
                  band = 1:4)

wrap2 = data.frame(daytime = c(8, 2, 14, 22, 4)) %>%
  mutate(nighttime = 24 - daytime,
         band = 1:5)

# maybe using start and ends of times?
ggplot(data = wrap, aes(x = band, fill = factor(band))) +
  geom_rect(aes(xmin = 0+band-.4, xmax = 0+band+.4, ymin = start, ymax=end), alpha = .6) +
  lims(x = c(0,8), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  theme_minimal()


# maybe using the lengths of days? this doesn't quite work.
ggplot(data = wrap2, aes(fill = factor(band))) +
  geom_rect(aes(xmin=band, xmax=band+.1, ymin=daytime, ymax=nighttime), alpha = .6) +
  coord_polar(theta = 'y') +
  lims(x = c(0,8), y = c(0,24)) +
  theme_minimal()


# major issue is not being able to cross over the 24-0 hour boundary. 
# not sure if I should keep looking for solution or hack a workaround.

