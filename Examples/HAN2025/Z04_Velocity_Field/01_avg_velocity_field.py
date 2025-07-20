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
figsize_inch = (cm_to_inch(16), cm_to_inch(10))
# -------------------------------------------------------------------------
# endregion

fig_number = 1
figs, axess = generatefiglist(fig_number, 2, 3, figsize_inch)
first_im = [None for _ in range(fig_number)]

cases_title = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']
xlables = [r'$x$ (mm)']
ylables = [r'$y$ (mm)']
xlims = [(-45,45)]
xtricks = [-40,-20,0,20,40]
ylims = [(-28,28)]
ytricks = [-20,0,20]
figtitles = ['averaged_velocity_field']
figformat = '.eps'



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


for i in range(2):
    for j in range(3):
        case_number = i*3+j 
        for axes_number in range(len(axess)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax = ax)
            # axconfig.title = cases_title[case_number]
            if i == 1:
                axconfig.xlable = xlables[axes_number]
            if j == 0:
                axconfig.ylable = ylables[axes_number]
            axconfig.ylim = ylims[axes_number]
            axconfig.xlim = xlims[axes_number]
            axconfig.xticks = xtricks
            axconfig.yticks = ytricks
            axconfig.apply()
            ax.set_ylabel(ax.get_ylabel(), labelpad=-4)
            ax.set_aspect('equal', adjustable='box')
        
    
        pBase.load_case(cases[case_number])

        central_x, central_y = pBase.CaseInfo.Central_Position_Flow
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom,up = pBase.CaseInfo.Effective_Range[1]

        
        'fig1'
        ax = axess[0][case_number]
        X = pBase.X[0][left:right,bottom:up].T
        Y = pBase.X[1][left:right,bottom:up].T
        U = pBase.avg_U[0][left:right,bottom:up].T
        V = pBase.avg_U[1][left:right,bottom:up].T
        magnitude = np.sqrt(U**2 + V**2)

        c = ax.imshow(magnitude, extent=[X.min(), X.max(), Y.min(), Y.max()], 
                                           cmap='viridis', origin='lower', interpolation='bicubic',
                                           vmin = global_min, vmax = global_max)
        if case_number == 0:
            first_im[0] = c
        density = [(0.5, 0.4),(0.6, 0.5),(0.6, 0.5),
                   (0.5, 0.4),(0.6, 0.5),(0.6, 0.5)]
        strm = ax.streamplot(X, Y, U, V, color='k', linewidth=0.8, arrowsize=0.8, density=density[case_number],integration_direction='both')
        
        ax.plot(pBase.X[0][central_x,central_y], pBase.X[1][central_x,central_y],  marker='+', color='red', markersize=6)


        # x1,y1 = pBase.X[0][central_x+10,central_y+10], pBase.X[1][central_x+10,central_y+10]
        # x2,y2 = pBase.X[0][central_x+17,central_y+17], pBase.X[1][central_x+17,central_y+17]
        # ax.plot([x1,x1,x2,x2,x1],[y2,y1,y1,y2,y2], color = 'y', linestyle = '-')


colorbarlabels = [r'$\left|{\langle \mathbf{U}} \rangle\right|$ (m/s)']
# colorbarticks = [0, 10, 20, 30, 40, 45]
for fig_id in range(fig_number):
    cbar_ax = figs[fig_id].add_axes([0.25, 0.13, 0.5, 0.03])
    colorbar = figs[fig_id].colorbar(first_im[fig_id], cax=cbar_ax, orientation='horizontal', label=colorbarlabels[fig_id])
    colorbar.set_label(colorbarlabels[fig_id], fontsize=12)
    colorbar.ax.minorticks_off()
    # colorbar.ax.set_xticks(colorbarticks)
    fig = figs[fig_id]
 
    label_index = ['a','b','c','d','e','f']
    for i, ax in enumerate(axess[fig_id]):
        if i < len(label_index):
            ax.text(-0.2, 1.2, fr'$\textbf{{({label_index[i]})}}$',
                    transform=ax.transAxes,
                    fontsize=12, fontweight='bold',
                    va='top', ha='left')  

    fig.subplots_adjust(left=0.07, right=0.93, top=0.95, bottom=0.25, wspace=0.3, hspace=0.1)
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:])
plt.clf()       