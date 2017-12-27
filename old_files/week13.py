"""
iUROP 2017 project

Authors:
Marcus Wallberg & Johanna Gustafsson

Please see the readme for more documentations

DATA FORMAT:
Every row includes:
['_id', 'created_on', 'date', 'starttime', 'user_id']

Every starttime is of the format:
[{"stay_node","endtime","starttime","duration","next_node","take_time"}]

Any questions can be sent to: marcus@wallberg.nu or johanna.gustafsson@live.se
"""

import json
import csv
import numpy as np
from datetime import date, datetime, timedelta
from calendar import day_name, day_abbr
import time
import matplotlib.pyplot as plt
import seaborn as sns
from random import choice
import pandas as pd
from tqdm import tqdm

# ---------------------------------------------
# Directories
src = './src/wifi_passive_trajectory_node2.csv'
jsonSrc = './src/nodes3.json'
csvSrc = './src/nodes.csv'
csvSrc2 = './src/nodes2.csv'
csvApril = './src/april_15-26.csv'
# ---------------------------------------------

# Buildings and area definitions
# ----------------------------------------------------------------------------------------------
buildings = [["A"], ["B"], ["E", "C", "D"], ["F", "G"], ["M", "L"], ["O", "N"], ["R", "S", "T"]]
bridges = [["A", "B"], ["A", "M"], ["O", "M"], ["T", "C"], ["E", "L"], ["G", "N"], ["F", "R"]]
jwalkArea = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'L', 'M', 'N', 'O', 'R', 'S', 'T']
HDBArea = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
# ----------------------------------------------------------------------------------------------

# Main function that is called at the bottom of this document
def main():
	with open('./src/wifi_passive_trajectory_node2.csv', newline='') as csvfile:
		jwalkReader = csv.reader(csvfile, delimiter=',', quotechar='"')
		next( jwalkReader )		# Remove the first line, which is info data
		
		# Call the function with jwalkReader as an argument
		AGE( jwalkReader )

# Some functions run without a reader as argument, these functions are using pandas
def mainPandas():
	exportStarttime()	# Only needs to run this once, saves all trajectories as json
	jsonToCsv()			# Reading the exported json-file and saves it as a csv-file, takes less space

	# Call a function
	plotTimeHDB_jwalk()

# This function 
def plotTimeHDB_jwalk():
	columns = ['duration', 'take_time', 'stay_node', 'next_node', 'starttime', 'endtime', 'id']
	df = pd.read_csv( csvApril, usecols = columns )
	df = df[ ( df.stay_node.isin( jwalkArea ) ) & ( df.next_node.isin( HDBArea ) ) ]
	df['date'] = df.starttime.apply( datetime.fromtimestamp )
	df['hour'] = df.date.dt.hour
	df['weekday'] = df.date.dt.weekday

	dfWeekDay = df[ df.weekday < 5 ]
	dfWeekEnd = df[ df.weekday >= 5 ]

	bins = [x for x in range(24)]
	plt.hist( dfWeekDay.hour.values, bins = bins )
	plt.hist( dfWeekEnd.hour.values, bins = bins )
	plt.show()


def checkHDB_jwalk_then():
	columns = ['duration', 'take_time', 'stay_node', 'next_node', 'starttime', 'endtime', 'id']
	df = pd.read_csv( csvApril, usecols = columns )
	df['date'] = df.starttime.apply( date.fromtimestamp )
	increment = timedelta(1) # One day increment
	for d in (date(2017,4,15) + timedelta(x) for x in range(12)):
		print('DAY:', d)
		dfOneDay = df[ df.date == d ]
		jwalk2hdb = dfOneDay[ ( dfOneDay.stay_node.isin( HDBArea ) ) & ( dfOneDay.next_node.isin( jwalkArea ) ) ]
		dfOneDay = dfOneDay[ dfOneDay.id.isin( jwalk2hdb.id ) ]
		dfOneDay = dfOneDay[ dfOneDay.stay_node.isin( jwalkArea ) ]
		print( dfOneDay[['duration', 'take_time', 'stay_node', 'id']].describe( include='all' ) )
		print( dfOneDay.stay_node.value_counts() )
		print()
		print()
		print()

