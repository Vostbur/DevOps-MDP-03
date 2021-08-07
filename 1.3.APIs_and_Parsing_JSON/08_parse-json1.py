# 1.3.3.6: Activity - Test the URL Request
import os
import urllib.parse
import requests

from dotenv import load_dotenv


load_dotenv()

main_api = "https://www.mapquestapi.com/directions/v2/route?"
orig = "Washington"
dest = "Baltimaore"
key = os.getenv("MAPQUESTAPI_CONSUMER_KEY")

url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
json_data = requests.get(url).json()
print(json_data)
