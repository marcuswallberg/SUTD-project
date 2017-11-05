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

f = open("featuredata2")
data = []
for i in range(10000):
# for i, line in enumerate(f):
  data.append(json.loads(f.readline()))
f.close()
data = np.array(data)
print(data[0])

k_means = cluster.KMeans(n_clusters=5)
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
sns.set(style="ticks")
# sns.plot(df)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax = fig.add_subplot(111)

for i in range(0, len(data), int(len(data) / 500)): 
	d = data[i]
	c = colorLabels[i]
	m = markers[d[3]]
	# print(d)
	ax.scatter(d[1], d[2], d[3], c = c, marker = m, s = 100 )
	# ax.scatter(d[1], d[2], c = c, marker = m, s = 100 )

plt.show()

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# Axes3D.plot(k_means.labels_[::10])
