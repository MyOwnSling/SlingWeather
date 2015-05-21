#!/usr/bin/python

import urllib2 as u2
import simplejson as sj
import datetime as dt
import sys

if len(sys.argv) != 3:
    print 'Bad arg count'
    sys.exit(1)

api = sys.argv[1]
loc = sys.argv[2]

# All info needed for the forecast.io service
forecastAPIKey = api
forecastURL = 'https://api.forecast.io/forecast'
forecastLocation = loc
timeout = 10

def printCurrent(jsonString):
    for top in jsonRoot:
        if top == 'currently':
            print top
            for mid in jsonRoot[top]:
                print '\t%s: %s' % (mid, jsonRoot[top][mid])

def printLatLong(jsonString):
    latitude = jsonRoot['latitude']
    longitude = jsonRoot['longitude']

    print 'Lat/Long'
    print '\t%s, %s' % (latitude, longitude)

def printDaily(jsonString):
    icon = jsonRoot['daily']['icon']
    dataDict = jsonRoot['daily']['data']
    print 'Daily: %s' % icon
    for dayData in dataDict:
        time = dt.date.fromtimestamp(dayData['time'])
        print '\t%s' % time
        for c in dayData:
            data = dayData[c]
            if 'time' in str(c).lower():
                data = dt.datetime.fromtimestamp(data)
            print '\t\t%s: %s' % (c, data)

def printFlags(jsonString):
    for tag in jsonString['flags']:
        print tag
        if tag == 'units':
            print '\t%s' % jsonString['flags'][tag]
            continue
        for data in jsonString['flags'][tag]:
            print '\t%s' % data

def printHourly(jsonString):
    icon = jsonString['hourly']['icon']
    print 'Hourly: %s' % icon
    hourlyData = jsonString['hourly']['data']
    for hour in hourlyData:
        time = dt.datetime.fromtimestamp(hour['time'])
        print '\t%s' % time
        for i in hour:
            if i == 'time':
                continue
            print '\t\t%s: %s' % (i, hour[i])

def printMinutely(jsonString):
    icon = jsonString['minutely']['icon']
    print 'Minutely: %s' % icon
    minutelyData = jsonString['minutely']['data']
    for minute in minutelyData:
        time = dt.datetime.fromtimestamp(minute['time'])
        print '\t%s' % time
        for i in minute:
            if i == 'time':
                continue
            print '\t\t%s: %s' % (i, minute[i])

# Make the call to the forecast site
fullURL = forecastURL + '/' + forecastAPIKey + '/' + forecastLocation
print 'Getting info from %s' % fullURL
webContent = u2.urlopen(fullURL, timeout=timeout) # Get json-formatted weather info

dataArray = []
for i in webContent:
    dataArray.append(i)

if not len(dataArray) > 0:
    print 'No weather data returned from %s' % forecastURL

jsonRoot = sj.loads(dataArray[0])
#printCurrent(jsonRoot)
#printLatLong(jsonRoot)
#printDaily(jsonRoot)
#printFlags(jsonRoot)
#printHourly(jsonRoot)
#printMinutely(jsonRoot)
# TODO: offset and timezone

from weatherTypes import *
min = Minutely(jsonRoot)
print min.summary
print min.minutes[0].precipProbability
print ''

cur = Currently(jsonRoot)
print cur.time
print cur.temperature
print ''

hour = Hourly(jsonRoot)
print hour.summary
print hour.hours[12].time
print hour.hours[12].temperature
print hour.hours[12].summary
print ''

day = Daily(jsonRoot)
print day.summary
print day.days[2].time
print day.days[2].temperatureMax
print day.days[2].summary
print ''

loc = Location(jsonRoot)
print loc.latitude, loc.longitude
print loc.timezone
print loc.offset
print ''

print 'Done'
