import os
import urllib.parse
import requests

from django.shortcuts import render


def index(request):
    output_text = ''

    if request.method == 'POST':

        main_api = "https://www.mapquestapi.com/directions/v2/route?"
        key = os.getenv("MAPQUESTAPI_CONSUMER_KEY")
        orig = request.POST.get('orig')
        dest = request.POST.get('dest')
        metric = True if request.POST.get('meas_type') == 'metric' else False
        url = main_api + \
            urllib.parse.urlencode({"key": key, "from": orig, "to": dest})

        json_data = requests.get(url).json()
        json_status = json_data["info"]["statuscode"]

        if json_status == 0:
            output_text += f"API Status: {json_status} A successful route call.\n"
            output_text += f"Directions from {orig} to {dest}\n"
            output_text += f"Trip Duration:   {json_data['route']['formattedTime']}\n"
            if metric:
                output_text += f"Kilometers:      {str('{:.2f}'.format((json_data['route']['distance']) * 1.61))}\n"
                output_text += f"Fuel Used (Ltr): {str('{:.2f}'.format((json_data['route']['fuelUsed']) * 3.78))}\n"
                output_text += "=============================================\n"
                for each in json_data["route"]["legs"][0]["maneuvers"]:
                    output_text += f"{each['narrative']} ({str('{:.2f}'.format((each['distance']) * 1.61))} km)\n"
            else:
                output_text += f"Miles:      {str('{:.2f}'.format((json_data['route']['distance'])))}\n"
                output_text += f"Fuel Used (Gal): {str('{:.2f}'.format((json_data['route']['fuelUsed'])))}\n"
                output_text += "=============================================\n"
                for each in json_data["route"]["legs"][0]["maneuvers"]:
                    output_text += f"{each['narrative']} ({str('{:.2f}'.format((each['distance'])))} ml)\n"
            output_text += "=============================================\n"
        elif json_status == 402:
            output_text += "****************************************************************\n"
            output_text += f"Status Code: {str(json_status)}; Invalid user inputs for one or both locations.\n"
            output_text += "****************************************************************\n"
        elif json_status == 611:
            output_text += "**********************************************\n"
            output_text += f"Status Code: {str(json_status)}; Missing an entry for one or both locations.\n"
            output_text += "**********************************************\n"
        else:
            output_text += "************************************************************************\n"
            output_text += f"Status Code: {str(json_status)}; Refer to:\n"
            output_text += "https://developer.mapquest.com/documentation/directions-api/status-codes\n"
            output_text += "************************************************************************\n"

    return render(request, 'index.html', {'text': output_text})