def checkB():
	columns = ['duration', 'take_time', 'stay_node', 'next_node', 'starttime', 'endtime']
	df = pd.read_csv( csvSrc2, usecols = columns )
	df['date'] = df.starttime.apply( date.fromtimestamp )
	df = df[ ['duration', 'take_time', 'stay_node', 'next_node', 'date'] ]
	df = df[ ( df.stay_node.isin( HDBArea ) ) & ( df.next_node.isin( jwalkArea ) ) ]

	print( df.describe( include='all' ) )
	# print( df.sample( 20 ) )
	print( df.stay_node.value_counts() )
	print( df.next_node.value_counts() )

	print( df.date.max() )
	print( df.date.min() )

def jan23():
	columns = ['duration', 'take_time', 'stay_node', 'next_node', 'starttime', 'endtime']
	df = pd.read_csv( csvSrc, usecols = columns )
	# df = df[  ]
	df['date'] = df.starttime.apply( date.fromtimestamp )
	df = toTimeStamp( df )
	df = df[ df.stay_node.isin( jwalkArea ) ]
	increment = timedelta(1) # One day increment
	dfJan23 = df[ (df.starttime > date(2017,1,23) ) & (df.starttime < date(2017,1,23) + increment )]
	print(dfJan23.describe(include='all'))
	dfJan9 = df[ (df.starttime > date(2017,1,9) ) & (df.starttime < date(2017,1,9) + increment )]
	print(dfJan9.describe(include='all'))
	dfJan30 = df[ (df.starttime > date(2017,1,30) ) & (df.starttime < date(2017,1,30) + increment )]
	print(dfJan30.describe(include='all'))

def HDBcross( df = pd.DataFrame() ):
	if df.empty:
		df = getDF()
	cross = {}
	for hdb in HDBArea:
		query = (df.stay_node.isin( jwalkArea ) & (df.next_node == hdb) ) | (df.next_node.isin( jwalkArea ) & (df.stay_node == hdb) )
		cross[hdb] = df[ query ].take_time.count()

	print(list(cross.values()))
	sns.set()
	plt.bar( HDBArea, list(cross.values()) )
	# plt.xticks( list(cross), HDBArea ) 
	plt.show()

def everyDayHDB():
	df = getDF()

	increment = timedelta(1) # One day increment
	startDate = df.starttime.min().date() + increment
	# Loops through every day of the data
	while startDate <= df.starttime.max().date():
		dfOneDay = df[ (df.starttime > startDate ) & (df.starttime < startDate + increment )]
		HDBcross( dfOneDay )
		startDate += increment

def perDay():
	df = pd.read_csv( csvSrc )
	df = df[ ['duration', 'take_time', 'stay_node', 'next_node', 'starttime', 'endtime'] ]
	# df['date'] = df.starttime.apply( date.fromtimestamp )
	df = toTimeStamp( df )
	query = ( df.stay_node.isin( jwalkArea ) & df.next_node.isin( HDBArea ) ) | ( df.stay_node.isin( HDBArea ) & df.next_node.isin( jwalkArea ) )
	# df = df[ query ]
	df = df[ df.stay_node.isin( jwalkArea ) ]

	increment = timedelta(1) # One day increment
	startDate = df.starttime.min().date() + increment
	columns = ['weekday', 'mean', 'median', 'count']
	df2 = pd.DataFrame( columns = columns )
	# Loops through every day of the data
	while startDate <= df.starttime.max().date():
		dfOneDay = df[ (df.starttime > startDate ) & (df.starttime < startDate + increment )]
		print(dfOneDay.describe())
		row = [day_abbr[startDate.weekday()], dfOneDay.take_time.mean(), dfOneDay.take_time.median(), dfOneDay.take_time.size]
		df2 = df2.append(pd.DataFrame( [row], columns = columns ))
		startDate += increment

	df2 = df2.set_index(['weekday'])
	print(df2)
	# df2 = (df2 - df2.min() ) / ( df2.max() - df2.min() )
	df2 = df2 / df2.max()
	df2.plot(kind='bar')
	plt.show()

def getDF( src = csvSrc ):
	df = pd.read_csv( src )
	df = df[ ['duration', 'take_time', 'stay_node', 'next_node', 'starttime', 'endtime'] ]
	df = toTimeStamp( df )
	return df

def toTimeStamp( DataFrame ):
	DataFrame.starttime = pd.to_datetime( DataFrame.starttime, unit = 's' )
	DataFrame.endtime = pd.to_datetime( DataFrame.endtime, unit = 's' )
	return DataFrame

