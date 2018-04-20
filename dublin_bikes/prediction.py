from sklearn.externals import joblib
from sklearn.datasets import load_digits
import pandas as pa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from dateutil.parser import parse

def roundToNearestHalfHourAndRemoveDate(dateTime):
    date = parse(dateTime)
    if(date.minute > 45):
        if(date.hour + 1 == 24):
            return str(date.hour) + ":" + str(30)
        return str(date.hour + 1) + ":" + "00"
    if(date.minute > 15):
        return str(date.hour) + ":" + str(30)
    return str(date.hour) + ":" + "00"

def predict(dateTime, description, rainBinary, available_bike_stands, temperature):
    time = roundToNearestHalfHourAndRemoveDate(dateTime)
    if(len(time) == 4):
        time = "0" + time
    times = ['19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30','23:00', '23:30', '00:00', '00:30', '01:00', '01:30', '02:00','02:30', '03:00', '03:30', '04:00', '04:30', '05:00', '05:30','06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00']
    desc = ['Mostly Cloudy', 'Light Drizzle', 'Light Rain', 'Overcast','Partly Cloudy', 'Fog', 'Clear', 'Scattered Clouds', '']
    if description not in desc:
        description = ''
    le = LabelEncoder()
    le.fit(times)
    time_transform = le.transform([time])
    desc_le = LabelEncoder()
    desc_le.fit(desc)
    desc_transform = desc_le.transform([description])
    d = {'Description': desc_transform,	'Time': time_transform,	'Rain': rainBinary,	'Temp':temperature ,'Available_bike_stands':available_bike_stands}
    
    df = pa.DataFrame(data=d)
    clf2 = joblib.load("bikes.pkl")
    prediction = clf2.predict(df)
    return prediction[0]