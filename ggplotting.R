setwd('~/Desktop/Real Life/Coding Projects/TimeZones/')
library(tidyverse)

wrap = data.frame(start = c(5, 18, 9, 16),
                  end = c(3, 6, 13, 12),
                  band = 1:4)

wrap_about = function(times){
  # Takes times split over 24/0 hour boundary and makes them into two rows.
  for (i in 1:nrow(times)){
    if (times$start[i] > times$end[i]){
      new_row1 = c(times$start[i], 24, times[i,3:length(times)])
      new_row2 = c(0, times$end[i], times[i,3:length(times)])
      if (typeof(new_row1) == 'list'){
        new_row1 = as.numeric(unlist(new_row1))
        new_row2 = as.numeric(unlist(new_row2))
      }
      times = rbind(times, new_row1, new_row2)
    }
  }
  times = times %>% filter(start <= end) %>% arrange(band, -start)
  return(times)
}

wrap2 = wrap_about(wrap)


# working on plotting the rings i'll be actually plotting.
actual_set = data.frame(start = c(13, 14), end = c(22, 22), color = c(1,2), band = c(4,5))

actual_set = actual_set %>%
  rbind(actual_set %>%
        rename(end = start, start = end) %>%
        mutate(color = c(3, 4)))

actual_set2 = wrap_about(actual_set)
colors = c('#f4c20d', '#3cba54', '#4885ed', '#db3236')


ggplot(data = actual_set2, aes(x = band, fill = factor(color))) +
  geom_rect(aes(xmin = band-.45, xmax = band+.45, ymin = start, ymax=end), alpha = 1) +
  geom_rect(aes(xmin = 2, xmax = 6.5, ymin = 11.95, ymax = 12.05), fill = '#808080', alpha = 1) +
  annotate("text", x = 0, y = 0, label = "City Name", size = 8) +
  annotate("text", x = 7, y = 12, label = 'Now', size = 4) +
  lims(x = c(0,8), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  scale_fill_manual(name = 'Time of Day', values = colors, labels = c('daytime', 'office', 'nighttime', 'home')) +
  theme_void() + theme(legend.title = element_text())



