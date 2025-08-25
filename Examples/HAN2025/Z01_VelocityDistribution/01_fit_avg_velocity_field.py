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
from G01_fitted_slope import FittedSlope
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
figtitles = ['fitted averaged_velocity_field']
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

first_im = None

for i in range(2):
    for j in range(3):
        case_number = i*3+j 
        for axes_number in range(len(axess)):
            ax = axess[axes_number][i,j]
            axconfig = myaxconfig(ax = ax)
            axconfig.title = cases[case_number]
            axconfig.xlable = xlables[axes_number]
            axconfig.ylable = ylables[axes_number]
            axconfig.ylim = ylims[axes_number]
            axconfig.xlim = xlims[axes_number]
            axconfig.apply()
        
        pBase.load_case(cases[case_number])
        a = FittedSlope(cases[case_number])
        a.load_fitted()

        central_x, central_y = pBase.CaseInfo.Central_Position_Grid
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom,up = pBase.CaseInfo.Effective_Range[1]

        
        'fig1'
        ax = axess[0][i,j]
        X = pBase.X[0][left:right,bottom:up].T
        Y = pBase.X[1][left:right,bottom:up].T
        U = a.fit_avg_U[0][left:right,bottom:up].T
        V = a.fit_avg_U[1][left:right,bottom:up].T
        magnitude = np.sqrt(U**2 + V**2)

        c = ax.imshow(magnitude, extent=[X.min(), X.max(), Y.min(), Y.max()], 
                                           cmap='viridis', origin='lower', interpolation='bicubic',
                                           vmin = global_min, vmax = global_max)
        if case_number == 0:
            first_im = c
        strm = ax.streamplot(X, Y, U, V, color='k', linewidth=1,density=(2,0.9),integration_direction='both')
        
        ax.plot(pBase.X[0][central_x,central_y], pBase.X[1][central_x,central_y],  marker='+', color='red', markersize=12)

        # plotted_x = np.array([-30, -30, 30,  30, -30]) + pBase.X[0][central_x,central_y]
        # plotted_y = np.array([-20,  20, 20, -20, -20]) + pBase.X[1][central_x,central_y]
        # ax.plot(plotted_x,plotted_y, color = 'red')

        # x1,y1 = pBase.X[0][central_x+10,central_y+10], pBase.X[1][central_x+10,central_y+10]
        # x2,y2 = pBase.X[0][central_x+17,central_y+17], pBase.X[1][central_x+17,central_y+17]
        # ax.plot([x1,x1,x2,x2,x1],[y2,y1,y1,y2,y2], color = 'y', linestyle = '-')

        

cbar_ax = figs[0].add_axes([0.25, 0.08, 0.5, 0.03])
figs[0].colorbar(first_im, cax=cbar_ax, orientation='horizontal', label=r'$|{\mathbf{U}}|$ (m/s)')

for fig_id in range(fig_number):
    fig = figs[fig_id]
    # fig.tight_layout()
    fig.subplots_adjust(left=0.06, right=0.94, top=0.95, bottom=0.15, wspace=0.3, hspace=0.3)
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:], bbox_inches='tight', pad_inches=0.05)
plt.clf()       