import re
import datetime
from typing import Optional

ru_numbers = {
    'один': 1,
    'два': 2,
    'три': 3,
    'четыре': 4,
    'пять': 4,
}


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

    if used == 0:
        return

    if not day_offset:
        day_offset = 0
    date = datetime.datetime.now() + datetime.timedelta(days=day_offset)
    if time_qualifier:
        if time_qualifier in time_qualifier_am:
            date = date.replace(hour=9, minute=0, second=0)
        elif time_qualifier in time_qualifier_noon:
            date = date.replace(hour=12, minute=0, second=0)
        elif time_qualifier in time_qualifier_pm:
            date = date.replace(hour=21, minute=0, second=0)
    return date


if __name__ == "__main__":
    date = extract_datetime("прогноз погоды через четыре дня вечером")
    print(date)



