# ['_id', 'created_on', 'date', 'starttime', 'user_id']
# starttime: [{"stay_node","endtime","starttime","duration","next_node","take_time"}]
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


with open('./src/wifi_passive_trajectory_node.csv', newline='') as csvfile:
	wifiReader = csv.reader(csvfile, delimiter=',', quotechar='"')
	# dict = []
	i = 0
	last = ""
	count = 0
	pathLengthList =[]
	wifiReader.__next__()

	stay_node_list = []

	for row in wifiReader:
		# if i > 5:
		# 	break
		
		current = json.loads(row[3])

		if (len(current) != 1):
			pathLengthList.append(len(current))

			for r in current:
				stay_node_list.append(ord(r["next_node"]))


		# last = current
		i += 1

	average = sum(pathLengthList) / len(pathLengthList)

	print(average)
	print(max(pathLengthList))
	sns.set()
	
	plt.hist(stay_node_list, bins= list(range(60,105)))
	plt.show()

	# Histogram of the path legngth
	# plt.hist(pathLengthList, bins=list(range(1,50)))
	# plt.show()



