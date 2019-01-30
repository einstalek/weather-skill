import re
import datetime
import pymorphy2
from typing import Optional, Dict

morph = pymorphy2.MorphAnalyzer()

ru_numbers = {
    'один': 1,
    'два': 2,
    'три': 3,
    'четыре': 4,
    'пять': 5,
}

cities = {"москва", "париж", "берлин"}


def extract_datetime(string: str) -> Optional[datetime.datetime]:
    words = re.split('\W', string.lower())
    if len(words) == 0:
        return

    time_qualifier_am = ["утром", "утра", "утро"]
    time_qualifier_noon = ["днем", "полдень"]
    time_qualifier_pm = ["ночью", "ночь", "вечером", "вечер"]
    time_qualifiers = set(time_qualifier_am + time_qualifier_pm + time_qualifier_noon)

    days = ['понедельник', 'вторник', 'среду',
            'четверг', 'пятницу', 'субботу', 'воскресенье']

    today = int(datetime.datetime.now().strftime("%w"))
    day_offset = False
    time_qualifier = False
    used = 0

    for idx, word in enumerate(words):
        word_prev = words[idx - 1] if idx > 0 else ""
        word_next = words[idx + 1] if idx < len(words) - 1 else ""
        word_next_next = words[idx + 2] if idx < len(words) - 2 else ""

        if word in time_qualifiers:
            time_qualifier = word
        elif word == "сегодня":
            day_offset = 0
            used += 1
        elif word == "завтра":
            day_offset = 1
            used += 1
        elif word == "послезавтра":
            day_offset = 2
            used += 1
        elif word in days:
            # погода в пятницу
            d = days.index(word)
            offset = (d + 1) - today
            if 1 <= offset <= 5:
                day_offset = offset
                used += 1
        elif word.startswith("выходны"):
            # погода на выходных
            d = days.index("субботу")
            offset = (d + 1) - today
            if 1 <= offset <= 5:
                day_offset = offset
                used += 1
        if word == "через" and word_next in ru_numbers:
            # погода через пять дней
            if word_next_next.startswith("дн"):
                day_offset = ru_numbers[word_next]
                used += 1

    if not day_offset:
        day_offset = 0

    date = datetime.datetime.now() + datetime.timedelta(days=day_offset)
    if time_qualifier:
        if time_qualifier in time_qualifier_am:
            date = date.replace(hour=9, minute=0, second=0)
        elif time_qualifier in time_qualifier_noon:
            date = date.replace(hour=15, minute=0, second=0)
        elif time_qualifier in time_qualifier_pm:
            date = date.replace(hour=21, minute=0, second=0)
    else:
        date = date.replace(hour=12, minute=0)
    return date


def extract_city(string: str) -> Optional[str]:
    words = [morph.parse(w)[0].normal_form for w in re.split("\W", string) if w != ""]
    if len(words) == 0:
        return
    for city in cities:
        if city in words:
            return city


class Forecast:
    def parse(self, forecast: Dict):
        self.detailed_status = forecast.get("detailed_status")
        self.weather_icon = forecast.get("weather_icon_name")
        self.temp  = forecast.get("temperature").get("temp") - 273
        self.temp_min = forecast.get("temperature").get("temp_min") - 273
        self.temp_max = forecast.get("temperature").get("temp_max") - 273
        self.pressure = forecast.get("pressure").get("press")
        self.humidity = forecast.get("humidity")
        self.speed = forecast.get("wind").get("speed")
        return self


if __name__ == "__main__":
    date = extract_datetime("погода в париже")
    print(date)



