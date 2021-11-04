import os
import glob
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

path = 'D:\\usr\\pras\\data\\AttentionTestData\\processed'
gazeHeadpath = 'D:\\usr\\pras\\data\\AttentionTestData\\gazeHead'
extension = 'csv'
os.chdir(path)
files = glob.glob('*.{}'.format(extension))
delay = 1.0
fs = 90.0
vlows = []
lows = []
highs = []
lhs = []
for file in files:
    # data = pd.read_csv(os.path.join(path, file))
    num = file.split(".")[0].split("_")
    gazeHeadFile = os.path.join(gazeHeadpath, "AT_" + num[1].rjust(6, '0') + "_gazeHeadPose.csv")
    if os.path.exists(gazeHeadFile):
        data = pd.read_csv(os.path.join(path, file))
        filteredDataNeg = data.loc[
            (data.PosResponse == 1) & (data.ResponseTime != -1) & (data.Distance > 0) & (
                    data.DiffTime > 0)]
        gazeHeadData = pd.read_csv(gazeHeadFile)
        #print(gazeHeadFile)
        if len(filteredDataNeg > 0):
            responseTimes = filteredDataNeg.ResponseTime.values
            for responseTime in responseTimes:
                gaze = gazeHeadData.loc[(gazeHeadData.Time >= responseTime - delay) & (gazeHeadData.Time < responseTime)]
                gaze = gaze[["GazeX", "GazeY"]].values
                if len(gaze) > 30:
                    gazeNorm = np.sqrt(np.sum(np.power(gaze, 2), -1))
                    #print(responseTime)
                    psd = np.abs(np.fft.fft(gazeNorm)) ** 2
                    freq = np.fft.fftfreq(len(psd), 1 / fs)
                    vLowIdx = (freq > 0.9) & (freq < 4.5)
                    lowIdx = (freq > 4.5) & (freq < 13.5)
                    highIdx = (freq > 13.5) & (freq < 45)

                    vLow = np.sum(psd[vLowIdx])
                    low = np.sum(psd[lowIdx])
                    high = np.sum(psd[highIdx])
                    lh = low/high

                    vlows.append(vLow)
                    lows.append(low)
                    highs.append(high)
                    lhs.append(lh)

vlows = np.array(vlows)
lows = np.array(lows)
highs = np.array(highs)
lhs = np.array(lhs)
print("Vlow Mean = %f and Vlow STD = %f", (np.average(vlows), np.std(vlows)))
print("low Mean = %f and low STD = %f", (np.average(lows), np.std(lows)))
print("high Mean = %f and high STD = %f", (np.average(highs), np.std(highs)))
print("lh Mean = %f and lh STD = %f", (np.average(lhs), np.std(lhs)))
#
# samp = 1
# freq = 90.0 / samp
#
# data = pd.read_csv(os.path.join(path, "AT_000030_gazeHeadPose.csv"))
#
# filteredData = data.loc[(data.Time > 0) & (data.GazeX >= 0) & (data.GazeY >= 0)]
# filteredData = filteredData[filteredData.index % samp == 0]
#
# xBefore = filteredData[["GazeX", "GazeY"]].values[:-1]
# xAfter = filteredData[["GazeX", "GazeY"]].values[1:]
# x = np.sqrt(np.sum(np.power(xAfter - xBefore, 2), -1))
# xNorm = np.sqrt(np.sum(np.power(filteredData[["GazeX", "GazeY"]].values, 2), -1))
# N = len(x)
#
# #gaze x
# sp = np.fft.fft(xNorm)
# sp[0] = 0
# psd = 1 / (N * freq) * np.abs(sp) ** 2
# f = np.fft.fftfreq(len(psd), 1/freq)
# i = f > 0
# plt.semilogy(f[i], psd[i])
#
# # #gaze y
# # sp = np.fft.fft(x[:, 1])
# # sp[0] = 0
# # psd =  1 / (N * freq) * np.abs(sp) ** 2
# # f = np.fft.fftfreq(len(psd), 1/freq)
# # i = f > 0
# # plt.plot(f[i], psd[i])
#
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('PSD (dB)')
# plt.show()
