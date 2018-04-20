
import DataRetrieval
from DataRetrieval import DataRetrieval
from DataRetrieval import create_Database
import sqlite3
import time
import mysql.connector

if __name__=='__main__':
    cnx = mysql.connector.Connect(user='root', password='password',host='dublinbikes.camdjkja0k3a.us-east-1.rds.amazonaws.com')
    c = cnx.cursor()
    while True:
        # Retrieve data from API
        dataObject = DataRetrieval() 
        data = dataObject.makeRequest()
        # Load data
        dataObject.saveToTxt(data)
        dataObject.saveToJSON(data)
        dataset = dataObject.getDatasetFromJSON('bikedata.JSON')
        # Store data in Amazon RDS MySQL Database
        create_Database()
        dataObject.createTable()
        dataObject.dataEntry(dataset)
        time.sleep(300)
    