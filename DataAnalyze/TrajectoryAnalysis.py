import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import numpy as np
from scipy import stats
from scipy import stats
import cv2
import os
from scipy.spatial import ConvexHull


# sns.set()


def plotPoly(x, y, label):
    plt.scatter(y, x * 100, label=label)
    plt.ylim(-1, 100)
    plt.xlim(0, 2)
    plt.ylabel("Response Percentage (%)")
    plt.xlabel("Trajectory Area")


# resultPath = "D:\\usr\\pras\\data\\googledrive\\Research-Doctoral\\Experiment-Result\\AttentionTest-2019-11-18-Hiro-Yoko\\GazeTrack\\"
# summaryPath = "D:\\usr\\pras\\data\\googledrive\\Research-Doctoral\\Experiment-Result\\AttentionTest-2019-11-18-Hiro-Yoko\\summary\\"


resultPath = "D:\\usr\\pras\\data\\AttentionTestData\\Hoikuen(2020-01-24)\\summaryResults\\"


# area of polygon
# def areaPoly(x, y):
#     xA = x[0:-1]
#     xB = x[1:]
#     yA = y[0:-1]
#     yB = y[1:]
#
#     area = np.abs(np.sum(xA * yB) - np.sum(xB * yA) + (x[-1] * y[0] - x[0] * y[-1])) * 0.5
#
#     return area
#
def areaPolyImage(x, y, impath=None):
    # max area (480, 640)
    maxArea = 306081.0
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.scatter(x, y, c="black")
    # ax.scatter(x, y, c="black", s = 50)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.canvas.draw()
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # ret, thresh = cv2.threshold(img, 125, 255, 0)
    # thresh = cv2.bitwise_not(thresh)

    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    edged = cv2.Canny(dilation, 1, 1)
    dilation2 = cv2.dilate(edged.copy(), kernel, iterations=1)
    im2, contours, hierarchy = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imwrite(impath, dilation2)
    print(len(contours))
    # print(len(contours))
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    # (x, y), (MA, ma), angle = cv2.fitEllipse(cnts[0])
    # im2 = cv2.ellipse(img, ellipse, (0, 255, 0), 2)

    # areaE = np.pi * MA * ma

    area = (cv2.contourArea(cnts[0]) + cv2.contourArea(cnts[1]) + cv2.contourArea(cnts[2])) / maxArea
    print(area)
    return area


def convexHullArea(data):
    hull = ConvexHull(points=data)
    return hull.volume


# yokoOrHiro = "_hiro"
# hiroPath = 'D:\\usr\\pras\\data\\AttentionTestData\\Hiroshima\\result\\'
# yokoPath = 'D:\\usr\\pras\\data\\AttentionTestData\\Yokodai\\AttentionTest\\result\\'
# summaryFile = 'D:\\usr\\pras\\data\\AttentionTestData\\Hiroshima\\summary.csv'
# summaryFile = 'D:\\usr\\pras\\data\\AttentionTestData\\Yokodai\\AttentionTest\\summary.csv'

yokoOrHiro = ""
summaryFile = 'D:\\usr\\pras\\data\\AttentionTestData\\Hoikuen(2020-01-24)\\summary_id.csv'
filePath = "D:\\usr\\pras\\data\\AttentionTestData\\Hoikuen(2020-01-24)\\results\\"

listFiles = pd.read_csv(summaryFile)
# # listFiles = listFiles[(listFiles["handOrFoot"] == 0)]
result = pd.DataFrame(
    columns=["id", "sex", "polyArea", "positivePer", "negativePer", "missPer", "avgResponseTime", "stdResponseTime",
             "avgResponseTimeGo", "stdResponseTimeGo",
             "avgResponseTimeNGo", "stdResponseTimeNGo",
             "avgDistanceGo", "stdDistanceGo", "avgDistanceNGo", "stdDistanceNGo"])
