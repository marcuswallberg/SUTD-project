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

bridges = [["A", "B"], ["A", "M"], ["O", "M"], ["O", "L"], ["E", "L"], ["G", "N"], ["F", "R"]]
buildings = [["A"], ["B"], ["E", "C", "D"], ["F", "G"], ["M", "L"], ["O", "N"], ["R", "S", "T"]]
averageBridgeTime = [95.2898899411313, 77.1288674116581, 12.477234429414873, 70.02633256822239, 23.62944144315667, 33.80125095736533, 61.48033157379018]

def main():
	with open('./src/wifi_passive_trajectory_node.csv', newline='') as csvfile:
		wifiReader = csv.reader(csvfile, delimiter=',', quotechar='"')
		wifiReader.__next__()	# Remove the first line, which is info data
		
		if not averageBridgeTime:
			getAverageBridgeTime(wifiReader)

		start = time.time()
		getAveragePerson(wifiReader)
		end = time.time()
		elapsed = end - start
		print("getAveragePerson took {e} seconds".format( e = int(elapsed) ))

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
							hour.append( t2.hour )
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
		h = np.argmax( np.bincount(h) )		# Getting the most frequent hour
		averageBridgeTimePerPerson.append( [average, int(w), int(h)] )

	with open( "data/averageBridgeTimePerPerson", 'w' ) as f:
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
					if int( c['take_time'] ) < 500 and int( c['take_time'] ) > 0:
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
	j = 0
	for i in range(len(bridges)):	# Plotting all the bridges
		axarr[i % 3, j].hist( bridgeTimings[i], bins=range(0, 200 + binwidth, binwidth) )
		axarr[i % 3, j].set_title( bridges[i] )
		if i % 3 == 2:
			j += 1

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
	
