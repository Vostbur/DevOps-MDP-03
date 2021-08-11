'''
Input base location: Moscow, Russia
Input target location: Washington,DC
Sunrise: 2021-08-10 17:16:13
Sunset: 2021-08-11 07:10:32
'''
import os
import sys
import json
import urllib.parse
from datetime import datetime

import requests
from dotenv import load_dotenv


def save_for_mock(json_data, filename):
    with open(filename, "w") as f:
        json.dump(json_data, f)


load_dotenv()

base_location = input("Input base location: ")
target_location = input("Input target location: ")

# get lat and lng from address
mapquestapi_key = os.getenv("MAPQUESTAPI_CONSUMER_KEY")

target_coordinates_api = "http://www.mapquestapi.com/geocoding/v1/address?"
target_coordinates_url = target_coordinates_api + urllib.parse.urlencode(
    {"key": mapquestapi_key, "location": target_location}
)

json_data = requests.get(target_coordinates_url).json()
save_for_mock(json_data, "mapquestapi.json")

json_status = json_data["info"]["statuscode"]

if json_status == 0:
    lat = json_data["results"][0]["locations"][0]["latLng"]["lat"]
    lng = json_data["results"][0]["locations"][0]["latLng"]["lng"]
else:
    print(f"Status Code: {json_status}; Refer to: {json_data['info']['messages'][0]}")
    sys.exit(0)

# get sunrise and sunset
sun_api = "https://api.sunrise-sunset.org/json?"
sun_url = sun_api + urllib.parse.urlencode(
    {"lat": lat, "lng": lng, "formatted": 0}
)

json_data = requests.get(sun_url).json()
save_for_mock(json_data, "sunrise-sunset.json")

json_status = json_data["status"]

if json_status == "OK":
    sunrise_iso8601 = json_data["results"]["sunrise"]
    sunset_iso8601 = json_data["results"]["sunset"]
elif json_status == "INVALID_REQUEST":
    print("Either lat or lng parameters are missing or invalid")
    sys.exit(0)
elif json_status == "INVALID_DATE":
    print("Date parameter is missing or invalid")
    sys.exit(0)
elif json_status == "UNKNOWN_ERROR":
    print("Request could not be processed due to a server error. The request may succeed if you try again.")
    sys.exit(0)
else:
    print("Unknown error occurred!")
    sys.exit(0)

# convert from UTC to local time
abstractapi_key = os.getenv("ABSTRACTAPI_KEY")

# sunrise
sunrise_datetime = datetime.strptime(sunrise_iso8601, "%Y-%m-%dT%H:%M:%S%z")
sunrise = sunrise_datetime.strftime("%Y-%m-%d %H:%M:%S")

convert_time_api = "https://timezone.abstractapi.com/v1/convert_time?"
convert_time_url = convert_time_api + urllib.parse.urlencode(
    {"api_key": abstractapi_key,
     "base_location": target_location,
     "base_datetime": sunrise,
     "target_location": base_location}
)

json_data = requests.get(convert_time_url).json()
save_for_mock(json_data, "sunrise-abstractapi.json")

if "error" in json_data:
    print(f"{json_data['error']['message']}: {json_data['error']['details']}")
    sys.exit(0)

print(f"Sunrise: {json_data['target_location']['datetime']}")

# sunset
sunset_datetime = datetime.strptime(sunset_iso8601, "%Y-%m-%dT%H:%M:%S%z")
sunset = sunset_datetime.strftime("%Y-%m-%d %H:%M:%S")

convert_time_api = "https://timezone.abstractapi.com/v1/convert_time?"
convert_time_url = convert_time_api + urllib.parse.urlencode(
    {"api_key": abstractapi_key,
     "base_location": target_location,
     "base_datetime": sunset,
     "target_location": base_location}
)

json_data = requests.get(convert_time_url).json()
save_for_mock(json_data, "sunset-abstractapi.json")

if "error" in json_data:
    print(f"{json_data['error']['message']}: {json_data['error']['details']}")
    sys.exit(0)

print(f"Sunset: {json_data['target_location']['datetime']}")
