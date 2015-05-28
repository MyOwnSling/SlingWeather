#!/usr/bin/python

import sys
import time
from subprocess import call

def evalWeather(apikey, location, threshold=.5):
    forecastInfo = getForecast(apikey, location)
    weather = Weather(forecastInfo)

    minutes = weather.minutely.minutes
    i = 1
    for min in minutes:
        if min.precipProbability != None:
            if min.precipProbability >= threshold:
                msg = str(min.precipProbability * 100) + "% chance of " + min.precipType + " in " + str(i) + " minute(s)"
                delay = 60 * i
                call([publishScript, msg, str(delay)])
                return
        i += 1

if len(sys.argv) != 4:
    print 'Bad arg count:'
    print '\tmonitorWeather.py <apiKey> <locationLatLong> <publishScript>'
    sys.exit(1)

api = sys.argv[1]
loc = sys.argv[2]
publishScript = sys.argv[3]

# Sleep interval
interval = 30 * 60

# All info needed for the forecast.io service
forecastAPIKey = api
forecastURL = 'https://api.forecast.io/forecast'
forecastLocation = loc
timeout = 10

from weatherTypes import *
from forecast import getForecast

# Evaluate the weather and wait for a little while
while True:
    evalWeather(forecastAPIKey, forecastLocation)
    time.sleep(interval)


print '************************************************************************************'
