import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os


def preprocess(df):
    print df.shape

    df.loc[:, 'Fixation'] = df['FixationSeq']
    df.loc[df.query('GazeEventType == "Fixation"').index, 'Fixation'] = 1
    df.loc[df.query('GazeEventType == "Unclassified"').index, 'Fixation'] = 1
    df.loc[df.query('GazeEventType == "Saccade"').index, 'Fixation'] = 0
    df.loc[df.query('GazeLeftx == -1').index, 'Fixation'] = 0
    df.loc[df.query('GazeLefty == -1').index, 'Fixation'] = 0
    df.loc[df.query('GazeRightx == -1').index, 'Fixation'] = 0
    df.loc[df.query('GazeRighty == -1').index, 'Fixation'] = 0

    sacc_start_ind = []
    sacc_end_ind = []
    stim = df['StimulusName'].unique()

    offset = 0
    for s in stim:
        sacc_start = df.loc[df.query('StimulusName == "{0}"'.format(s)).index, 'SaccadeStart'] + 1
        sacc_dur = df.loc[df.query('StimulusName == "{0}"'.format(s)).index, 'SaccadeDuration']
        sacc_start = np.nan_to_num(sacc_start)
        sacc_dur = np.nan_to_num(sacc_dur)
        temp_start, ind_start = np.unique(sacc_start, return_index=True)
        temp_dur, ind_dur = np.unique(sacc_dur, return_index=True)

        for t, i in zip(temp_start, ind_start):
            if t != 0:
                sacc_start_ind.append(i + offset)
                sacc_end_ind.append(int(i + sacc_dur[i] + offset))

        offset += len(sacc_start)

    for i in sacc_end_ind:
        df.loc[i:i + 40, 'Fixation'] = 0

    for i in sacc_start_ind:
        df.loc[i - 8:i, 'Fixation'] = 0

    print("Preprocessed")
    return df
    # print len(sacc_start_ind), len(sacc_end_ind)


def velocity(df, freq=1000.):
    df.loc[:, 'VelocityLeftx'] = df['FixationX']
    df.loc[:, 'VelocityLefty'] = df['FixationY']
    df.loc[:, 'VelocityRightx'] = df['FixationX']
    df.loc[:, 'VelocityRighty'] = df['FixationY']

    # converting positions to velocities
    df.loc[:, 'GazeLeftx'] = np.nan_to_num(df.loc[:, 'GazeLeftx'])
    df.loc[:, 'GazeLefty'] = np.nan_to_num(df.loc[:, 'GazeLefty'])
    df.loc[:, 'GazeRightx'] = np.nan_to_num(df.loc[:, 'GazeRightx'])
    df.loc[:, 'GazeRighty'] = np.nan_to_num(df.loc[:, 'GazeRighty'])

    N = len(df['Fixation'])
    for eye in ['Left', 'Right']:
        for coord in ['x', 'y']:
            a = [x for x in df['Gaze{0}{1}'.format(eye, coord)][4:N]]
            b = [x for x in df['Gaze{0}{1}'.format(eye, coord)][3:N - 1]]
            c = [x for x in df['Gaze{0}{1}'.format(eye, coord)][1:N - 3]]
            d = [x for x in df['Gaze{0}{1}'.format(eye, coord)][0:N - 4]]
            e = np.subtract(np.add(a, b), np.add(c, d))

            df.loc[2:N - 3, 'Velocity{0}{1}'.format(eye, coord)] = e * (freq / 6.)
            df[1, 'Velocity{0}{1}'.format(eye, coord)] = (df['Gaze{0}{1}'.format(eye, coord)][2] - df['Gaze{0}{1}'.format(eye, coord)][0]) * (freq / 2.)
            df[N - 2, 'Velocity{0}{1}'.format(eye, coord)] = (df['Gaze{0}{1}'.format(eye, coord)][N - 1] - df['Gaze{0}{1}'.format(eye, coord)][N - 3]) * (freq / 2.)

    print("Found Velocities")
    return df


def plotGazeVel(df):
    for ind in range(1, 16):
        right_x = df.loc[df.query('StimulusName == "Relevant{0}" and Fixation == 1'.format(str(ind))).index, 'GazeRightx']
        left_x = df.loc[df.query('StimulusName == "Relevant{0}" and Fixation == 1'.format(str(ind))).index, 'GazeLeftx']
        right_y = df.loc[df.query('StimulusName == "Relevant{0}" and Fixation == 1'.format(str(ind))).index, 'GazeRighty']
        left_y = df.loc[df.query('StimulusName == "Relevant{0}" and Fixation == 1'.format(str(ind))).index, 'GazeLefty']

        right_vel_x = df.loc[df.query('StimulusName == "Relevant{0}" and Fixation == 1'.format(str(ind))).index, 'VelocityRightx']
        left_vel_x = df.loc[df.query('StimulusName == "Relevant{0}" and Fixation == 1'.format(str(ind))).index, 'VelocityLeftx']
        right_vel_y = df.loc[df.query('StimulusName == "Relevant{0}" and Fixation == 1'.format(str(ind))).index, 'VelocityRighty']
        left_vel_y = df.loc[df.query('StimulusName == "Relevant{0}" and Fixation == 1'.format(str(ind))).index, 'VelocityLefty']

        # a = plt.subplot(221)
        # plt.plot(right_x)
        # b = plt.subplot(222)
        # plt.plot(right_y)
        # c = plt.subplot(223)
        # plt.plot(left_x)
        # d = plt.subplot(224)
        # plt.plot(left_y)
        plt.subplot(121)
        plt.plot(right_x, right_y)
        plt.plot(left_x, left_y)
        plt.subplot(122)
        plt.plot(right_vel_x, right_vel_y)
        plt.plot(left_vel_x, left_vel_y)
        plt.show()


data = pd.read_csv('/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/IVTData/Guilty/002_Cheok Kah Jie.txt', sep='\t')
print data.keys()

data = data[['GazeEventType', 'Timestamp', 'StimulusName', 'GazeRightx', 'GazeRighty', 'GazeLeftx', 'GazeLefty', 'SaccadeSeq', 'SaccadeStart', 'SaccadeDuration', 'FixationSeq', 'FixationX',
             'FixationY', 'FixationStart', 'FixationDuration']]

data = preprocess(data)
data = velocity(data)
plotGazeVel(data)
