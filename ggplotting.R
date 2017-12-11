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
  times = times %>% filter(start <= end) %>% arrange(symbol, -start)
  return(times)
}

wrap2 = wrap_about(wrap)


# working on plotting the rings i'll be actually plotting.
actual_set = data.frame(start = c(13, 14), end = c(22, 22), color = c(1,2), band = c(4,5), city = c(1,1))

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


# testing with two different (made up) cities.
city1 = data.frame(start = c(13, 14), end = c(22, 22), color = c(1,2), band = c(4,5), city = 1)
city2 = data.frame(start = c(10, 8), end = c(20, 23), color = c(1,2), band = c(4,5), city = 2)

city1 = city1 %>% rbind(city1 %>% rename(end = start, start = end) %>% mutate(color = c(3,4)))
city2 = city2 %>% rbind(city2 %>% rename(end = start, start = end) %>% mutate(color = c(3,4)))
city1 = wrap_about(city1)
city2 = wrap_about(city2)

colors = c('#f4c20d', '#3cba54', '#4885ed', '#db3236')

cities = rbind(city1, city2)
daycolors = colors[c(1,3)]
sp = .4


# plotting multiple cities (very much experimenting stages).
ggplot(data = cities, aes(x = band, fill = factor(color))) +
  geom_rect(data = cities %>% filter(band == 4) %>% mutate(city = city + 5), aes(xmin = city-sp, xmax = city+sp, ymin = start, ymax = end, alpha = 1/city)) +
  geom_rect(data = cities %>% filter(band == 5) %>% mutate(city = city + 7), aes(xmin = city-sp, xmax = city+sp, ymin = start, ymax = end, alpha = 1/city)) +
  geom_rect(aes(xmin = 3, xmax = 10.5, ymin = 11.95, ymax = 12.05), fill = '#808080', alpha = 1) +
  annotate("text", x = 0, y = 0, label = "City Name", size = 8) +
  annotate("text", x = 2, y = 0, label = "Other City", size = 7, alpha = .5) +
  annotate("text", x = 11, y = 12, label = 'Now', size = 4) +
  lims(x = c(0,12), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  scale_fill_manual(name = 'Time of Day', values = colors, labels = c('daytime', 'office', 'nighttime', 'home')) +
  scale_alpha_continuous(guide = FALSE) +
  theme_void() + theme(legend.title = element_text())


# slight improvement, needs design and coding overhaul.
ggplot(data = cities, aes(x = band, fill = factor(color))) +
  geom_rect(data = cities %>% filter(band == 4 & city == 1), aes(xmin = 4.9, xmax = 5.1, ymin = start, ymax = end), alpha = 1) +
  geom_rect(data = cities %>% filter(band == 4 & city == 2), aes(xmin = 5.3, xmax = 5.5, ymin = start, ymax = end), alpha = .6) +
  geom_rect(aes(xmin = 2, xmax = 6, ymin = 11.95, ymax = 12.05), fill = '#808080', alpha = 1) +
  annotate("text", x = 1, y = 12, label = "City Name", size = 8) +
  annotate("text", x = 1, y = 0, label = "Other City", size = 7, alpha = .5) +
  annotate("text", x = 6.5, y = 12, label = 'Now', size = 4) +
  lims(x = c(0,12), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  scale_fill_manual(name = 'Time of Day', values = daycolors, labels = c('daytime', 'nighttime')) +
  # scale_fill_manual(name = 'Time of Day', values = daycolors, labels = c('daytime', 'office', 'nighttime', 'home')) +
  # scale_alpha_continuous(guide = FALSE) +
  theme_void() + theme(legend.title = element_text())






# Testing a new way of structuring the data.

# the format we get is:
# Sunrise, Sunset, Work_Start, Work_End

# the format we want to end up with is: 
# City, Symbol, Start, End

# this calls for some reshaping or something.

pydata = read_csv('for_ggplotting.csv', col_names = c('names', 'values'))
pydata

pydata = pydata %>% mutate(city = rep(1:(nrow(pydata)/4), each = 4)) # labels each city
pydata

dayta = data_frame(city = pydata$city,
                   symbol = rep(1:4, nrow(pydata)/4),
                   start = pydata$values)

dayta = dayta %>% mutate(end = ifelse(symbol %in% c(1,3), lead(start), lag(start))) %>% select(3,4,2,1) # rearranges start/end values

dayta
dayta = wrap_about(dayta)
dayta

dayta = dayta %>%
        mutate(ring = ifelse(symbol %in% c(1,2), 1, 2),
               gen = ring*2 + 5,
               # loc = ifelse(city == 1, -.15, .15),
               loc = ifelse(city%%2==0, -.15*city, +.15*city),
               xmin = gen+loc-.1,
               xmax = gen+loc+.1,
         # xmin = gen+loc-.25,
         # xmax = gen+loc+.25,
               alpha = 1/city,
               clr = colors[symbol]) %>%
        filter(symbol != 4)

dayta

# naming the colors as themselves, then arranging labels as needed, apparently works? not sure why, just got it by playing around.
colors = c('#f4c20d' = '#f4c20d', '#4885ed' = '#4885ed', '#3cba54' = '#3cba54', '#db3236' = '#db3236')

dayta

ggplot(data = dayta, aes(fill = clr)) +
  geom_rect(aes(xmin = xmin, xmax = xmax, ymin = start, ymax = end), alpha = 1) +
  # geom_rect(aes(xmin = xmin, xmax = xmax, ymin = start, ymax = end), alpha = .65) +
  # geom_rect(aes(xmin = 2, xmax = 10, ymin = 11.95, ymax = 12.05), fill = '#808080', alpha = 1) +
  # annotate("text", x = 10.5, y = 12, label = 'Now', size = 4) +
  # annotate("text", x = 1, y = 12, label = "City Name", size = 8) +
  # annotate("text", x = 1, y = 0, label = "Other City", size = 7, alpha = .5) +
  lims(x = c(0,12), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  scale_fill_manual(name = 'Time of Day', values = colors, labels = c('home', 'night', 'day')) +
  # scale_fill_manual(name = 'Time of Day', values = colors, labels = c('day', 'night', 'work', 'home')) +
  # scale_alpha_continuous(guide = FALSE) +
  # theme_void() + theme(legend.title = element_text()) +
  theme_minimal()

dayta






