from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2
import seaborn as sns; sns.set(color_codes=True)
from scipy import stats


path = 'D:\\usr\\pras\\data\\Yokohama Kokudai Data\\AttentionTest\\result\\'
resultPath = "D:\\usr\\pras\\data\\googledrive\\Research-Doctoral\\Experiment-Result\\AttentionTest-2019-11-18"
extension = 'csv'
os.chdir(path)
files = glob.glob('*.{}'.format(extension))

dataAll = []

def plotCluster(img, clusterObj, sizeObj, clusterGaze, sizeGaze, filename):
    plt.imshow(img, extent=[0, 1, 0, 1], aspect='auto')
    pltObj = plt.scatter(clusterObj.means_[:, 0], clusterObj.means_[:, 1], s=sizeObj,
                            alpha=0.7, color="yellow", edgecolors="face")
    pltGaze = plt.scatter(clusterGaze.means_[:, 0], clusterGaze.means_[:, 1], s=sizeGaze,
                             alpha=0.7, color="royalblue", edgecolors="face")

    plt.legend((pltObj, pltGaze),
               ("Object cluster", "Gaze Clusters"),
               scatterpoints=1,
               loc='lower center',
               ncol=2,
               fontsize=8)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.savefig(filename)
    plt.show()


#add yokohama
summaryFile = 'D:\\usr\\pras\\data\\Yokohama Kokudai Data\\AttentionTest\\Results\\EvaluationResults\\summary.csv'
listFiles = pd.read_csv(summaryFile)
listFiles = listFiles[listFiles["handOrFoot"] == 0]
for index, row in listFiles.iterrows():
    data = pd.read_csv(os.path.join(path, row["id"]+"_gameResults.csv"))
    dataAll.append(data)


# for file in files:
#     data = pd.read_csv(file)
#     dataAll.append(data)

concatData = pd.concat(dataAll, ignore_index=True)

positifResponseNoMiss = concatData.loc[(concatData.PosResponse == 1) & (concatData.ResponseTime != -1) & (concatData.Distance >0) & (concatData.DiffTime > 0)]
negativeResponse = concatData.loc[(concatData.NegResponse == 1) & (concatData.ResponseTime != -1) & (concatData.Distance >0) & (concatData.DiffTime > 0)]
missResponse =  concatData.loc[(concatData.MissResponse == 1)]

#positif and  response

#----------------------------------------------kde - Response Time-------------------------------------------#
sns.kdeplot(positifResponseNoMiss.DiffTime.values, label="Positive", shade=True)
sns.kdeplot(negativeResponse.DiffTime.values, label="Negative", shade=True)
plt.legend()
plt.xlabel("Response Time (s)")
plt.savefig(os.path.join(resultPath, "ResponseTimePosNeg.png"))
plt.show()
#----------------------------------------------kde - DiffGaze Time-------------------------------------------#
sns.kdeplot(positifResponseNoMiss.Distance.values, label="Positive", shade=True)
sns.kdeplot(negativeResponse.Distance.values, label="Negative", shade=True)
plt.legend()
plt.xlabel("Distance (Object - Gaze) (pix)")
plt.savefig(os.path.join(resultPath, "DistanceGazePosNeg.png"))
plt.show()




#scatter plotting
posPlot = plt.scatter(positifResponseNoMiss.Distance.values, positifResponseNoMiss.DiffTime.values, marker="+", color="royalblue")
negPlot = plt.scatter(negativeResponse.Distance.values, negativeResponse.DiffTime.values, marker="x", color="orangered")
plt.ylabel("Response Time (s)")
plt.xlabel("Distance (Object - Gaze) (pix)")


plt.legend((posPlot, negPlot),
           ("Positive Response", "Negative Response"),
           scatterpoints=1,
           loc='upper center',
           ncol=2,
           fontsize=8)
plt.savefig(os.path.join(resultPath, "RawResult.png"))
plt.show()

