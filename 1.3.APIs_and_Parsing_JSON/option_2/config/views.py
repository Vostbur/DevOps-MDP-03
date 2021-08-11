import datetime
import urllib.parse
import requests

from django.shortcuts import render

from config.settings import MAPQUESTAPI_KEY, ABSTRACTAPI_KEY


def index(request):
    output_text = ''

    if request.method == 'POST':

        base_location = request.POST.get("current_location")
        target_location = request.POST.get("target_location")

        # get lat and lng from address
        target_coordinates_api = "http://www.mapquestapi.com/geocoding/v1/address?"
        target_coordinates_url = target_coordinates_api + urllib.parse.urlencode(
            {"key": MAPQUESTAPI_KEY, "location": target_location}
        )

        json_data = requests.get(target_coordinates_url).json()
        json_status = json_data["info"]["statuscode"]

        if json_status == 0:
            lat = json_data["results"][0]["locations"][0]["latLng"]["lat"]
            lng = json_data["results"][0]["locations"][0]["latLng"]["lng"]
        else:
            output_text = f"Status Code: {json_status}; Refer to: {json_data['info']['messages'][0]}"
            render(request, 'index.html', {'text': output_text})

        # get sunrise and sunset
        sun_api = "https://api.sunrise-sunset.org/json?"
        sun_url = sun_api + urllib.parse.urlencode(
            {"lat": lat, "lng": lng, "formatted": 0}
        )

        json_data = requests.get(sun_url).json()
        json_status = json_data["status"]

        if json_status == "OK":
            sunrise_iso8601 = json_data["results"]["sunrise"]
            sunset_iso8601 = json_data["results"]["sunset"]
        elif json_status == "INVALID_REQUEST":
            output_text = "Either lat or lng parameters are missing or invalid"
            render(request, 'index.html', {'text': output_text})
        elif json_status == "INVALID_DATE":
            output_text = "Date parameter is missing or invalid"
            render(request, 'index.html', {'text': output_text})
        elif json_status == "UNKNOWN_ERROR":
            output_text = "Request could not be processed due to a server error. Please try again."
            render(request, 'index.html', {'text': output_text})
        else:
            output_text = "Unknown error occurred!"
            render(request, 'index.html', {'text': output_text})

        # sunrise
        sunrise_datetime = datetime.datetime.strptime(sunrise_iso8601, "%Y-%m-%dT%H:%M:%S%z")
        sunrise = sunrise_datetime.strftime("%Y-%m-%d %H:%M:%S")

        convert_time_api = "https://timezone.abstractapi.com/v1/convert_time?"
        convert_time_url = convert_time_api + urllib.parse.urlencode(
            {"api_key": ABSTRACTAPI_KEY,
             "base_location": target_location,
             "base_datetime": sunrise,
             "target_location": base_location}
        )

        json_data = requests.get(convert_time_url).json()

        if "error" in json_data:
            output_text = f"{json_data['error']['message']}: {json_data['error']['details']}"
            render(request, 'index.html', {'text': output_text})

        output_text += f"Sunrise: {json_data['target_location']['datetime']}"

        # sunset
        sunset_datetime = datetime.strptime(sunset_iso8601, "%Y-%m-%dT%H:%M:%S%z")
        sunset = sunset_datetime.strftime("%Y-%m-%d %H:%M:%S")

        convert_time_api = "https://timezone.abstractapi.com/v1/convert_time?"
        convert_time_url = convert_time_api + urllib.parse.urlencode(
            {"api_key": ABSTRACTAPI_KEY,
             "base_location": target_location,
             "base_datetime": sunset,
             "target_location": base_location}
        )

        json_data = requests.get(convert_time_url).json()

        if "error" in json_data:
            output_text = f"{json_data['error']['message']}: {json_data['error']['details']}"
            render(request, 'index.html', {'text': output_text})

        output_text += f"Sunset: {json_data['target_location']['datetime']}"
    return render(request, 'index.html', {'text': output_text})
