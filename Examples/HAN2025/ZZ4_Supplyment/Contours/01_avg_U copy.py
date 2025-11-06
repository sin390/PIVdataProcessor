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

cases = ['Case01XZ_Y0_Ethanol', 'Case01XY_Z0_Ethanol', 'Case01XY_Z12_Ethanol']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(16), cm_to_inch(6))
# -------------------------------------------------------------------------
# endregion

fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 3, figsize_inch)
first_im = [None for _ in range(fig_number)]

cases_title = cases
d_array_nozzle = 12  # mm
Uin = 404     # m/s
xlables = [r'$x/d_{a}$', r'$x/d_{a}$', r'$x/d_{a}$']
ylables = [r'$z/d_{a}$', r'$y/d_{a}$', r'$y/d_{a}$']
xlims = [(-4,4)]
xtricks = [-4,-2,0,2,4]
ylims = [(-2.3,2.3)]
ytricks = [-2,0,2]

# xlims = [(-3,3)]
# xtricks = [-3,-1.5,0,1.5,3]
# ylims = [(-1.8,1.8)]
# ytricks = [-1.5,0,1.5]

figtitles = ['averaged_velocity_field']
figformat = '.pdf'

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
    print(f'abs(U)max = {global_max:.3f} m/s')

global_min = 0
global_max = 45

for axes_number in range(len(cases)):
    ax = axess[0][axes_number]
    axconfig = myaxconfig(ax = ax)
    # axconfig.title = cases_title[case_number]
    axconfig.xlable = xlables[axes_number]
    axconfig.ylable = ylables[axes_number]
    axconfig.ylim = ylims[0]
    axconfig.xlim = xlims[0]
    axconfig.xticks = xtricks
    axconfig.yticks = ytricks
    axconfig.apply()
    ax.set_ylabel(ax.get_ylabel(), labelpad=-4)
    ax.set_aspect('equal', adjustable='box')

for i in range(1):
    for j in range(3):
        case_number = i*3+j     
        pBase.load_case(cases[case_number])
        central_x, central_y = pBase.CaseInfo.Central_Position_Flow
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom,up = pBase.CaseInfo.Effective_Range[1]     
        'fig1'
        ax = axess[0][case_number]
        X = pBase.X[0][left:right,bottom:up]/d_array_nozzle
        X = X.T
        Y = pBase.X[1][left:right,bottom:up]/d_array_nozzle
        Y = Y.T
        U = pBase.avg_U[0][left:right,bottom:up].T
        V = pBase.avg_U[1][left:right,bottom:up].T
        magnitude = np.sqrt(U**2 + V**2) / Uin

        c = ax.imshow(magnitude, extent=[X.min(), X.max(), Y.min(), Y.max()], 
                                           cmap='turbo', origin='lower', interpolation='bicubic',
                                           vmin = global_min/Uin, vmax = global_max/Uin)
        if case_number == 0:
            first_im[0] = c
        density = [(0.5, 0.4),(0.6, 0.5),(0.6, 0.5),
                   (0.5, 0.4),(0.6, 0.5),(0.6, 0.5)]
        density = [(0.5, 0.4),(0.5, 0.4),(0.5, 0.4)]
        strm = ax.streamplot(X, Y, U, V, color='k', linewidth=0.5, arrowsize=0.6, density=density[case_number],integration_direction='both')
        
        ax.plot(pBase.X[0][central_x,central_y]/d_array_nozzle, pBase.X[1][central_x,central_y]/d_array_nozzle,  marker='+', color='red', markersize=6)


        # x1,y1 = pBase.X[0][central_x+10,central_y+10], pBase.X[1][central_x+10,central_y+10]
        # x2,y2 = pBase.X[0][central_x+17,central_y+17], pBase.X[1][central_x+17,central_y+17]
        # ax.plot([x1,x1,x2,x2,x1],[y2,y1,y1,y2,y2], color = 'y', linestyle = '-')


colorbarlabels = [r'$\left|{\langle \mathbf{U}} \rangle\right| / U_{in}$']
# colorbarticks = [0, 10, 20, 30, 40, 45]
for fig_id in range(fig_number):
    cbar_ax = figs[fig_id].add_axes([0.2, 0.2, 0.6, 0.03])
    colorbar = figs[fig_id].colorbar(first_im[fig_id], cax=cbar_ax, orientation='horizontal', label=colorbarlabels[fig_id])
    colorbar.set_label(colorbarlabels[fig_id], fontsize=12)
    colorbar.ax.minorticks_off()
    # colorbar.ax.set_xticks(colorbarticks)
    fig = figs[fig_id]
 
    label_index = ['a','b','c','d','e','f']
    for i, ax in enumerate(axess[fig_id]):
        if i < len(label_index):
            ax.text(-0.25, 1.2, fr'$\textbf{{({label_index[i]})}}$',
                    transform=ax.transAxes,
                    fontsize=12, fontweight='bold',
                    va='top', ha='left')  

    fig.subplots_adjust(left=0.1, right=0.93, top=0.95, bottom=0.37, wspace=0.3, hspace=0.1)
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:])
plt.clf()       