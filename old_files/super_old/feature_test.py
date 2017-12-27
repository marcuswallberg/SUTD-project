# ['_id', 'created_on', 'date', 'starttime', 'user_id']
# starttime: [{"stay_node","endtime","starttime","duration","next_node","take_time"}]
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""
----- TASK -----
1. For each person find walking duration for every bridge, starting time. 
2. For each person every building starting time and stay duration 
3. For each person average stay duration per building 
4. For each person's average walking duration per bridge 
5. For each bridge average speed of very person per hour 
6. For each person, First detection time, Last detection time, Total duration, first detect building, last detect building, number of buildings visited
"""

bridges = [["A", "B"], ["A", "M"], ["O", "M"], ["O", "L"], ["E", "L"], ["G", "N"], ["F", "R"]]

with open('./src/wifi_passive_trajectory_node.csv', newline='') as csvfile:
	wifiReader = csv.reader(csvfile, delimiter=',', quotechar='"')
	i = 0
	count = 0
	pathLengthList =[]
	wifiReader.__next__()

	stay_node_list = []

	people = []

	for row in wifiReader:
		# if i > 1000:
		# 	break
		
		current = json.loads(row[3])

		# Ignore all the paths that is not of length 1
		if (len(current) != 1):
			for c in current:
				
				for index, bridge in enumerate(bridges):
					if c['stay_node'] in bridge and c['next_node'] in bridge:
						durations[index].append( int( c['take_time'] ) )
		i += 1

	for duration in durations:
		print( sum( duration ) / len( duration ) )

	# print(average)
	# print(max(pathLengthList))
	# sns.set()
	
	# plt.hist(stay_node_list, bins= list(range(60,105)))
	# plt.show()

	# Histogram of the path legngth
	# plt.hist(pathLengthList, bins=list(range(1,50)))
	# plt.show()



