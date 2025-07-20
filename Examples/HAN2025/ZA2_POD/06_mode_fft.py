''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.A01_toolbox import float_precsion
from G01_POD import POD

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(33), cm_to_inch(19))
# -------------------------------------------------------------------------
# endregion

fig_number = 1
figs, axess = generatefiglist(fig_number, 2, 3, figsize_inch)

xlables = [r'$f$ (Hz)']
ylables = [r'$Amplitude$']
axtitles = ['Mode 1', 'Mode 2', 'Mode 3', 'Mode 4', 'Mode 5', 'Mode 6']
figtitles = ['fft']
xlims = [(-50,50)]
ylims = [(-35,35)]
figformat = '.jpg'

for i in range(2):
    for j in range(3):
        case_number = i*3+j 
        for axes_number in range(len(axess)):
            ax = axess[axes_number][i,j]
            axconfig = myaxconfig(ax = ax)
            axconfig.title = axtitles[case_number]
            axconfig.xlable = xlables[0]
            axconfig.ylable = ylables[0]
            # axconfig.ylim = ylims[0]
            # axconfig.xlim = xlims[0]
            axconfig.apply()


for i in range(2):
    for j in range(3):
        mode_id = i*3 + j
        for case_id in range(len(cases)):
            pod = POD(cases[case_id])
            pod.PODload()
            ax = axess[0][i,j]
            a_t = pod.sigma[mode_id]*pod.VmatrixT[mode_id,:]
            N = len(a_t)
            window = np.hanning(N)
            a_t = a_t * window
            a_f = np.fft.fft(a_t)
            freq = np.fft.fftfreq(len(a_t),d=1/15)
            ax.plot(freq[:N//2], np.abs(a_f[:N//2])**2, color = mycolors[case_id], label = cases[case_id])
        




for fig_id in range(fig_number):
    for i in range(2):
        for j in range(3):
            axess[fig_id][i,j].legend()
    fig = figs[fig_id]
    fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format='jpg')
plt.clf()