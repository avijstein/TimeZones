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


# just a test to generate random ranges and plot those.
breakme = data.frame(start = sample(0:24, 5, replace=T),
                     end = sample(0:24, 5, replace=T),
                     band = 1:5)
breakme2 = wrap_about(breakme)

ggplot(data = breakme2, aes(x = band, fill = factor(band))) +
  geom_rect(aes(xmin = 0+band-.4, xmax = 0+band+.4, ymin = start, ymax=end), alpha = .75) +
  lims(x = c(0,8), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  scale_fill_discrete(name = 'Bands') +
  theme_minimal()



# working on plotting the rings i'll be actually plotting.
actual_set = data.frame(start = c(12, 14),
                        end = c(22, 22),
                        # color = c('orange', 'green'),
                        color = c(1,2),
                        band = c(1,2))

actual_set = actual_set %>%
  rbind(actual_set %>%
        rename(end = start, start = end) %>%
        # mutate(color = c('blue', 'red')))
        mutate(color = c(3, 4)))

actual_set2 = wrap_about(actual_set)

# haven't been able to customize colors yet, but i'm  getting there.
actual_set2 = actual_set2 %>%
              # mutate(color = as.factor(color)) %>%
              mutate(recode(color, 'orange' = 1,
                                   'green' = 2,
                                   'blue' = 3,
                                   'red' = 4))

# color = c('orange', 'green', 'blue', 'red'))
str(actual_set2)

ggplot(data = actual_set2, aes(x = band, fill = factor(color))) +
  geom_rect(aes(xmin = band-.4, xmax = band+.4, ymin = start, ymax=end), alpha = .75) +
  lims(x = c(0,8), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  scale_fill_discrete(name = 'Bands') +
  theme_minimal()

