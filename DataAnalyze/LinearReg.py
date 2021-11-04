import matplotlib.pyplot as plt
import os
import glob
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import pearsonr
from scipy import stats
import seaborn as sns

# sns.set()
sex = ""

# path = 'D:\\usr\\pras\\data\\AttentionTestData\\processed'
hiroPath = 'D:\\usr\\pras\\data\\AttentionTestData\\Hiroshima\\result\\'
yokoPath = 'D:\\usr\\pras\\data\\AttentionTestData\\Yokodai\\AttentionTest\\result\\'

# resultPath = "D:\\usr\\pras\\data\\googledrive\\Research-Doctoral\\Experiment-Result\\AttentionTest-2019-10-25"
resultPath = "D:\\usr\\pras\\data\\googledrive\\Research-Doctoral\\Experiment-Result\\AttentionTest-2019-11-18-Hiro-Yoko\\" + sex + "\\"
# extension = 'csv'
# os.chdir(path)
# files = glob.glob('*.{}'.format(extension))

dataAll = []

# Adding HIROSHIMA DATA
summaryFile = 'D:\\usr\\pras\\data\\AttentionTestData\\Hiroshima\\summary.csv'
listFiles = pd.read_csv(summaryFile)
# listFiles = listFiles[listFiles["sex"] == sex]
for index, row in listFiles.iterrows():
    data = pd.read_csv(os.path.join(hiroPath, row["id"] + "_gameResults.csv"))
    dataAll.append(data)

# Adding YOKODAI DATA
summaryFile = 'D:\\usr\\pras\\data\\AttentionTestData\\Yokodai\\AttentionTest\\summary.csv'
listFiles = pd.read_csv(summaryFile)
# listFiles = listFiles[(listFiles["handOrFoot"] == 0) & (listFiles["sex"] == sex)]
listFiles = listFiles[listFiles["handOrFoot"] == 0]
for index, row in listFiles.iterrows():
    data = pd.read_csv(os.path.join(yokoPath, row["id"] + "_gameResults.csv"))
    dataAll.append(data)

# for file in files:
#     data = pd.read_csv(os.path.join(path, file))
#     dataAll.append(data)

# concatData = pd.concat(dataAll, ignore_index=True, sort=True)
# filteredDataNeg = concatData.loc[
#     (concatData.NegResponse == 1) & (concatData.ResponseTime != -1) & (concatData.Distance > 0) & (
#                 concatData.DiffTime > 0)]
# filteredDataPos = concatData.loc[
#     (concatData.PosResponse == 1) & (concatData.ResponseTime != -1) & (concatData.Distance > 0) & (
#                 concatData.DiffTime > 0)]
#
# filteredDataMiss = concatData.loc[
#     (concatData.MissResponse == 1) ]

# plt.figure()
# X = filteredDataNeg[["Distance"]].values
# y = filteredDataNeg[["DiffTime"]].values
#
# plt.boxplot(labels=["Correct Response", "Wrong Response","Correct Response", "Wrong Response"],
#             x=[filteredDataPos.DiffTime.values * 1000, filteredDataPos.DiffTime.values * 100,
#                filteredDataNeg.DiffTime.values * 1000, filteredDataNeg.DiffTime.values * 100], showmeans=True)
#
# plt.ylabel("Response Time (ms)")
# plt.savefig(os.path.join(resultPath, "responseTime.png"))

