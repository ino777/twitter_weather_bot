import os
import string
import configparser
import datetime
from dateutil.tz import gettz
import random
import tweepy


import weathers


CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

CK = CONFIG['TwitterAPI']['Consumer_key']
CS = CONFIG['TwitterAPI']['Consumer_secret']
AT = CONFIG['TwitterAPI']['Access_token']
AS = CONFIG['TwitterAPI']['Access_secret']

OW_KEY = CONFIG['OpenWeatherAPI']['Key']


def makeAPI():
    """ create Twitter object """
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)

    api = tweepy.API(auth)
    return api


def get_random_template():
    """ return template path randomly """
    dir_path = 'templates'
    templates = os.listdir(dir_path)
    if not templates:
        raise OSError('There is no template file')

    filename = random.choice(templates)
    file_path = os.path.join(dir_path, filename)
    return file_path


def convert_utc(utc, region, city):
    """  convert UTC into the standard time of the given region/city."""
    datetime_utc = datetime.datetime.strptime(utc + '+0000', '%Y-%m-%d %H:%M:%S%z')
    timestamp = datetime_utc.astimezone(gettz('{}/{}'.format(region, city))).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp


if __name__ == "__main__":
    region ='Asia'
    city = 'Tokyo'

    context = {
        'city': city,
    }

    # get current weather
    current = weathers.fetch_current_weather(city, OW_KEY)
    context['current_weather'] = current['weather'][0]['main']

    # get weather forecast
    forecast = weathers.fetch_three_hour_forecast(city, OW_KEY)
    for i in range(8):
        dt = convert_utc(forecast['list'][i]['dt_txt'], region, city)
        context['hour{}'.format(i)] = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
        context['weather{}'.format(i)] = forecast['list'][i]['weather'][0]['main']

    # select template
    template = get_random_template()

    # read template
    with open(template, 'r', encoding='utf-8') as f:
        content = f.read()
        t = string.Template(content).substitute(context)
    
    # tweet
    api = makeAPI()
    api.update_status(t)