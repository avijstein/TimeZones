# Tasks

## Time

### General Time Functions / Continuous Time Zones

We can get the current time using the `time.gmtime()` function in Python. This gives a tuple of the current UTC-0 datetime broken down by category (e.g. year, month, day). It's displayed nicely (as a string) with the `time.asctime()` function.

By converting to a list, modifying the list, and then converting back, we can change the time.

Okay, it turns out that the `datetime` library is so much better than `time`. It has much smarter, cleaner functions. Instead of 10 lines plus my own function, it uses two lines and its own functions.

Latitude doesn't affect the time difference at all, even in combination with longitude. Because we're using decimal degrees as the difference (rather than kilometers, or another measurement that would be distorted with projection or latitudinally dependent), the difference is a combination of the vertical and horizontal vectors.

Longitude is a remarkably simple calculation. If we assume no leap seconds, there are 62,400 seconds (24 hours) around the globe in 360 degrees. This is a clean 240 seconds for 1 degree.

A difference of 5.3 degrees would be 1272.0 second time difference.

Now that I'm getting the hang of changing times based on distance, I realized I've reinvented time zones. Albeit, these are now continuous time zones rather than discrete, generally by the hour, time zones.


### Sunrise / Sunset

I'm using this sunrise-sunset [API](https://sunrise-sunset.org/api). This is baby's first API accessed by Python all by himself! So far it's going pretty well, considering this is a great, easy API to work with.


There's something weird going on right now. The sunrise times should line up exactly thanks to continuous times zones, but that's not what we're seeing. Indianapolis and Philly are on the same line of latitude, but are on opposite sides of the time zone. They should be 45 minutes apart (according to my continuous time zone calculations), and their sunrise times should be 45 minutes apart (according to google), but when entering their XY coordinates into the API, I'm getting their sunrise times as being identical. I'm not sure yet where the error is. This is for you to work on tomorrow.

Okay, I think I've figured some of the problem out. The time that's returned is a time in UTC-0, which is just asking to be converted to its local time zone. For example, I entered Durham, NC into the latitude and longitude, and it returned 11:50am, or at what time in UTC-0 time the sunrise would happen.

What I would like is a time that is not based on the old time zone system. In this example, a value that is exactly 5 hours ahead. Instead, I would like to know what the sunrise value would be at the prime meridian (at latitude, because that changes sunrise times), so that I can adjust its value based my continuous time zone calculation.

The problem I'm currently running into is that this doesn't quite work. My assumption is that as you move around the world on a line of constant latitude, I expect the sunrise at that location, consistent with a continuous time zone, to be the same.

I think I got it. I've just been confusing myself here. When I give it Durham's latitude and 0.0 longitude, I get a sunrise time of ~6:35am. Durham's sunrise is at 6:51am. If I want to see this number, I need to ignore the major time zone difference (as it is doing), and only adjust to where Durham is in the time zone. In our case, it's 16 minutes from the center, which explains this difference. However, the point of this project wasn't to get that exact number, it was to have the comparison points of sunrise and sunset and work time hours without the exact numbers. The UTC time for Durham, NC at sunrise is 11:51.











<!-- bottom -->
