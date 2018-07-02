import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/007_Justin Wong Jingjie.txt', sep='\t')
# data_guilty = pd.read_csv('/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/007_Justin Wong Jingjie.txt', sep='\t', verbose=True)

# for i in data.keys():
	# print i

stim_innocent = data['StimulusName'].unique()
# stim_guilty = data_guilty['StimulusName'].unique()

rel_stim = []
rel_follow_stim = []

for i in range(len(stim_innocent)):
	if 'Relevant' in stim_innocent[i]:
		rel_stim.append(stim_innocent[i])
		try:
			rel_follow_stim.append(stim_innocent[i+1])
		except Exception:
			rel_follow_stim.append('NA')

for i in range(len(rel_stim)):
	print rel_stim[i], '\t\t', rel_follow_stim[i]	

final_rel = []
final_rel_follow = []

for ind, j in enumerate(rel_stim):
	prev1, prev2 = -1, -1
	cnt1 = 0
	cnt2 = 0
	temp_rel = 0
	temp_rel_follow = 0
	for i, d in enumerate(data['PupilLeft']):
		if data['StimulusName'][i] == j:
			if d == -1 and prev1 != -1 and cnt1 <= 300:
				temp_rel += 1
				cnt1 = 0
			elif d==-1 and prev1 == -1:
				cnt1 += 1
			prev1 = d

		elif data['StimulusName'][i] == rel_follow_stim[ind]:
			if d == -1 and prev2 != -1 and cnt2 <= 300:
				temp_rel_follow += 1
				cnt2 = 0

			elif d == -1 and prev2 == -1:
				cnt2 += 1
			prev2 = d
	
	final_rel.append(temp_rel)
	final_rel_follow.append(temp_rel_follow)
	
plt.subplot(211)
plt.plot(final_rel, label='Relevant')
plt.subplot(212)
plt.plot(final_rel_follow, label='Relevant Follow')
plt.show()