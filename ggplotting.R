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

# It might be best to only limit the incoming data to two cities.
pydata = read_csv('for_ggplotting.csv', col_names = c('names', 'city', 'values'))
pydata

city_name = unique(pydata$city)

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

new_pal = data.frame('names' = c('Day1', 'Day2', 'Night1', 'Night2', 'Office1', 'Office2'),
                     'symbol' = rep(1:3, each = 2),
                     'city' = rep(1:2),
                     'hex_codes' = c('#C39B0A', '#F6CE3D', '#396ABD', '#6C9DF0', '#309443', '#62C776'),
                     stringsAsFactors = F)
new_pal = new_pal[c(6,4,5,3:1),]

dayta = dayta %>%
  filter(symbol != 4) %>%
  mutate(ring = ifelse(symbol %in% c(1,2), 1, 2),
                         gen = ifelse(ring == 1, 5, 6),
                         loc = ifelse(city == 1, -.25, +.25),
                         xmin = gen+loc-.25,
                         xmax = gen+loc+.25)

dayta = dayta %>% left_join(y = new_pal, by = c('symbol', 'city'))


ggplot(data = dayta, aes(fill = hex_codes)) +
  geom_rect(aes(xmin = xmin, xmax = xmax, ymin = start, ymax = end, fill = hex_codes), color = 'grey') +
  geom_rect(aes(xmin = 3, xmax = 8, ymin = 11.95, ymax = 12.05), fill = '#808080', alpha = 1) +
  annotate("text", x = 8.5, y = 12, label = 'Now', size = 4) +
  annotate("text", x = 1, y = 12, label = city_name[1], size = 8) +
  annotate("text", x = 1, y = 0, label = city_name[2], size = 8, alpha = .5) +
  lims(x = c(0,12), y = c(0,24)) +
  coord_polar(theta = 'y', start = pi) +
  scale_fill_manual(name = 'Time of Day', values = new_pal$hex_codes, labels = new_pal$names) +
  theme_void() + theme(legend.title = element_text())