def describe():
	df = pd.read_csv( csvSrc, usecols = [0,1,3,5,6] )
	print( df.columns.values )
	print( df.describe( include = 'all' ) )
	print( df.stay_node.unique() )

def readCompare():
	s = time.time()
	df = pd.read_json( jsonSrc )
	end = time.time() - s
	print("json took:", end)

	s = time.time()
	df = pd.read_csv( csvSrc )
	end = time.time() - s
	print("csv took:", end)

# END OF THE PANDAS FUNCTIONS
# ---------------------------

# -------------------------
# PYTHON FOR LOOP FUNCTIONS
def printNormalSpikes2( reader ):
	peaktime = 90
	peakNodes = [[] for _ in bridges ]
	for row in reader:
		nodes = json.loads( row[3] )
		for node in nodes:
			for i, bridge in enumerate(bridges):
				if node['stay_node'] in bridge and node['next_node'] in bridge and int( node['take_time']) == 45:
					peakNodes[i].append(node)
	# Prining:
	for i, bridge in enumerate(bridges):
		print( "-" * 22 )
		print("|", "Bridge:", bridge, "|")
		print( "-" * 22 )
		for _ in range(50):
			print( choice( peakNodes[i] ) )
		print("")

def printNormalSpikes( reader ):
	peaktime = 90
	peakNodes = [[] for _ in bridges ]
	for row in reader:
		nodes = json.loads( row[3] )
		for node in nodes:
			for i, bridge in enumerate(bridges):
				if node['stay_node'] in bridge and node['next_node'] in bridge and int( node['take_time']) == 90:
					peakNodes[i].append(row)
	# Prining:
	for i, bridge in enumerate(bridges):
		print( "-" * 22 )
		print("|", "Bridge:", bridge, "|")
		print( "-" * 22 )
		for _ in range(20):
			print( choice( peakNodes[i] ) )
		print("")

def jsonToCsv( jsonSrc = jsonSrc, dest = './src/april_15-26.csv' ):
	print("Reading the csv-file")
	df = pd.read_json( jsonSrc )

	print("Writing")
	df.to_csv( dest )
	print("Done writing the file to:", dest)

def spikes():
	print("Reading the csv-file")
	df = pd.read_csv( csvSrc )

	print("Filtering")
	df = df[['duration', 'take_time', 'stay_node', 'next_node']]
	# df = df[ (df.take_time >= 85) & (df.take_time <= 95) ]
	df = df[ (df.take_time == 90) ]
	bn1 = bridges[0][0]
	bn2 = bridges[0][1]
	df = df[ ((df.stay_node == bn1) & (df.next_node == bn2) | (df.stay_node == bn2) & (df.next_node == bn1)) ]
	print( df.columns )
	print( df.head() )
	print( df.describe() )
	# print( df )

	# Take the median of columns: axis = 1 (rows = 0)
	print( df['take_time'].median( ) )

def readNodes():
	print("Reading the json-file")
	df = pd.read_json( jsonSrc )
	# print( df.columns )
	# print( df.head() )
	# print( df.describe())

	print("Filtering")
	query = df[ (df.take_time < 500) & (df.duration < 500) ]
	print( query.columns )
	print( query.head() )
	print( query.describe())

	# print( df.stay_node.unique() )
	print( query.shape )

def exportStarttime2():
	# df = pd.read_csv( src, usecols = [3], index_col = None, nrows = None )
	df = pd.read_csv( src, nrows = None )
	dest = './src/nodes3.json'
	print("Starting export")
	# j = list(df['starttime'])
	with open(dest, 'w') as f:
		writeString = ""
		f.write('[')
		for index, row in tqdm( df.iterrows() ):
			j = json.loads( row.starttime )
			for node in j:
				node['id'] = row['user_id']
			writeString += json.dumps( j ).strip( '[]' ) + ','

		writeString = writeString.strip(',') + ']'
		f.write(writeString)

	# Checking if the json is readable
	df2 = pd.read_json( dest )
	print( "Exported and verified to:", dest )

def exportStarttime():
	df = pd.read_csv( src, usecols = [3], index_col = None, nrows = None )
	dest = './src/nodes3.json'
	print("Starting export")
	j = list(df['starttime'])
	with open(dest, 'w') as f:
		writeString = ""
		f.write('[')
		for nodes in j:
			writeString += nodes.strip('[]') + ','
		writeString = writeString.strip(',') + ']'
		f.write(writeString)

	# Checking if the json is readable
	df2 = pd.read_json( dest )
	print( "Exported and verified to:", dest )

