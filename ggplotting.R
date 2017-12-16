setwd('~/Desktop/Real Life/Coding Projects/TimeZones/')
library(tidyverse)

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


# Testing a new way of structuring the data.

# the format we get is:
# Sunrise, Sunset, Work_Start, Work_End

# the format we want to end up with is: 
# City, Symbol, Start, End

# this calls for some reshaping or something.

# It might be best to only limit the incoming data to two cities.
pydata = read_csv('for_ggplotting.csv', col_names = c('names', 'city', 'values'))
pydata

pydata = pydata %>% mutate(city = as.numeric(as.factor(city))) # converting city names to numeric values
pydata

# pydata = pydata %>% mutate(city = rep(1:(nrow(pydata)/4), each = 4)) # labels each city (can handle n-cities)

dayta = data_frame(city = pydata$city,
                   symbol = rep(1:4, nrow(pydata)/4),
                   start = pydata$values)

dayta = dayta %>% mutate(end = ifelse(symbol %in% c(1,3), lead(start), lag(start))) %>% select(3,4,2,1) # rearranges start/end values

dayta
dayta = wrap_about(dayta)
dayta

dayta = dayta %>%
        mutate(ring = ifelse(symbol %in% c(1,2), 1, 2),
               gen = ifelse(ring == 1, 5, 5.9),
               # gen = ring*1.25 + 5,
               # loc = ifelse(city == 1, -.15, .15),
               loc = ifelse(city%%2==0, -.15*city, +.15*city),
               # xmin = gen+loc-.1,
               # xmax = gen+loc+.1,
               xmin = gen+loc-.23,
               xmax = gen+loc+.23,
               # xmin = ifelse(ring == 1, gen+loc-.23, gen+loc),
               # xmax = ifelse(ring == 1, gen+loc+.23, gen+loc),
               # alpha = 1/city,
               beta = ifelse(ring == 1, 1, 1),
               clr = colors[symbol]) %>%
        filter(symbol != 4)

dayta

# naming the colors as themselves, then arranging labels as needed, apparently works? not sure why, just got it by playing around.
colors = c('#f4c20d' = '#f4c20d', '#4885ed' = '#4885ed', '#3cba54' = '#3cba54', '#db3236' = '#db3236')

dayta

ggplot(data = dayta, aes(fill = clr)) +
  geom_rect(aes(xmin = xmin, xmax = xmax, ymin = start, ymax = end), color = 'grey', alpha = 1) +
  # geom_rect(aes(xmin = xmin, xmax = xmax, ymin = start, ymax = end), alpha = .65) +
  geom_rect(aes(xmin = 2, xmax = 10, ymin = 11.95, ymax = 12.05), fill = '#808080', alpha = 1) +
  annotate("text", x = 10.5, y = 12, label = 'Now', size = 4) +
  annotate("text", x = 1, y = 12, label = "City Name", size = 8) +
  annotate("text", x = 1, y = 0, label = "Other City", size = 7, alpha = .5) +
  lims(x = c(0,12), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  scale_fill_manual(name = 'Time of Day', values = colors, labels = c('office', 'night', 'day')) +
  # scale_fill_manual(name = 'Time of Day', values = colors, labels = c('day', 'night', 'work', 'home')) +
  # scale_alpha_continuous(guide = FALSE) +
  theme_void() + theme(legend.title = element_text())
  # theme_minimal()

dayta



# TODO: DESIGN
# two levels of color (pick a light and dark pair for each of the colors)
# assign color pairs to each of the rings.
# make the two city the same size and space them out appropriately. 




