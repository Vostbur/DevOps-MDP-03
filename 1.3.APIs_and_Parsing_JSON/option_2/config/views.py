import datetime
import logging
import urllib.parse
import requests

from django.shortcuts import render

from config.settings import MAPQUESTAPI_KEY, ABSTRACTAPI_KEY, ABSTRACTAPI_GEO_KEY


logger = logging.getLogger(__name__)


def get_location_by_IP() -> dict:
    location_by_IP_api = "https://ipgeolocation.abstractapi.com/v1/?"
    location_by_IP_url = location_by_IP_api + urllib.parse.urlencode(
        {"api_key": ABSTRACTAPI_GEO_KEY}
    )
    json_data = requests.get(location_by_IP_url).json()
    error = f"{json_data['error']['message']}: {json_data['error']['details']}" if "error" in json_data else None
    current_location = f"{json_data['city']}, {json_data['country']}" if not error else None
    return {
        "current_location": current_location,
        "error": error
    }


def get_latlng(target_location: str) -> dict:
    lat, lng, error = None, None, None

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
        error = f"Status Code: {json_status}; Refer to: {json_data['info']['messages'][0]}"
    return {"lat": lat, "lng": lng, "error": error}


def get_sun_iso8601(latlng: dict) -> dict:
    sunrise_iso8601, sunset_iso8601, error = None, None, None

    sun_api = "https://api.sunrise-sunset.org/json?"
    latlng["formatted"] = 0
    sun_url = sun_api + urllib.parse.urlencode(latlng)

    json_data = requests.get(sun_url).json()
    json_status = json_data["status"]

    if json_status == "OK":
        sunrise_iso8601 = json_data["results"]["sunrise"]
        sunset_iso8601 = json_data["results"]["sunset"]
    elif json_status == "INVALID_REQUEST":
        error = "Either lat or lng parameters are missing or invalid"
    elif json_status == "INVALID_DATE":
        error = "Date parameter is missing or invalid"
    elif json_status == "UNKNOWN_ERROR":
        error = "Request could not be processed due to a server error. Please try again."
    else:
        error = "Unknown error occurred!"
    return {"sunrise": sunrise_iso8601, "sunset": sunset_iso8601, "error": error}


def get_UTC_from_iso8601(timestamp: str) -> str:
    dt_timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
    return dt_timestamp.strftime("%Y-%m-%d %H:%M:%S")


def get_localtime(target_location: str, timestamp: str, current_location: str) -> dict:
    sun_time, error = None, None

    convert_time_api = "https://timezone.abstractapi.com/v1/convert_time?"
    convert_time_url = convert_time_api + urllib.parse.urlencode(
        {"api_key": ABSTRACTAPI_KEY,
            "base_location": target_location,
            "base_datetime": timestamp,
            "target_location": current_location}
    )

    json_data = requests.get(convert_time_url).json()

    if "error" in json_data:
        error = f"{json_data['error']['message']}: {json_data['error']['details']}"
    sun_time = json_data['target_location']['datetime']

    return {"sun_time": sun_time, "error": error}


def index(request):
    if request.method == 'POST':

        # Get current location by POST request or by IP
        current_location = request.POST.get("current_location")
        if current_location is None:
            location_response = get_location_by_IP()
        if location_response["error"] is not None:
            render(request, 'index.html', {'error': location_response["error"]})
        current_location = location_response["current_location"]
        logger.debug("current_location >>> " + current_location)

        # Get target location by POST reques
        target_location = request.POST.get("target_location")
        logger.debug("target_location >>> " + target_location)

        # get lat and lng from address
        latlng = get_latlng(target_location)
        if latlng["error"] is not None:
            render(request, 'index.html', {'error': latlng["error"]})
        del latlng["error"]
        logger.debug("lat >>> " + str(latlng["lat"]) + "\tlng >>> " + str(latlng["lng"]))

        # get sunrise and sunset in iso8601 format
        sun_iso8601 = get_sun_iso8601(latlng)
        if sun_iso8601["error"] is not None:
            render(request, 'index.html', {'error': sun_iso8601["error"]})

        # convert iso8601 to UTC datetime format
        sunrise_utc = get_UTC_from_iso8601(sun_iso8601["sunrise"])
        sunset_utc = get_UTC_from_iso8601(sun_iso8601["sunset"])
        logger.debug("sunrise_utc >>> " + sunrise_utc + "\tsunset_utc >>> " + sunset_utc)

        # get local time sunrise
        response = get_localtime(target_location, sunrise_utc, current_location)
        if response["error"] is not None:
            render(request, 'index.html', {'error': response["error"]})
        sunrise = response["sun_time"]

        # get local time sunset
        response = get_localtime(target_location, sunset_utc, current_location)
        if response["error"] is not None:
            render(request, 'index.html', {'error': response["error"]})
        sunset = response["sun_time"]

        logger.debug("sunrise >>> " + sunrise + "\tsunset >>> " + sunset)
        return render(request, 'index.html', {
            'current_location': current_location,
            'target_location': target_location,
            'sunrise': sunrise,
            'sunset': sunset
        })
    return render(request, 'index.html')
