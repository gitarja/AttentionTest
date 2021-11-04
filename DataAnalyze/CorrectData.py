from sklearn.cluster import KMeans
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = 'D:\\usr\\pras\\data\\AttentionTestData\\processed\\incomplete'
correctedPath = 'D:\\usr\\pras\\data\\AttentionTestData\\processed'
extension = 'csv'
os.chdir(path)
files = glob.glob('*.{}'.format(extension))

dataAll = []

rep = np.array([[0.2514444,0.3542949,-0.00354167,0.00241799],
[0.5085708,0.3542949,-0.00151042,0.00241799],
[0.765749,0.3544508,0.00052083,0.00241799],
[0.2995009,0.6284335,-0.00354167,0.00245983],
[0.5069138,0.6284335,-0.00151042,0.00245983],
[0.7143266,0.6284335,0.00052083,0.00245983],
[0.3332066,0.8204052,-0.00354167,0.00249804],
[0.5057507,0.8202399,-0.00151042,0.00249804],
[0.6782964,0.8204052,0.00052083,0.00249804]])

falseLoc = rep[:, 2:4]
trueLoc = rep[:, 0:2]
for file in files:
    data = pd.read_csv(os.path.join(path, file))
    dataMiss = data.loc[(data.ResponseTime == -1)| (data.MissResponse == 1)]
    uniqueX = np.unique(dataMiss.ObjectX.values)
    uniqueY = np.unique(dataMiss.ObjectY.values)
    #print(uniqueX)
    for i  in range(len(uniqueX)):
        for j in range(len(uniqueY)):
            currLoc = np.array([uniqueX[i], uniqueY[j]])
            distances = np.average(np.sqrt((falseLoc - currLoc) ** 2), axis=1)
            idx = np.argmin(distances)
            #print(idx)
            data.loc[(data.ObjectX == uniqueX[i]) & (data.ObjectY == uniqueY[j]), ["ObjectX", "ObjectY"]] = trueLoc[idx]
    data.to_csv(correctedPath+"\\corrected_"+file)