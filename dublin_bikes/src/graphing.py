import plotly.plotly as py
import plotly.graph_objs as go
from DataRetrieval import DataRetrieval
from IPython.display import Image


def createGraph(stationNumber):
	# Call data from SQL query in DataRetrieval.py for given station number
	station = str(stationNumber)
	dr = DataRetrieval()
	d = dr.getAverageStationStatistics(stationNumber)
	name = (d[1][2])
	
	# Iterate the average available bikes and stands for each hour
	x_hour = []
	y_bikes = []
	y_stands = []
	i = 0
	for row in range(0,24):
		hour = (d[i][1])
		bikes = (d[i][5])
		stands = (d[i][6])
		x_hour.append(hour)
		y_bikes.append(bikes)
		y_stands.append(stands)
		i = i+ 1

	# Create Plotly graphs for each station
	py.sign_in('sybrob', 'CRU7sBrmobYVmTWVHFrz')
	trace1 = go.Bar(x=[x_hour[0],x_hour[1],x_hour[2],x_hour[3],x_hour[4],x_hour[5],x_hour[6],x_hour[7],x_hour[8],x_hour[9],x_hour[10],x_hour[11],x_hour[12],x_hour[13],x_hour[14],x_hour[15],x_hour[16],x_hour[17],x_hour[18],x_hour[19],x_hour[20],x_hour[21],x_hour[22],x_hour[23],], \
		y= [y_bikes[0],y_bikes[1],y_bikes[2],y_bikes[3],y_bikes[4],y_bikes[5],y_bikes[6],y_bikes[7],y_bikes[8],y_bikes[9],y_bikes[10],y_bikes[11],y_bikes[12],y_bikes[13],y_bikes[14],y_bikes[15],y_bikes[16],y_bikes[17],y_bikes[18],y_bikes[19],y_bikes[20],y_bikes[21],y_bikes[22],y_bikes[23]], \
		name='Avg Bikes Available')
	trace2 = go.Bar(x=[x_hour[0],x_hour[1],x_hour[2],x_hour[3],x_hour[4],x_hour[5],x_hour[6],x_hour[7],x_hour[8],x_hour[9],x_hour[10],x_hour[11],x_hour[12],x_hour[13],x_hour[14],x_hour[15],x_hour[16],x_hour[17],x_hour[18],x_hour[19],x_hour[20],x_hour[21],x_hour[22],x_hour[23],], \
		y= [y_stands[0],y_stands[1],y_stands[2],y_stands[3],y_stands[4],y_stands[5],y_stands[6],y_stands[7],y_stands[8],y_stands[9],y_stands[10],y_stands[11],y_stands[12],y_stands[13],y_stands[14],y_stands[15],y_stands[16],y_stands[17],y_stands[18],y_stands[19],y_stands[20],y_stands[21],y_stands[22],y_stands[23]], \
		name='Avg Stands Available')
	data = [trace1,trace2]
	layout = go.Layout(title=station+': '+name, width=800, height=640)
	fig = go.Figure(data=data, layout=layout)
	# Save image
	py.image.save_as(fig, filename='/Users/sybilla/Documents/GitHub/DublinBikes/dublin_bikes/static/graphs/ST' + station + '.png')
	
	# ...Print stations for testing
	#print(stationNumber)

	#Used to open image file 
	Image('ST'+station+'.png') 


# Calls function for each station
# 105 stations, no station 20
for x in range(18,20):
	createGraph(x)
for x in range(21,23):
	createGraph(x)

# ...For Testing
#createGraph(21)

