
import requests
import json
import sqlite3
import datetime
import mysql.connector
import os, shutil, datetime, sys
import csv, json
import codecs
import time
from threading import Thread



# Test function to initialize database if does not exist - *DO NOT create new database on AWS RDS as it exceeds free tier limit*
def create_Database():
    cnx = mysql.connector.Connect(user='root', password='password',host='dublinbikes.camdjkja0k3a.us-east-1.rds.amazonaws.com')
    c = cnx.cursor()
    sql = 'CREATE DATABASE IF NOT EXISTS bike_data'
    c.execute(sql)

# Retrieves data from API and sends to txt file, json file, and Amazon MySQL RDS
class DataRetrieval(object):

    def __init__(self):

        self.url ='https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e5370c5f5f18f19d1bd95ba3279ace3208759ab'
    
    def makeRequest(self):
        data = requests.get(self.url).text
        return data
    
    # Test function to write to txt file
    def saveToTxt(self, dataset):
        with open("test_data.txt", "w") as file:
                file.write(dataset)

    # Test function to write to test json file
    def saveToJSON(self, dataset):
        with open("test_bikedata.json", 'w') as file:
                file.write(dataset)
    
    def getDatasetFromJSON(self, JSONfile):
        with open(JSONfile) as data_file:
            dataset = json.load(data_file)
        return dataset
    
    # Create table 'Test' to test function
    def createTable(self):
        # Function to create table to store all data from request to Dublin Bikes API in Amazon MySQL RDS
        cnx = mysql.connector.Connect(user='root', password='password',
                              host='dublinbikes.camdjkja0k3a.us-east-1.rds.amazonaws.com',
                              database='bike_data')
        # initialise cursor for database
        c = cnx.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS Test (\
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
        cnx.close()
    
    # Test function for entering data into Amazon MySQL RDS table   
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

            c.execute('INSERT IGNORE INTO Test(Number, Name, Address, Latitude, Longitude, Banking, Bonus, Status, Bike_stands, Available_bike_stands, Available_bikes, Last_update) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',\
                (Number, Name, Address, Latitude, Longitude, Banking, Bonus, Status, Bike_stands, Available_bike_stands, Available_bikes, Last_update))
            
            
        cnx.commit()    
        c.close
        cnx.close()    

    # Function for querying Amazon MySQL RDS
    def getAverageStationStatistics(self, stationNumber):
        # connect to database       
        cnx = mysql.connector.Connect(user='root', password='password',
                              host='dublinbikes.camdjkja0k3a.us-east-1.rds.amazonaws.com',
                              database='bike_data')
        # initialise cursor for database
        c = cnx.cursor()
        c.callproc('stations', [stationNumber])
        for (data) in c.stored_results():
            d = data.fetchall()
            print d
            
        c.close
        cnx.close()  


# Calling All Functions For Testing
print ('Initializing bike_data database on Amazon RDS...')
create_Database()
dr = DataRetrieval()

# make a request to Dublin bikes API
print("Making request to Dublin Bikes API...")
dataset = dr.makeRequest()
print("Saving data to TEST text file...")
# save data to text file 
dr.saveToTxt(dataset)
print("Saving data to TEST JSON file...")
# save data to JSON file
dr.saveToJSON(dataset)
print("Loading data from TEST JSON file into data frame...")
# load data from JSON file into a data frame
dataset = dr.getDatasetFromJSON('test_bikedata.JSON')
print("Creating test table in database to store data...")
# create table in database to store data
dr.createTable()
print("Importing data in data frame to test table...")
# import data in dataframe to database table
dr.dataEntry(dataset)
#dr.dataEntry(dr.getDatasetFromJSON('bikedata.json'))

print("Testing function to query station statistics.")
print("Station 1...")
dr.getAverageStationStatistics(1)
time.sleep(2)
print("Station 21...")
dr.getAverageStationStatistics(21)
time.sleep(2)
print("Station 105...")
dr.getAverageStationStatistics(105)

print("Test of DataRetrieval.py Completed")


