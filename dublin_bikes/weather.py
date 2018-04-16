'''
Created on Mar 30, 2018

@author: Brynja
'''
# Reference from https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
import urllib.request 

def get_json_from_url (url, filename):
    urllib.request.urlretrieve(url, filename)


def updateWeather():
    get_json_from_url('http://api.wunderground.com/api/74d4737442833c9a/hourly/q/IE/Dublin.json', 'hourly_weather.json')
    
updateWeather()
    
print ('finished')  
