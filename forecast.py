
import urllib2 as u2
import simplejson as sj

def getForecast(forecastAPIKey, locationLatLong, forecastURL='https://api.forecast.io/forecast', timeout=10):
    # Make the call to the forecast site
    fullURL = forecastURL + '/' + forecastAPIKey + '/' + locationLatLong
    print 'Getting info from %s' % fullURL
    webContent = u2.urlopen(fullURL, timeout=timeout) # Get json-formatted weather info

    dataArray = []
    for i in webContent:
        dataArray.append(i)

    if not len(dataArray) > 0:
        print 'No weather data returned from %s' % forecastURL
        return None

    jsonRoot = sj.loads(dataArray[0])

    return jsonRoot