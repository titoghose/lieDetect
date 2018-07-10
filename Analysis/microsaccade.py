import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import pandas as pd


def velocity(pos, freq=1000., factor=6.):
    vx = []
    vy = []

    # converting positions to velocities
    for i in range(2, len(pos['x']) - 2):
        vel_x = (pos['x'][i + 2] + pos['x'][i + 1] - pos['x'][i - 1] - pos['x'][i - 2]) / (freq * factor)
        vel_y = (pos['y'][i + 2] + pos['y'][i + 1] - pos['y'][i - 1] - pos['y'][i - 2]) / (freq * factor)
        vx.append(vel_x)
        vy.append(vel_y)

    return {'x': vx, 'y': vy}


def plot_micsacc(path):
    data = pd.read_csv(path, sep='\t')
    print data.keys()

    stimuli = []
    for i in range(1, 17):
        stimuli.append('Relevant'+str(i))

    for s in stimuli:
        print s

        timestamp = data['TimeSignal']
        glx = data['GazeLeftx']
        gly = data['GazeLefty']
        grx = data['GazeRightx']
        gry = data['GazeRighty']

        lx, ly, rx, ry = [], [], [], []

        for ind, i in enumerate(timestamp):
            if grx[ind] >= 0 and gry[ind] >= 0 and glx[ind] >= 0 and gly[ind] >= 0 and data['GazeEventType'][ind] != 'Saccade' and data['StimulusName'][ind] == s:
                print data['StimulusName'][ind], data['GazeEventType'][ind]
                lx.append(glx[ind])
                ly.append(gly[ind])
                rx.append(grx[ind])
                ry.append(gry[ind])

        vell = velocity({'x': lx, 'y': ly})
        velr = velocity({'x': rx, 'y': ry})

        # finding threshold points
        medxl = np.median(vell['x'])
        medyl = np.median(vell['y'])
        # msdxl = np.sqrt(np.median(np.square(vell['x'] - medxl)))
        # msdyl = np.sqrt(np.median(np.square(vell['y'] - medyl)))
        msdxl = np.sqrt(np.mean(np.square(vell['x'])) - np.square(np.mean(vell['x'])))
        msdyl = np.sqrt(np.mean(np.square(vell['y'])) - np.square(np.mean(vell['y'])))
        # medxr = np.median(velr['x'])
        # medyr = np.median(velr['y'])
        # msdxr = np.sqrt(np.median(np.square(velr['x'] - medxr)))
        # msdyr = np.sqrt(np.median(np.square(velr['y'] - medyr)))

        # msdx2 = np.sqrt(np.mean(np.square(gaze_vel_x)) - np.square(np.mean(gaze_vel_x)))
        # msdy2 = np.sqrt(np.mean(np.square(gaze_vel_y)) - np.square(np.mean(gaze_vel_y)))

        radxl = msdxl * 6.
        radyl = msdyl * 6.
        # radxr = msdxr * 6.
        # radyr = msdyr * 6.

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.plot(lx, ly)
        # ax1.scatter(sac_x, sac_y, marker='.')

        ells = Ellipse(xy=(0, 0), width=radxl, height=radyl, color='r', linestyle='dashed', fill=False, zorder=2)
        ax2 = fig.add_subplot(1, 2, 2)
        # ax2.add_artist(ells2)
        ax2.plot(vell['x'], vell['y'], color='g', lw=0.2, zorder=1)
        ax2.add_artist(ells)
        # ax2.scatter(m_x, m_y, color='r')
        # ax2.scatter(sac_vel_x, sac_vel_y, color='k', marker='x')
        
        fig.savefig(fname=str(data['Name'][0] + '_' + str(s)), dpi=fig.dpi)
        # plt.show()


path1 = '/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/IVTData/Guilty/002_Cheok Kah Jie.txt'
path2 = '/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/IVTData/Guilty/005_Limjin Yong.txt'
path3 = '/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/IVTData/Innocent/001_Joel Tan.txt'
path4 = '/home/upamanyu/Documents/FinalExp/22-06-18 Final Experiment/IVTData/Innocent/008_Lee Sze Inn.txt'
try:
    plot_micsacc(path1)
except Exception:
    None

try:
    plot_micsacc(path2)
except Exception:
    None

try:
    plot_micsacc(path3)
except Exception:
    None

try:
    plot_micsacc(path4)
except Exception:
    None