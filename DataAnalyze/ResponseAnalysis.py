import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
from Controllers.DataProcessor import DataProcessor
import seaborn as sns
import cv2
import numpy as np
import matplotlib
# matplotlib.use('Agg')
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

sns.set()


def areaPolyImage(x, y, impath=None):
    # max area (480, 640)
    maxArea = 306081.0
    fig, ax = plt.subplots(nrows=1, ncols=1)
    # ax.plot(x, y, c="black")
    ax.scatter(x, y, c="black", s=50)
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
    # print(len(contours))
    # print(len(contours))
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    # (x, y), (MA, ma), angle = cv2.fitEllipse(cnts[0])
    # im2 = cv2.ellipse(img, ellipse, (0, 255, 0), 2)

    # areaE = np.pi * MA * ma
    # print(len(cnts))
    area = (cv2.contourArea(cnts[0]) + cv2.contourArea(cnts[1]) + cv2.contourArea(cnts[2])) / maxArea
    # print(area)
    return area

def convexHullArea(data):
    hull = ConvexHull(points=data)
    return hull.volume
def PolyArea2D(pts):
    lines = np.hstack([pts,np.roll(pts,-1,axis=0)])
    area = 0.5*abs(sum(x1*y2-x2*y1 for x1,y1,x2,y2 in lines))
    return area
def plotGazeObject(data, filename):
    '''
    :param figure: the plotting figure
    :param canvas: the canvas where the figure is attached into
    The player's gaze position and object position
    '''

    # Open game background
    img = cv2.imread("D:\\usr\\pras\\project\\PyhtonProject\\AttentionTest\\Conf\\game_bg.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    major_ticks = np.arange(0, 1, 0.2)
    fig, ax = plt.subplots(frameon=False)
    ax.imshow(img, extent=[0, 1, 0, 1])
    # ax.plot(self.gazeObject[0], self.gazeObject[1], '-o', label="Object", alpha=0.5, color="green")
    # ax.plot(data[:, 0], data[:, 1], '-', label="Gaze", color="yellow")
    ax.scatter(data[:, 0], data[:, 1], c="yellow", marker = "x")

    # ax.set_xlabel("X")
    # ax.set_ylabel("Y")
    ax.set_xlim([0.0, 1.0])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_ylim([0.0, 1.0])
    ax.set_xticks(major_ticks)
    ax.set_yticks(major_ticks)
    # And a corresponding grid
    ax.yaxis.grid(True, which='major')
    ax.xaxis.grid(True, which='major')
    plt.tight_layout()

    plt.savefig(filename, bbox_inches='tight', pad_inches=0)


# path = "D:\\usr\\pras\\data\\AttentionTestData\\Yokodai\\AttentionTest\\result\\"
# path = 'D:\\usr\\pras\\data\\AttentionTestData\\Hiroshima\\result\\'
# path = "D:\\usr\\pras\\data\\AttentionTestData\\DisorderedChildren\\"
path = "D:\\usr\\pras\\data\\AttentionTestData\\Hoikuen(2020-01-24)\\results\\"
extension = '_gameResults.csv'
os.chdir(path)
files = glob.glob('*{}'.format(extension))

process = DataProcessor()
# columns = ["id", "RT1", "RT2", "RT3", "RT4", "RT5", "RT6", "RT7", "RT8", "RT9", "RT10", "RTVar1", "RTVar2", "RTVar3",
#              "RTVar4", "RTVar5", "RTVar6", "RTVar7", "RTVar8", "RTVar9", "RTVar10"]

columns = ["id", "Go", "GoError", "NoGoError", "RT1", "RT2", "RT3", "RT4", "RTVar1", "RTVar2", "RTVar3", "RTVar4", "RT", "RTVar","Trajectory Area"]

# columns = ["id", "Go", "GoError", "NoGoError", "RT1", "RT2", "RT3", "RTVar1", "RTVar2", "RTVar3",  "Trajectory Area"]
data = pd.DataFrame(columns=columns)
i = 0
for file in files:
    filePath = os.path.join(path, file)
    gazeData = pd.read_csv(filePath.replace("_gameResults.csv", "_gazeHeadPose.csv"))
    gazeData = gazeData.fillna(0)
    gazeData = gazeData[(gazeData.Time > 1) & (gazeData.GazeX >= 0) & (gazeData.GazeY >= 0)]
    plotGazeObject(gazeData[["GazeX", "GazeY"]].values, file.split("_gameResults")[0]+".png")
    gazeData = gazeData.groupby(gazeData.Time // 0.005).mean()
    area = convexHullArea(gazeData[["GazeX", "GazeY"]].values)
    print(area)
    process.ProceedGameResult(gameResultPath=filePath)
    RT = process.computeResponseTimeGroup(process.response).transpose().flatten()
    RTAVG, RTVarAVG = np.mean(process.response.DiffTime[process.response.DiffTime>=0]), np.std(process.response.DiffTime[process.response.DiffTime>=0])

    #Save response time
    RTseries = pd.DataFrame({"Time": process.goodResponse["SpawnTime"].values, "RT": process.goodResponse["ResponseTime"].values - process.goodResponse["SpawnTime"].values})
    RTseries.to_csv(file.split("_gameResults")[0]+"_RTSeries.csv")

    # print("#--------------------------------------------------------------------------#")
    # print(process.averageGoodResponseTime())
    # print(process.averageNegResponseTime())
    # print("#--------------------------------------------------------------------------#")
    # print(RT)
    # data = data.append({"id": file.split("_gameResults")[0]+"_hiro", "RT1": RT[0], "RT2": RT[1], "RT3": RT[2], "RT4": RT[3], "RT5": RT[4],
    #                "RT6": RT[5], "RT7": RT[6], "RT8": RT[7], "RT9": RT[8], "RT10": RT[9], "RTVar1": RT[10],
    #                "RTVar2": RT[11], "RTVar3": RT[12],
    #                "RTVar4": RT[13], "RTVar5": RT[14], "RTVar6": RT[15], "RTVar7": RT[16], "RTVar8": RT[17],
    #                "RTVar9": RT[18], "RTVar10": RT[19]}, ignore_index=True)
    if len(RT) > 2:
        data = data.append(
            {"id": file.split("_gameResults")[0] + "_hiro",  "Go": process.response.PosResponse.mean(),  "GoError": process.response.MissResponse.mean(),
             "NoGoError": process.response.NegResponse.mean(), "RT1": RT[0], "RT2": RT[1], "RT3": RT[2], "RT4": RT[3],
             "RTVar1": RT[4],
             "RTVar2": RT[5], "RTVar3": RT[6],  "RTVar4": RT[7], "RT":RTAVG, "RTVar": RTVarAVG,

             "Trajectory Area": area}, ignore_index=True)

        # data = data.append(
        #     {"id": file.split("_gameResults")[0] + "_hiro",  "Go": process.response.PosResponse.mean(),  "GoError": process.response.MissResponse.mean(),
        #      "NoGoError": process.response.NegResponse.mean(), "RT1": RT[0], "RT2": RT[1], "RT3": RT[2],
        #      "RTVar1": RT[3],
        #      "RTVar2": RT[4], "RTVar3": RT[5],  "Trajectory Area": area}, ignore_index=True)

        i += 1

data.to_csv(os.path.join(path, "summary_response_new.csv"), columns=columns)
