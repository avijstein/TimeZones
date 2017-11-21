from time import sleep
from datetime import datetime, timedelta, date, time
import requests, json
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
# import pandas as pd
# import seaborn as sns

# sample city locations
indianapolis = [39.768597, -86.162682, 'Indianapolis']
nyc = [40.730610, -73.935242, 'NYC']
philly = [39.952583, -75.165222, 'Philly']
durham = [35.994034, -78.898621, 'Durham']
alameda =  [37.767282, -122.246999, 'Alameda']
dubai = [25.276987, 55.296249, 'Dubai']
beijing = [39.913818, 116.363625, 'Beijing']
sydney = [-33.865143, 151.209900, 'Sydney']

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
    right_now = (datetime.utcnow()).time()
    # rightnow = (right_now - datetime.combine(right_now, time.min)).total_seconds()/3600
    # print(right_now)
    shift = conTimeZones(city[1])
    work_param = [(work_start+shift),(work_lunch+shift),(work_end+shift),(right_now)]
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
                    'work_start','work_lunch','work_end','right_now']
    all_markers = day + work
    if display == True:
        print('City: ', '\t', '\t', city[2].upper())
        for i in range(0,len(all_markers)):
            if marker_names[i] == 'sunset':
                print(marker_names[i], '\t', '\t', all_markers[i])
            else:
                print(marker_names[i], '\t', all_markers[i])
    return(all_markers)

def tdiff(times):
    """
    This function calculates daytime and nighttime, as well as sunrise/sunset
    times. It accepts two datetime.time objects and a string, and returns four
    floats of the data needed for plotting.
    """
    thyme = [times[0], times[2], times[3], times[4], times[6], times[7]]
    for t in range(0,len(thyme)):
        thyme[t] = datetime.strptime(str(thyme[t])[:8], '%H:%M:%S')
        thyme[t] = (thyme[t] - datetime.combine(thyme[t], time.min)).total_seconds()/3600
    daytime, nighttime, sunrise, sunset = thyme[2], 24-thyme[2], thyme[0], thyme[1]
    work_time, free_time, work_start, work_end, right_now = 8, 24-8, thyme[3], thyme[4], thyme[5]
    return([daytime, nighttime, sunrise, sunset, work_time, free_time, work_start, work_end, right_now])

def Plotting(city, plot):
    """
    This function calcuates the plotting parameters and plots them.
    It accepts a list of time parameters for a location and a boolean for
    graphing, and returns a graph (if needed).
    """
    data = tdiff(AllMarkers(city, True))
    labels = ['day', 'night']
    colors = ['#f4c20d', '#4885ed']
    offset = -((15*data[2]) + 90)

    work_labels = ['office', 'home']
    work_colors = ['#3cba54', '#db3236']
    work_offset = -((15*data[6]) + 90)

    now_data = [0.1, 24 - 0.1]
    now_labels = ['now', '']
    grey = plt.cm.Greys
    now_colors = [grey(.999), grey(.001)]
    now_offset = -((15*data[8]) + 90)


    a = plt.pie(now_data, labels=now_labels, colors=now_colors, startangle=now_offset,
                          labeldistance=1.1, counterclock=False, radius=1)
    b= plt.pie(data[4:6], labels=None, colors=work_colors, startangle=work_offset,
                          labeldistance=1.1, counterclock=False, radius=.75)
    c = plt.pie(data[0:2], labels=None, colors=colors, startangle=offset,
                           labeldistance=.25, counterclock=False, radius=.5)
    # centre_circle = plt.Circle((0,0),0.5, color='white', fc='white',linewidth=1.25)
    d = plt.pie(now_data, labels=None, colors=now_colors, startangle=now_offset,
                          labeldistance=0, counterclock=False, radius=.25)
    fig = plt.gcf()
    # fig.gca().add_artist(centre_circle)
    # fig.legend([centre_circle], [city[2]])
    plt.axis('equal')
    plt.suptitle(city[2])
    plt.legend(b[0] + c[0], work_labels + labels, title = 'Times of Day')

    if plot == True:
        plt.show()

def GridPlotting(cities):
    dims = int(np.sqrt(len(cities)))
    the_grid = GridSpec(dims, dims)
    i = 0
    for j in range(0,dims):
        for k in range(0,dims):
            data = tdiff(AllMarkers(cities[i], False))
            labels = ['day', 'night']
            # colors = ['orange','blue']
            colors = ['#f4c20d', '#4885ed']
            offset = -((15*data[2]) + 90)

            work_labels = ['office', 'home']
            # work_colors = [plt.cm.Greens(.85), plt.cm.Reds(.70)]
            work_colors = ['#3cba54', '#db3236']
            work_offset = -((15*data[6]) + 90)

            now_data = [0.1, 24 - 0.1]
            now_labels = ['now', '']
            grey = plt.cm.Greys
            now_colors = [grey(.999), grey(.001)]
            now_offset = -((15*data[8]) + 90)
            # now_offset = 90

            ax = plt.subplot(the_grid[j, k], aspect=1)
            a = plt.pie(now_data, labels=now_labels, colors=now_colors, startangle=now_offset,
                              labeldistance=1.07, counterclock=False, radius=1.25)
            b = plt.pie(data[4:6], labels=None, colors=work_colors, startangle=work_offset,
                               labeldistance=1.1, counterclock=False, radius=1.0)
            c = plt.pie(data[0:2], labels=None, colors=colors, startangle=offset,
                               labeldistance=.1, counterclock=False, radius=.75)
            # centre_circle = plt.Circle((0,0),1.0, color='white', fc='white',linewidth=1.25)
            d = plt.pie(now_data, labels=None, colors=now_colors, startangle=now_offset,
                              labeldistance=0, counterclock=False, radius=.5)
            fig = plt.gcf()

            # fig.gca().add_artist(centre_circle)
            ax.set_title(cities[i][2])
            plt.axis('equal')
            i += 1

    plt.suptitle('Cities Without Timezones')
    plt.subplots_adjust(left=.04, bottom=.04, right=.98, top=.88, wspace=.35, hspace=.17)
    plt.legend(b[0] + c[0], work_labels + labels, loc = (-.3, .85), title = 'Time of Day')
    plt.show()

