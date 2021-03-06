import requests
import logging
from .objects.weather_obj import WeatherObject
import sys
from .unit import Unit


class Weather(object):
    URL = 'http://query.yahooapis.com/v1/public/yql'
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def __init__(self, unit=Unit.CELSIUS):
        self.unit = unit

    def lookup(self, woeid):
        url = "%s?q=select * from weather.forecast where woeid = '%s' and u='%s' &format=json" % (
            self.URL, woeid, self.unit)
        results = self._call(url)
        return results

    def lookup_by_location(self, location):
        url = "%s?q=select* from weather.forecast " \
              "where woeid in (select woeid from geo.places(1) where text='%s') and u='%s' &format=json" % (
                  self.URL, location, self.unit)
        results = self._call(url)
        return results

    def lookup_by_latlng(self, lat, lng):
        url = "%s?q=select* from weather.forecast " \
              "where woeid in (select woeid from geo.places(1) where text='(%s,%s)') and u='%s' &format=json" % (
                  self.URL, lat, lng, self.unit)
        results = self._call(url)
        return results

    def _call(self, url):
        req = requests.get(url)
        self.logger.info("Status Code: %s" % req.status_code)
        if not req.ok:
            req.raise_for_status()

        try:
            results = req.json()
            if int(results['query']['count']) > 0:
                wo = WeatherObject(results['query']['results']['channel'])
                return wo
            else:
                self.logger.warn("No results found: %s " % results)
        except Exception as e:
            self.logger.warn(e)
            self.logger.warn(req.content)
            sys.exit(0)
