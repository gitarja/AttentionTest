from Controllers.DataProcessor import DataProcessor


filePath = "D:\\usr\\pras\\data\\AttentionTestData\\Collaboration\\Typical-Hoikuen\\AT_000049_gazeHeadPose.csv"
process = DataProcessor()

process.ProceedGameResult(gazeHeadPath=filePath)
process.computeGazeVTime()
print(process.computeGazeArea())