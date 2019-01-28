from typing import Dict, List
import datetime
import pyowm
from pyowm.exceptions.api_response_error import NotFoundError

from utils import extract_datetime

def assign_value(d: Dict, keys: List, value):
    for k in keys:
        d[k] = value


class OWMApi:
    def __init__(self):
        self.key = "b737879096cabe3d9ff3800d3cba2bc8"
        self.lang = 'ru'
        self.api = pyowm.OWM(self.key, language=self.lang, use_ssl=False)
        self.codes = {}
        assign_value(self.codes, ["01d", "01n"], 0)
        assign_value(self.codes, ['02d', '02n', '03d', '03n'], 1)
        assign_value(self.codes, ['04d', '04n'], 2)
        assign_value(self.codes, ['09d', '09n'], 3)
        assign_value(self.codes, ['10d', '10n'], 4)
        assign_value(self.codes, ['11d', '11n'], 5)
        assign_value(self.codes, ['13d', '13n'], 6)
        assign_value(self.codes, ['50d', '50n'], 7)

    def at_place(self, name: str = "Moscow,ru"):
        """
        Current weather at location
        :param name: Moscow,ru
        :return:
        """
        null = None
        try:
            forecast = self.api.weather_at_place(name)
        except NotFoundError:
            return
        return eval(forecast.to_JSON())


