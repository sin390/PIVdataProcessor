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
from pivdataprocessor.A01_toolbox import WelfordStatisticsCalculator as WSC
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

xlables = [r'$x$ (mm)']
ylables = [r'$y$ (mm)']
xlims = [(-50,50)]
ylims = [(-35,35)]
figtitles = ['instanteneous_velocity_field']
figformat = '.jpg'


global_min = np.inf
global_max = -np.inf

for case in cases:
    pBase.load_case(case)
    left, right = pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]
    U = pBase.avg_U[0][left:right, bottom:up]
    V = pBase.avg_U[1][left:right, bottom:up]
    magnitude = np.sqrt(U**2 + V**2)
    global_min = min(global_min, magnitude.min())
    global_max = max(global_max, magnitude.max())

first_quiv = None

for i in range(2):
    for j in range(3):
        case_number = i*3 + j 
        for axes_number in range(len(axess)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax=ax)
            axconfig.title = cases[case_number]
            axconfig.xlable = xlables[axes_number]
            axconfig.ylable = ylables[axes_number]
            axconfig.ylim = ylims[axes_number]
            axconfig.xlim = xlims[axes_number]
            axconfig.apply()
        
        pBase.load_case(cases[case_number])
        central_x, central_y = pBase.CaseInfo.Central_Position_Flow
        left, right = pBase.CaseInfo.Effective_Range[0]
        bottom, up = pBase.CaseInfo.Effective_Range[1]

        # 'fig1'
        ax = axess[0][case_number]
        X = pBase.X[0][left:right, bottom:up]
        Y = pBase.X[1][left:right, bottom:up]
        U = pBase.U[0][left:right, bottom:up]
        V = pBase.U[1][left:right, bottom:up]
        magnitude = np.sqrt(U**2 + V**2)

        step = 3 
        quiv = ax.quiver(X[::step, ::step], Y[::step, ::step],
                         U[::step, ::step], V[::step, ::step],
                         magnitude[::step, ::step],
                         cmap='viridis', clim=(global_min, global_max), scale=1000)

        if case_number == 0:
            first_quiv = quiv

        ax.plot(pBase.X[0][central_x, central_y], pBase.X[1][central_x, central_y],
                marker='+', color='red', markersize=12)


cbar_ax = figs[0].add_axes([0.25, 0.08, 0.5, 0.03])
figs[0].colorbar(first_quiv, cax=cbar_ax, orientation='horizontal', label=r'$|{\mathbf{U}}|$ (m/s)')


for fig_id in range(fig_number):
    fig = figs[fig_id]
    # fig.tight_layout()
    fig.subplots_adjust(left=0.06, right=0.94, top=0.95, bottom=0.15, wspace=0.3, hspace=0.3)
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format='jpg')
plt.clf()       