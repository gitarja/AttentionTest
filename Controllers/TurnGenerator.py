import numpy as np
import pandas as pd
from datetime import datetime
import os
import math

class TurnGenerator:


    def generate(self, percentage, totalTime, maxTime, minTime, appearanceTime):
        '''
        :param percentage: percentage of chicken prob
        :param totalTime: total time of evaluation value
        :param maxTime: max time of an object to appear
        :param minTime: min time of an object to appear
        :return: the path of turn file that will be send to game
        half of total time consists of object with maxTime and the other half consists of object with minTime
        '''

        #the path of generated file
        filePath = os.getcwd() + "\\TurnsFiles\\Turns.csv"
        halfTime = math.floor((totalTime * 60) / 2)

        #turn with maxTime
        numTurn = math.floor(halfTime / maxTime)
        chickenTurnNum = int(numTurn *   percentage)
        maxProbTurns = np.ones((int(numTurn), 3))
        maxProbTurns[:, 1] =  maxProbTurns[:, 1]  * maxTime
        maxProbTurns[:, 2] = maxProbTurns[:, 2] * appearanceTime
        maxProbTurns[:chickenTurnNum, 0] = maxProbTurns[:chickenTurnNum, 0] - 1

        # turn with minTime
        numTurn = math.floor(halfTime / minTime)
        chickenTurnNum = int(numTurn * percentage)
        minProbTurns = np.ones((int(numTurn), 3))
        minProbTurns[:, 1] = minProbTurns[:, 1] * minTime
        minProbTurns[:, 2] = minProbTurns[:, 2] * appearanceTime
        minProbTurns[:chickenTurnNum, 0] = minProbTurns[:chickenTurnNum, 0] - 1

        turns = np.concatenate([maxProbTurns, minProbTurns])

        turnsData = pd.DataFrame({"Character": turns[:, 0].astype(int), "Sleep": turns[:, 1], "Appearance": turns[:, 2], "IndexPost": np.ones(len(turns)).astype(int)}, columns=["Character", "Sleep", "Appearance", "IndexPost"])

        #set the location of objects uniformly

        #GoResponse
        turnsData.loc[turnsData.Character == 0, "IndexPost"] = np.arange(len(turnsData.loc[turnsData.Character == 0])).astype(int)
        turnsData.loc[turnsData.Character == 1, "IndexPost"] = np.arange(len(turnsData.loc[turnsData.Character == 1])).astype(int)

        #shuffle the position of data
        randomData = turnsData.sample(frac=1.0)
        #save the turns file
        randomData.to_csv(filePath, index=False)

        return filePath
