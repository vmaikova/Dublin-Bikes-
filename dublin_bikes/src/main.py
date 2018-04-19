
import DataRetrieval
from DataRetrieval import DataRetrieval
import sqlite3
import time
import mysql.connector

if __name__=='__main__':
    cnx = mysql.connector.Connect(user='root', password='password',host='dublinbikes.camdjkja0k3a.us-east-1.rds.amazonaws.com')
    c = cnx.cursor()
    while True:
        # create DataRetrieval object
        dataObject = DataRetrieval() 
        # make a request to Dublin bikes API
        data = dataObject.makeRequest()
        # save data to text file 
        dataObject.saveToTxt(data)
        # save data to JSON file
        dataObject.saveToJSON(data)
        # load data from JSON file into a data frame
        dataset = dataObject.getDatasetFromJSON('bikedata.JSON')
        # create table in database to store data
        dataObject.createTable()
        # import data in dataframe to database table
        dataObject.dataEntry(dataset)
        time.sleep(300)
    