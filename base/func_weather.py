#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @author: wangwei50

import requests
import json
import logging

''' official website  https://www.qweather.com '''
'''      dev website  https://dev.qweather.com'''
mykey = '&key=' + '' # EDIT HERE!

url_api_weather = 'https://devapi.qweather.com/v7/weather/'
url_api_geo = 'https://geoapi.qweather.com/v2/city/'
url_api_rain = 'https://devapi.qweather.com/v7/minutely/5m'
url_api_air = 'https://devapi.qweather.com/v7/air/now'

class Weather(object):
    def __init__(self) -> None:
        self.LOG = logging.getLogger(__name__)
        
    def get(self, city_id, api_type):
        url = url_api_weather + api_type + '?location=' + city_id + mykey
        return requests.get(url).json()

    def rain(self, lat, lon):
        url = url_api_rain  + '?location=' + lon + ',' + lat + mykey
        return requests.get(url).json()

    def air(self, city_id):
        url = url_api_air + '?location=' + city_id + mykey
        return requests.get(url).json()

    def get_city(self, city_kw):
        url_v2 = url_api_geo + 'lookup?location=' + city_kw + mykey
        city = requests.get(url_v2).json()['location'][0]

        city_id = city['id']
        district_name = city['name']
        city_name = city['adm2']
        province_name = city['adm1']
        country_name = city['country']
        lat = city['lat']
        lon = city['lon']

        return city_id, district_name, city_name, province_name, country_name, lat, lon

    def getWeatherByCity(self, city_input):
        msg=''
        city_idname = self.get_city(city_input)
        city_id = city_idname[0]

        get_now = self.get(city_id, 'now')
        get_daily = self.get(city_id, '3d') # 3d/7d/10d/15d
        get_hourly = self.get(city_id, '24h') # 24h/72h/168h
        #get_rain = rain(city_idname[5], city_idname[6]) # input longitude & latitude
        air_now = self.air(city_id)['now']

        #print(json.dumps(get_now, sort_keys=True, indent=4))
        if city_idname[2] == city_idname[1]:
            msg=msg+city_idname[3] + str(city_idname[2]) + '市' + "\n"
        else:
            msg=msg+city_idname[3] +str(city_idname[2]) + '市'+ str(city_idname[1]) + '区' + "\n"
        msg=msg+'当前天气：'+ get_now['now']['text']+ get_now['now']['temp']+ '°C'+ '体感温度'+ get_now['now']['feelsLike']+ '°C' + "\n"
        msg=msg+'空气质量指数：'+ air_now['aqi'] + "\n"
        #print('降水情况：', get_rain)
        
        msg=msg+'今日天气：'+ get_daily['daily'][0]['textDay']+ get_daily['daily'][0]['tempMin']+ '-'+ get_daily['daily'][0]['tempMax']+ '°C'+"\n"

        # nHoursLater = 1 # future weather hourly
        # print(nHoursLater, '小时后天气：', get_hourly['hourly'][1]['text'], get_hourly['hourly'][1]['temp'], '°C')

        nDaysLater = 1 # future weather daily
        msg=msg+'明天天气：'+ get_daily['daily'][nDaysLater]['textDay']+ get_daily['daily'][nDaysLater]['tempMin']+ '-'+ get_daily['daily'][nDaysLater]['tempMax']+ '°C'+"\n"
        return msg

if __name__ == '__main__':
    qweather = Weather()
    print(qweather.getWeatherByCity('上海'))    