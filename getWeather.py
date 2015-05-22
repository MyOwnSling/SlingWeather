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

from weatherTypes import *
from forecast import getForecast

forecastInfo = getForecast(forecastAPIKey, forecastLocation)

weather = Weather(forecastInfo)

#min = Minutely(jsonRoot)
print weather.minutely.summary
print weather.minutely.minutes[0].precipProbability
print ''

#cur = Currently(jsonRoot)
print weather.currently.time
print weather.currently.temperature
print ''

#hour = Hourly(jsonRoot)
print weather.hourly.summary
print weather.hourly.hours[12].time
print weather.hourly.hours[12].temperature
print weather.hourly.hours[12].summary
print ''

#day = Daily(jsonRoot)
print weather.daily.summary
print weather.daily.days[2].time
print weather.daily.days[2].temperatureMax
print weather.daily.days[2].summary
print ''

#loc = Location(jsonRoot)
print weather.location.latitude, weather.location.longitude
print weather.location.timezone
print weather.location.offset
print ''

print 'Done'
