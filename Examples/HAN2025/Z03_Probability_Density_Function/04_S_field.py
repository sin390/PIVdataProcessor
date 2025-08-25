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
figsize_inch = (cm_to_inch(33), cm_to_inch(19))
# -------------------------------------------------------------------------
# endregion

fig_number = 2
figs, axess = generatefiglist(fig_number, 2, 3, figsize_inch)

xlables = [r'$x$ (mm)',r'$x$ (mm)']
ylables = [r'$y$ (mm)',r'$y$ (mm)']
xlims = [(-50,50),(-50,50)]
ylims = [(-35,35),(-35,35)]
figtitles = ['Skewness_u_field','Skewness_v_field']
figformat = '.jpg'



levels = [-0.05, -0.03, -0.01, 0.01, 0.03, 0.05]
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
        # S_u = nanmean_filter2d(sf.S_u,kernel_size=7)
        # F_u = nanmean_filter2d(sf.F_u,kernel_size=7)
        # S_v = nanmean_filter2d(sf.S_v,kernel_size=7)
        # F_v = nanmean_filter2d(sf.F_v,kernel_size=7)

        for axes_number in range(len(axess)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax = ax)
            axconfig.title = cases[case_number]
            axconfig.xlable = xlables[axes_number]
            axconfig.ylable = ylables[axes_number]
            axconfig.xlim = xlims[axes_number]
            axconfig.ylim = ylims[axes_number]
            axconfig.apply()

        central_x, central_y = pBase.CaseInfo.Central_Position_Grid
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom,up = pBase.CaseInfo.Effective_Range[1]

        plotted_x = np.array([-30, -15, 0, 15, 30]) + pBase.X[0][central_x,central_y]
        plotted_y = np.array([-20, -10, 0, 10, 20]) + pBase.X[1][central_x,central_y]
        plotted_x, plotted_y = pBase.pos_mm_to_index_list(plotted_x,plotted_y)

        'fig1'
        ax = axess[0][case_number]
        X = pBase.X[0][left:right,bottom:up].T
        Y = pBase.X[1][left:right,bottom:up].T
        magnitude = S_u[left:right,bottom:up].T

        c = ax.imshow(magnitude, extent=[X.min(), X.max(), Y.min(), Y.max()], 
                                           cmap='viridis', origin='lower', interpolation='none', norm = norm)
        ax.plot(pBase.X[0][central_x,central_y], pBase.X[1][central_x,central_y],  marker='+', color='red', markersize=12)

        if case_number == 0:
            first_im_1 = c

        'fig2'
        ax = axess[1][case_number]
        X = pBase.X[0][left:right,bottom:up].T
        Y = pBase.X[1][left:right,bottom:up].T
        magnitude = S_v[left:right,bottom:up].T

        c = ax.imshow(magnitude, extent=[X.min(), X.max(), Y.min(), Y.max()], 
                                           cmap='viridis', origin='lower', interpolation='none', norm = norm)
        ax.plot(pBase.X[0][central_x,central_y], pBase.X[1][central_x,central_y],  marker='+', color='red', markersize=12)

        if case_number == 0:
            first_im_2 = c



cbar_ax = figs[0].add_axes([0.25, 0.08, 0.5, 0.03])
figs[0].colorbar(first_im_1, cax=cbar_ax, orientation='horizontal', label=r'$Skewness$')

cbar_ax = figs[1].add_axes([0.25, 0.08, 0.5, 0.03])
figs[1].colorbar(first_im_2, cax=cbar_ax, orientation='horizontal', label=r'$Skewness$')

for fig_id in range(fig_number):
    fig = figs[fig_id]
    # fig.tight_layout()
    fig.subplots_adjust(left=0.06, right=0.94, top=0.95, bottom=0.15, wspace=0.3, hspace=0.3)
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format='jpg')
plt.clf()       