#----------------------------------------------Visual Processing-------------------------------------------#
# Open game background
img = cv2.imread("D:\\usr\\pras\\project\\PyhtonProject\\AttentionTest\\Conf\\game_bg.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Cluster of object for negative response
X = negativeResponse[["ObjectX", "ObjectY"]]
clusterObj = GaussianMixture(n_components=9).fit(X)
sizeObj = 1000 * clusterObj.weights_
print(clusterObj.means_)
# Cluster of gaze for negative response
X = negativeResponse[["GazeX", "GazeY"]]
clusterGaze = GaussianMixture(n_components=9).fit(X)
sizeGaze = 1000 * clusterGaze.weights_

#Plotting
plotCluster(img, clusterObj, sizeObj, clusterGaze, sizeGaze, os.path.join(resultPath, "NegativeCluster.png"))


# Cluster of object for miss response
X = missResponse[["ObjectX", "ObjectY"]]
clusterObj = GaussianMixture(n_components=9).fit(X)
sizeObj = 1000 * clusterObj.weights_

# Cluster of gaze for miss response
X = missResponse[["GazeX", "GazeY"]]
clusterGaze = GaussianMixture(n_components=9).fit(X)
sizeGaze = 1000 * clusterGaze.weights_

#Plotting
plotCluster(img, clusterObj, sizeObj, clusterGaze, sizeGaze, os.path.join(resultPath, "MissCluster.png"))

#Cluster for Mid to Slow response time (0.35-0.45s) and Slow to VerySlow (0.45-0.65s)
midResponse = positifResponseNoMiss.loc[(positifResponseNoMiss.DiffTime >=0.35) & (positifResponseNoMiss.DiffTime <0.45)]
slowResponse = positifResponseNoMiss.loc[(positifResponseNoMiss.DiffTime >=0.45) & (positifResponseNoMiss.DiffTime <0.65)]

negativeMidResponse = negativeResponse.loc[(negativeResponse.DiffTime >=0.35) & (negativeResponse.DiffTime <0.45)]

# Cluster of object for mid response
X = midResponse[["ObjectX", "ObjectY"]]
clusterObj = GaussianMixture(n_components=9).fit(X)
sizeObj = 1000 * clusterObj.weights_

# Cluster of gaze for mid response
X = midResponse[["GazeX", "GazeY"]]
clusterGaze = GaussianMixture(n_components=9).fit(X)
sizeGaze = 1000 * clusterGaze.weights_

#Plotting
plotCluster(img, clusterObj, sizeObj, clusterGaze, sizeGaze, os.path.join(resultPath, "MidSlowCluster.png"))


# Cluster of object for slow response
X = slowResponse[["ObjectX", "ObjectY"]]
clusterObj = GaussianMixture(n_components=9).fit(X)
sizeObj = 1000 * np.unique(clusterObj.weights_, return_counts=True)[1] / len(X)

# Cluster of gaze for slow response
X = slowResponse[["GazeX", "GazeY"]]
clusterGaze = GaussianMixture(n_components=9).fit(X)
sizeGaze = 1000 * np.unique(clusterGaze.weights_, return_counts=True)[1] / len(X)

#Plotting
#plotCluster(img, clusterObj, sizeObj, clusterGaze, sizeGaze)

#----------------------------------------------kde - Response Time Neg-Mid-------------------------------------------#
sns.kdeplot(midResponse.DiffTime.values, label="Positive", shade=True)
sns.kdeplot(negativeMidResponse.DiffTime.values, label="Negative", shade=True)
plt.legend()
plt.xlabel("Response Time (s)")
plt.savefig(os.path.join(resultPath, "ResponseTimeNegMid.png"))
plt.show()
#----------------------------------------------kde - DistanceGaze Neg-Mid-------------------------------------------#
sns.kdeplot(midResponse.Distance.values, label="Mid", shade=True)
sns.kdeplot(negativeResponse.Distance.values, label="Negative", shade=True)
plt.legend()
plt.savefig(os.path.join(resultPath, "DistanceGazeTimeNegMid.png"))
plt.xlabel("Distance (Object - Gaze) (pix)")
plt.show()

