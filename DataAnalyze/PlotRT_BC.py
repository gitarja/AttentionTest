import matplotlib.pyplot as plt
import  numpy as np


# #Cluster plotting

mean_c1 = np.array([435.5216852,433.6005814,430.3127076,432.544398,435.2702439,437.9321449,438.9365067,436.780513,436.2767187,446.8718993])
std_c1= np.array([47.1932631,45.1709956,40.61890428,44.61066643,43.71133458,43.49355554,44.00506348,47.71510572,48.35833185,48.35225427])

mean_c2 = np.array([483.119564,474.6947169,471.8533784,476.4817892,478.8096513,484.5178811,488.3063424,483.1928318,484.184395,487.7453528])
std_c2= np.array([56.3380799,60.08993621,55.09579847,65.56965754,56.07305896,66.44605172,58.3980325,59.17977935,69.05309578,66.21558376])


times = np.arange(1, 11)
ylim = [350, 560]
plt.subplot(2, 1, 1)
plt.title("First cluster")

plt.plot(times, mean_c1, color="#1b9e77", label="Average RT")
plt.fill_between(times, mean_c1 + std_c1, mean_c1 - std_c1, alpha=0.5, color="#1b9e77")
plt.ylim(ylim)
# plt.xlabel("Minutes")
plt.ylabel("ms")
# plt.legend(loc='lower center')

plt.subplot(2, 1, 2)
plt.title("Second cluster")
plt.plot(times, mean_c2, color="#d95f02", label="Average RT")
plt.fill_between(times, mean_c2 + std_c2, mean_c2 - std_c2, alpha=0.5, color="#d95f02")
plt.ylim(ylim)
plt.xlabel("Minutes")
plt.ylabel("ms")
# plt.legend(loc='lower center')
plt.savefig("D:\\usr\\pras\\data\\googledrive\\Conferences & Journal\\CBMS2020\\figures\\clusters_response.png")

#Rehabilitation

# #ASD
# mean_c1 = np.array([557.61,623.3270968,572.7903226])
# std_c1= np.array([218.9090576,146.9631374,180.7135272])
#
# mean_c2 = np.array([426.7716667,485.1342308,472.6117647])
# std_c2= np.array([149.2,391.4676312,249.5261162])
#
# mean_c3 = np.array([450.7340541,491.4869697,504.3964286])
# std_c3= np.array([60.86635423,69.12426543,81.69771511])
#
# mean_c4 = np.array([467.7108966,453.5811429,482.134375])
# std_c4 = np.array([83.26285859,82.3912783,80.00261129])
#
# #Typical
# mean_t1 = np.array([463.7199032,509.9074359,510.9837838])
# std_t1= np.array([48.49039657,111.0693867,81.50531855])
#
# mean_t2 = np.array([563.3371935,524.515641,583.8085714])
# std_t2= np.array([109.4438709,149.4066057,112.3224805])
#
#
# times = np.arange(1, 4)
# ylim = [100, 900]
# plt.subplot(6, 1, 1)
# # plt.title("Before Rehab")
#
# plt.plot(times, mean_c1, color="#1b9e77", label="Average RT")
# plt.fill_between(times, mean_c1 + std_c1, mean_c1 - std_c1, alpha=0.5, color="#1b9e77")
# plt.ylim(ylim)
# # plt.xlabel("Minutes")
# plt.ylabel("ms")
# # plt.legend(loc='lower center')
#
# plt.subplot(6, 1, 2)
# # plt.title("1st Rehab")
# plt.plot(times, mean_c2, color="#d95f02", label="Average RT")
# plt.fill_between(times, mean_c2 + std_c2, mean_c2 - std_c2, alpha=0.5, color="#d95f02")
# plt.ylim(ylim)
# # plt.xlabel("Minutes")
# plt.ylabel("ms")
# # plt.legend(loc='lower center')
#
# plt.subplot(6, 1, 3)
# # plt.title("2nd Rehab")
# plt.plot(times, mean_c3, color="#d95f02", label="Average RT")
# plt.fill_between(times, mean_c3 + std_c3, mean_c3 - std_c3, alpha=0.5, color="#d95f02")
# plt.ylim(ylim)
# # plt.xlabel("Minutes")
# plt.ylabel("ms")
#
#
# # plt.legend(loc='lower center')
#
# plt.subplot(6, 1, 4)
# # plt.title("3rd Rehab")
# plt.plot(times, mean_c4, color="#d95f02", label="Average RT")
# plt.fill_between(times, mean_c4 + std_c4, mean_c4 - std_c4, alpha=0.5, color="#d95f02")
# plt.ylim(ylim)
# # plt.xlabel("Minutes")
# plt.ylabel("ms")
#
#
# plt.subplot(6, 1, 5)
# # plt.title("1st Typical")
# plt.plot(times, mean_c2, color="#7570b3", label="Average RT")
# plt.fill_between(times, mean_t1 + std_t1, mean_t1 - std_t1, alpha=0.5, color="#7570b3")
# plt.ylim(ylim)
# # plt.xlabel("Minutes")
# plt.ylabel("ms")
#
# plt.subplot(6, 1, 6)
# # plt.title("2nd Typical")
# plt.plot(times, mean_c3, color="#7570b3", label="Average RT")
# plt.fill_between(times, mean_t2 + std_t2, mean_t2 - std_t2, alpha=0.5, color="#7570b3")
# plt.ylim(ylim)
# plt.xlabel("Minutes")
# plt.ylabel("ms")
# # plt.legend(loc='lower center')
#
# plt.savefig("D:\\usr\\pras\\data\\googledrive\\Conferences & Journal\\CBMS2020\\figures\\typical_disorder.png")



plt.show()
