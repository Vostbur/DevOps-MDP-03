import os

import requests
from flask import Flask, render_template
from dotenv import load_dotenv


obj = requests.get("http://api.open-notify.org/iss-now.json").json()
lat = obj['iss_position']['latitude']
lng = obj['iss_position']['longitude']

load_dotenv()
api_key = os.getenv("HERE_COM_KEY")

app = Flask(__name__)


@app.route('/')
def map_func():
    return render_template('map.html', apikey=api_key, latitude=lat, longitude=lng)


if __name__ == '__main__':
    app.run(debug=False)
