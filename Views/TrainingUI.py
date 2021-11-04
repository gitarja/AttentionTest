# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Training.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TrainingUI(object):
    def setupUi(self, TrainingUI):
        TrainingUI.setObjectName("TrainingUI")
        TrainingUI.resize(640, 480)
        self.formLayoutWidget = QtWidgets.QWidget(TrainingUI)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 351, 31))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.turnFileLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.turnFileLabel.setFont(font)
        self.turnFileLabel.setObjectName("turnFileLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.turnFileLabel)
        self.turnBrowseButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.turnBrowseButton.setObjectName("turnBrowseButton")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.turnBrowseButton)
        self.horizontalLayoutWidget = QtWidgets.QWidget(TrainingUI)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 440, 621, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startTrainingButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.startTrainingButton.setObjectName("startTrainingButton")
        self.horizontalLayout.addWidget(self.startTrainingButton)
        self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)

        self.retranslateUi(TrainingUI)
        QtCore.QMetaObject.connectSlotsByName(TrainingUI)

    def retranslateUi(self, TrainingUI):
        _translate = QtCore.QCoreApplication.translate
        TrainingUI.setWindowTitle(_translate("TrainingUI", "Form"))
        self.turnFileLabel.setText(_translate("TrainingUI", "Turn file"))
        self.turnBrowseButton.setText(_translate("TrainingUI", "Choose file"))
        self.startTrainingButton.setText(_translate("TrainingUI", "Start Training"))
        self.cancelButton.setText(_translate("TrainingUI", "Cancel"))