def AGE(reader):
	Hospitals = ["L", "M", "N", "O"]		
	hospitalExit = [["G", "F", "R", "S"], ["A", "B"]]	# G and A
	hospitalExit = [["G", "F", "R", "S"], ["E", "C", "T", "D"]]	# G and E
	hospitalExit = [["E", "C", "T", "D"], ["A", "B"]]	# E and A

	weekday = []
	weekend = []
	totalWeekday = []
	totalWeekend = []
	for row in reader:
		current = json.loads( row[3] )
		dayType = datetime.fromtimestamp( int( row[2] ) ).weekday()
		insideOfHospital = False
		starttime = 0
		enterHospital = 0

		startnode = ""
		for c in current:
			staynode = c['stay_node']

			if (staynode in hospitalExit[0] or staynode in hospitalExit[1]) and insideOfHospital:
				if (staynode in hospitalExit[0] and enterHospital) or (staynode in hospitalExit[1] and not enterHospital):
					duration = int( c['starttime'] ) - starttime
					# t = int( datetime.fromtimestamp( int(c['starttime']) ).hour )
					t = c['next_node']
					
					staynode = ""
					if duration > 0 and duration <= 10000:
						if t in jwalkArea and t != " ":
							if dayType < 5:
								weekday.append(t)
							else:
								weekend.append(t)
					insideOfHospital = False

			if (staynode in hospitalExit[0] or staynode in hospitalExit[1]) and not insideOfHospital:
				if staynode in hospitalExit[1]:
					enterHospital = 1
				if c['next_node'] in Hospitals:
					insideOfHospital = True
					starttime = int( c['starttime'] )
					startnode = staynode

	bins = [x for x in range(24)]

	# weekend = np.array(weekend)
	# weekday = np.array(weekday)

	# s = list( set( weekend ) ) + list( set(weekday) )
	# weekend = [s.index(x) for x in weekend]
	# weekday = [s.index(x) for x in weekday]
	# for l in jwalkArea:
	# 	weekend.append(l)
	# 	weekday.append(l)
	for l in jwalkArea:
		weekend.append(l)
		weekday.append(l)
	plt.hist(weekday)
	plt.hist(weekend)	
	# plt.xticks( s )
	# plt.hist(weekday, bins = bins)
	# plt.hist(weekend, bins = bins)
	plt.show()

def InsideOutsideInside(reader):
	Hospitals = ["L", "M", "N", "O"]
	notHostpitals = ["G", "E", "A", "B", "C", "D", "R", "S", "T", "F"]
	weekday = []
	weekend = []
	totalWeekday = []
	totalWeekend = []
	for row in reader:
		current = json.loads( row[3] )
		dayType = datetime.fromtimestamp( int( row[2] ) ).weekday()
		outsideOfHospital = False
		starttime = 0

		startnode = ""
		for c in current:
			staynode = c['stay_node']
			nextnode = c['next_node']

			if staynode in Hospitals and outsideOfHospital:
				duration = int( c['starttime'] ) - starttime
				t = int( datetime.fromtimestamp( int(c['starttime']) ).hour )
				t = c['next_node']
				staynode = ""
				if duration > 2000 and duration <= 3000:
					if dayType < 5:
						weekday.append(t)
					else:
						weekend.append(t)
				outsideOfHospital = False

			if staynode in Hospitals and nextnode in notHostpitals and not outsideOfHospital:
				outsideOfHospital = True
				starttime = int( c['starttime'] )
				startnode = staynode

	bins = [x for x in range(24)]

	plt.hist(weekday)
	plt.hist(weekend)
	plt.show()

