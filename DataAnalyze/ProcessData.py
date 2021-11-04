from Controllers.DataProcessor import DataProcessor
import os
import glob


# path = 'D:\\usr\\pras\\data\\AttentionTestData\\Hiroshima\\result\\'
# path = "D:\\usr\\pras\\data\\AttentionTestData\\Yokodai\\AttentionTest\\result\\"
path = "D:\\usr\\pras\\data\\AttentionTestData\\Hoikuen(2020-01-24)\\results\\"
extension = '_gameResults.csv'
os.chdir(path)
files = glob.glob('*{}'.format(extension))

process = DataProcessor()
for file in files:
    filePath = os.path.join(path, file)
    process.ProceedGameResult(filePath)
    data = process.responseGaze(reponse=4)
    processedFile = data.to_csv(os.path.join(path, file))


