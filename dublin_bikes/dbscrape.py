from urllib import urlopen
import datetime, time
import re

print ("Starting...")

#Get dublinbikes data
address = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e5370c5f5f18f19d1bd95ba3279ace3208759ab"

#Get day
#Use date as filename for each day's scraping results

current_time = time.localtime() #use time to figure out what day it is
today = time.strftime('%Y-%-m-%-d', current_time) #format it to read year-month-day
start_time = datetime.datetime.now()

#file_name = today + ".txt"
file_name = "dbscraper_sleep.txt"

#Scrape 2880 times, every 5 minutes = 10 days 
count = 0
while count < 2880:
	output = open(file_name, "a")
	webpage = urlopen(address).read()
	webpage = re.sub( r'<[^>]*>', ' ', webpage ).strip() #strip tags
	output.write(webpage)
	count += 1
	start_time = datetime.datetime.now()
	print ('Process #'), count, ('Time:'), start_time
	time.sleep(300)

print ("Scraping finished.")