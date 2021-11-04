import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
import cv2

class PlottingProcessor:

    def setResponses(self, correctResponse, wrongResponse, missResponse):
        '''
        response(average, average_group_by)
        :param correctResponse: summary of correct response
        :param wrongResponse: summary of wrong response
        :param missResponse: miss of wrong response
        :return:
        '''
        self.correctResponse = correctResponse
        self.wrongResponse = wrongResponse
        self.missResponse = missResponse

    def setResponseTime(self, responseTime):
        '''
        :param responseTime: summary of response time
        '''
        self.responseTime = responseTime

    def plotResponse(self, figure, canvas):
        '''
        :param figure: the plotting figure
        :param canvas: the canvas where the figure is attached into
        The bar charts are plotted side by side and if there is no summary for a response , len(response) = 0, no plotting is conducted
        '''
        bar_width = 0.25
        ax = self.getAxes(figure)
        y_pos = None
        # good response
        if (len(self.correctResponse[0]) >= 1):
            x = self.correctResponse[0] * 100
            y_pos = np.arange(len(x)) + 1
            ax.bar(y_pos, x.flatten(), bar_width, align='center', alpha=0.5, label="Corrent")

        # neg response
        if (len(self.wrongResponse[0]) >= 1):
            xNeg = self.wrongResponse[0] * 100
            y_neg = np.arange(len(xNeg)) + 1
            ax.bar(y_neg + bar_width, xNeg.flatten(), bar_width, align='center', alpha=0.5, label="Wrong")

        # miss response
        if (len(self.missResponse[0]) >= 1):
            xMiss = self.missResponse[0] * 100
            y_miss = np.arange(len(xMiss)) + 1
            ax.bar(y_miss + (bar_width * 2), xMiss.flatten(), bar_width, align='center', alpha=0.5, label="Miss")

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=3)

        ax.set_xticks(y_pos + bar_width)
        ax.set_xticklabels(y_pos)

        self.setLabel(ax, "Time (mins)", "Accuracy (%)")
        ax.set_ylim([0.0, 100.0])

        figure.tight_layout()
        canvas.draw()
        canvas.flush_events()

    def plotResponseTime(self, figure, canvas):
        '''
        :param figure: the plotting figure
        :param canvas: the canvas where the figure is attached into
        The response time for each minute is plot
        '''
        x = []

        for i in range(self.responseTime.__len__()):
            if self.responseTime.groups.get(i) is not None:
                x.append(self.responseTime.get_group(i).values)
            else:
                x.append([0])

        ax = self.getAxes(figure)

        ax.boxplot(x, 0, '')
        self.setLabel(ax, "Time (mins)", "Seconds")
        figure.tight_layout()
        canvas.draw()
        canvas.flush_events()

    def setGazeAndHead(self, gazeData, gazeObject, headData, gazeOverTime):
        '''
        :param gazeData: filtered out gaze data
        :param headData: filtered out head data
        '''
        self.gazeData = gazeData
        self.gazeObject = gazeObject
        self.headData = headData
        self.gazeOverTime = gazeOverTime

    def plotGaze(self, figure, canvas):
        '''
        :param figure: the plotting figure
        :param canvas: the canvas where the figure is attached into
        The gaze dense probability is plotted
        '''
        sns.set_style("white")

        ax = self.getAxes(figure)

        # ax.hist2d(self.gazeData[0], self.gazeData[1], bins=100)
        sns.kdeplot(self.gazeData[0], self.gazeData[1], shade=True, cmap="Reds", bw=.15, ax=ax)

        self.setLabel(ax, "X axis", "Y axis")
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.0])
        figure.tight_layout()
        canvas.draw()
        canvas.flush_events()

    def plotClusterGaze(self, figure, canvas, nCluster=20, clusterSize=100):
        '''
        :param figure: the plotting figure
        :param canvas: the canvas where the figure is attached into
        :param nCluster: number of cluster
        :param clusterSize: the radius of each cluter, higher value means bigger radius
        '''

        ax = self.getAxes(figure)

        points = np.column_stack([self.gazeData[0], self.gazeData[1]])
        kmeans = KMeans(n_clusters=nCluster, random_state=0).fit(points)
        sizes = (clusterSize * np.array([np.sum(kmeans.labels_ == i) for i in range(nCluster)]) / points.shape[0]) ** 2
        ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=sizes, alpha=0.3, cmap='viridis')
        self.setLabel(ax, "X axis", "Y axis")
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.0])
        figure.tight_layout()
        canvas.draw()
        canvas.flush_events()

    def plotGazeObject(self, figure, canvas):
        '''
        :param figure: the plotting figure
        :param canvas: the canvas where the figure is attached into
        The player's gaze position and object position
        '''

        #Open game background
        img = cv2.imread("Conf\\game_bg.png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        ax = self.getAxes(figure)
        ax.imshow(img, extent=[0, 1, 0, 1], aspect=0.3)
        #ax.plot(self.gazeObject[0], self.gazeObject[1], '-o', label="Object", alpha=0.5, color="green")
        ax.plot(self.gazeObject[2], self.gazeObject[3], '-o', label="Gaze", alpha=0.7, color="yellow")
        #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=2)
        self.setLabel(ax, "X axis", "Y axis")
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.0])


        figure.tight_layout()
        canvas.draw()
        canvas.flush_events()

    def plotGazeAreaVTime(self, figure, canvas):
        '''
        :param figure: the plotting figure
        :param canvas: the canvas where the figure is attached into
        The head rotation time for each minute is plot
        '''
        ax = self.getAxes(figure)

        ax.plot(np.arange(1, len(self.gazeOverTime) + 1),self.gazeOverTime, '-*',color="red")

        self.setLabel(ax, "Time (mins)", "Trajectory area")
        figure.tight_layout()
        canvas.draw()
        canvas.flush_events()

    def plotHeadRot(self, figure, canvas):
        '''
        :param figure: the plotting figure
        :param canvas: the canvas where the figure is attached into
        The head rotation time for each minute is plot
        '''
        x1 = []
        x2 = []

        for i in range(self.headData.__len__()):
            x1.append(self.headData.get_group(i).HeadPosChange.values)
            x2.append(self.headData.get_group(i).HeadRotChange.values)

        x = np.concatenate([x1, x2]).T

        ax = self.getAxes(figure)

        ax.boxplot(x2, 0, '')

        self.setLabel(ax, "Time (mins)", "Degree of changes")
        figure.tight_layout()
        canvas.draw()
        canvas.flush_events()

    def getAxes(self, figure):
        '''
        :param figure: the plotting figure
        If this is the first plot then create a new subplot
        Otherwise just use the previous plot
        '''

        if len(figure.get_axes()) > 0:
            ax = figure.get_axes()[0]
        else:
            ax = figure.subplots()

        ax.clear()
        return ax

    def setLabel(self, ax, xLabel, yLabel):
        '''
        :param ax: axes in the figure
        Set the value of x and y axes
        '''

        ax.set_xlabel(xLabel, fontsize=12)
        ax.set_ylabel(yLabel, fontsize=12)
