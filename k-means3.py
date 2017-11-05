from time import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn import cluster
from sklearn.datasets import load_svmlight_file
import math
import json

f = open("data/averageBridgeTimePerPerson3")
data = []
for i in range(10000):
# for i, line in enumerate(f):
  data.append(json.loads(f.readline()))
f.close()
data = np.array(data)
# data = np.delete( data, 2, 1 )
print(data[0])

k_means = cluster.KMeans(n_clusters=4)
k_means.fit(data) 
y = k_means.labels_

colors = ['r', 'b', 'g', 'y', 'm']
markers = ['x', 'o', '8', 'p', 'd', '*', '2', 'x']
# markers = ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']
colorLabels = [ colors[x] for x in y ]
markerLabels = [ markers[x] for x in y ]

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
# sns.set()
# df = pd.DataFrame(dict(x = data, y = y, labels = colorLabels ))
# sns.set(style="ticks")
sns.set()
# sns.plot(df)

fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
# f, axarr = plt.subplots(1, 3)
for i in range(0, len(data), int(len(data) / 500)): 
	d = data[i]
	c = colorLabels[i]
	# print(d)
	# ax.scatter(d[1], d[2], d[0], c = c, s = 100 )
	ax1.scatter(d[1], d[0], c = c, s = 100 )
	ax2.scatter(d[2], d[0], c = c, s = 100 )
	ax3.scatter(d[2], d[1], c = c, s = 100 )

plt.show()

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# Axes3D.plot(k_means.labels_[::10])
