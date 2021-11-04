import subprocess
import os
from Views.MainUI import Ui_MainWindow
from Views.ObservationUI import Ui_ObservationUI
from Views.TrainingSetupUI import Ui_TrainingSetupUI
import sys
import yaml
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from Controllers.TrainingController import TrainingController
from Controllers.EvaluationController import EvaluationController
from Controllers.DataProcessor import DataProcessor
from Controllers.PlottingProcessor import PlottingProcessor
from Controllers.TurnGenerator import TurnGenerator
from Models.Subject import Subject, GameMode
from PyQt5 import QtPrintSupport, QtGui
from Controllers.VideoRecorder import VideoRecorder
import datetime


class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = Ui_MainWindow()
        # self.observationView = Ui_ObservationUI()
        # action of evaluation button
        self.view.observationButton.clicked.connect(self.evaluationClick)
        #self.view.proceedButton.clicked.connect(self.proceedClick)
        # action of training button
        self.view.trainingButton.clicked.connect(self.trainingClick)

        #submenu
        self.view.actionPrint.triggered.connect(self.printWidget)
        self.view.actionExit.triggered.connect(self.view.close)

        # processor
        self.dataProcessor = DataProcessor()
        self.plotProcessor = PlottingProcessor()
        self.turnGenerator = TurnGenerator()

        # controllers
        self.trainingController = TrainingController()
        self.evaluationController = EvaluationController()

        self.filename = None
        self.gameDir = None
        self.videoRecorder = VideoRecorder()
        #default id for training
        self.defaultId = "GM0001"
        self.currentDir = os.getcwd()

        #GameSettings
        with open("conf\\GameSettings.yml", 'r') as stream:
            try:
                self.conf = yaml.safe_load(stream)
                #change the game directory with current project path
                #self.conf["GAME_DIR"] = self.currentDir + "\\" + self.conf["GAME_DIR"]
                self.conf["GAME_DIR"] = os.path.join(self.currentDir, self.conf["GAME_DIR"])
            except yaml.YAMLError as exc:
                print(exc)


    def trainingClick(self):
        # activate the training dialog
        dialog = self.openDialog(Ui_TrainingSetupUI())
        # action of maxTime select box (set minTime values)
        dialog.ui.maxTimeBox.activated.connect(self.trainingController.maxTimeActivated(dialog=dialog))
        # action of probCharacter, set text
        dialog.ui.probCharField.valueChanged.connect(self.trainingController.probCharChanged(dialog=dialog))
        dialog.ui.cancelButton.clicked.connect(self.close(dialog))
        dialog.ui.startTrainingButton.clicked.connect(self.startGameTraining(dialog))
        dialog.exec_()

    def evaluationClick(self):
        #activation the evaluation box
        dialog = self.openDialog(Ui_ObservationUI())
        dialog.ui.cancelButton.clicked.connect(self.close(dialog))
        dialog.ui.startButton.clicked.connect(self.startGameEvaluation(dialog))
        dialog.ui.levelBox.activated.connect(self.levelMessage(dialog))
        dialog.exec_()

    def close(self, dialog):
        def cancelClick():
            dialog.close()

        return cancelClick

    def openDialog(self, ui):
        '''
        :param ui: the interface that wants to be showed in the dialog
        :return: dialog window
        '''
        dialog = QDialog()
        dialog.ui = ui
        dialog.ui.setupUi(dialog)
        # observation form controller

        return dialog



    def launcGame(self, dialog, id="GM0001", fileName=None, turnFile=None, feedBack=False, distraction=False):
        '''
        :param dialog: dialog window that activates this function
        :param id: id of the subject
        :param fileName: the game file path
        :param turnFile: the turns file path
        '''
        FNULL = open(os.devnull, 'w')  # use this if you want to suppress output to stdout from the subprocess
        args = fileName
        if turnFile is not None:
            args += " -turnFile " + turnFile + " -id " + id + " -feedback " + str(feedBack) + " -distraction " + str(distraction)
        # print(args)
        subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
        dialog.close()


    def startGameTraining(self, dialog):

        def startGame():
            # get the selected mode 0 = mogura, 1 = gaze
            selectedIndex = dialog.ui.gameModeBox.currentIndex()
            if (selectedIndex == 0):
                self.gameDir = self.conf["GAME_DIR"]
            else:
                self.gameDir = self.conf["GAME_DIR_GAZE"]
            #the normalized precentage of chiken to appear during the game (0 - 100)
            self.defaultId = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-").replace(".", "-")
            chickenPercentage = (100 - dialog.ui.probCharField.value()) / 100
            totalTime = float(dialog.ui.totalTimeBox.currentText().split(" ")[0])
            maxTime = float(dialog.ui.maxTimeBox.currentText().split(" ")[0])
            minTime = float(dialog.ui.minTimeBox.currentText().split(" ")[0])
            appTime = float(dialog.ui.apperanceTimeBox.currentText().split(" ")[0])
            feedBack = dialog.ui.feedBackBox.isChecked()
            distraction = dialog.ui.distractionBox.isChecked()
            #fileName = self.gameDir + self.conf["GAME_FILE"]
            fileName = os.path.join(self.gameDir, self.conf["GAME_FILE"])
            #generate the turns file
            turnFile = self.turnGenerator.generate(chickenPercentage, totalTime, maxTime, minTime, appTime)

            # recordvideo
            #videoFile = self.currentDir + "\\" + self.conf["TRAINING_VIDEO_RESULTS"] + "\\" + self.defaultId + ".avi"
            videoFile = os.path.join(self.currentDir, self.conf["TRAINING_VIDEO_RESULTS"], self.defaultId + ".avi")
            self.videoRecorder.setFileName(videoFile)
            self.videoRecorder.start()

            #launch the game
            self.launcGame(dialog, self.defaultId, fileName, turnFile, feedBack, distraction)

            # stop recordvideo
            self.videoRecorder.stop()

            #close dialog
            dialog.close()
            # proceed results
            resultPath = self.gameDir + self.conf["GAME_RESULT_DIR"] + self.defaultId
            self.showProcessDialog(resultPath)

        return startGame

    def startGameEvaluation(self, dialog):
        def startGame():
            #validate form

            #validate birth date
            bdYear = dialog.ui.bdYearBox.currentText()
            bdMonth = dialog.ui.bdMonthBox.currentText()
            bdDay = dialog.ui.bdDayBox.currentText()
            bdValid = self.evaluationController.validateBirthDate(self.view, bdYear, bdMonth,
                                   bdDay)

            #validate weight and height
            height = dialog.ui.heightBox.text()
            weight = dialog.ui.weightBox.text()
            weightHeightValid = self.evaluationController.validateHeightWeight(self.view, height, weight)

            #get other forms
            name = dialog.ui.nameBox.text()
            kana = dialog.ui.kanaBox.text()
            sex = dialog.ui.sexBox.currentText()
            sleep = dialog.ui.sleepBox.currentText()
            handOrFoot = dialog.ui.handFootBox.currentIndex()
            leftOrRight = dialog.ui.dominantHandBox.currentIndex()
            comment = dialog.ui.commentBox.text()
            feedBack = dialog.ui.feedBackBox.isChecked()
            distraction = dialog.ui.distractionBox.isChecked()
            level = dialog.ui.levelBox.currentText()
            mode = dialog.ui.gameModeBox.currentText()
            if bdValid & weightHeightValid:
                id = dialog.ui.idBox.text()
                # get the selected mode 0 = mogura, 1 = gaze
                modeIndex = dialog.ui.gameModeBox.currentIndex()

                if (modeIndex == 0):
                    self.gameDir = self.conf["GAME_DIR"]
                else:
                    self.gameDir = self.conf["GAME_DIR_GAZE"]


                #fileName = self.gameDir + self.conf["GAME_FILE"]
                fileName = os.path.join(self.gameDir, self.conf["GAME_FILE"])
                #the turn file used for evaluation
                turnFile = os.path.join(self.currentDir, self.conf["TURNF_FILES"], self.levelFile(level))

                # recordvideo
                #videoFile = self.currentDir + "\\" + self.conf["EVALUATION_VIDEO_RESULTS"] + "\\" + id + ".avi"
                videoFile = os.path.join(self.currentDir, self.conf["EVALUATION_VIDEO_RESULTS"], id + ".avi")
                self.videoRecorder.setFileName(videoFile)
                self.videoRecorder.start()


                #launch the game
                self.launcGame(dialog, id, fileName, turnFile, feedBack, distraction)

                # stop recordvideo
                self.videoRecorder.stop()

                # save subject
                gameMode = GameMode(mode, level, feedBack, distraction)
                subject = Subject(id, name, kana,
                                  bdYear, bdMonth,
                                  bdDay,
                                  sex, sleep, height, weight, handOrFoot, leftOrRight, comment, gameMode, conf=self.conf)
                #evaluationPath = self.currentDir + "\\" + self.conf["EVALUATION_RESULTS"]
                evaluationPath = os.path.join(self.currentDir, self.conf["EVALUATION_RESULTS"])
                subject.save(evaluationPath)

                # update counter
                f = open("conf/IdCounter.txt", "a+")
                f.write(id + "\n")

                # close dialog
                dialog.close()

                #proceed results
                #resultPath = self.gameDir + self.conf["GAME_RESULT_DIR"] + id
                resultPath = os.path.join(self.gameDir,  self.conf["GAME_RESULT_DIR"] + id)
                self.showProcessDialog(resultPath)

        return startGame


    def showProcessDialog(self, resultPath):
        try:

            QMessageBox.information(self.view, "Information", "実験の結果が進められます")
            self.proceedClick(resultPath)
        except:
            QMessageBox.warning(self.view, "Error", "最新の実験結果が見つかりません")


    def run(self):
        self.view.show()
        return self.app.exec_()

    def proceedClick(self, resultPath):
        '''
        :param resultPath: the path of game and gaze results and the id path+id_+
        :return:
        '''
        self.dataProcessor.ProceedGameResult(
            resultPath +"_"+ self.conf["GAME_RESULTS_FILE"],
            resultPath +"_"+ self.conf["GAZE_HEAD_FILE"])

        # correct response
        correctSum, correctDetail = self.dataProcessor.averageGoodResponseTime(mode=2)
        self.view.corAvgField.setText(str(round(correctSum[0] * 100, 2)))
        self.view.corStdField.setText(str(round(correctSum[1] * 100, 2)))
        self.view.corAvgTimeField.setText(str(round(correctSum[2] * 1000, 2)))
        self.view.corStdTimeField.setText(str(round(correctSum[3] * 1000, 2)))

        # wrong response
        wrongSum, wrongDetail = self.dataProcessor.averageNegResponseTime(mode=2)
        self.view.wroAvgField.setText(str(round(wrongSum[0] * 100, 2)))
        self.view.wroStdField.setText(str(round(wrongSum[1] * 100, 2)))
        self.view.wroAvgTimeField.setText(str(round(wrongSum[2] * 1000, 2)))
        self.view.wroStdTimeField.setText(str(round(wrongSum[3] * 1000, 2)))

        # miss response
        missSum, missDetail = self.dataProcessor.averageMissResponseTime(mode=2)
        self.view.missField.setText(str(round(missSum[0] * 100, 2)))

        # overall response
        sum, sumDetail = self.dataProcessor.averageResponseTimes(mode=2)
        self.view.avgTimeField.setText(str(round(sum[0] * 1000, 2)))
        self.view.stdTimeField.setText(str(round(sum[1] * 1000, 2)))

        # gazearea
        gazearea = self.dataProcessor.computeGazeArea()
        self.view.trajectoryAreaField.setText(str(round(gazearea, 2)))

        #plot the respose by times
        self.plotProcessor.setResponses(correctDetail, wrongDetail, missDetail)
        self.plotProcessor.plotResponse(figure=self.view.figureResponse, canvas=self.view.canvasResponse)

        self.plotProcessor.setResponseTime(sumDetail)
        self.plotProcessor.plotResponseTime(figure=self.view.figureTime, canvas=self.view.canvasTime)

        # gaze and head
        gaze = self.dataProcessor.computeGaze()
        gazeObject = self.dataProcessor.computeGazeObject()
        #head = self.dataProcessor.computeHead()
        gazeOverTime = self.dataProcessor.computeGazeVTime()
        self.plotProcessor.setGazeAndHead(gaze, gazeObject, None, gazeOverTime)

        #self.plotProcessor.plotGaze(figure=self.view.figureGaze, canvas=self.view.canvasGaze)
        #self.plotProcessor.plotClusterGaze(figure=self.view.figureGaze, canvas=self.view.canvasGaze, nCluster=10)
        self.plotProcessor.plotGazeObject(figure=self.view.figureGaze, canvas=self.view.canvasGaze)
        self.plotProcessor.plotGazeAreaVTime(figure=self.view.figureHead, canvas=self.view.canvasHead)
        # self.plotProcessor.plotHeadRot(figure=self.view.figureHead, canvas=self.view.canvasHead)


    def levelFile(self, mode):
        turnFile = "Turns"
        if mode == "Easy":
            return turnFile+ "_easy.csv"
        elif mode == "Medium":
            return turnFile + "_medium.csv"
        elif mode == "Hard":
            return turnFile + "_hard.csv"
        elif mode == "Unbalance cat":
            return turnFile + "_ucat.csv"
        elif mode == "Unbalance chicken":
            return turnFile + "_uchicken.csv"
        elif mode == "Children":
            return turnFile + "_children.csv"
        elif mode == "Children-Sym-Asym":
            return turnFile + "_sym_asym_children.csv"
        else:
            return turnFile + "_def.csv"

    def levelMessage(self, dialog):
        def setDescription():
            level = dialog.ui.levelBox.currentText()
            if level == "Easy":
                dialog.ui.levelDescLabel.setText("10分\t\t\t最大待ち時間=0.9s\t\t\t最小待ち時間=0.7s\t\t\t提示時間=0.5s\t\t\t鳥の割合=50")
            elif level == "Medium":
                dialog.ui.levelDescLabel.setText("10分\t\t\t最大待ち時間=1.1s\t\t\t最小待ち時間=0.9s\t\t\t提示時間=0.5s\t\t\t鳥の割合=50")
            elif level == "Hard":
                dialog.ui.levelDescLabel.setText("10分\t\t\t最大待ち時間=1.3s\t\t\t最小待ち時間=1.1s\t\t\t提示時間=0.5s\t\t\t鳥の割合=50")
            elif level == "Unbalance cat":
                dialog.ui.levelDescLabel.setText("10分\t\t\t最大待ち時間=1.1s\t\t\t最小待ち時間=0.9s\t\t\t提示時間=0.5s\t\t\t鳥の割合=15")
            elif level == "Unbalance chicken":
                dialog.ui.levelDescLabel.setText("10分\t\t\t最大待ち時間=1.1s\t\t\t最小待ち時間=0.9s\t\t\t提示時間=0.5s\t\t\t鳥の割合=85")
            elif level == "Children":
                dialog.ui.levelDescLabel.setText("4分\t\t\t最大待ち時間=1.0s\t\t\t最小待ち時間=0.7s\t\t\t提示時間=0.7s\t\t\t鳥の割合=50")
            elif level == "Children-Sym-Asym":
                dialog.ui.levelDescLabel.setText("3分\t\t\t最大待ち時間=0.7s\t\t\t最小待ち時間=0.7s\t\t\t提示時間=1.5-1.s\t\t\t鳥の割合=50")
            else:
                dialog.ui.levelDescLabel.setText("10分\t\t\t最大待ち時間=1.0s\t\t\t最小待ち時間=0.7s\t\t\t提示時間=0.7s\t\t\t鳥の割合=50")

        return setDescription



    def printWidget(self):
        # # Create printer
        # printer = QtPrintSupport.QPrinter()
        # # Create painter
        # painter = QtGui.QPainter()
        # # Start painter
        # painter.begin(printer)
        # # Grab a widget you want to print
        #
        # # Draw grabbed pixmap
        # painter.drawPixmap(10, 10, screen)
        # # End painting

        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        painter = QtGui.QPainter(printer)
        screen = self.view.grab()
        painter.drawPixmap(10, 10, screen)
        self.view.render(painter)