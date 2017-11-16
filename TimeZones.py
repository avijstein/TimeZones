from datetime import datetime, timedelta, date, time
import requests, json
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import seaborn as sns

# Longitudinal Time Difference

def conTimeZones(longitude_shift):
    """
    This function accepts a shift in decimal degrees and calculates
    the new apparent time in the new location.
    """
    if abs(longitude_shift) / 360 >= 1:
        return('Please enter valid distance.')

    now = datetime.utcnow()
    shift_sec = longitude_shift*240
    if shift_sec >= 0:
        diff = -timedelta(seconds = abs(shift_sec))
    else:
        diff = timedelta(seconds = abs(shift_sec))
    return(diff)


# sample city locations
indianapolis = [39.768597, -86.162682]
nyc = [40.730610, -73.935242]
philly = [39.952583, -75.165222]
durham = [35.994034, -78.898621]

# Sunrise Sunset Markers
def DayMarkers(city):
    """
    This function takes a city's latitude and longitude and calculates
    the sunrise, sunset, etc. This could be a city or any XY coordinate pair.
    """
    payload = {'lat':city[0], 'lng':0.0}
    r = requests.get('https://api.sunrise-sunset.org/json', params=payload)
    q = r.json()['results']
    day_markers = [q['sunrise'], q['solar_noon'], q['sunset'], q['day_length']]
    for i in range(0,3):
        day_markers[i] = datetime.strptime(day_markers[i], '%I:%M:%S %p')
        day_markers[i] = day_markers[i] + conTimeZones(city[1])
        day_markers[i] = datetime.time(day_markers[i])
    return(day_markers)

# Work Day Markers
def WorkMarkers(city):
    """
    This function takes XY coordinates and calculates the traditional
    "9-5" workday for that location in the UTC-0 time.
    """
    work_start = datetime.combine(datetime.utcnow(), time(hour = 9))
    work_lunch = datetime.combine(datetime.utcnow(), time(hour = 12))
    work_end = datetime.combine(datetime.utcnow(), time(hour = 17))
    shift = conTimeZones(city[1])
    work_param = [(work_start+shift),(work_lunch+shift),(work_end+shift)]
    for i in range(0,3):
        work_param[i] = datetime.time(work_param[i])
    return(work_param)

# day = DayMarkers(durham)
# work = WorkMarkers(durham)
#
# marker_names = ['sunrise','solar_noon','sunset','day_length',
#                 'work_start','work_lunch','work_end']
#
#
# all_markers = day + work
#
# for i in range(0,len(all_markers)):
#     if marker_names[i] == 'sunset':
#         print(marker_names[i], '\t', '\t', all_markers[i])
#     else:
#         print(marker_names[i], '\t', all_markers[i])
#



import matplotlib.pyplot as plt

times = ['daytime', 'nighttime']
# lengths = [(sunset-sunrise), (24 - (sunset-sunrise)), sunrise, sunset]
lengths = [(21-11.5), (24 - (21-11.5)), 11.5, 21]
shades = ['orange','blue']
start = (15*lengths[2]) + 90
worktimes = ['before_work', 'before_lunch', 'after_lunch', 'after_work', 'sleeping']
worklengths = [2,3,5,6,8]

# plt.pie(sizes, explode=explode, labels=labels, colors=colors, radius=1.25)
plt.pie(lengths[0:2], labels=times, colors=shades, startangle=-start, counterclock=False, radius=1.25)
# plt.pie(worklengths, labels=worktimes, startangle=(15*()), radius=1)

#draw a circle at the center of pie to make it look like a donut
centre_circle = plt.Circle((0,0),0.75, color='white', fc='white',linewidth=1.25)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.show()


















# bottom
