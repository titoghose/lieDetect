import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_data(name, num):
    plt.subplot(4, 1, num)
    data = pd.read_csv(name, sep='\t')

    # for i in data.keys():
    # 	print i

    # for i in data['StimulusName'].unique():
    # 	print i

    timestamp, indices = np.unique(data['SystemTimestamp (Epoc)'], return_index=True)

    eeg_avg = []
    for s in range(12):
        eeg_temp = []
        cnt = 0
        for ind, i in enumerate(indices):
            if data['StimulusName'][i] == 'Irrelevant_Secretary2-1-' + str(s + 1):
                cnt += 1
                if not np.isnan(data['O1/Pz (Epoc)'][i]):
                    eeg_temp.append(data['O1/Pz (Epoc)'][i])
                # t.append(timestamp[ind])
        if cnt >= 256:
            if len(eeg_avg) == 0:
                # print len(eeg_avg)
                eeg_avg = eeg_temp[:256]
            else:
                # print len(eeg_avg)
                # print len(eeg_temp[:256])
                eeg_avg = np.mean([eeg_avg, eeg_temp[:256]], axis=0)
        eeg_avg = np.clip(eeg_avg, 3500, 5000)
    eeg_avg = abs(np.fft.rfft(eeg_avg))
    plt.plot(eeg_avg[20:], label='Irrelevant_Sec')

    eeg_avg = []
    for s in range(12):
        eeg_temp = []
        cnt = 0
        for ind, i in enumerate(indices):
            if data['StimulusName'][i] == 'Jon_Secretary2-1-' + str(s + 1):
                cnt += 1
                if not np.isnan(data['O1/Pz (Epoc)'][i]):
                    eeg_temp.append(data['O1/Pz (Epoc)'][i])
                # t.append(timestamp[ind])
        if cnt >= 256:
            if len(eeg_avg) == 0:
                # print len(eeg_avg)
                eeg_avg = eeg_temp[:256]
            else:
                # print len(eeg_avg)
                # print len(eeg_temp[:256])
                eeg_avg = np.mean([eeg_avg, eeg_temp[:256]], axis=0)
        eeg_avg = np.clip(eeg_avg, 3500, 5000)
    eeg_avg = abs(np.fft.rfft(eeg_avg))
    plt.plot(eeg_avg[20:], label='Jon')

    eeg_avg = []
    for s in range(12):
        eeg_temp = []
        cnt = 0
        for ind, i in enumerate(indices):
            if data['StimulusName'][i] == 'Wallet-1-' + str(s + 1):
                cnt += 1
                if not np.isnan(data['O1/Pz (Epoc)'][i]):
                    eeg_temp.append(data['O1/Pz (Epoc)'][i])
                # t.append(timestamp[ind])
        if cnt >= 256:
            if len(eeg_avg) == 0:
                # print len(eeg_avg)
                eeg_avg = eeg_temp[:256]
            else:
                # print len(eeg_avg)
                # print len(eeg_temp[:256])
                eeg_avg = np.mean([eeg_avg, eeg_temp[:256]], axis=0)
        eeg_avg = np.clip(eeg_avg, 3500, 5000)
    eeg_avg = abs(np.fft.rfft(eeg_avg))
    plt.plot(eeg_avg[20:], label='Wallet')

    eeg_avg = []
    for s in range(12):
        eeg_temp = []
        cnt = 0
        for ind, i in enumerate(indices):
            if data['StimulusName'][i] == 'Irrelevant_Room-1-' + str(s + 1):
                cnt += 1
                if not np.isnan(data['O1/Pz (Epoc)'][i]):
                    eeg_temp.append(data['O1/Pz (Epoc)'][i])
                # t.append(timestamp[ind])
        if cnt >= 256:
            if len(eeg_avg) == 0:
                # print len(eeg_avg)
                eeg_avg = eeg_temp[:256]
            else:
                # print len(eeg_avg)
                # print len(eeg_temp[:256])
                eeg_avg = np.mean([eeg_avg, eeg_temp[:256]], axis=0)
        eeg_avg = np.clip(eeg_avg, 3500, 5000)

    eeg_avg = abs(np.fft.rfft(eeg_avg))
    plt.plot(eeg_avg[20:], label='Irrelevant_Room')

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    print name, "DONE"


plot_data('/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/012_Adhitan.txt', 1)
plot_data('/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/013_Omkar Prabhune.txt', 2)
plot_data('/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/014_Ranjith.txt', 3)
plot_data('/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/TestData/015_Ridhima Bector.txt', 4)

plt.show()
