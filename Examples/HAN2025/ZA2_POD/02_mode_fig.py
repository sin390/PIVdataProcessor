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

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06','Mori465']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(33), cm_to_inch(19))
# -------------------------------------------------------------------------
# endregion

fig_number = 7
figs, axess = generatefiglist(fig_number, 2, 3, figsize_inch)

xlables = [r'$x$ (mm)']
ylables = [r'$y$ (mm)']
axtitles = ['Mode 1', 'Mode 2', 'Mode 3', 'Mode 4', 'Mode 5', 'Mode 6']
figtitles = cases
xlims = [(-50,50)]
ylims = [(-35,35)]
figformat = '.jpg'

for i in range(2):
    for j in range(3):
        case_number = i*3+j 
        for axes_number in range(len(axess)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax = ax)
            axconfig.title = axtitles[case_number]
            axconfig.xlable = xlables[0]
            axconfig.ylable = ylables[0]
            axconfig.ylim = ylims[0]
            axconfig.xlim = xlims[0]
            axconfig.apply()

for case_id in range(fig_number):
    pod = POD(cases[case_id])
    pod.PODload()

    central_x, central_y = pBase.CaseInfo.Central_Position_Flow
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    X = pod.POD_X[0].T
    Y = pod.POD_X[1].T

    magmax = 0
    magmin = 0

    for i in range(2):
        for j in range(3):
            mode_id = i*3 + j
            ax = axess[case_id][mode_id]
            pod_uv = pod.singlePODmode(mode_id)
            pod_u = pod_uv[0].T
            pod_v = pod_uv[1].T
            magnitude = np.sqrt(pod_u**2 + pod_v**2)
            if mode_id == 0:
                magmax = magnitude.max()
                magmin = 0
            c = ax.imshow(magnitude, extent=[X.min(), X.max(), Y.min(), Y.max()], 
                                    cmap='viridis', origin='lower', interpolation='bicubic',
                                    vmax = magmax, vmin = magmin)
            if mode_id == 0:
                first_im=c
            strm = ax.streamplot(X, Y, pod_u, pod_v, color='k', linewidth=1,density=(2,0.9),integration_direction='both')
            # ax.plot(pBase.X[0][central_x,central_y], pBase.X[1][central_x,central_y],  marker='+', color='red', markersize=12)            
    # cbar_ax = figs[case_id].add_axes([0.25, 0.08, 0.5, 0.03])
    # figs[case_id].colorbar(first_im, cax=cbar_ax, orientation='horizontal', label=r'$|{\mathbf{U}}|$ (m/s)')

for fig_id in range(fig_number):
    fig = figs[fig_id]
    fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format='jpg')
plt.clf()