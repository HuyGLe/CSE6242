import requests
import json
import csv
import time
import datetime
import calendar

with open('weather_input.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    colleges_list = list(csv_reader)

weather_data = []
snow_id = [600,601,602,611,612,613,615,616,620,621,622]
rain_id = [200,201,202,232,300,301,302,310,311,312,313,314,321,500,501,502,503,504,511,520,521,522,531]

start = 1618444800 ## Apr 15, 2021
end = 1647302400  ## Mar 15, 2022

apiKey='963b9ea6728b7bebf52836843f5ee923'


for college in colleges_list[1:]:
    unitId = college[0]
    #collegeName = college[1]
    city = college[2]
    zipCode = college[4]
    lat = college[11]
    lon = college[12]
    url = f'http://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={apiKey}'
    r = requests.get(url)
    if r.status_code != 200:
        print('Request Failed , check URL')
        break
    weather_json = r.json()
    hourly_weather = weather_json.get('list')
    total_days = len(hourly_weather)

    for i in range(total_days):
        dt = hourly_weather[i]['dt']
        dt_hr_utc_str = datetime.datetime.fromtimestamp(dt).strftime('%H')
        dt_utc_str = datetime.datetime.fromtimestamp(dt).strftime('%Y-%m-%d')
        temp = hourly_weather[i]['main']['temp']
        tempMin = hourly_weather[i]['main']['temp_min']
        tempMax = hourly_weather[i]['main']['temp_max']
        isCloudyPerc = hourly_weather[i]['clouds']['all']
        weatherDesc = hourly_weather[i]['weather'][0]['description']
        weatherId = hourly_weather[i]['weather'][0]['id']


        snow_1h = 0
        rain_1h = 0
        if 'snow' in hourly_weather[i]:
                #print("Inside snow")
            if '1h' in hourly_weather[i]['snow']:
                snow_1h = hourly_weather[i]['snow']['1h']

        if 'rain' in hourly_weather[i]:
            if '1h' in hourly_weather[i]['rain']:
                rain_1h = hourly_weather[i]['rain']['1h']

        data = [unitId,city,zipCode,lat,lon,dt,dt_utc_str,dt_hr_utc_str,temp,tempMin,tempMax,snow_1h,rain_1h,isCloudyPerc,weatherId,weatherDesc]
        weather_data.append(data)

    time.sleep((r.elapsed.total_seconds()))

columns = ['unitId','city','zipCode','lat','lon','dt','dateTime','hour','temp','tempMin','tempMax','snow1h','rain1h','isCloudyPerc','weatherId','weatherDesc']
with open('weather_data_hourly.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(columns)
    write.writerows(weather_data)


print('Done saving the weather Data to file!!')