def OutsideInsideOutside(reader):
	Hospitals = ["L", "M", "N", "O"]
	notHostpitals = ["G", "E", "A", "B", "C", "D", "R", "S", "T", "F"]
	weekday = []
	weekend = []
	totalWeekday = []
	totalWeekend = []
	for row in reader:
		current = json.loads( row[3] )
		dayType = datetime.fromtimestamp( int( row[2] ) ).weekday()
		insideOfHospital = False
		starttime = 0

		startnode = ""
		for c in current:
			staynode = c['stay_node']
			nextnode = c['next_node']

			if staynode in notHostpitals and insideOfHospital:
				duration = int( c['starttime'] ) - starttime
				# t = int( datetime.fromtimestamp( int(c['starttime']) ).hour )
				t = c['next_node']
				staynode = ""
				if duration >= 0 and duration < 200:
					if dayType < 5:
						weekday.append(t)
					else:
						weekend.append(t)
				insideOfHospital = False

			if staynode in notHostpitals and nextnode in Hospitals and not insideOfHospital:
				insideOfHospital = True
				starttime = int( c['starttime'] )
				startnode = staynode

	bins = [x for x in range(24)]

	plt.hist(weekday)
	plt.hist(weekend)	
	plt.show()


def countHoursPerBuildingOLD(reader):
	Hospitals = ["L", "M", "N", "O"]
	hospitalExit = ["G", "E", "A"]
	weekday = []
	weekend = []
	totalWeekday = []
	totalWeekend = []
	for row in reader:
		current = json.loads( row[3] )
		dayType = datetime.fromtimestamp( int( row[2] ) ).weekday()
		insideOfHospital = False
		starttime = 0

		for c in current:
			staynode = c['stay_node']

			if staynode in hospitalExit and insideOfHospital:
				duration = int( c['starttime'] ) - starttime
				t = int( datetime.fromtimestamp( int(c['starttime']) ).hour )
				if duration < 300:
					if dayType < 5:
						weekday.append(t)
					else:
						weekend.append(t)

			if staynode in Hospitals:
				insideOfHospital = True
				starttime = int( c['starttime'] )

	bins = [x for x in range(24)]

	weekend = np.array(weekend)
	weekday = np.array(weekday)

	plt.hist(weekday, bins = bins)
	plt.hist(weekend, bins = bins)
	plt.show()

def countHours(reader):
	weekday = []
	weekend = []
	for row in reader:
		current = json.loads( row[3] )

		dayType = datetime.fromtimestamp( int( row[2] ) ).weekday()

		for c in current:
			t = int( datetime.fromtimestamp( int(c['starttime']) ).hour )
			if dayType < 5:
				weekday.append(t)
			else:
				weekend.append(t)

	bins = [x for x in range(24)]
	plt.hist(weekday, bins = bins)
	plt.hist(weekend, bins = bins)
	plt.show()

def getBuildingIndex(node):
	if not node:
		return None
	for index, b in enumerate(buildings):
		if node in b:
			return index
	return None

def personDetection(reader):
	print("Getting person detection time ")
	profiles = []
	for row in reader:
		id = row[4]
		current = json.loads( row[3] )

		starttime = 0
		cStarttime = 0
		duration = 0
		firstBuilding = -1
		lastBuilding = 0
		buildingCount = 0
		for c in current: 
			buildingCount += 1
			if not starttime:
				starttime = int( datetime.fromtimestamp( int(c['starttime']) ).weekday())
				cStarttime = int( c['starttime'] )

			duration = int( c['endtime'] ) - cStarttime

			currentBuilding = getBuildingIndex( c['stay_node'] )
			if ( firstBuilding == -1 and currentBuilding != None ):
				firstBuilding = getBuildingIndex( c['stay_node'] )
			
			if currentBuilding != None:
				lastBuilding = currentBuilding

		if buildingCount and firstBuilding != -1 and buildingCount < 100:
			profiles.append( [starttime, duration, firstBuilding, lastBuilding, buildingCount] )

	print("Done with profiles, printing...")

	with open( "data/personDetection1", 'w' ) as f:
		for person in profiles:
			f.write( json.dumps(person) )
			f.write( "\n" )

