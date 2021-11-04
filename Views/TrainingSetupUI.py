# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TrainingSetUp.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TrainingSetupUI(object):

    def __init__(self):
        super(Ui_TrainingSetupUI, self).__init__()

    def setupUi(self, TrainingSetupUI):
        TrainingSetupUI.setObjectName("TrainingSetupUI")
        TrainingSetupUI.resize(640, 480)
        self.formLayoutWidget = QtWidgets.QWidget(TrainingSetupUI)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 621, 182))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.probCharLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.probCharLabel.setFont(font)
        self.probCharLabel.setObjectName("probCharLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.probCharLabel)
        self.probCharField = QtWidgets.QSlider(self.formLayoutWidget)
        self.probCharField.setProperty("value", 50)
        self.probCharField.setOrientation(QtCore.Qt.Horizontal)
        self.probCharField.setObjectName("probCharField")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.probCharField)
        self.totalTimeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.totalTimeLabel.setFont(font)
        self.totalTimeLabel.setObjectName("totalTimeLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.totalTimeLabel)
        self.totalTimeBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.totalTimeBox.setObjectName("totalTimeBox")
        self.totalTimeBox.addItem("")
        self.totalTimeBox.addItem("")
        self.totalTimeBox.addItem("")
        self.totalTimeBox.addItem("")
        self.totalTimeBox.addItem("")
        self.totalTimeBox.addItem("")
        self.totalTimeBox.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.totalTimeBox)
        self.probCharExpLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.probCharExpLabel.setFont(font)
        self.probCharExpLabel.setText("")
        self.probCharExpLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.probCharExpLabel.setObjectName("probCharExpLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.probCharExpLabel)
        self.maxTimeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.maxTimeLabel.setFont(font)
        self.maxTimeLabel.setObjectName("maxTimeLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.maxTimeLabel)
        self.minTimeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.minTimeLabel.setFont(font)
        self.minTimeLabel.setObjectName("minTimeLabel")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.minTimeLabel)
        self.maxTimeBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.maxTimeBox.setObjectName("maxTimeBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.maxTimeBox)
        self.minTimeBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.minTimeBox.setObjectName("minTimeBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.minTimeBox)
        self.modeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.modeLabel.setFont(font)
        self.modeLabel.setObjectName("modeLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.modeLabel)
        self.gameModeBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.gameModeBox.setObjectName("gameModeBox")
        self.gameModeBox.addItem("")
        self.gameModeBox.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.gameModeBox)
        self.apperanceTimeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.apperanceTimeLabel.setFont(font)
        self.apperanceTimeLabel.setObjectName("apperanceTimeLabel")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.apperanceTimeLabel)
        self.apperanceTimeBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.apperanceTimeBox.setObjectName("apperanceTimeBox")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.apperanceTimeBox)
        self.horizontalLayoutWidget = QtWidgets.QWidget(TrainingSetupUI)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 440, 621, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startTrainingButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.startTrainingButton.setFont(font)
        self.startTrainingButton.setObjectName("startTrainingButton")
        self.horizontalLayout.addWidget(self.startTrainingButton)
        self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.line = QtWidgets.QFrame(TrainingSetupUI)
        self.line.setGeometry(QtCore.QRect(10, 200, 621, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayoutWidget = QtWidgets.QWidget(TrainingSetupUI)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 210, 621, 41))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.distractionLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.distractionLabel.setFont(font)
        self.distractionLabel.setObjectName("distractionLabel")
        self.gridLayout.addWidget(self.distractionLabel, 0, 2, 1, 1)
        self.feedBackBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.feedBackBox.setText("")
        self.feedBackBox.setObjectName("feedBackBox")
        self.gridLayout.addWidget(self.feedBackBox, 0, 1, 1, 1)
        self.distractionBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.distractionBox.setText("")
        self.distractionBox.setObjectName("distractionBox")
        self.gridLayout.addWidget(self.distractionBox, 0, 3, 1, 1)

        self.retranslateUi(TrainingSetupUI)
        QtCore.QMetaObject.connectSlotsByName(TrainingSetupUI)

    def retranslateUi(self, TrainingSetupUI):
        _translate = QtCore.QCoreApplication.translate
        TrainingSetupUI.setWindowTitle(_translate("TrainingSetupUI", "Form"))
        self.probCharLabel.setText(_translate("TrainingSetupUI", "人物の役割"))
        self.totalTimeLabel.setText(_translate("TrainingSetupUI", "実験の総時間"))
        self.totalTimeBox.setItemText(0, _translate("TrainingSetupUI", "1 minute"))
        self.totalTimeBox.setItemText(1, _translate("TrainingSetupUI", "3 minutes"))
        self.totalTimeBox.setItemText(2, _translate("TrainingSetupUI", "5 minutes"))
        self.totalTimeBox.setItemText(3, _translate("TrainingSetupUI", "7 minutes"))
        self.totalTimeBox.setItemText(4, _translate("TrainingSetupUI", "10 minutes"))
        self.totalTimeBox.setItemText(5, _translate("TrainingSetupUI", "15 minutes"))
        self.totalTimeBox.setItemText(6, _translate("TrainingSetupUI", "20 minutes"))
        self.maxTimeLabel.setText(_translate("TrainingSetupUI", "最大待ち時間"))
        self.minTimeLabel.setText(_translate("TrainingSetupUI", "最小待ち時間"))
        self.modeLabel.setText(_translate("TrainingSetupUI", "モード"))
        self.gameModeBox.setItemText(0, _translate("TrainingSetupUI", "Mogura"))
        self.gameModeBox.setItemText(1, _translate("TrainingSetupUI", "Gaze"))
        self.apperanceTimeLabel.setText(_translate("TrainingSetupUI", "提示時間"))
        self.startTrainingButton.setText(_translate("TrainingSetupUI", "練習"))
        self.cancelButton.setText(_translate("TrainingSetupUI", "キャンセル"))
        self.label.setText(_translate("TrainingSetupUI", "手応え"))
        self.distractionLabel.setText(_translate("TrainingSetupUI", "気晴らし"))

        # set boxes
        self.setMaxTime(_translate)
        self.setApperance(_translate)
        self.setMinTime(1)
        self.setProbChar()

    def setProbChar(self):
        self.probCharExpLabel.setText("Cat: " + str(self.probCharField.value()) + "%, Chicken: " + str(
            100 - self.probCharField.value()) + "%")
    def setMaxTime(self, _translate):
        self.maxTimeBox.addItem("")
        self.maxTimeBox.setItemText(0, _translate("ObservationUI", str(0.9) + " seconds"))
        minTime = 1.0
        j = 1
        while (minTime <= 2):
            self.maxTimeBox.addItem("")
            self.maxTimeBox.setItemText(j, _translate("ObservationUI", str(round(minTime, 2)) + " seconds"))
            minTime += 0.1
            j += 1

    def setMinTime(self, maxTime):
        minTime = 0.5
        j = 0
        self.minTimeBox.clear()
        while (minTime < maxTime):
            self.minTimeBox.addItem("")
            self.minTimeBox.setItemText(j, str(round(minTime, 2)) + " seconds")
            if minTime < 0.8:
                minTime += 0.2
            elif (minTime > 0.8) & (minTime < 1.0):
                minTime = 1.0
            else:
                minTime += 0.5
            j += 1

    def setApperance(self, _translate):
        minTime = 0.5
        j = 0

        while (minTime <= 1.0):
            self.apperanceTimeBox.addItem("")
            self.apperanceTimeBox.setItemText(j, _translate("ObservationUI", str(round(minTime, 2)) + " second"))
            minTime += 0.1
            j += 1
