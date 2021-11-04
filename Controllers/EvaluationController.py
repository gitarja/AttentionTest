from PyQt5.QtWidgets import QMessageBox
class EvaluationController:

    def validateBirthDate(self, view, year, month, day):
        '''
        :param year: year of birth day
        :param month: month of birth day
        :param day: day of birth day
        :return: true if all are ok otherwise false
        '''
        try:
            int(year)
            int(month)
            int(day)
            return True
        except:
            QMessageBox.warning(view, "Error", "Please select the birth day")
            return False


    def validateHeightWeight(self, view, height, weight):
        '''
        :param view: the parent view
        :param height: height of subject
        :param weight: weight of subject
        :return: true if all are ok otherwise false
        '''
        try:
            float(height)
            float(weight)
            return True
        except:
            QMessageBox.warning(view, "Error", "Please select the birth day")
            return False