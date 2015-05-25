#!/usr/bin/python

import urllib2 as u2
import simplejson as sj
import datetime as dt
import sys


class _dataPoint(dict):
    def __init__(self, dataBlock):
        # Assign dataBlock dictionary to this object's inherited dict (iteratively)
        for key in dataBlock:
            self[key] = dataBlock[key]

        # Get all of the values in the data block
        self.time       = dataBlock.get('time')
        self.summary    = dataBlock.get('summary')
        self.icon       = dataBlock.get('icon')
        self.nearestStormDistance       = dataBlock.get('nearestStormDistance')
        self.nearestStormBearing        = dataBlock.get('nearestStormBearing')
        self.precipIntensity            = dataBlock.get('precipIntensity')
        self.precipProbability          = dataBlock.get('precipProbability')
        self.precipType                 = dataBlock.get('precipType')
        self.precipAccumulation         = dataBlock.get('precipAccumulation')
        self.temperature                = dataBlock.get('temperature')
        self.apparentTemperature        = dataBlock.get('apparentTemperature')
        self.dewPoint                   = dataBlock.get('dewPoint')
        self.humidity                   = dataBlock.get('humidity')
        self.windSpeed                  = dataBlock.get('windSpeed')
        self.windBearing                = dataBlock.get('windBearing')
        self.visibility                 = dataBlock.get('visibility')
        self.cloudCover                 = dataBlock.get('cloudCover')
        self.pressure                   = dataBlock.get('pressure')
        self.ozone                      = dataBlock.get('ozone')
        self.moonPhase                  = dataBlock.get('moonPhase')
        self.sunriseTime                = dataBlock.get('sunriseTime')
        self.sunsetTime                 = dataBlock.get('sunsetTime')
        self.precipIntensityMax         = dataBlock.get('precipIntensityMax')
        self.precipIntensityMaxTime     = dataBlock.get('precipIntensityMaxTime')
        self.temperatureMin             = dataBlock.get('temperatureMin')
        self.temperatureMinTime         = dataBlock.get('temperatureMinTime')
        self.temperatureMax             = dataBlock.get('temperatureMax')
        self.temperatureMaxTime         = dataBlock.get('temperatureMaxTime')
        self.apparentTemperatureMin     = dataBlock.get('apparentTemperatureMin')
        self.apparentTemperatureMinTime = dataBlock.get('apparentTemperatureMinTime')
        self.apparentTemperatureMax     = dataBlock.get('apparentTemperatureMax')
        self.apparentTemperatureMaxTime = dataBlock.get('apparentTemperatureMaxTime')

        # Convert all of the time values from raw to human-readable
        if self.time:
            self.time = dt.datetime.fromtimestamp(self.time)
            self['time'] = self.time
        if self.apparentTemperatureMaxTime:
            self.apparentTemperatureMaxTime = dt.datetime.fromtimestamp(self.apparentTemperatureMaxTime)
            self['apparentTemperatureMaxTime'] = self.apparentTemperatureMaxTime
        if self.apparentTemperatureMinTime:
            self.apparentTemperatureMinTime = dt.datetime.fromtimestamp(self.apparentTemperatureMinTime)
            self['apparentTemperatureMinTime'] = self.apparentTemperatureMinTime
        if self.precipIntensityMaxTime:
            self.precipIntensityMaxTime = dt.datetime.fromtimestamp(self.precipIntensityMaxTime)
            self['precipIntensityMaxTime'] = self.precipIntensityMaxTime
        if self.sunriseTime:
            self.sunriseTime = dt.datetime.fromtimestamp(self.sunriseTime)
            self['sunriseTime'] = self.sunriseTime
        if self.sunsetTime:
            self.sunsetTime = dt.datetime.fromtimestamp(self.sunsetTime)
            self['sunsetTime'] = self.sunsetTime
        if self.temperatureMaxTime:
            self.temperatureMaxTime = dt.datetime.fromtimestamp(self.temperatureMaxTime)
            self['temperatureMaxTime'] = self.temperatureMaxTime
        if self.temperatureMinTime:
            self.temperatureMinTime = dt.datetime.fromtimestamp(self.temperatureMinTime)
            self['temperatureMinTime'] = self.temperatureMinTime

class Currently(_dataPoint):
    def __init__(self, jsonDict):
        # Parse through the json string
        currently = jsonDict.get('currently')
        if not currently:
            print 'Bad json dictionary; no "currently" data'
            return
        _dataPoint.__init__(self, currently)

    def printData(self, full=False):
        if full:
            print 'time', ':', self.time
            print 'summary', ':', self.summary
            print
            for key in self:
                if key != 'time' and key != 'summary':
                    print key, ':', self[key]
        else:
            print self.time
            print self.summary
            print
            print 'Temperature: ', self.temperature, 'F'
            print 'Wind speed:', self.windSpeed, 'MPH'
            print 'Wind bearing (from):', self.windBearing, 'deg'
            print 'Precipitation chance:', self.precipProbability * 100, '%'
            print
            if self.nearestStormDistance != None:
                print 'Nearest storm distance:', self.nearestStormDistance, 'mi'
                print 'Nearest storm bearing:', self.nearestStormBearing, 'deg'
                print
            print 'Humidity:', self.humidity * 100, '%'
            print 'Dew point:', self.dewPoint, 'F'
            print 'Visibility:', self.visibility, 'mi'
            print 'Cloud cover:', self.cloudCover * 100, '%'
            print 'Pressure:', self.pressure, 'mb'
            print 'Ozone:', self.ozone

