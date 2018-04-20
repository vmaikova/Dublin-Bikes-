# -*- coding: utf-8 -*-

"""Main module."""

import os 
from flask import Flask, send_from_directory, request
from prediction import predict
#from flask.helpers import make_response

app = Flask(__name__)

@app.route("/")
def hello():
    return send_from_directory("../static", "index.html")

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('../static/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../static/js', path)

@app.route("/weather/hourly")
def hourly_weather():
    return send_from_directory('', 'hourly_weather.json')

@app.route("/weather/forecast")
def forecast():
    return send_from_directory('', 'forecast.json')

@app.route("/favicon.ico")
def icon():
    return send_from_directory('../static', 'favicon.ico')

@app.route("/prediction")
def predictAvailableBikes():
    dateTime = request.args.get('dateTime')
    description = request.args.get('description')
    rainBinary = request.args.get('rainBinary')
    available_bike_stands = request.args.get('available_bike_stands')
    temperature = request.args.get('temperature')
    result = predict(dateTime, description, rainBinary, available_bike_stands, temperature)
    return str(result)

#if __name__ == "__main__":
port = int(os.environ.get("PORT", 5000))
app.run(host='127.0.0.1', port=port, debug = True) #Has to be 127.0.0.1 on windows
