from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
class TrainingController:

    def maxTimeActivated(self, dialog=None):
        def handleActivated():
            dialog.ui.setMinTime(float(dialog.ui.maxTimeBox.currentText().split(" ")[0]))

        return handleActivated

    def probCharChanged(self, dialog=None):
        def valueChange():
            dialog.ui.probCharExpLabel.setText("Cat: " + str(dialog.ui.probCharField.value()) + "%, Chicken: " + str(
                100 - dialog.ui.probCharField.value()) + "%")

        return valueChange

    def browseFile(self):
        self.filename, _ = QFileDialog.getOpenFileName(self.view, 'Single File', QtCore.QDir.rootPath(), '*.csv')