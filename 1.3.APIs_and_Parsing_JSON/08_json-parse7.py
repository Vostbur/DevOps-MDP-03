# 1.3.3.19: Activity - Test Full Application Functionality
import os
import urllib.parse
import requests

from dotenv import load_dotenv


load_dotenv()

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = os.getenv("MAPQUESTAPI_CONSUMER_KEY")

while True:
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    print("URL: " + (url))

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("Directions from " + (orig) + " to " + (dest))
        print("Trip Duration:   " + (json_data["route"]["formattedTime"]))
        print("Kilometers:      " + str("{:.2f}".format((json_data["route"]["distance"]) * 1.61)))
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"]) * 3.78)))
        print("=============================================")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"]) * 1.61) + " km)"))
        print("=============================================\n")
    elif json_status == 402:
        print("\n****************************************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("****************************************************************\n")
    else:
        print("\n************************************************************************")
        print("Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")

'''
OUTPUT
Starting Location: Washington
Destination: Beijing
URL: https://www.mapquestapi.com/directions/v2/route?from=Washington&to=Beijing&key=your_api_key

****************************************************************
Staus Code: 402; Invalid user inputs for one or both locations.
****************************************************************

Starting Location: Washington
Destination: Balt
URL: https://www.mapquestapi.com/directions/v2/route?from=Washington&to=Balt&key=your_api_key

************************************************************************
Staus Code: 602; Refer to:
https://developer.mapquest.com/documentation/directions-api/status-codes
************************************************************************

Starting Location: Washington
Destination:
URL: https://www.mapquestapi.com/directions/v2/route?from=Washington&to=&key=your_api_key

************************************************************************
Staus Code: 611; Refer to:
https://developer.mapquest.com/documentation/directions-api/status-codes
************************************************************************

Starting Location: q
>>>
'''
