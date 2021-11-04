import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
import seaborn as sns; sns.set(color_codes=True)
from datetime import datetime


path = 'D:\\usr\\pras\\data\\AttentionTestData\\Yokodai\\AttentionTest\\Results\\EvaluationResults\\'
extension = 'yml'
os.chdir(path)
files = glob.glob('*.{}'.format(extension))
data = pd.DataFrame(columns=["id", "name", "sex", "sleepingHours", "handOrFoot", "leftOrRight", "mode", "age"])
i = 0
for file in files:
    with open(os.path.join(path, file), 'r', encoding='utf8', errors='ignore') as f:
        subject = yaml.load(f)
        birthDate = datetime(subject["birthDate"]["year"], subject["birthDate"]["month"], subject["birthDate"]["day"])
        evaluationDate = datetime(subject["evaluationDate"]["year"], subject["evaluationDate"]["month"], subject["evaluationDate"]["day"])
        age = evaluationDate - birthDate
        data.loc[i] = [subject["id"], subject["fullName"]["name"], subject["sex"], subject["sleepingHours"].split(" ")[0], subject["handOrFoot"], subject["rightOrLeft"], subject["gameMode"]["mode"], age.days/365]
        i+= 1

data.to_csv(os.path.join(path, "summary.csv"))
print(data)