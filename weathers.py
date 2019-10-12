import requests


def fetch_current_weather(city, appid):
    """ call current data """
    params = {
        'q': city,
        'appid': appid,
    }
    url = 'https://api.openweathermap.org/data/2.5/weather'
    res = requests.get(url, params=params)
    return res.json()


def fetch_three_hour_forecast(city, appid):
    """ call 5 day / 3 hour forecast data """
    params = {
        'q': city,
        'appid': appid,
    }
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    res = requests.get(url, params=params)
    return res.json()