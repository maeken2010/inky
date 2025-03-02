#!/usr/bin/env python3

import os
import requests

def _request_api(url, params = {}):
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API Key is not set! Please set OPENWEATHER_API_KEY.")

    params['appid'] = api_key

    result = ''
    try:
        response = requests.get(url, params=params, timeout=5)  # タイムアウトを5秒に設定
        response.raise_for_status()  # HTTPエラーがあれば例外を発生
        result = response.json()
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")

    return result

def get_current_weather():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': '24.8054647',
        'lon': '125.2811296',
        'units': 'metric',
    }
    data = _request_api(url, params)

    return {
        'weatherCode': data['weather'][0]['main'],
        'weatherDescription': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'temp': data['main']['temp'],
    }

def get_forecast_weather():
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'lat': '24.8054647',
        'lon': '125.2811296',
        'units': 'metric',
    }
    data = _request_api(url, params)

    date_list = list(map(lambda x: x['dt_txt'], data['list']))
    pop_list = list(map(lambda x: x['pop'], data['list']))
    weather_code_list = list(map(lambda x: x['weather'][0]['main'], data['list']))
    temperature_list = list(map(lambda x: x['main']['temp'], data['list']))

    return {
        'date_list': date_list,
        'pop_list': pop_list,
        'weather_code_list': weather_code_list,
        'temperature_list': temperature_list
    }

