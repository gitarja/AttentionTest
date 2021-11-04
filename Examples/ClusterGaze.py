import pandas as pd
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans

with open("..\\conf\\GameSettings.yml", 'r') as stream:
    try:
        conf = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)





data = pd.read_csv("..\\" + conf["GAME_DIR"] + conf["GAME_RESULT_DIR"] + "AT_000008_" + conf["GAZE_HEAD_FILE"])

# dataHeadPos = data[["HeadPosX","HeadPosY","HeadPosZ"]]
# dataHeadRot = data[["HeadRotX","HeadRotY","HeadRotZ"]]
#
# dataBeforePos = dataHeadPos.iloc[:-1]
# dataAfterPos = dataHeadPos.iloc[1:]
#
# dataBeforeRot = dataHeadRot.iloc[:-1]
# dataAfterRot = dataHeadRot.iloc[1:]
#
# headPosChanges = np.sum(np.sqrt(np.square(dataAfterPos.values - dataBeforePos.values)), axis=-1)
#
# headRotChanges = np.sum(np.sqrt(np.square(dataAfterRot.values - dataBeforeRot.values)), axis=-1)

#dataHead = pd.DataFrame({"Time":data.Time[1:].values, "HeadPosChange":headPosChanges, "HeadRotChange":headRotChanges})

groupCons = np.floor(data.Time // 0.3).astype(int)
data = data.loc[(data.GazeX >= 0) & (data.GazeY >= 0) & (data.Time > 0)]
x = data.GazeX.groupby(groupCons).mean().values
y = data.GazeY.groupby(groupCons).mean().values
times = data.Time.groupby(groupCons).mean().values

points = np.column_stack([x, y])
pointsBef = points[:-1]
pointsNext = points[1:]

distances = np.average(np.sqrt(np.square(pointsNext - pointsBef)), axis=-1)
nCluster = 20
kmeans = KMeans(n_clusters=nCluster, random_state=0).fit(points)
sizes = (300 * np.array([np.sum(kmeans.labels_ == i) for i in range(nCluster)]) / points.shape[0]) **2
rng = np.random.RandomState(0)
plt.scatter(kmeans.cluster_centers_[:, 0],kmeans.cluster_centers_[:,1],  s=sizes, alpha=0.3, cmap='viridis')
# plt.figure(311)
# plt.scatter(x, y, alpha=0.3)
# plt.figure(312)
# plt.plot(times[1:], distances)
#
# plt.figure(313)
# N = distances.shape[0]
# sp = np.fft.fft(distances)
# mag = np.sqrt(sp.real ** 2 + sp.imag ** 2)
# freq = np.fft.fftfreq(distances.shape[0])
# print(np.average(mag[1:int(N/2)]))
# plt.plot(freq[1:int(N/2)], mag[1:int(N/2)])

plt.show()



#
#
# sns.set_style("white")
# ax = sns.kdeplot(data.GazeX.values.flatten(), data.GazeY.values.flatten(), shade=True, cmap="Reds",  bw=.15)
# ax.set_xlim([0.0,1.0])
# ax.set_ylim([0.0,1.0])
# plt.show()


# Plot
# plt.scatter(data.GazeX.values.flatten(), data.GazeY.values.flatten(), alpha=0.5)
# plt.title('Scatter plot pythonspot.com')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.show()
