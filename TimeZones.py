from datetime import datetime, timedelta, date
import requests, json
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

# print('durham time: ', now + (conTimeZones(durham[1])))
# print('indianapolis time: ', now + conTimeZones(indianapolis[1]))
# print('philly time: ', now + conTimeZones(philly[1]))
# print('UTC time: ', now)
# print(now + conTimeZones(78.898621))
# print('\n')
# print(conTimeZones(durham[1]))
# print('\n')

# Sunrise Sunset
# city = durham
# payload = {'lat':city[0], 'lng':0.0}
# r = requests.get('https://api.sunrise-sunset.org/json', params=payload)
#
# print(r.json())
# q = r.json()['results']
# # qtime = q['sunrise']
# # print(qtime)
#
# day_markers = [q['sunrise'], q['solar_noon'], q['sunset'], q['day_length']]
# print('old day_markers: ', day_markers)
#
# for i in range(0,3):
#     day_markers[i] = datetime.strptime(day_markers[i], '%I:%M:%S %p')
#     day_markers[i] = day_markers[i] + conTimeZones(city[1])
#     day_markers[i] = datetime.time(day_markers[i])
#
# # print('new day_markers: ', day_markers)
# marker_names = ['sunrise','solar_noon','sunset','day_length']
# for i in range(0,len(day_markers)):
#     print(marker_names[i], '\t', day_markers[i])


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

x = DayMarkers(durham)

marker_names = ['sunrise','solar_noon','sunset','day_length']
print('CITY: Durham, NC')
for i in range(0,len(x)):
    print(marker_names[i], '\t', x[i])







# bottom
