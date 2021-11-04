import yaml
import datetime
import codecs
# import sqlite3
import os

class GameMode:

    def __init__(self, mode, level, feedBack, distraction):
        self.mode = mode
        self.level = level
        self.feedBack = feedBack
        self.distraction = distraction

class Subject:

    def __init__(self, id, name, kana, bdYear, bdMonth, bdDay, sex, sleepingHours, height, weight, handOrFoot, rightOrLeft, comment, gameMode, conf=None):
        '''
        :param id: evaluation ID according to IdCounter
        :param mode: mode that is selected during evaluation 0= mogura, 1 = gaze
        :param name: name of the subjectt
        :param kana: kana name of the subject
        :param bdYear: year of subject's birth date
        :param bdMonth: month of subject's birth date
        :param bdDay: day of subject's birth date
        :param sex: subject's sex
        :param sleepingHours: subject's previous day sleeping hours
        :param height: subject's height
        :param weight: subject's weight
        :param handOrFoot: 0 = hand 1 = foot
        :param rightOrLeft: 0 = right 1 = left
        :param comment: subject's condition
        '''
        self.id = id
        self.name = name
        self.kana = kana
        self.birthDate = self.setBirthDate(bdYear, bdMonth, bdDay)
        self.sex = sex
        self.sleepingHours = sleepingHours
        self.height = float(height)
        self.weight = float(weight)
        self.handOrFoot = handOrFoot
        self.rightOrLeft = rightOrLeft
        self.comment = comment
        self.now = datetime.datetime.now()
        self.gameMode = gameMode

        # open configuration
        self.currentDir = os.getcwd()
        self.conf = conf



    def setBirthDate(self, year, month, day):
        self.bdYear = int(year)
        self.bdMonth = int(month)
        self.bdDay = int(day)
        return str(year) + "-" + str(month) + "-" + str(day)

    def save(self, path):
        '''
        :param path: path of the yaml file
        '''
        data = {
            "id": self.id,
            "fullName": {"name": self.name, "kana": self.kana},
            "birthDate": {"year": self.bdYear, "month": self.bdMonth, "day": self.bdDay},
            "sex": self.sex,
            "sleepingHours": self.sleepingHours,
            "evaluationDate": {"year": self.now.year, "month": self.now.month, "day": self.now.day},
            "evaluationTime": {"hour": self.now.hour, "minute": self.now.minute, "second": self.now.second},
            "height": self.height,
            "weight": self.weight,
            "handOrFoot": self.handOrFoot,
            "rightOrLeft": self.rightOrLeft,
            "comment": self.comment,
            "gameMode": {"feedBack": self.gameMode.feedBack,
            "distraction": self.gameMode.feedBack,
            "mode": self.gameMode.mode,
            "level": self.gameMode.level}


        }
        with codecs.open(path + str(self.id)+".yml", 'w', 'utf-8') as outfile:
            yaml.dump(data, outfile,  encoding='utf-8', allow_unicode=True, default_flow_style=False)



    # def saveToDatabase(self):
    #     db_path =  "..\\" + self.conf["DB_PATH"]
    #     conn = sqlite3.connect(db_path)
    #     c = conn.cursor()
    #     #insert new subject
    #     combinedName = self.name + "-" + self.kana
    #     combinedDirthDate = str(self.bdYear) + "-" + str(self.bdMonth) + "-" + str(self.bdDay)
    #     subjectValues = (self.id, combinedName, combinedDirthDate,  self.sex, self.sleepingHours, self.height, self.weight, self.rightOrLeft, self.comment)
    #     c.execute("INSERT INTO Subject VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", subjectValues)
    #     #insert new evaluation
    #     evaluationDate = str(self.now.year) + "-" + str(self.now.month) + "-" + str(self.now.day) + " " + str(self.now.hour) +":"+str(self.now.minute)+":"+str(self.now.second)
    #     gameModeValues = (self.id, self.handOrFoot, self.gameMode.mode, self.gameMode.distraction, self.gameMode.level, evaluationDate,self.gameMode.feedBack)
    #     c.execute("INSERT INTO Evaluation(subjectId, handOrFoot, gameMode, distraction, level, evaluationDateTime, feedBack) VALUES (?, ?, ?, ?, ?, ?, ?)", gameModeValues)
    #
    #     conn.commit()
    #     conn.close()

