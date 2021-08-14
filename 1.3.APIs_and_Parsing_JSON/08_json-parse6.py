# 1.3.3.17: Activity - Test JSON Iteration and Application Functionality
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

'''
OUTPUT
Starting Location: Washington
Destination: Baltimore
URL: https://www.mapquestapi.com/directions/v2/route?key=your_api_key&to=Baltimore&from=Washington
API Status: 0 = A successful route call.

Directions from Washington to Baltimore
Trip Duration:   00:49:19
Kilometers:      61.32
Fuel Used (Ltr): 6.24
=============================================
Start out going north on 6th St/US-50 E/US-1 N toward Pennsylvania Ave/US-1 Alt N. (1.28 km)
Turn right onto New York Ave/US-50 E. Continue to follow US-50 E (Crossing into Maryland). (7.51 km)
Take the Balt-Wash Parkway exit on the left toward Baltimore. (0.88 km)
Merge onto MD-295 N. (50.38 km)
Turn right onto W Pratt St. (0.86 km)
Turn left onto S Calvert St/MD-2. (0.43 km)
Welcome to BALTIMORE, MD. (0.00 km)
=============================================

Starting Location: Washington
Destination: Beijing
URL: https://www.mapquestapi.com/directions/v2/route?to=Beijing&key=your_api_key&from=Washington
Starting Location: Washington
Destination: Balt
URL: https://www.mapquestapi.com/directions/v2/route?to=Balt&key=your_api_key&from=Washington
Starting Location: Washington
Destination:
URL: https://www.mapquestapi.com/directions/v2/route?to=&key=your_api_key&from=Washington
Starting Location: q
>>>
'''
