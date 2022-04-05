import requests
import json
import csv
import time
import datetime
import calendar
#import datetime

date_time = datetime.datetime(2021,4,15,00,00)  ## Start 20210301 - > 1617235200 End 20220320->1647734400
#date = datetime.datetime.utcnow()
utc_time = calendar.timegm(date_time.utctimetuple())
print(utc_time)


with open('CollegeMasterData.csv', 'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    colleges_list = list(csv_reader)

print(colleges_list[1:10])
#date_time = datetime.datetime(2021,3,1,00,00)  ## Start 20210301 - > 1617235200 End 20220320->1647734400
#date = datetime.datetime.utcnow()
#utc_time = calendar.timegm(date_time.utctimetuple())

#dt = datetime.datetime.fromtimestamp(1647975600)
#print(utc_time)
#date_time = datetime.datetime(2021,3,1,00,00)
#date = datetime.datetime.utcnow()
#print(date_time)
#utc_time = calendar.timegm(date_time.utctimetuple())

#startdt = datetime.datetime.fromtimestamp(1640995200)
#enddt = datetime.datetime.fromtimestamp(1641081600)
# http://history.openweathermap.org/data/2.5/history/accumulated_temperature?q=Tempe,US&start=1609459200&end=1640908800&threshold=284&appid=963b9ea6728b7bebf52836843f5ee923
#API_Key = '963b9ea6728b7bebf52836843f5ee923'
#import datetime



#print(startdt)
#print(enddt)

# print(utc_time)

# http://history.openweathermap.org/data/2.5/history/accumulated_temperature?q=Tempe,US&start=1609459200&end=1641081600&threshold=284&appid=963b9ea6728b7bebf52836843f5ee923
#API_Key = '963b9ea6728b7bebf52836843f5ee923'

weather_data = []
snow_id = [600,601,602,611,612,613,615,616,620,621,622]
rain_id = [200,201,202,232,300,301,302,310,311,312,313,314,321,500,501,502,503,504,511,520,521,522,531]
lat = 61.190163
lon = -149.82619
start = 1617235200
end = 1617580800   ##1647734400
APIkey='963b9ea6728b7bebf52836843f5ee923'
#url = 'http://history.openweathermap.org/data/2.5/history/city?lat=42.3601&lon=71.0942&type=hour&start=1617235200&end=1617580800&appid=963b9ea6728b7bebf52836843f5ee923'
print(datetime.datetime.fromtimestamp(1617235200).strftime('%Y-%m-%d'))
print(datetime.datetime.fromtimestamp(1647734400).strftime('%Y-%m-%d'))

url = 'http://history.openweathermap.org/data/2.5/history/city?lat=42.360&lon=71.0942&type=hour&start=1617235200&end=1647734400&appid=963b9ea6728b7bebf52836843f5ee923'
r = requests.get(url)
weather_json = r.json()
hourly_weather = weather_json.get('list')
daily_weather_str = json.dumps(hourly_weather, indent=4)

#print(daily_weather_str)
total_days = len(hourly_weather)
print(total_days)
for i in range(total_days):
    dt = hourly_weather[i]['dt']
    dt_hr_utc_str = datetime.datetime.fromtimestamp(dt).strftime('%H')
    dt_utc_str = datetime.datetime.fromtimestamp(dt).strftime('%Y-%m-%d')
    temp = hourly_weather[i]['main']['temp']
    temp_min = hourly_weather[i]['main']['temp_min']
    temp_max = hourly_weather[i]['main']['temp_max']
    isCloudyPerc = hourly_weather[i]['clouds']['all']
    weather_desc = hourly_weather[i]['weather'][0]['description']
    print(hourly_weather[i]['weather'])
    weather_id = hourly_weather[i]['weather'][0]['id']

    if weather_id in snow_id:
        snow_1h = hourly_weather[i]['snow']['1h']
        print(snow_1h)
    elif weather_id in rain_id:
        rain_1h = hourly_weather[i]['rain']['1h']
    else:
        snow_1h = 0
        rain_1h = 0
    data = [dt_utc_str,dt_hr_utc_str,temp,temp_min,temp_max,snow_1h,rain_1h,isCloudyPerc,weather_desc]
    weather_data.append(data)
#print(weather_data)


columns = ['DateTime','Hour','Temp','Temp_min','Temp_max','Snow_1h','Rain_1h','IsCloudyPerc','Weather_Desc']
with open('weather_deta.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(columns)
    write.writerows(weather_data)


print('Done saving the weather Data to file!!')
