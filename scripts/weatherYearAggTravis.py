import requests
import json
import csv
import time
import datetime
import calendar

apiKey='963b9ea6728b7bebf52836843f5ee923'

weather_data = []
year = 2021

with open('final.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    colleges_list = list(csv_reader)

for college in colleges_list[1000:1500]:
    unitId = college[0]
    #collegeName = college[1]
    city = college[2]
    zipCode = college[4]
    lat = college[11]
    lon = college[12]

    url = f'https://history.openweathermap.org/data/2.5/aggregated/year?lat={lat}&lon={lon}&appid={apiKey}'
    r = requests.get(url)
    weather_json = r.json()
    daily_weather = weather_json.get('result')


    for i in range(len(daily_weather)):
        #print(daily_weather[i])
        month = daily_weather[i]["month"]
        day = daily_weather[i]["day"]
        temp_record_min = daily_weather[i]["temp"]["record_min"]
        temp_record_max = daily_weather[i]["temp"]["record_max"]
        temp_avg_min = daily_weather[i]["temp"]["average_min"]
        temp_avg_max = daily_weather[i]["temp"]["average_max"]
        temp_p75 = daily_weather[i]["temp"]["p75"]
        humidity_min = daily_weather[i]["humidity"]["min"]
        humidity_max = daily_weather[i]["humidity"]["max"]
        humidity_mean = daily_weather[i]["humidity"]["mean"]
        humidity_p75 = daily_weather[i]["humidity"]["p75"]
        precipitation_min = daily_weather[i]["precipitation"]["min"]
        precipitation_max = daily_weather[i]["precipitation"]["max"]
        precipitation_mean = daily_weather[i]["precipitation"]["mean"]
        precipitation_p75 = daily_weather[i]["precipitation"]["p75"]
        clouds_min = daily_weather[i]["clouds"]["min"]
        clouds_max = daily_weather[i]["clouds"]["max"]
        clouds_mean = daily_weather[i]["clouds"]["mean"]
        clouds_p75 = daily_weather[i]["clouds"]["p75"]
        data =[unitId,city,zipCode,lat,lon,year,month,day,temp_record_min,temp_record_max,temp_avg_min,temp_avg_max,temp_p75,humidity_min,humidity_max,humidity_mean,humidity_p75,precipitation_min,precipitation_max,precipitation_mean,precipitation_p75,clouds_min,clouds_max,clouds_mean,clouds_p75]
        weather_data.append(data)
    time.sleep((r.elapsed.total_seconds()))

columns = ['unitId','city','zipCode','lat','lon','year','month','day','temp_record_min','temp_record_max','temp_avg_min','temp_avg_max','temp_p75','humidity_min','humidity_max','humidity_mean','humidity_p75','precipitation_min','precipitation_max','precipitation_mean','precipitation_p75','clouds_min','clouds_max','clouds_mean','clouds_p75']

with open('weatherTravis.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(columns)
    write.writerows(weather_data)

#print(weather)
print('Done saving the weather Data to file!!')
