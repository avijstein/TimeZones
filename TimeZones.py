from datetime import datetime, timedelta, date, time
import requests, json
import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import seaborn as sns

# Longitudinal Time Difference


# sample city locations
indianapolis = [39.768597, -86.162682, 'indianapolis']
nyc = [40.730610, -73.935242, 'nyc']
philly = [39.952583, -75.165222, 'philly']
durham = [35.994034, -78.898621, 'Durham']
alameda =  [37.767282, -122.246999, 'Alameda']

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

def AllMarkers(city, display):
    """
    This function combines the marker functions (to consolidated later).
    It accepts a city location and name, and boolean for display. It returns
    all of the markers, and possibly a print out of the values.
    """
    day = DayMarkers(city)
    work = WorkMarkers(city)
    marker_names = ['sunrise','solar_noon','sunset','day_length',
                    'work_start','work_lunch','work_end']
    all_markers = day + work
    if display == True:
        print('City: ', '\t', '\t', city[2].upper())
        for i in range(0,len(all_markers)):
            if marker_names[i] == 'sunset':
                print(marker_names[i], '\t', '\t', all_markers[i])
            else:
                print(marker_names[i], '\t', all_markers[i])
    return(all_markers)

def tdiff(time1, time2, time3):
    """
    This function calculates daytime and nighttime, as well as sunrise/sunset
    times. It accepts two datetime.time objects and a string, and returns four
    floats of the data needed for plotting.
    """
    a = datetime.strptime(str(time1), '%H:%M:%S.%f')
    b = datetime.strptime(str(time2), '%H:%M:%S.%f')
    c = datetime.strptime(str(time3), '%H:%M:%S')
    d = (a - datetime.combine(a, time.min)).total_seconds()/3600
    e = (b - datetime.combine(b, time.min)).total_seconds()/3600
    f = (c - datetime.combine(b, time.min)).total_seconds()/3600
    daytime, nighttime, sunrise, sunset = f, 24-f, d, e
    return([daytime, nighttime, sunrise, sunset])

def Plotting(times, cityname, plot):
    """
    This function calcuates the plotting parameters and plots them.
    It accepts a list of time parameters for a location and a boolean for
    graphing, and returns a graph (if needed).
    """
    data = tdiff(times[0], times[2], times[3])
    labels = ['daytime', 'nighttime']
    colors = ['orange','blue']
    offset = -((15*data[2]) + 90)

    plt.pie(data[0:2], labels=labels, colors=colors, startangle=offset, counterclock=False, radius=1)
    centre_circle = plt.Circle((0,0),0.75, color='white', fc='white',linewidth=1.25)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    fig.legend([centre_circle], [cityname])
    plt.axis('equal')
    if plot == True:
        plt.show()

# Plotting(AllMarkers(indianapolis, True), indianapolis[2], True)
# Plotting(AllMarkers(philly, True), philly[2], True)
Plotting(AllMarkers(durham, True), durham[2], True)
# Plotting(AllMarkers(alameda, True), alameda[2], True)


# worktimes = ['before_work', 'before_lunch', 'after_lunch', 'after_work', 'sleeping']
# worklengths = [2,3,5,6,8]





# bottom
