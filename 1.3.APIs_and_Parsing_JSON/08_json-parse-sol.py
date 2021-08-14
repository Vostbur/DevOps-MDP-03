# FINAL VERSION. It differs from the training one by the presence of additional error code processing
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
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print("\n************************************************************************")
        print("Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")

'''
Starting Location: Washington
Destination: Baltimore
URL: https://www.mapquestapi.com/directions/v2/route?key=your_api_key&from=Washington&to=Baltimore
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

Starting Location: Moscow
Destination: Beijing
URL: https://www.mapquestapi.com/directions/v2/route?key=your_api_key&from=Moscow&to=Beijing
API Status: 0 = A successful route call.

Directions from Moscow to Beijing
Trip Duration:   84:31:10
Kilometers:      7826.83
Fuel Used (Ltr): 793.20
=============================================
Start out going west on Кремлёвская набережная/Kremlin Embankment. (0.37 km)
Turn slight right onto ramp. (0.15 km)
Turn slight right onto Боровицкая площадь. (0.23 km)
[output omitted]
Turn left onto 广场东侧路/E. Guangchang Rd. (0.82 km)
广场东侧路/E. Guangchang Rd becomes 东长安街/E. Chang'an Str. (0.19 km)
Welcome to BEIJING. (0.00 km)
=============================================

Starting Location: Washington
Destination: Beijing
URL: https://www.mapquestapi.com/directions/v2/route?key=your_api_key&from=\
    WashingtonTurn+right+onto+%E5%89%8D%E9%97%A8%E8%A5%BF%E5%A4%A7%E8%A1%97%2FQianmen+West+Street.+%281.01+km%29&to=Beijing

****************************************************************
Staus Code: 402; Invalid user inputs for one or both locations.
****************************************************************

Starting Location: Washington
Destination: Balt
URL: https://www.mapquestapi.com/directions/v2/route?key=your_api_key&from=Washington&to=Balt

************************************************************************
Staus Code: 602; Refer to:
https://developer.mapquest.com/documentation/directions-api/status-codes
************************************************************************

Starting Location: Washington
Destination:
URL: https://www.mapquestapi.com/directions/v2/route?key=your_api_key&from=Washington&to=

************************************************************************
Staus Code: 611; Refer to:
https://developer.mapquest.com/documentation/directions-api/status-codes
************************************************************************

Starting Location: q
>>>
'''
