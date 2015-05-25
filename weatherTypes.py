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
            return None
        _dataPoint.__init__(self, currently)

class Minutely():
    def __init__(self, jsonDict):
        minutely = jsonDict.get('minutely')
        if not minutely:
            print 'Bad json dictionary; no "minutely" data'
            return None
        self.summary = minutely.get('summary')
        self.icon = minutely.get('icon')
        self.minutes = []
        data = minutely.get('data')
        for minute in data:
            self.minutes.append(_dataPoint(minute))

class Hourly():
    def __init__(self, jsonDict):
        hourly = jsonDict.get('hourly')
        if not hourly:
            print 'Bad json dictionary; no "hourly" data'
            return None
        self.summary = hourly.get('summary')
        self.icon = hourly.get('icon')
        self.hours = []
        data = hourly.get('data')
        for hour in data:
            self.hours.append(_dataPoint(hour))

class Daily():
    def __init__(self, jsonDict):
        daily = jsonDict.get('daily')
        if not daily:
            print 'Bad json dictionary; no "daily" data'
            return None
        self.summary = daily.get('summary')
        self.icon = daily.get('icon')
        self.days = []
        data = daily.get('data')
        for day in data:
            self.days.append(_dataPoint(day))

class Location():
    def __init__(self, jsonDict):
        self.latitude = jsonDict.get('latitude')
        self.longitude = jsonDict.get('longitude')
        self.timezone = jsonDict.get('timezone')
        self.offset = jsonDict.get('offset')

class Weather():
    def __init__(self, jsonDict):
        self.currently = Currently(jsonDict)
        self.minutely = Minutely(jsonDict)
        self.hourly = Hourly(jsonDict)
        self.daily = Daily(jsonDict)
        self.location = Location(jsonDict)
