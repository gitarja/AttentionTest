import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
rt_length = 3
path = "D:\\usr\\pras\\data\\AttentionTestData\\TypicalVsHoikuen\\"
file = "Hoikuen-High-Risk.csv"
data = pd.read_csv(path+file)

subjects = data.iloc[:, 0].values
rt = data.iloc[:, 1:1+rt_length].values
rt_var = data.iloc[:, 1+rt_length:1+(rt_length*2)].values

times = np.arange(1, rt_length+1)
ylim = [-100, 900]

#colors
typical_col = "#4daf4a"
highrisk_col = "#e41a1c"
i=1
for s in subjects:
    plt.title(s)
    #plt.subplot(len(subjects), 1, i)
    plt.plot(times, rt[i-1], color=highrisk_col, label="Average RT")
    plt.fill_between(times, rt[i-1] + rt_var[i-1], rt[i-1] - rt_var[i-1], alpha=0.5, color=highrisk_col)
    plt.ylim(ylim)
    plt.xlabel("Minutes")
    plt.ylabel("ms")
    i+=1
    plt.savefig(path+"subject_"+s+".png")
    plt.close()

