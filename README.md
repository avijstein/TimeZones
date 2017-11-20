# TimeZones


I've thought for a while about how weird time zones are. This morning I decided I wanted to come up with a solution for it. Not a practical one, mind you. Just a solution.

My two biggest complaints about time zones are:
* Times can be different over small distances (e.g. crossing a political boundary).
* They don't always correspond to geography.

The basis of this project stems from the idea that time is just a social construct (can you tell I went to a liberal arts college?). Yes, the time value (e.g. 03:45:26.223) is important for coordination, but the value is often not intrinsically important in normal life. I don't need to wake up at 06:23:45.734, I need to wake up an hour or so before work. The project aims to build a system by which our times are set by important events in our day, not by the values themselves.

My first objective has been to build a comparison between different cities, so we can see their differences. I've visualized each city as a pie plot, with important day markers as its rings. For example, here is just NYC as I'm writing this.

![NYC](/Ring Examples/nyc_sample.png)


Here is a comparison between several cities around the world at a different moment in time.

![Various Cities](/Ring Examples/sample_cities.png)