def Comparison(cities, rings):
    data1 = tdiff(AllMarkers(cities[0], True))
    data2 = tdiff(AllMarkers(cities[1], True))

    now_data = [0.1, 24 - 0.1]
    now_labels = ['now', '']
    now_colors = [plt.cm.Greys(.999), plt.cm.Greys(.001)]
    now_offset = -((15*data1[8]) + 90)

    if rings == 'daylight':
        labels = ['day', 'night']
        colors = ['#f4c20d', '#4885ed']
        offset1 = -((15*data1[2]) + 90)
        offset2 = -((15*data2[2]) + 90)
        data1 = data1[0:2]
        data2 = data2[0:2]
    if rings == 'workday':
        labels = ['office', 'home']
        colors = ['#3cba54', '#db3236']
        offset1 = -((15*data1[6]) + 90)
        offset2 = -((15*data2[6]) + 90)
        data1 = data1[4:6]
        data2 = data2[4:6]

    a = plt.pie(now_data, labels=now_labels, colors=now_colors, startangle=now_offset,
                          labeldistance=1.07, counterclock=False, radius=1.25)
    b = plt.pie(data1, labels=None, colors=colors, startangle=offset1,
                           labeldistance=.1, counterclock=False, radius=1.0)
    c = plt.pie(data2, labels=None, colors=colors, startangle=offset2,
                           labeldistance=.1, counterclock=False, radius=.75)
    d = plt.pie(now_data, labels=None, colors=now_colors, startangle=now_offset,
                          labeldistance=0, counterclock=False, radius=.5)
    fig = plt.gcf()
    plt.axis('equal')

    plt.suptitle(cities[0][2] + ' and ' + cities[1][2])
    plt.legend(b[0], labels, title = 'Times of Day')
    # fig.set_edgecolor('black')
    plt.show()

def Comparison2(cities):
    the_grid = GridSpec(1, 2)

    data1 = tdiff(AllMarkers(cities[0], True))
    data2 = tdiff(AllMarkers(cities[1], True))

    now_data = [0.1, 24 - 0.1]
    now_labels = ['now', '']
    now_colors = [plt.cm.Greys(.999), plt.cm.Greys(.001)]
    now_offset = -((15*data1[8]) + 90)

    # DAYLIGHT PLOT
    ax = plt.subplot(the_grid[0, 0], aspect=1)

    labels = ['day', 'night']
    colors = ['#f4c20d', '#4885ed']
    offset1 = -((15*data1[2]) + 90)
    offset2 = -((15*data2[2]) + 90)

    a1 = plt.pie(now_data, labels=now_labels, colors=now_colors, startangle=now_offset,labeldistance=1.07,counterclock=False,radius=1.25)
    b1 = plt.pie(data1[0:2], labels=None, colors=colors, startangle=offset1, labeldistance=.1, counterclock=False, radius=1.0)
    c1 = plt.pie(data2[0:2], labels=None, colors=colors, startangle=offset2, labeldistance=.1, counterclock=False, radius=.75)
    d1 = plt.pie(now_data, labels=None, colors=now_colors, startangle=now_offset, labeldistance=0, counterclock=False, radius=.5)

    ax.set_title('Daylight')

    # WORKDAY PLOT
    ax = plt.subplot(the_grid[0, 1], aspect=1)

    work_labels = ['office', 'home']
    work_colors = ['#3cba54', '#db3236']
    offset1 = -((15*data1[6]) + 90)
    offset2 = -((15*data2[6]) + 90)

    a2 = plt.pie(now_data, labels=now_labels, colors=now_colors, startangle=now_offset, labeldistance=1.07,counterclock=False,radius=1.25)
    b2 = plt.pie(data1[4:6], labels=None, colors=work_colors, startangle=offset1, labeldistance=.1, counterclock=False, radius=1.0)
    c2 = plt.pie(data2[4:6], labels=None, colors=work_colors, startangle=offset2, labeldistance=.1, counterclock=False, radius=.75)
    d2 = plt.pie(now_data, labels=None, colors=now_colors, startangle=now_offset, labeldistance=0, counterclock=False, radius=.5)

    ax.set_title('Workday')


    fig = plt.gcf()
    plt.axis('equal')

    plt.suptitle(cities[0][2] + ' and ' + cities[1][2])
    plt.legend(b1[0] + b2[0], labels + work_labels, loc = (-.4,.75), title = 'Time of Day')
    # plt.subplots_adjust(left=.04, bottom=.04, right=.98, top=.88, wspace=.35, hspace=.17)
    plt.show()


# Plotting(nyc, True)
# GridPlotting([durham, beijing, dubai, sydney])
# Comparison([durham, dubai], 'daylight')
# Comparison2([durham, dubai])







# bottom