i = 0
img = cv2.imread("..\\Conf\\game_bg.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

for index, row in listFiles.iterrows():
    gameResult = pd.read_csv(os.path.join(filePath, row["id"] + "_gameResults.csv"))
    data = pd.read_csv(os.path.join(filePath, row["id"] + "_gazeHeadPose.csv"))
    gaze = data[(data.Time > 0) & (data.GazeX >= 0) & (data.GazeY >= 0) & (data.GazeX <= 1) & (data.GazeY <= 1)][
        ["Time", "GazeX", "GazeY"]]
    # filteredGaze = gaze.groupby(gaze.Time.values // 0.01).mean()

    filteredGaze = gaze
    # polyArea = areaPolyImage(filteredGaze.GazeX.values, filteredGaze.GazeY.values, os.path.join(resultPath, row["id"] + yokoOrHiro + "p.png"))
    polyArea = convexHullArea(filteredGaze[["GazeX", "GazeY"]].values)
    result.loc[i] = [row["id"] + yokoOrHiro, row["sex"], polyArea, np.average(gameResult.PosResponse),
                     np.average(gameResult.NegResponse), np.average(gameResult.MissResponse),
                     np.average(gameResult[(gameResult.DiffTime > 0)].DiffTime.values),
                     np.std(gameResult[(gameResult.DiffTime > 0)].DiffTime.values),
                     np.average(gameResult[(gameResult.DiffTime >= 0) & (gameResult.PosResponse == 1)].DiffTime.values),
                     np.std(gameResult[(gameResult.DiffTime >= 0) & (gameResult.PosResponse == 1)].DiffTime.values),
                     np.average(gameResult[(gameResult.DiffTime >= 0) & (gameResult.NegResponse == 1)].DiffTime.values),
                     np.std(gameResult[(gameResult.DiffTime >= 0) & (gameResult.NegResponse == 1)].DiffTime.values),
                     np.average(gameResult[(gameResult.Distance >= 0) & (gameResult.PosResponse == 1) & (
                             gameResult.ResponseTime >= 0)].Distance.values),
                     np.std(gameResult[(gameResult.Distance >= 0) & (gameResult.PosResponse == 1) & (
                             gameResult.ResponseTime >= 0)].Distance.values),
                     np.average(gameResult[(gameResult.Distance >= 0) & (gameResult.NegResponse == 1) & (
                             gameResult.ResponseTime >= 0)].Distance.values),
                     np.std(gameResult[(gameResult.Distance >= 0) & (gameResult.NegResponse == 1) & (
                             gameResult.ResponseTime >= 0)].Distance.values),

                     ]
    i += 1

result.to_csv(os.path.join(resultPath, "summary" + yokoOrHiro + ".csv"))

# plotting trajectory result
# _old means using average of 300 ms
# hiroData = pd.read_csv(os.path.join(resultPath, "summary_hiro.csv"))
# yokoData = pd.read_csv(os.path.join(resultPath, "summary_yoko.csv"))
# result = pd.concat([hiroData, yokoData])
#
# # result = pd.read_csv(os.path.join(resultPath, "summary.csv"))
#
# result = result.fillna(0)
# polyArea = result.polyArea.values
# print(np.mean(polyArea))
# positivePer = result.positivePer.values
# negativePer = result.negativePer.values
# missPer = result.missPer.values
# avgResponseTime = result.avgResponseTime.values
# numOfSubj = len(polyArea)
# polyAreaF = result[result.sex == "F"].polyArea.values
# polyAreaM = result[result.sex == "M"].polyArea.values
# print(str(np.average(polyAreaM)) + "," + str(np.std(polyAreaM)))
# print(str(np.average(polyAreaF))+ "," + str(np.std(polyAreaF)))
#
# # #negative by sex
# negativePerF = result[result.sex == "F"].negativePer.values * 100
# negativePerM = result[result.sex == "M"].negativePer.values * 100
#
# #response by sex
# avgResponseTimeF = result[result.sex == "F"].avgResponseTime.values
# avgResponseTimeM = result[result.sex == "M"].avgResponseTime.values
#
# plt.bar(np.arange(1, len(polyArea)+1), polyArea)
# plt.show()
#
#
# plt.boxplot(polyArea, showmeans=True, showbox=True, notch=True)
# plt.ylabel("Poly Area")
# plt.savefig(os.path.join(summaryPath, "averagePolyArea.png"))
# plt.show()
#
# plt.pie(labels=["area<=0.16", "0.15>area<=0.35", "area>0.35"], x=[np.sum(polyArea<=0.162121095)/numOfSubj, np.sum((polyArea>0.162121095) & (polyArea<=0.35))/numOfSubj, np.sum(polyArea>0.35)/numOfSubj], autopct='%1.1f%%')
# plt.savefig(os.path.join(summaryPath, "summaryPolyArea.png"))
# plt.show()
#
# plt.boxplot(labels=["Female", "Men"], x = [polyAreaF, polyAreaM], showmeans=True)
# plt.ylabel("Poly Area")
# plt.savefig(os.path.join(summaryPath, "polyAreaBySex.png"))
# plt.show()
#
#
# plt.boxplot(labels=["Female", "Men"], x = [negativePerF, negativePerM], showmeans=True)
# plt.ylabel("Percentage of False Alarm (%)")
# plt.savefig(os.path.join(summaryPath, "falseAlarmBySex.png"))
# plt.show()
#
# plt.boxplot(labels=["Female", "Men"], x = [avgResponseTimeF * 1000, avgResponseTimeM * 1000], showmeans=True)
# plt.ylabel("Response Time (ms)")
# plt.savefig(os.path.join(summaryPath, "responseTimeBySex.png"))
# plt.show()


# summary
# result.polyArea = result.polyArea
# print("----------------------------------------Trajectory --------------------------------------")
# print(np.average(result[result.sex.values == "M"].polyArea))
# print(np.std(result[result.sex.values == "M"].polyArea))
# print(np.average(result[result.sex.values == "F"].polyArea))
# print(np.std(result[result.sex.values == "F"].polyArea))
# print("----------------------------------------Reaction Time  --------------------------------------")
# print(np.average(result.avgResponseTime) * 1000)
# print(np.std(result.avgResponseTime)* 1000)
# print(np.average(result[result.sex.values == "M"].avgResponseTime)* 1000)
# print(np.std(result[result.sex.values == "M"].avgResponseTime)* 1000)
# print(np.average(result[result.sex.values == "F"].avgResponseTime)* 1000)
# print(np.std(result[result.sex.values == "F"].avgResponseTime)* 1000)
# print("----------------------------------------Reaction Time  Var--------------------------------------")
# print(np.average(result.stdResponseTime) * 1000)
# print(np.std(result.stdResponseTime)* 1000)
# print(np.average(result[result.sex.values == "M"].stdResponseTime)* 1000)
# print(np.std(result[result.sex.values == "M"].stdResponseTime)* 1000)
# print(np.average(result[result.sex.values == "F"].stdResponseTime)* 1000)
# print(np.std(result[result.sex.values == "F"].stdResponseTime)* 1000)
# print("----------------------------------------Reaction Time Var Go --------------------------------------")
# print(np.average(result.stdResponseTimeGo) * 1000)
# print(np.std(result.stdResponseTimeGo)* 1000)
# print(np.average(result[result.sex.values == "M"].stdResponseTimeGo)* 1000)
# print(np.std(result[result.sex.values == "M"].stdResponseTimeGo)* 1000)
# print(np.average(result[result.sex.values == "F"].stdResponseTimeGo)* 1000)
# print(np.std(result[result.sex.values == "F"].stdResponseTimeGo)* 1000)
# print("----------------------------------------Reaction Time Var NoGo --------------------------------------")
# print(np.average(result[result.stdResponseTimeNGo != 0].stdResponseTimeNGo)* 1000)
# print(np.std(result[result.stdResponseTimeNGo != 0].stdResponseTimeNGo)* 1000)
# print(np.average(result[(result.sex.values == "M") & (result.stdResponseTimeNGo != 0)].stdResponseTimeNGo)* 1000)
# print(np.std(result[(result.sex.values == "M") & (result.stdResponseTimeNGo != 0)].stdResponseTimeNGo)* 1000)
# print(np.average(result[(result.sex.values == "F") & (result.stdResponseTimeNGo != 0)].stdResponseTimeNGo)* 1000)
# print(np.std(result[(result.sex.values == "F")&  (result.stdResponseTimeNGo != 0)].stdResponseTimeNGo)* 1000)
# pearson coefficient

# # response perc - trajectory are
# rp_t = stats.linregress(result.polyArea.values, result.positivePer.values * 100 )
# rp_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].positivePer* 100 )
# rp_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].positivePer* 100 )
#
# #ERROR-Go
# rpM_t = stats.linregress(result.polyArea.values, result.missPer.values* 100 )
# rpM_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].missPer* 100 )
# rpM_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].missPer* 100 )
#
# #ERROR-NoGo
# rpN_t = stats.linregress(result.polyArea.values,  result.negativePer.values* 100 )
# rpN_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].negativePer* 100 )
# rpN_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].negativePer* 100 )
#
#
# #response time - trajectory are
#
# rtA_t = stats.linregress(result.polyArea.values, result.avgResponseTime.values * 1000)
# rtA_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].avgResponseTime* 1000)
# rtA_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].avgResponseTime* 1000)
# #Plotting
# plt.figure(0)
# plt.plot(result.polyArea.values, result.avgResponseTime.values* 1000 , 'o', label='original data')
# plt.plot(result.polyArea.values, rtA_t.intercept +  (rtA_t.slope * result.polyArea.values) , 'r', label='fitted line')
# plt.xlabel("Trajectory Area")
# plt.ylabel("Average RT")
# plt.show()
#
# #GO
# rt_t = stats.linregress(result.polyArea.values, result.avgResponseTimeGo.values* 1000)
# rt_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].avgResponseTimeGo* 1000)
# rt_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].avgResponseTimeGo* 1000)
#
# #NoGO
# rtN_t = stats.linregress(result.polyArea.values, result.avgResponseTimeNGo.values* 1000)
# rtN_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].avgResponseTimeNGo* 1000)
# rtN_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].avgResponseTimeNGo* 1000)
#
#
# #response time Var - trajectory are
# rvA_t = stats.linregress(result.polyArea.values, result.stdResponseTime.values* 1000)
# rvA_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].stdResponseTime* 1000)
# rvA_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].stdResponseTime* 1000)
# #Plotting
# plt.figure(0)
# plt.plot(result.polyArea.values, result.stdResponseTime.values* 1000 , 'o', label='original data')
# plt.plot(result.polyArea.values, rvA_t.intercept +  (rvA_t.slope * result.polyArea.values) , 'r', label='fitted line')
# plt.xlabel("Trajectory Area")
# plt.ylabel("Average RT Var")
# plt.show()
#
# #GO
# rv_t = stats.linregress(result.polyArea.values, result.stdResponseTimeGo.values* 1000)
# rv_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].stdResponseTimeGo* 1000)
# rv_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].stdResponseTimeGo* 1000)
#
# #NoGO
# rvN_t = stats.linregress(result.polyArea.values, result.stdResponseTimeNGo.values* 1000)
# rvN_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].stdResponseTimeNGo* 1000)
# rvN_tF = stats.linregress(result[result.sex.values == "F"].stdResponseTimeNGo, result[result.sex.values == "F"].polyArea* 1000)



#distance objects - trajectory are
#GO
# do_t = stats.linregress(result.polyArea.values, result.avgDistancesObjGo.values)
# do_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].avgDistancesObjGo)
# do_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].avgDistancesObjGo)
#
# #NoGO
# doN_t = stats.linregress(result.polyArea.values, result.avgDistancesObjNGo.values)
# doN_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].avgDistancesObjNGo)
# doN_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].avgDistancesObjNGo)

# #distance - trajectory are
# #GO
# d_t = stats.linregress(result.polyArea.values, result.avgDistanceGo.values)
# d_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].avgDistanceGo)
# d_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].avgDistanceGo)
#
# #NoGO
# dN_t = stats.linregress(result.polyArea.values, result.avgDistanceNGo.values)
# dN_tM = stats.linregress(result[(result.avgDistanceNGo != 0) & (result.sex.values == "M")].polyArea, result[(result.avgDistanceNGo != 0) & (result.sex.values == "M")].avgDistanceNGo)
# dN_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].avgDistanceNGo)
#
# #stddistance - trajectory are
# #GO
# s_d_t = stats.linregress(result.polyArea.values, result.stdDistanceGo.values)
# s_d_tM = stats.linregress(result[result.sex.values == "M"].polyArea, result[result.sex.values == "M"].stdDistanceGo)
# s_d_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].stdDistanceGo)
#
# #NoGO
# s_dN_t = stats.linregress(result.polyArea.values, result.stdDistanceNGo.values)
# s_dN_tM = stats.linregress(result[(result.avgDistanceNGo != 0) & (result.sex.values == "M")].polyArea, result[(result.avgDistanceNGo != 0) & (result.sex.values == "M")].stdDistanceNGo)
# s_dN_tF = stats.linregress(result[result.sex.values == "F"].polyArea, result[result.sex.values == "F"].stdDistanceNGo)
#
#
#
# #distance - RTVar
# #GO
# goCondition = (result.avgResponseTimeGo != -1) & (result.avgDistanceGo != -1)
# d_rv = stats.linregress(result[goCondition].avgResponseTimeGo.values, result[goCondition].avgDistanceGo.values)
# d_rvM = stats.linregress(result[goCondition & (result.sex.values == "M")].avgResponseTimeGo, result[goCondition & (result.sex.values == "M")].avgDistanceGo)
# d_rvF = stats.linregress(result[goCondition & (result.sex.values == "F")].avgResponseTimeGo, result[goCondition & (result.sex.values == "F")].avgDistanceGo)
#
# #NoGO
# nGoCondition = (result.avgResponseTimeNGo != -1) & (result.avgDistanceNGo != -1)
# dN_rv = stats.linregress(result[nGoCondition].avgResponseTimeNGo.values, result[nGoCondition].avgDistanceNGo.values)
# dN_rvM = stats.linregress(result[nGoCondition & (result.sex.values == "M")].avgResponseTimeNGo, result[nGoCondition & (result.sex.values == "M")].avgDistanceNGo)
# dN_rvF = stats.linregress(result[nGoCondition & (result.sex.values == "F")].avgResponseTimeNGo, result[nGoCondition & (result.sex.values == "F")].avgDistanceNGo)
#
#
# print("---------------------------------Trajectory Area-----------------------")
# print("----------------------------Go--------------------------------------")
# print(rp_t)
# print(rp_tM)
# print(rp_tF)
# print("----------------------------Error-Go--------------------------------------")
# print(rpM_t)
# print(rpM_tM)
# print(rpM_tF)
# print("----------------------------Error-NoGo--------------------------------------")
# print(rpN_t)
# print(rpN_tM)
# print(rpN_tF)
# print("----------------------------RT--------------------------------------")
# print(rtA_t)
# print(rtA_tM)
# print(rtA_tF)
# print("----------------------------RT-Go--------------------------------------")
# print(rt_t)
# print(rt_tM)
# print(rt_tF)
# print("----------------------------RT-NoGo--------------------------------------")
# print(rtN_t)
# print(rtN_tM)
# print(rtN_tF)
# print("----------------------------RTVar--------------------------------------")
# print(rvA_t)
# print(rvA_tM)
# print(rvA_tF)
# print("----------------------------RTVar-Go--------------------------------------")
# print(rv_t)
# print(rv_tM)
# print(rv_tF)
# print("----------------------------RTVar-NoGo--------------------------------------")
# print(rvN_t)
# print(rvN_tM)
# print(rvN_tF)
# print("----------------------------AVGDistance-Go--------------------------------------")
# print(d_t)
# print(d_tM)
# print(d_tF)
# print("----------------------------AVGDistance-NoGo--------------------------------------")
# print(dN_t)
# print(dN_tM)
# print(dN_tF)
# print("----------------------------STDDistance-Go--------------------------------------")
# print(s_d_t)
# print(s_d_tM)
# print(s_d_tF)
# print("----------------------------STDDistance-NoGo--------------------------------------")
# print(s_dN_t)
# print(s_dN_tM)
# print(s_dN_tF)
#
# print("----------------------------Distance--------------------------------------")
#
#
# print("----------------------------RT-Go--------------------------------------")
# print(d_rv)
# print(d_rvM)
# print(d_rvF)
# print("----------------------------RT-NoGo--------------------------------------")
# print(dN_rv)
# print(dN_rvM)
# print(dN_rvF)



# print("----------------------------DistanceOBJ-Go--------------------------------------")
# print(do_t)
# print(do_tM)
# print(do_tF)
# print("----------------------------DistanceOBJ-NoGo--------------------------------------")
# print(doN_t)
# print(doN_tM)
# print(doN_tF)

# plotPoly(positivePer, polyArea, "Correct")
#
#
# plotPoly(negativePer, polyArea, "Incorrect")
#
#
# plotPoly(missPer, polyArea, "Miss")
#
# plt.legend()
# plt.savefig(os.path.join(summaryPath, "responseXpolyArea.png"))
# plt.show()
# #trajectory with avg response time
# plt.figure(2)
#
# plt.scatter(polyArea, avgResponseTime*1000)
# plt.ylim(0, 1000)
# plt.xlim(0, 2)
# plt.ylabel("Average Response Time (ms)")
# plt.xlabel("Trajectory Area")
#
# plt.show()
