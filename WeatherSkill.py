import datetime
from typing import Dict, List
from Builder import IntentBuilder, Builder
import pyowm
from pyowm.exceptions.api_response_error import NotFoundError

from utils import extract_datetime, extract_city, Forecast


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

    def weather_at_place(self, city: str = "Moscow,ru"):
        """
        Current weather at location
        :param city: Moscow,ru
        :return:
        """
        null = None
        try:
            forecast = self.api.weather_at_place(city)
        except NotFoundError:
            return
        return eval(forecast.to_JSON())

    def weather_forecast(self, date, city: str = "Moscow,ru"):
        null = None
        forecast = eval(self.api.three_hours_forecast(city).get_forecast().to_JSON())
        weathers = forecast['weathers']
        dates = [float(x['reference_time']) for x in weathers]
        deltas = [x - date.timestamp() for x in dates]
        idx = 0
        for delta in deltas:
            if delta < 0:
                idx += 1
            else:
                idx -= 1
                break
        return weathers[idx]


class WeatherSkill:
    api = OWMApi()

    @staticmethod
    @IntentBuilder(Builder("weather"))
    def handle_current_weather(string: str):
        """
        Погода в Париже
        :return:
        """
        forecast = WeatherSkill.get_forecast(string)
        parsed = Forecast().parse(forecast)
        return "Сейчас наблюдается %s. Температура %.1f градусов" % (parsed.detailed_status, parsed.temp)


    @staticmethod
    @IntentBuilder(Builder("forecast").require("weather"))
    def handle_forecast(string: str):
        return WeatherSkill.get_forecast(string)

    @staticmethod
    @IntentBuilder(Builder("weather").require("will"))
    def handle_forecast_alternative(string: str):
        return WeatherSkill.get_forecast(string)

    @staticmethod
    def get_forecast(string: str):
        city = extract_city(string)
        if city is None:
            city = "Moscow,ru"
        date = extract_datetime(string)
        forecast = WeatherSkill.api.weather_forecast(date, city)
        return forecast


if __name__ == "__main__":
    forecast = WeatherSkill().handle_current_weather("погода в париже")
    print(forecast)
