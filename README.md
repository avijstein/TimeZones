# TimeZones


I've thought for a while about how weird time zones are. This morning I decided I wanted to come up with a solution for it. Not a practical one, mind you. Just a solution.

My two biggest complaints about time zones are:
* Times can be different over small distances (e.g. crossing a political boundary).
* They don't always correspond to geography.

The basis of this project stems from the idea that time is just a social construct (can you tell I went to a liberal arts college?). Yes, the time value (e.g. 03:45:26.223) is important for coordination, but the value is often not intrinsically important in normal life. I don't need to wake up at 06:23:45.734, I need to wake up an hour or so before work. The project aims to build a system by which our times are set by important events in our day, not by the values themselves.

My first objective has been to build a comparison between different cities, so we can see their differences. I've visualized each city as a pie plot, with important day markers as its rings. For example, here is NYC as I'm writing this.

![NYC](/Ring%20Examples/nyc.png)


Here is a comparison between several cities around the world at a different moment in time.

![Various Cities](/Ring%20Examples/cities.png)

New cities for comparison can be added by using the Google Maps API, which geocodes a city to XY coordinates, and then the rest of the script adds the city to the graphs. Cities can be compared one-on-one, in a group of four, or by aligning their daytime and/or workday rings.

I [posted](https://redd.it/7g8597) this projected to r/dataisbeautiful to share / get feedback, which will be incorporated into new iterations of this project.

Because of the differing strengths and weaknesses of how Python's matplotlib and R's ggplot2 work, I tried recreating these graphs in R. I also tried to incorporate some feedback from Reddit, including thinner lines and minimalist color schemes. I don't know how well I succeeded. Some issues (e.g., transparency) were a breeze, but some (e.g., color picking and labeling) were a headache. Here is a sample of one of the graphs in R:

![ggplotting](/Ring%20Examples/ggplotting.png)


(This project uses a Google Maps API free key. I'm keeping mine private in a separate file, so cloning this repository would require a user to add their own key when using this specific API.)