# Outputs 
def getAveragePerson(reader):
	print("Getting Average bridge time per person")
	bridgeProfiles = {}
	for row in reader:
		id = row[4]
		linuxTime = int( row[2] )
		current = json.loads( row[3] )

		weekday = []
		hour = []
		normalizedTime = []
		data = [[] * x for x in range(3)]
		for c in current:
			for index, bridge in enumerate(bridges):
				if c['stay_node'] in bridge and c['next_node'] in bridge:
					if int( c['take_time'] ) < 500 and int( c['take_time'] ) > 0:
							t = datetime.fromtimestamp( linuxTime )
							t2 = datetime.fromtimestamp( int(c['starttime']) )
							weekday.append( t.weekday() )
							hour.append( t2 )
							normalizedTime.append( int(c['take_time']) / averageBridgeTime[index] )

		if normalizedTime:
			if id in bridgeProfiles:
				bridgeProfiles[id][0] += normalizedTime
				bridgeProfiles[id][1] += weekday
				bridgeProfiles[id][2] += hour
			else: 
				bridgeProfiles[id] = [normalizedTime, weekday, hour]

	print("Done with profiles, averaging...") 

	averageBridgeTimePerPerson = []
	for id, d in bridgeProfiles.items():	# Profiling for each person
		times = d[0]
		w = d[1]	# List of weekdays
		h = d[2]	# List of hours
		average = sum( times ) / len( times )
		w = np.argmax( np.bincount(w) )		# Getting the most frequent weekday
		# h = np.argmax( np.bincount(h) )		# Getting the most frequent hour
		h = sum( h ) / len( h )
		averageBridgeTimePerPerson.append( [average, int(w), int(h)] )

	with open( "data/averageBridgeTimePerPerson3", 'w' ) as f:
		for person in averageBridgeTimePerPerson:
			f.write( json.dumps(person) )
			f.write( "\n" )

def checkDutation(reader):
	duration = []
	for row in reader:
		nodes = json.loads(row[3])
		c = choice(nodes)
		if int( c['take_time'] ) < 500:
			duration.append( int(c['take_time']) )

	plotDuration(duration)

def plotDuration(duration):
	sns.set()						# Making the plots look nice (using seaborn)
	binwidth = 1					# Setting for the histogram plot

	plt.hist( duration, bins=range(0, 500 + binwidth, binwidth) )

	plt.ylim(0, 11000)
	plt.show()
	
def getAverageBridgeTime(reader):
	print("Getting Average bridge time")
	i = 0

	bridgeTimings = [[] for i in range(len(bridges))]
	for row in reader:	# Loop through all the trajetories
		current = json.loads(row[3])
		dayType = datetime.fromtimestamp( int( row[2] ) ).weekday()

		onePersonTimings = [[] for i in range(len(bridges))]
		for c in current:	# Loop through the whole trip
			for index, bridge in enumerate(bridges):
				if c['stay_node'] in bridge and c['next_node'] in bridge:
					if int( c['take_time'] ) < 200 and int( c['take_time'] ) > 2:
						if dayType == 5:
							onePersonTimings[index].append( int(c['take_time']) )

		# Getting the average bridge timing
		for index, bridge in enumerate(onePersonTimings):
			if bridge:
				bridgeTimings[index].append( choice(bridge) )
				# bridgeTimings[index].append( sum(bridge) / len(bridge) )

	print("Counting average!")
	bridgeAverages = []
	for bridge in bridgeTimings:
		average = sum( bridge ) / len( bridge )
		bridgeAverages.append( average )

	print(bridges)
	print(bridgeAverages)
	plotBridgeTimings(bridgeTimings)

# Plotting the bridge duration histogram times of all the bridges
def plotBridgeTimings(bridgeTimings):
	sns.set()						# Making the plots look nice (using seaborn)
	binwidth = 1					# Setting for the histogram plot
	f, axarr = plt.subplots(3, 3)	# The general plot
	plt.ylim(0, 5000)
	j = 0
	for i in range(len(bridges)):	# Plotting all the bridges
		axarr[i % 3, j].hist( bridgeTimings[i], bins=range(0, 200 + binwidth, binwidth) )
		axarr[i % 3, j].set_title( bridges[i] )
		if i % 3 == 2:
			j += 1

	plt.ylim(0, 5000)
	plt.show()

# I'm going to fix this later, this is from the old code
def getSomeBuildingData(reader):
	people = []	
	i = 0

	for row in reader:
		current = json.loads(row[3])
		weekday = json.loads(row[2])

		# Ignore all the paths that is not of length 1
		if (len(current) != 1):
			p = [ 0 ] * ( 4 )

			for c in current:
				last = ""
				for index, building in enumerate(buildings):
					if c['stay_node'] in building and c['next_node'] in building:
						if last not in building:
							if p[2] == 0:
								people.append(p)
							p[0] = date.fromtimestamp(int(weekday)).weekday()
							p[1] = int( c['starttime'] )
							p[2] += int( c['duration'] )
							p[3] = index	# Number of the building
						else:
							p[2] += int( c['duration'] )
		i += 1


if __name__ == "__main__":
	main()
	
