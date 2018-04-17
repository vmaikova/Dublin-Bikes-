## MySQL


import requests
import json
import sqlite3
import datetime
import mysql.connector
from sqlalchemy import create_engine

import os, shutil, datetime, sys
import csv, json
import codecs
import time
from threading import Thread


cnx = mysql.connector.Connect(user='root', password='password',host='dublinbikes.camdjkja0k3a.us-east-1.rds.amazonaws.com')
c = cnx.cursor()
sql = 'CREATE DATABASE IF NOT EXISTS bike_data'
c.execute(sql)

def create_Database():
    cnx = mysql.connector.Connect(user='root', password='password',host='dublinbikes.camdjkja0k3a.us-east-1.rds.amazonaws.com')
    c = cnx.cursor()
    sql = 'CREATE DATABASE IF NOT EXISTS bike_data'
    c.execute(sql)

class DataRetrieval(object):


    def __init__(self):
        '''
        Constructor
        '''
        self.url ='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e5370c5f5f18f19d1bd95ba3279ace3208759ab'
    
    def makeRequest(self):
        data = requests.get(self.url).text
        return data
    
    def saveToTxt(self, dataset):
        with open("data.txt", "w") as file:
                file.write(dataset)
    
    def saveToJSON(self, dataset):
        with open("bikedata.json", 'w') as file:
                file.write(dataset)
    
    def getDatasetFromJSON(self, JSONfile):
        with open(JSONfile) as data_file:
            dataset = json.load(data_file)
        return dataset
    
    def createTable(self):
        '''Create table to store all data from request to Dublin Bikes API in bike_data.db'''
        cnx = mysql.connector.Connect(user='root', password='password',
                              host='dublinbikes.camdjkja0k3a.us-east-1.rds.amazonaws.com',
                              database='bike_data')
        # initialise cursor for database
        #c = conn.cursor()
        c = cnx.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS Bike_Occupancy (\
            Number INT(10), \
            Name VARCHAR(45), \
            Address VARCHAR(45), \
            Latitude FLOAT(10,8), \
            Longitude FLOAT(10,8), \
            Banking VARCHAR(10), \
            Bonus VARCHAR(10), \
            Status VARCHAR(10), \
            Bike_stands INT(4), \
            Available_bike_stands INT(4), \
            Available_bikes INT(4), \
            Last_update VARCHAR(255),\
            PRIMARY KEY (Number, Last_update))')
        cnx.commit()
        c.close
        #conn.close()
        cnx.close()
    
        
    def dataEntry(self, dataset): 
        value = dataset[0]['last_update']  
        res = datetime.datetime.fromtimestamp(value/1000).strftime('%Y-%m-%d %H:%M:%S')
        
        for i in range(0,len(dataset)):
            dataset[i]['last_update'] = res
        
        # connect to database       
        cnx = mysql.connector.Connect(user='root', password='password',
                              host='dublinbikes.camdjkja0k3a.us-east-1.rds.amazonaws.com',
                              database='bike_data')
        # initialise cursor for database
        c = cnx.cursor()
        for record in dataset:

            Number = record['number']
            Name = record['name']
            Address = record['address']
            Latitude = record['position']['lat']
            Longitude = record['position']['lng']
            Banking = record['banking']
            Bonus = record['bonus']
            Status = record['status']
            Bike_stands = record['bike_stands']
            Available_bike_stands = record['available_bike_stands']
            Available_bikes = record['available_bikes']
            Last_update = record['last_update']

            c.execute('INSERT IGNORE INTO Bike_Occupancy(Number, Name, Address, Latitude, Longitude, Banking, Bonus, Status, Bike_stands, Available_bike_stands, Available_bikes, Last_update) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',\
                (Number, Name, Address, Latitude, Longitude, Banking, Bonus, Status, Bike_stands, Available_bike_stands, Available_bikes, Last_update))
            
            #break
            
        cnx.commit()    
        c.close
        cnx.close()    


dr = DataRetrieval()
dataset = dr.makeRequest()
dr.saveToJSON(dataset)
dr.createTable()
dr.dataEntry(dr.getDatasetFromJSON('bikedata.json'))
