import numpy as np
from scipy.spatial import ConvexHull
from scipy.stats import gaussian_kde as kde, entropy
from scipy.signal import welch
from scipy.signal._savitzky_golay import savgol_filter

def euclidianDist(x1, x2):
    dist = np.sqrt(np.sum(np.power(x1 - x2, 2), 1))
    return dist


def computeVelocityAccel(time, gaze, n, poly):
    # x_filtered
    # first derivative
    gaze_x_d1 = savgol_filter(gaze[:, 0], n, polyorder=poly, deriv=1)
    gaze_y_d1 = savgol_filter(gaze[:, 1], n, polyorder=poly, deriv=1)
    # time_d1 =  savgol_filter(time, n, polyorder=poly, deriv=1)

    gaze_d1 = np.array([gaze_x_d1, gaze_y_d1]).transpose()

    # second derivative
    gaze_x_d2 = savgol_filter(gaze[:, 0], n, polyorder=poly, deriv=2)
    gaze_y_d2 = savgol_filter(gaze[:, 1], n, polyorder=poly, deriv=2)
    # time_d2 =  savgol_filter(savgol_filter(time, n, polyorder=poly, deriv=0), n, polyorder=poly, deriv=1)

    gaze_d2 = np.array([gaze_x_d2, gaze_y_d2]).transpose()

    velocity_filtered = np.sqrt(np.sum(np.power(gaze_d1, 2), -1))

    acceleration_filtered = np.sqrt(np.sum(np.power(gaze_d2, 2), -1))

    return velocity_filtered, acceleration_filtered

    # compute convex hull of given points


def convexHullArea(data):
    hull = ConvexHull(points=data[["GazeX", "GazeY"]].values)
    return hull.volume


def gazeEntropy(xy, relative=True):
    ''' proposed by Sergio A. Alvarez
    :param xy: distance between gaze and obj
    :param relative:
    :return: the entropy of heatmap
    '''
    est = kde(xy.transpose())
    if relative:
        xgrid, ygrid = np.mgrid[-1:1:51j, -1:1:51j]
    else:
        xgrid, ygrid = np.mgrid[0:1:51j, 0:1:51j]
    return entropy(np.array([est.pdf([x, y]) for (x, y) in zip(xgrid, ygrid)]).ravel()) \
           / np.log2(len(xgrid.ravel()))


def spectralEntropy(xy, fs=72):  # defaults to downsampled frequency
    ''' proposed by Sergio A. Alvarez
    :param xy: gaze - object series
    :param fs:
    :return:
    '''
    _, spx = welch(xy[:, 0], fs, nperseg=fs / 2)  # scipy.signal.welch
    _, spy = welch(xy[:, 1], fs, nperseg=fs / 2)  # equal spectrum discretization for x, y
    return entropy(spx + spy) / np.log2(len(_))  # scipy.stats.entropy

def bernouliSTD(data):
        p = data.mean()
        std = p * (1-p)
        return std

def computeResponseTime(spawnTime, responseTime):
        '''
        :param spawnTime: time when the object appears
        :param responseTime: time when the player responses
        :returns: average and std response time
        '''
        timeDiff = (responseTime - spawnTime)
        timeDiff = timeDiff[timeDiff >= 0]

        #compute both avg and std if there are response times
        if len(timeDiff.values) > 0:
            avgTime = np.average(timeDiff.values)
            stdTime = np.std(timeDiff.values)
            #stdTime = self.bernouliSTD(responseTime.values)
        else:
            avgTime = 0
            stdTime = 0

        return avgTime, stdTime

def filterFixation(fixation):
    ''' decide when the gaze enter and leave the fixation area
    :param fixation: a series of distance between gaze and stimulus
    :return: the series of fixation
    '''
    fixation_list = []
    fixation_g = []
    for i in range(1, len(fixation)):
        if (fixation[i-1] == True) and (fixation[i] == False):
            fixation_list.append(fixation_g)
            fixation_g = []
        if fixation[i]:
            fixation_g.append(i)

    if len(fixation_g) > 0:
        fixation_list.append(fixation_g)


    return fixation_list

#only take gaze when the stimulus appears
def removeNoObjectData(numpyData):
    return numpyData[numpyData[:,1]!= -1, :]

def euclidianDistT(x, time=None, skip=3):
    ''' compute the euclidian distance for the series
    :param x: must be series > skip + 3
    :param skip:
    :return:
    '''
    if len(x) < (skip + 3):
        raise ValueError("length of x must be greater than skip + 3")
    dist = np.array([euclidianDist(x[i], x[i-skip]) for i in range(skip, len(x), 1)])
    return dist

def anglesEstimation(data, skip=3):
    ''' compute angles of consecutive gazes
    :param data: a series
    :param skip: stride
    :return: a series of angles
    '''
    angles = np.array(
        [np.dot(data[i, :], data[i - skip, :]) / (np.linalg.norm(data[i, :]) * np.linalg.norm(data[i - skip, :])) for i in range(skip, len(data), 1)])
    angles = np.arccos(relu(angles))
    return angles