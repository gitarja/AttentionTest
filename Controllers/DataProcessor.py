import pandas as pd
import numpy as np
from Utils.Lib import computeResponseTime, bernouliSTD, convexHullArea, euclidianDist, filterFixation, spectralEntropy, gazeEntropy, removeNoObjectData, euclidianDistT, anglesEstimation
from scipy.signal._savitzky_golay import savgol_filter
from Conf.Setting import AVG_WIN_SIZE, AREA_FIX_TH, CUT_OFF, FREQ_SAMP, FREQ_GAZE
from Utils.OutliersRemoval import OutliersRemoval
# from nolds import sampen

class DataProcessor:


    def ProceedGameResult(self, gameResultPath=None, gazeHeadPath=None):
        '''
        :param gameResultPath: the path of game results
        :param gazeHeadPath: the path of gaze and head tracking results
        :return:
        '''
        startTime = 0
        if (gameResultPath is not None):
            self.gameData = pd.read_csv(gameResultPath)
            self.gameData = self.gameData.fillna(0)

            # proceed data, remove the first one minute data
            self.processedData = self.gameData.loc[(self.gameData.SpawnTime >= 0)].reset_index(drop=True)
            # self.processedData.SpawnTime = self.processedData.SpawnTime - startTime
            # self.processedData.ResponseTime = self.processedData.ResponseTime - startTime
            #normalize the spawn time so it starts from zero
            startTime = self.gameData.SpawnTime[0]
            self.gameData.SpawnTime = self.gameData.SpawnTime - startTime
            self.gameData.loc[self.gameData.ResponseTime != -1, "ResponseTime"] = self.gameData.ResponseTime.loc[self.gameData.ResponseTime!=-1] - startTime
            #good response: data with response time and pos response = 1
            self.goodResponse = self.gameData.loc[(self.gameData.PosResponse == 1) & (self.gameData.ResponseTime != -1.0)]
            #neg response: data with response time and neg response = 1
            self.negResponse = self.gameData.loc[(self.gameData.NegResponse == 1) & (self.gameData.ResponseTime != -1.0)]
            #miss response: data with response time and miss response = 1
            self.missResponse = self.gameData.loc[(self.gameData.MissResponse == 1) & (self.gameData.ResponseTime != -1.0)]
            #reponse data with response = 1
            self.response = self.gameData.loc[self.gameData.ResponseTime != -1.0]
            #group response spawntime for every minute
            self.groupConsRes = np.floor(self.response.SpawnTime // 61).astype(int)
            #group data spawntime for every minute
            self.groupCons = np.floor(self.gameData.SpawnTime // 61).astype(int)


            #proceed data
            self.processedGoodResponse = self.processedData.loc[(self.processedData.PosResponse == 1) & (self.processedData.ResponseTime != -1.0)]
            self.processedNegResponse = self.processedData.loc[(self.processedData.NegResponse == 1) & (self.processedData.ResponseTime != -1.0)]
            self.processedMissResponse = self.processedData.loc[(self.processedData.MissResponse == 1) & (self.processedData.ResponseTime != -1.0)]
            self.processedResponse = self.processedData.loc[self.processedData.ResponseTime != -1.0]



        if (gazeHeadPath is not None):
            normalize_col = ["ObjectX", "ObjectY"]
            gazeData = pd.read_csv(gazeHeadPath)
            gazeData = gazeData.fillna(0)
            gazeData = gazeData[gazeData.Time >= startTime]
            gazeData.Time = gazeData.Time - startTime
            # gazeData_down = gazeData.loc[gazeData.index % 2 == 1] #downsample from 144 to 72
            gazeData_down = gazeData.loc[np.floor(gazeData.index % FREQ_SAMP /FREQ_GAZE).astype(int) == 1] #downsample from 100 to 72
            gazeData_avg = pd.DataFrame(columns=gazeData_down.columns.values)
            gazeData_down = gazeData_down[(gazeData_down.GazeX >= 0) & (gazeData_down.GazeY >= 0)]
            for col in gazeData_down:
                if col in normalize_col:
                    gazeData_avg[col] = gazeData_down[col].values
                else:
                    gazeData_avg[col] = savgol_filter(gazeData_down[col].values, AVG_WIN_SIZE, polyorder=3)

            removed_idx = (gazeData_avg["ObjectX"].values < 0.1) | (gazeData_avg["ObjectY"].values < 0.1)
            gazeData_avg["ObjectX"].loc[removed_idx] = -1
            gazeData_avg["ObjectY"].loc[removed_idx] = -1
            self.gazeData = gazeData_avg





    def averageResponseTimes(self, mode=1):
        '''
        :param mode: 1 for using unprocessed data, 2 otherwise
        :return: [avg response time, std response time, compute overall avg and std of response time]
        '''
        if mode == 1:
            response = self.response
        elif mode == 2:
            response = self.processedResponse
        avgTime, stdTime = computeResponseTime(spawnTime=response.SpawnTime, responseTime=response.ResponseTime)
        return [avgTime, stdTime], self.computeResponseTimeNS(self.response)

    def averageGoodResponseTime(self, mode=1):
        """
        :param mode: 1 for using unprocessed data, 2 otherwise
        :return:
        """
        if mode==1:
            dataGame = self.gameData
            goodResponse = self.goodResponse
        elif mode == 2:
            dataGame = self.processedData
            goodResponse = self.processedGoodResponse
        #overall avg and std positif response
        avg = dataGame.PosResponse.mean()
        # compute variance of the response using bernouli
        std = bernouliSTD(dataGame.PosResponse)

        #compute avg and std response time of positif response
        avgTime, stdTime = computeResponseTime(spawnTime=goodResponse.SpawnTime,
                                                    responseTime=goodResponse.ResponseTime)
        #compute avg and std positif response for each minute
        avgTimes = self.gameData.PosResponse.groupby(self.groupCons).mean().values.reshape(-1, 1)
        #stdTimes = self.gameData.PosResponse.groupby(self.groupCons).std().values.reshape(-1, 1)
        stdTimes = self.gameData.PosResponse.groupby(self.groupCons).apply(bernouliSTD).values.reshape(-1, 1)

        return [avg, std, avgTime, stdTime], [avgTimes, stdTimes, self.computeResponseTimeGroup(self.goodResponse)]

    def averageNegResponseTime(self, mode=1):
        """
        :param mode: 1 for using unprocessed data, 2 otherwise
        :return:
        """
        if mode == 1:
            dataGame = self.gameData
            negResponse = self.negResponse
        elif mode==2:
            dataGame = self.processedData
            negResponse = self.processedNegResponse

        # overall avg and std negative response
        avg = dataGame.NegResponse.mean()
        # compute variance of the response using bernouli
        std = bernouliSTD(dataGame.NegResponse)

        # compute avg and std response time of negative response
        avgTime, stdTime = computeResponseTime(spawnTime=negResponse.SpawnTime,
                                                    responseTime=negResponse.ResponseTime)

        # compute avg and std negative response for each minute
        avgTimes = self.gameData.NegResponse.groupby(self.groupCons).mean().values.reshape(-1, 1)
        #stdTimes = self.gameData.NegResponse.groupby(self.groupCons).std().values.reshape(-1, 1)
        stdTimes = self.gameData.NegResponse.groupby(self.groupCons).apply(bernouliSTD).values.reshape(-1, 1)


        return [avg, std, avgTime, stdTime], [avgTimes, stdTimes, self.computeResponseTimeGroup(self.negResponse)]


    def averageMissResponseTime(self, mode=1):
        """
        :param mode: 1 for using unprocessed data, 2 otherwise
        :return:
        """
        if mode == 1:
            dataGame = self.gameData
        elif mode == 2:
            dataGame = self.processedData

        # overall avg and std miss response
        avg = dataGame.MissResponse.mean()
        # compute variance of the response using bernouli
        std = bernouliSTD(dataGame.MissResponse)
        # compute avg and std response time of miss response
        avgTimes = self.gameData.MissResponse.groupby(self.groupCons).mean().values.reshape(-1, 1)
        # stdTimes = self.gameData.MissResponse.groupby(self.groupCons).std().values.reshape(-1, 1)
        stdTimes = self.gameData.MissResponse.groupby(self.groupCons).apply(bernouliSTD).values.reshape(-1, 1)


        return [avg, std], [avgTimes, stdTimes]

    def computeResponseTimeGroup(self, response):
        '''
        :param response: response (responseTime, spawnTime)
        :return:
        '''

        responseTimes = (response.ResponseTime - response.SpawnTime)
        responseTimes = responseTimes[responseTimes>=0]
        #group by response times for each one minute and compute their avg and std
        reponseTimesMean = responseTimes.groupby(self.groupConsRes).mean().values.reshape(-1, 1)
        reponseTimesStd = responseTimes.groupby(self.groupConsRes).std().values.reshape(-1, 1)
        #reponseTimesStd = responseTimes.groupby(self.groupConsRes).apply(self.bernouliSTD).values.reshape(-1, 1)


        return np.concatenate([reponseTimesMean, reponseTimesStd], axis=-1)

    def computeResponseTimeNS(self, response):
        responseTimes = (response.ResponseTime - response.SpawnTime)
        groupedResponseTimes = responseTimes.groupby(self.groupCons)

        return groupedResponseTimes



    def computeGazeObject(self):
        #filter out the object and the player's gaze position when he gives correct answer
        data = self.gameData[(self.gameData.ResponseTime >=0) & (self.gameData.GazeX >= 0) & (self.gameData.GazeY >= 0) & (self.gameData.PosResponse == 1)]

        return [data.ObjectX.values.flatten(), data.ObjectY.values.flatten(), data.GazeX.values.flatten(), data.GazeY.values.flatten()]
    def computeGaze(self):
        #filterout the gaze, only the validate ones,
        data = self.gazeData[(self.gazeData.GazeX >= 0) & (self.gazeData.GazeY >= 0)]

        return [data.GazeX.values.flatten(), data.GazeY.values.flatten()]

    def computeGazeArea(self):
        area = convexHullArea(self.gazeData[["Time", "GazeX", "GazeY"]])
        return area

    def computeGazeVTime(self):
        #compute the rotations and movements of head by computing distance between the following data with the previous data

        dataGaze = self.gazeData[["Time", "GazeX", "GazeY"]]

        groupCons = np.floor(dataGaze.Time // 61).astype(int)
        gazeTrajectoryArea = dataGaze.groupby(groupCons).apply(convexHullArea)

        return gazeTrajectoryArea

    def computeHead(self):
        #compute the rotations and movements of head by computing distance between the following data with the previous data

        dataHeadPos = self.gazeData[["Time", "HeadPosX", "HeadPosY", "HeadPosZ"]]
        dataHeadRot = self.gazeData[["Time", "HeadRotX", "HeadRotY", "HeadRotZ"]]
        groupCons = np.floor(dataHeadPos.Time // 1).astype(int)
        # Average the values
        dataHeadPos = dataHeadPos.groupby(groupCons).mean()
        dataHeadRot = dataHeadRot.groupby(groupCons).mean()
        # sampleAfter = (dataHeadPos.index) % 5 == 0
        # sampleBefore = (dataHeadPos.index + 2) % 5 == 0
        dataBeforePos = dataHeadPos.iloc[:-1]
        dataAfterPos = dataHeadPos.iloc[1:]

        dataBeforeRot = dataHeadRot.iloc[:-1]
        dataAfterRot = dataHeadRot.iloc[1:]

        headPosChanges = np.sum(np.sqrt(np.square(dataAfterPos.values - dataBeforePos.values)), axis=-1)

        headRotChanges = np.sum(np.sqrt(np.square(dataAfterRot.values - dataBeforeRot.values)), axis=-1)

        dataHead = pd.DataFrame(
            {"Time": dataHeadPos.Time[1:].values, "HeadPosChange": headPosChanges, "HeadRotChange": headRotChanges})

        #group  by times for each one minute
        groupCons = np.floor(dataHead.Time // 61).astype(int)
        dataHead = dataHead.groupby(groupCons)
        return dataHead

    #----------------------Gaze and Object Processing--------------------------------------#

    def responseGaze(self, reponse=1):
        """
        :param reponse: 1 for positive, 2 for negative, 3 for miss, 4 for all data
        :return: distance between gaze and object and gaze positions
        """
        if reponse==1:
            data = self.processedGoodResponse
        elif reponse==2:
            data = self.processedNegResponse
        elif reponse==3:
            data = self.processedMissResponse
        else:
            data = self.processedData

        if len(data) > 0:
            #compute response
            data = data.assign(DiffTime=pd.Series(data.ResponseTime - data.SpawnTime).values)
            #compute the distance between object and gaze
            objectPosition = data[['ObjectX','ObjectY']].values
            gazePosition = data[['GazeX','GazeY']].values

            distances = np.sqrt(np.sum(np.power(objectPosition - gazePosition, 2), axis=1))
            data = data.assign(Distance=pd.Series(distances).values)

            #compute distance between object
            objDistance = np.sqrt(np.sum(np.power(objectPosition[1:] - objectPosition[:-1], 2), axis=1))
            objDistance = np.insert(objDistance, 0, [0], axis=0)

            data = data.assign(ObjDistance = pd.Series(objDistance).values)
            data.loc[data.ResponseTime == -1, "ObjDistance"] = -1
            if len(data[:-1].ResponseTime == -1) > 1:
                data.loc[data[:-1].loc[data[:-1].ResponseTime == -1].index + 1, "ObjDistance"] = -1

        return data


    # def spatialFeaturesExtractor(self):
    #     removal = OutliersRemoval(cutoff=CUT_OFF)
    #     # edges
    #     xedges, yedges = np.arange(0, 101, 1), np.arange(0, 101, 1)
    #     game_data = self.gameData  # game data
    #     game_data = removal.transformGameResult(game_data)  # remove response with RT less that TH
    #     gaze_data = self.gazeData  # all gaze data
    #     gaze_data = gaze_data[(gaze_data["Time"].values > 0.1)]
    #     gaze_obj_data = gaze_data[(gaze_data["ObjectX"].values != -1) & (gaze_data["ObjectY"].values != -1)].copy()
    #     gaze_obj_data.loc[:, "Distance"] = euclidianDist(gaze_obj_data[["GazeX", "GazeY"]].values,
    #                                               gaze_obj_data[["ObjectX", "ObjectY"]].values)
    #
    #     area = convexHullArea(gaze_data)  # compute gaze area
    #
    #     # compute RT, RTVar, Correct and Incorrect Percentage
    #     response = game_data[game_data["ResponseTime"] != -1]
    #     Go_response = len(response[response["PosResponse"] == 1]) / len(game_data)
    #     NoGo_E_reponse = len(game_data[game_data["NegResponse"] == 1]) / len(game_data)
    #     Go_E_reponse = len(game_data[game_data["MissResponse"] == 1]) / len(game_data)
    #     NoGo_reponse = len(game_data[(game_data["PosResponse"] == 1) & (game_data["ResponseTime"] == -1)]) / len(game_data)
    #
    #     RT_AVG, RT_Var_AVG = np.mean(response.RT[response.RT >= 0]), np.std(response.RT[response.RT >= 0])
    #
    #
    #     # compute gaze velocity
    #     skip = 1
    #     time = gaze_data["Time"].values
    #     gazex = gaze_data["GazeX"].values
    #     gazey = gaze_data["GazeY"].values
    #     gaze_avg = np.array([gazex, gazey]).transpose()
    #     velocity = gaze_data["Velocity"].values
    #     acceleration = gaze_data["Acceleration"].values
    #     sampen_velocity = sampen(velocity, 2)  # computed sample entropy of gaze velocity
    #     sampen_acceleration = sampen(acceleration, 2)  # compute sample entropy of gaze acceleration
    #
    #     # compute sample entropy and angle (1e-25 to avoid NAN)
    #
    #     dist_avg = euclidianDistT(gaze_avg, skip=2)  # compute euclidian distance for consecutive gaze
    #     angle_avg = anglesEstimation(gaze_avg, skip=2)  # compute angle distance for consecutive gaze
    #
    #     # compute sample entropy of gaze distance
    #     sampen_dist = sampen(dist_avg, 2)
    #     sampen_angle = sampen(angle_avg, 2)
    #
    #     # compute spatial entropy
    #     H, _, _ = np.histogram2d(gazex * 100, gazey * 100, bins=(xedges, yedges), density=True)
    #
    #     p = H.flatten()
    #     p = p[p > 0]
    #     spatial_entropy = np.sum(p * np.log(1 / p)) / np.log(len(p))
    #
    #     # compute gaze-object-entropy
    #     gaze_obj = removeNoObjectData(
    #         gaze_obj_data[['Time', 'GazeX', 'GazeY', 'ObjectX', 'ObjectY']].dropna().to_numpy())
    #     gaze_point = gaze_obj[:, 1:3]
    #     obj_point = gaze_obj[:, 3:]
    #     gaze_obj_en = gazeEntropy(gaze_point - obj_point)
    #     spectral_entropy = spectralEntropy(gaze_point - obj_point)
    #
    #     #  start compute fixation time avg sample dist and sample angle
    #     fixation_times = []
    #     sampen_gaze_objs = []
    #     for _, g in game_data.iterrows():
    #         response_time = g["ResponseTime"]
    #         if (g["ResponseTime"] == -1) | (g["ResponseTime"] <= g["SpawnTime"]):
    #             response_time = g["SpawnTime"] + 0.7
    #         # take gaze based on response time
    #         gaze_t = gaze_obj_data[(gaze_obj_data["Time"] >= g["SpawnTime"]) & (gaze_obj_data["Time"] <= response_time)]
    #         idx_filter = filterFixation(gaze_t["Distance"].values <= AREA_FIX_TH)
    #
    #         # compute sample entropy
    #         gaze_samp_avg = np.array([gaze_t["GazeX"].values, gaze_t["GazeY"].values]).transpose()
    #         obj_samp_avg = np.array([gaze_t["ObjectX"].values, gaze_t["ObjectY"].values]).transpose()
    #         gaze_to_obj = np.linalg.norm(gaze_samp_avg - obj_samp_avg, axis=-1)
    #
    #         # the embeding is 6 so it requires minimum lenth of 8
    #         if len(gaze_to_obj) > 10:
    #             sampen_gaze_obj = sampen(gaze_to_obj, 2)  # sample entropy of gaze-to-obj
    #             if np.isinf(sampen_gaze_obj) == False:
    #                 sampen_gaze_objs.append(sampen_gaze_obj)
    #         # end compute the avg sample entropy
    #
    #         for idx in idx_filter:
    #             if len(idx) > 2:
    #                 distances_time = gaze_t["Time"].values
    #                 # compute fixation time
    #                 fix_time = distances_time[np.max(idx)] - distances_time[np.min(idx)]
    #                 fixation_times.append(fix_time)
    #     fixation_times = np.array(fixation_times) * 1000




