# 1.3.3.10: Activity - Test User Input
import os
import urllib.parse
import requests

from dotenv import load_dotenv


load_dotenv()

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = os.getenv("MAPQUESTAPI_CONSUMER_KEY")

while True:
    orig = input("Starting Location: ")
    dest = input("Destination: ")
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    print("URL: " + (url))

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")

'''
OUTPUT
Starting Location: Washington
Destination: Baltimore
URL: https://www.mapquestapi.com/directions/v2/route?from=Washington&key=your_api_key&to=Baltimore
API Status: 0 = A successful route call.

Starting Location: <Ctrl+C>
>>>
'''
