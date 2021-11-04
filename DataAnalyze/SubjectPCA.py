from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
import  matplotlib
# matplotlib.use('Agg')
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import os
import glob
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns

# sns.set()

resultPath = "D:\\usr\\pras\\data\\googledrive\\Research-Doctoral\\Experiment-Result\\AttentionTest-2019-11-18-Hiro-Yoko\\GazeTrack\\"
hiroData = pd.read_csv(os.path.join(resultPath, "summary_hiro.csv"))
yokoData = pd.read_csv(os.path.join(resultPath, "summary_yoko.csv"))
result = pd.concat([hiroData, yokoData])
result = result.fillna(0)


X = result[["polyArea", "avgResponseTime", "stdResponseTime"]].values
y = result[["polyArea"]].values
subjects = result[["id", "polyArea", "stdResponseTime", "avgResponseTime", "negativePer", "missPer"]]
pca = PCA(n_components=2)

meanPloy = np.mean(y)
# X[:, 0] = (X[:, 0] - np.min(X[:, 0])) / (np.max(X[:, 0]) - np.min(X[:, 0]))
components = pca.fit_transform(X, y)


cluster = KMeans(n_clusters=2)
labels = cluster.fit_predict(X)
# print(labels)
means = cluster.cluster_centers_

# plotting
print(labels)
group1 = np.where(labels==0)[0]
group2 = np.where(labels==1)[0]
group3 = np.where(labels==2)[0]
group4 = np.where(labels==3)[0]
# print(np.average(subjects[group1], 0))
#
# print(np.average(subjects[group2], 0))
subjects.iloc[group1].to_csv("group1.csv")
subjects.iloc[group2].to_csv("group2.csv")
# print(subjects[group1].to)
# print(subjects[group2])

#
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(components[group1, 0], components[group1, 1], marker = "+", c="#1b9e77")
ax.scatter(components[group2, 0], components[group2, 1],  marker = "x", c="#d95f02")
# ax.scatter(components[group3, 0], components[group3, 1], components[group3, 2], marker = "*")
# ax.scatter(components[group3, 0], components[group3, 1], marker = ".")
ax.scatter(means[:, 0], means[:, 1], marker = "^", s = 50, c="#e41a1c")
# ax = fig.add_subplot(111)
# ax.scatter(components[:, 0], components[:, 1], marker = "^")
# ax.scatter(components[group2, 0], components[group2, 1], marker = "o")


ax.set_xlabel('Component 1')
ax.set_ylabel('Component 2')
# ax.set_zlabel('Component 3')
# ax.view_init(-84, 31)


plt.savefig(os.path.join(resultPath, "clusterSubjects_2.eps"), format='eps')
# plt.show()