class Minutely():
    def __init__(self, jsonDict):
        minutely = jsonDict.get('minutely')
        if not minutely:
            print 'Bad json dictionary; no "minutely" data'
            return
        self.summary = minutely.get('summary')
        self.icon = minutely.get('icon')
        self.minutes = []
        data = minutely.get('data')
        for minute in data:
            self.minutes.append(_dataPoint(minute))

    def printData(self, full=False):
        print
        print self.summary
        if full:
            for minute in self.minutes:
                for key in minute:
                    print key, ':', minute[key]
                print
        else:
            for minute in self.minutes:
                print
                print str(minute.time).split(' ')[1]
                print '\tPrecipitation chance:', minute.precipProbability * 100, '%'
                if minute.precipProbability != 0:
                    print '\tType:', minute.precipType
                    print '\tIntensity:', minute.precipIntensity, 'in/hr'
                if minute.precipAccumulation != None:
                    print '\tAccumulation:', minute.precipIntensity, 'in/hr'

class Hourly():
    def __init__(self, jsonDict):
        hourly = jsonDict.get('hourly')
        if not hourly:
            print 'Bad json dictionary; no "hourly" data'
            return
        self.summary = hourly.get('summary')
        self.icon = hourly.get('icon')
        self.hours = []
        data = hourly.get('data')
        for hour in data:
            self.hours.append(_dataPoint(hour))

    def printData(self, full=False):
        print
        print self.summary
        if full:
            for hour in self.hours:
                for key in hour:
                    print key, ':', hour[key]
                print
        else:
            for hour in self.hours:
                print
                print hour.time
                print '\t', hour.summary
                print
                print '\tTemperature: ', hour.temperature, 'F'
                print '\tWind speed:', hour.windSpeed, 'MPH'
                print '\tWind bearing (from):', hour.windBearing, 'deg'
                print
                print '\tPrecipitation chance:', hour.precipProbability * 100, '%'
                if hour.precipProbability != 0:
                    print '\tType:', hour.precipType
                    print '\tIntensity', hour.precipIntensity, 'in/hr'
                if hour.precipAccumulation != None:
                    print '\tAccumulation:', hour.precipAccumulation, 'in'
                print
                if hour.nearestStormDistance != None:
                    print 'Nearest storm distance:', hour.nearestStormDistance, 'mi'
                    print 'Nearest storm bearing:', hour.nearestStormBearing, 'deg'
                    print
                print '\tHumidity:', hour.humidity * 100, '%'
                print '\tDew point:', hour.dewPoint, 'F'
                print '\tVisibility:', hour.visibility, 'mi'
                print '\tCloud cover:', hour.cloudCover * 100, '%'
                print '\tPressure:', hour.pressure, 'mb'
                print '\tOzone:', hour.ozone

class Daily():
    def __init__(self, jsonDict):
        daily = jsonDict.get('daily')
        if not daily:
            print 'Bad json dictionary; no "daily" data'
            return
        self.summary = daily.get('summary')
        self.icon = daily.get('icon')
        self.days = []
        data = daily.get('data')
        for day in data:
            self.days.append(_dataPoint(day))

    def printData(self, full=False):
        print
        print self.summary
        if full:
            for day in self.days:
                for key in day:
                    print key, ':', day[key]
                print
        else:
            for day in self.days:
                print
                print str(day.time).split(' ')[0]
                print '\t', day.summary
                print
                print '\tTemperature Low: ', day.temperatureMin, 'F'
                print '\tTemperature High: ', day.temperatureMax, 'F'
                if day.windSpeed != None:
                    print '\tWind speed:', day.windSpeed, 'MPH'
                    print '\tWind bearing (from):', day.windBearing, 'deg'
                print
                print '\tPrecipitation chance:', day.precipProbability * 100, '%'
                if day.precipProbability != 0:
                    print '\tType:', day.precipType
                    print '\tIntensity', day.precipIntensity, 'in/hr'
                if day.precipAccumulation != None:
                    print '\tAccumulation:', day.precipAccumulation, 'in'
                print
                if day.nearestStormDistance != None:
                    print 'Nearest storm distance:', day.nearestStormDistance, 'mi'
                    print 'Nearest storm bearing:', day.nearestStormBearing, 'deg'
                    print
                print '\tSunrise:', str(day.sunriseTime).split(' ')[1]
                print '\tSunset:', str(day.sunsetTime).split(' ')[1]
                print '\tMoon phase:', day.moonPhase * 100, '% full'
                print
                print '\tHumidity:', day.humidity * 100, '%'
                print '\tDew point:', day.dewPoint, 'F'
                print '\tVisibility:', day.visibility, 'mi'
                print '\tCloud cover:', day.cloudCover * 100, '%'
                print '\tPressure:', day.pressure, 'mb'
                print '\tOzone:', day.ozone

class Location():
    def __init__(self, jsonDict):
        self.latitude = jsonDict.get('latitude')
        self.longitude = jsonDict.get('longitude')
        self.timezone = jsonDict.get('timezone')
        self.offset = jsonDict.get('offset')

    def printData(self):
        print 'Lat/Long:', self.latitude, self.longitude
        print 'Timezone:', self.timezone, '/', self.offset, 'offset'

class Weather():
    def __init__(self, jsonDict):
        self.currently = Currently(jsonDict)
        self.minutely = Minutely(jsonDict)
        self.hourly = Hourly(jsonDict)
        self.daily = Daily(jsonDict)
        self.location = Location(jsonDict)
