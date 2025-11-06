''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.A01_toolbox import WelfordStatisticsCalculator as WSC
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist
from Z01_VelocityDistribution.G01_fitted_slope import FittedSlope

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

cases_title = cases
d_array_nozzle = 12  # mm
Uin = 404     # m/s
xlables = [r'$x/d_{a}$',r'$x/d_{a}$',r'$x/d_{a}$']
ylables = [r'$z/d_{a}$',r'$y/d_{a}$',r'$y/d_{a}$']
xlims = [(-4,4)]
xtricks = [-4,-2,0,2,4]
ylims = [(-2.3,2.3)]
ytricks = [-2,0,2]
vmin, vmax = 0.25,0.75


colorbarlabels = [r'$-A_{33}/A_{11}$, $-A_{22}/A_{11}$']
figtitles = ['S33_S11']
figformat = '.pdf'

first_im = [None for _ in range(fig_number)]
max_values = np.zeros(shape=(fig_number,6))
min_values = np.zeros(shape=(fig_number,6))

for case_number in range(len(cases)):
    ax = axess[0][case_number]
    axconfig = myaxconfig(ax = ax)
    # axconfig.title = cases_title[case_number]
    axconfig.xlable = xlables[case_number]
    axconfig.ylable = ylables[case_number]
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
        fs = FittedSlope(cases[case_number])
        fs.load_fitted()

        central_x, central_y = pBase.CaseInfo.Central_Position_Grid
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom,up = pBase.CaseInfo.Effective_Range[1]

        
        fig_id = 0
        ax = axess[fig_id][case_number]
        X = pBase.X[0][left:right,bottom:up]/d_array_nozzle
        X = X.T
        Y = pBase.X[1][left:right,bottom:up]/d_array_nozzle
        Y = Y.T
        N_S22 = fs.fit_avg_dUdX[1][1][left:right,bottom:up]/(-fs.fit_avg_dUdX[0][0][left:right,bottom:up])
        N_S22 = N_S22.T
        max_values[fig_id,case_number] = np.nanmax(N_S22)
        min_values[fig_id,case_number] = np.nanmin(N_S22)

        c = ax.imshow(N_S22, extent=[X.min(), X.max(), Y.min(), Y.max()],
                    cmap='turbo', origin='lower', interpolation='None',
                    vmin=vmin, vmax=vmax)
        contours = ax.contour(X, Y, N_S22, levels=[0.3,0.4,0.5,0.6,0.7], colors='black', linestyles = '-', linewidths=0.5)
        if case_number == 0:
            first_im[fig_id] = c         

colorbarticks = [
    [0.3,0.4,0.5,0.6,0.7]
]

for fig_id in range(fig_number):
    print(f'fig_id={fig_id}')
    print(np.nanmin(min_values[fig_id]))
    print(np.nanmax(max_values[fig_id]))    
    cbar_ax = figs[fig_id].add_axes([0.2, 0.2, 0.6, 0.03])
    colorbar = figs[fig_id].colorbar(first_im[fig_id], cax=cbar_ax, orientation='horizontal', label=colorbarlabels[fig_id])
    colorbar.ax.minorticks_off()
    colorbar.ax.set_xticks(colorbarticks[fig_id])
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