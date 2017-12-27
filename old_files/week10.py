# ['_id', 'created_on', 'date', 'starttime', 'user_id']
# starttime: [{"stay_node","endtime","starttime","duration","next_node","take_time"}]
import json
import csv
import numpy as np
from datetime import date
from datetime import datetime
import time
import matplotlib.pyplot as plt
import seaborn as sns

"""
----- FEATURES -----
1. For each person find walking duration for every bridge, starting time. 
2. For each person every building starting time and stay duration 
3. For each person average stay duration per building 
4. For each person's average walking duration per bridge 
5. For each bridge average speed of every person per hour 
6. For each person, First detection time, Last detection time, Total duration, 
7. For each person first detect building, last detect building, number of buildings visited
"""

buildings = [["A"], ["B"], ["E", "C", "D"], ["F", "G"], ["M", "L"], ["O", "N"], ["R", "S", "T"]]
bridges = [["A", "B"], ["A", "M"], ["O", "M"], ["T", "C"], ["E", "L"], ["G", "N"], ["F", "R"]]
averageBridgeTime = [99.01482453496001, 79.64656635224834, 116.42084775086505, 65.2228693747511, 63.19306946584489, 118.37664715593577, 85.67405063291139]

def main():
	with open('./src/wifi_passive_trajectory_node.csv', newline='') as csvfile:
		jwalkReader = csv.reader(csvfile, delimiter=',', quotechar='"')
		jwalkReader.__next__()	# Remove the first line, which is info data
		
		# countRepeats( jwalkReader )
		AGE( jwalkReader )

# Counts how many times one person gets back to a visited node for each path
def countRepeats(reader):
	count = 0

	for row in reader:
		paths = json.loads( row[3] )

		lastNode = "x"
		for node in paths:
			if lastNode == node['next_node'] and lastNode != " ":
				count += 1
			lastNode = node['stay_node']

	print( count )



def AGE(reader):
	Hospitals = ["L", "M", "N", "O"]		
	# hospitalExit = ["G", "F", "R", "S", "A", "B"]	# G and A
	# hospitalExit = ["G", "F", "R", "S", "E", "C", "T", "D"]	# G and E
	hospitalExit = ["E", "C", "T", "D" "A", "B"]	# E and A
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

			if staynode in hospitalExit and insideOfHospital:
				duration = int( c['starttime'] ) - starttime
				t = int( datetime.fromtimestamp( int(c['starttime']) ).hour )
				staynode = ""
				if duration < 300:
					if dayType < 5:
						weekday.append(t)
					else:
						weekend.append(t)

			if staynode in hospitalExit and not insideOfHospital:
				if c['next_node'] in Hospitals:
					insideOfHospital = True
					starttime = int( c['starttime'] )
					startnode = staynode

	bins = [x for x in range(24)]

	weekend = np.array(weekend)
	weekday = np.array(weekday)

	plt.hist(weekday, bins = bins)
	plt.hist(weekend, bins = bins)
	plt.show()

def countHoursPerBuilding(reader):
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

		startnode = ""
		for c in current:
			staynode = c['stay_node']

			if staynode in hospitalExit and insideOfHospital:
				duration = int( c['starttime'] ) - starttime
				t = int( datetime.fromtimestamp( int(c['starttime']) ).hour )
				staynode = ""
				if duration < 300:
					if dayType < 5:
						weekday.append(t)
					else:
						weekend.append(t)

			if staynode in Hospitals and not insideOfHospital:
				insideOfHospital = True
				starttime = int( c['starttime'] )
				startnode = staynode

	bins = [x for x in range(24)]

	weekend = np.array(weekend)
	weekday = np.array(weekday)

	plt.hist(weekday, bins = bins)
	plt.hist(weekend, bins = bins)
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
	# totalWeekend = np.array(totalWeekend)
	# totalWeekday = np.array(totalWeekday)

	# unique1, counts1 = np.unique(weekday, return_counts=True)
	# unique2, counts2 = np.unique(weekend, return_counts=True)
	# unique3, counts3 = np.unique(totalWeekday, return_counts=True)
	# unique4, counts4 = np.unique(totalWeekend, return_counts=True)

	# w1 = counts1 / counts3 
	# w2 = counts2 / counts4

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

	
def getAverageBridgeTime(reader):
	print("Getting Average bridge time")
	i = 0
	bridgeTimings = [[] for i in range(len(bridges))]
	for row in reader:	# Loop through all the trajetories
		current = json.loads(row[3])

		for c in current:	# Loop through the whole trip
			for index, bridge in enumerate(bridges):
				if c['stay_node'] in bridge and c['next_node'] in bridge:
					if int( c['take_time'] ) < 500 and int( c['take_time'] ) > 2:
						bridgeTimings[index].append( int(c['take_time']) )
		# i += 1

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
	binwidth = 5					# Setting for the histogram plot
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
		# if i > 1000:		# Uncomment this if you want to stop early
		# 	break
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

def plot():
		print("Plotting")
		# print(people[23])

		f = open('featuredata2', 'w')
		for p in people:
			f.write(str(p))
			f.write("\n")
		f.close()

		# print(average)
		# print(max(pathLengthList))
		sns.set()

if __name__ == "__main__":
	main()
	
