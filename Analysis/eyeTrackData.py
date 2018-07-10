import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def plot_blinks(name, n, N):
    print name
    data = pd.read_csv(name, sep='\t')
    # plt.subplot(N, 1, n)
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
                rel_follow_stim.append(stim_innocent[i + 1])
            except Exception:
                rel_follow_stim.append('NA')

    for i in range(len(rel_stim)):
        print rel_stim[i], '\t\t', rel_follow_stim[i]

    final_rel = []
    final_rel_follow = []

    prev_rel = 0

    try:
        for ind, j in enumerate(rel_stim):

            end_ind = 10000000
            prev1, prev2 = -1, -1
            cnt1 = 0
            cnt2 = 0
            temp_rel = 0
            temp_rel_follow = 0

            i = prev_rel
            while True:
                if data['StimulusName'][i] != j and i > end_ind:
                    break
                while data['StimulusName'][i] == j:
                    if data['PupilLeft'][i] == -1 and prev1 != -1 and cnt1 <= 300:
                        temp_rel += 1
                        cnt1 = 0
                    elif data['PupilLeft'][i] == -1 and prev1 == -1:
                        cnt1 += 1

                    prev1 = data['PupilLeft'][i]
                    i += 1
                    end_ind = i
                i += 1
            print "***************************************************************************"

            k = end_ind
            while k < end_ind + 10000:
                if data['PupilLeft'][k] == -1 and prev2 != -1 and cnt2 <= 300:
                    temp_rel_follow += 1
                    cnt1 = 0
                elif data['PupilLeft'][k] == -1 and prev2 == -1:
                    cnt2 += 1
                prev2 = data['PupilLeft'][k]
                k += 1
            print j, end_ind, k

            final_rel.append(temp_rel)
            final_rel_follow.append(temp_rel_follow)
            prev_rel = end_ind
    except Exception:
        None

    # plt.bar(np.arange(len(final_rel)), final_rel, label='Relevant', alpha=0.5)
    # plt.bar(np.arange(len(final_rel_follow)), final_rel_follow, label='Relevant Follow', alpha=0.5)
    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    return final_rel, final_rel_follow


guilty_folder = '/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/Guilty/'
guilty_blinks = 0
guilty_blinks_after = 0
cnt1 = 0.
for i in os.listdir(guilty_folder):
    cnt1 += 1.
    x, y = plot_blinks(guilty_folder + i, None, None)
    guilty_blinks += np.sum(x) / float(len(x))
    guilty_blinks_after += np.sum(y) / float(len(y))

innocent_blinks = 0
innocent_blinks_after = 0
cnt2 = 0.
innocent_folder = '/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/Innocent/'
for i in os.listdir(innocent_folder):
    cnt2 += 1.
    x, y = plot_blinks(innocent_folder + i, None, None)
    innocent_blinks += np.sum(x) / float(len(x))
    innocent_blinks_after += np.sum(y) / float(len(y))

print guilty_blinks / cnt1, guilty_blinks_after / cnt1
print innocent_blinks / cnt2, innocent_blinks_after / cnt2

# plot_blinks('/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/007_Justin Wong Jingjie.txt', 1, 2)
# plot_blinks('/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/003_Xue Hao Ran.txt', 2, 2)
# plt.show()
