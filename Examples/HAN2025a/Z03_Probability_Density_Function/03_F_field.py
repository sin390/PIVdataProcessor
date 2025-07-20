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

from pivdataprocessor.A01_toolbox import nanmean_filter2d
from G01_SkewFlat import SkewFlat as SF

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

fig_number = 2
figs, axess = generatefiglist(fig_number, 2, 3, figsize_inch)
first_im = [None for _ in range(fig_number)]

cases_title = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']
xlables = [r'$x$ (mm)']
ylables = [r'$y$ (mm)']
xlims = [(-45,45)]
xtricks = [-40,-20,0,20,40]
ylims = [(-28,28)]
ytricks = [-20,0,20]
figtitles = ['Flatness_u_field','Flatness_v_field']
figformat = '.eps'

from matplotlib.colors import BoundaryNorm

levels = [1.25, 1.75, 2.25, 2.75, 3.25, 3.75, 4.25, 4.75]
norm = BoundaryNorm(levels, ncolors=plt.get_cmap('viridis').N, clip=True)

for i in range(2):
    for j in range(3):
        case_number = i*3+j     

        sf = SF(cases[case_number])
        sf.load()
        S_u = sf.S_u
        F_u = sf.F_u
        S_v = sf.S_v
        F_v = sf.F_v
        S_u = nanmean_filter2d(sf.S_u,kernel_size=8)
        F_u = nanmean_filter2d(sf.F_u,kernel_size=8)
        S_v = nanmean_filter2d(sf.S_v,kernel_size=8)
        F_v = nanmean_filter2d(sf.F_v,kernel_size=8)

        for axes_number in range(len(axess)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax = ax)
            # axconfig.title = cases_title[case_number]
            if i == 1:
                axconfig.xlable = xlables[0]
            if j == 0:
                axconfig.ylable = ylables[0]
            axconfig.ylim = ylims[0]
            axconfig.xlim = xlims[0]
            axconfig.xticks = xtricks
            axconfig.yticks = ytricks
            axconfig.apply()
            ax.set_ylabel(ax.get_ylabel(), labelpad=-4)
            ax.set_aspect('equal', adjustable='box')

        central_x, central_y = pBase.CaseInfo.Central_Position_Flow
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom,up = pBase.CaseInfo.Effective_Range[1]

        plotted_x = np.array([-30, -15, 0, 15, 30]) + pBase.X[0][central_x,central_y]
        plotted_y = np.array([-20, -10, 0, 10, 20]) + pBase.X[1][central_x,central_y]
        plotted_x, plotted_y = pBase.pos_mm_to_index_list(plotted_x,plotted_y)

        'fig1'
        ax = axess[0][case_number]
        X = pBase.X[0][left:right,bottom:up].T
        Y = pBase.X[1][left:right,bottom:up].T
        magnitude = F_u[left:right,bottom:up].T

        c = ax.imshow(magnitude, extent=[X.min(), X.max(), Y.min(), Y.max()], 
                                           cmap='viridis', origin='lower', interpolation='none', norm = norm)
        ax.plot(pBase.X[0][central_x,central_y], pBase.X[1][central_x,central_y],  marker='+', color='red', markersize=6)

        if case_number == 0:
            first_im[0] = c

        'fig2'
        ax = axess[1][case_number]
        X = pBase.X[0][left:right,bottom:up].T
        Y = pBase.X[1][left:right,bottom:up].T
        magnitude = F_v[left:right,bottom:up].T

        c = ax.imshow(magnitude, extent=[X.min(), X.max(), Y.min(), Y.max()], 
                                           cmap='viridis', origin='lower', interpolation='none', norm = norm)
        ax.plot(pBase.X[0][central_x,central_y], pBase.X[1][central_x,central_y],  marker='+', color='red', markersize=6)
        if case_number == 0:
            first_im[1] = c



colorbarlabels = [r'$\mathrm{Flatness\ of}\ u_1$', r'$\mathrm{Flatness\ of}\ u_2$']
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