# #Response percentage
# print(np.average(concatData.PosResponse.values) * 100)
# print("=============================================NoGo: =============================================")
# print(np.average(concatData.NegResponse.values) * 100)
# #print("=============================================STD NoGo:=============================================")
# print(np.std(concatData.NegResponse.values) * 100)
# print("=============================================Go:=============================================")
# print(np.average(concatData.MissResponse.values) * 100)
# #print("=============================================STD Go:=============================================")
# print(np.std(concatData.MissResponse.values) * 100)
#
# #Response Time
# #Go
# print("=============================================GO RT:=============================================")
# print(np.average(filteredDataPos.DiffTime.values) * 1000)
# #print("=============================================STD Go RT:=============================================")
# print(np.std(filteredDataPos.DiffTime.values) * 1000)
# #NoGo
# print("=============================================NoGo RT:=============================================")
# print(np.average(filteredDataNeg.DiffTime.values) * 1000)
# #print("=============================================STD NoGo RT:=============================================")
# print(np.std(filteredDataNeg.DiffTime.values) * 1000)
#
#
# #Distance Objects
# #Go
# print("=============================================Distance Objects Go:=============================================")
# print(np.average(filteredDataPos[filteredDataPos.ObjDistance != -1].ObjDistance.values))
# #print("=============================================STD Distance Objects Go:=============================================")
# print(np.std(filteredDataPos[filteredDataPos.ObjDistance != -1].ObjDistance.values))
# #NoGo
# print("=============================================Distance Objects NoGo:=============================================")
# print(np.average(filteredDataNeg[filteredDataNeg.ObjDistance != -1].ObjDistance.values))
# #print("=============================================STD Distance Objects NoGo:=============================================")
# print(np.std(filteredDataNeg[filteredDataNeg.ObjDistance != -1].ObjDistance.values))
#
# #Distance Gaze-Object
# #Go
# print("=============================================Distance Go:=============================================")
# print(np.average(filteredDataPos[filteredDataPos.Distance != 0].Distance.values))
# #print("=============================================STD Distance Go:=============================================")
# print(np.std(filteredDataPos[filteredDataPos.Distance != 0].Distance.values))
# #NoGo
# print("=============================================Distance NoGo:=============================================")
# print(np.average(filteredDataNeg[filteredDataNeg.Distance != 0].Distance.values))
# #print("=============================================STD Distance NoGo:=============================================")
# print(np.std(filteredDataNeg[filteredDataNeg.Distance != 0].Distance.values))

# polynomial_features= PolynomialFeatures(degree=5)
# x_poly = polynomial_features.fit_transform(X)


# # #Linear reg
#
# reg = stats.linregress(X[:, 0], y[:, 0])
# print(reg)
# yPred = reg.intercept + reg.slope*X
#
# plt.figure()
# plt.scatter(X, y * 1000, marker="x", color="orangered")
# plt.plot(X, yPred * 1000, color="blue", linewidth=3)
# plt.xlim(0, 1)
# plt.ylabel("Response Time (ms)")
# plt.xlabel("Distance (Object - Gaze)")
# plt.savefig(os.path.join(resultPath, "NegativeRes.eps"))
# plt.show()
#
# # Pearson corr
#
# # write summary
# f = open(os.path.join(resultPath, "negative_summary.txt"), "w+")
# f.write("RMSE:" + str(reg.stderr) + "\n")
# f.write("Pearson-coefficient:" + str(reg.rvalue) + "\n")
# f.write("P-val:" + str(reg.pvalue))
# f.write("Slope:" + str(reg.slope))
#
# X = filteredDataPos[["Distance"]].values
# y = filteredDataPos[["DiffTime"]].values
#
# reg = stats.linregress(X[:, 0], y[:, 0])
# print(reg)
# yPred = reg.intercept + reg.slope*X
#
#
# plt.scatter(X, y * 1000, marker="x", color="orangered")
# plt.plot(X, yPred * 1000, color="blue", linewidth=3)
# plt.xlim(0, 1)
#
# plt.ylabel("Response Time (ms)")
# plt.xlabel("Distance (Object - Gaze)")
# plt.savefig(os.path.join(resultPath, "PositiveRes.eps"))
# plt.show()
#
# # write summary
# f = open(os.path.join(resultPath, "positive_summary.txt"), "w+")
# f.write("RMSE:" + str(reg.stderr) + "\n")
# f.write("Pearson-coefficient:" + str(reg.rvalue) + "\n")
# f.write("P-val:" + str(reg.pvalue))
# f.write("Slope:" + str(reg.slope))
