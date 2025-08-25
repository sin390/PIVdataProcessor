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
from pivdataprocessor.A01_toolbox import nanmean_filter2d
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

from G01_SkewFlat import SkewFlat as SF

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(12), cm_to_inch(10))
# -------------------------------------------------------------------------
# endregion

fig_number = 8
figs, axess = generatefiglist(fig_number, 3, 2, figsize_inch)

xlables = [r'$x-x_{c}$ (mm)', r'$x-x_{c}$ (mm)', r'$x-x_{c}$ (mm)', r'$x-x_{c}$ (mm)',
           r'$y-y_{c}$ (mm)', r'$y-y_{c}$ (mm)', r'$y-y_{c}$ (mm)', r'$y-y_{c}$ (mm)']
ylables = [r'$S_{u_{1}}$', r'$S_{u_{2}}$', r'$F_{u_{1}}$', r'$F_{u_{2}}$',
           r'$S_{u_{1}}$', r'$S_{u_{2}}$', r'$F_{u_{1}}$', r'$F_{u_{2}}$']
figtitles = ['S-u-x','S-v-x','F-u-x','F-v-x','S-u-y','S-v-y','F-u-y','F-v-y']
xlims = [(-60,60),(-60,60),(-60,60),(-60,60),
         (-50,50),(-50,50),(-50,50),(-50,50)]
ylims = [(-0.1,0.1),(-0.1,0.1),(1,5),(1,5),
         (-0.1,0.1),(-0.1,0.1),(1,5),(1,5)]
yticks = [2,3,4]
figformat = '.eps'

for i in range(3):
    for j in range(2):
        case_number = i*2+j     

        sf = SF(cases[case_number])
        sf.load()
        kernel_size = 10
        S_u = nanmean_filter2d(sf.S_u,kernel_size=kernel_size)
        F_u = nanmean_filter2d(sf.F_u,kernel_size=kernel_size)
        S_v = nanmean_filter2d(sf.S_v,kernel_size=kernel_size)
        F_v = nanmean_filter2d(sf.F_v,kernel_size=kernel_size)
        # S_u = sf.S_u
        # F_u = sf.F_u
        # S_v = sf.S_v
        # F_v = sf.F_v

        for axes_number in range(len(figs)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax = ax)
            axconfig.title = cases[case_number]
            if i == 2:
                axconfig.xlable = xlables[axes_number]
            if j == 0:
                axconfig.ylable = ylables[axes_number]
            axconfig.xlim = xlims[axes_number]
            axconfig.ylim = ylims[axes_number]
            # if axes_number in [2,3,6,7]:
            #     axconfig.yticks = yticks
            axconfig.apply()

        
        central_x, central_y = pBase.CaseInfo.Central_Position_Grid
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom,up = pBase.CaseInfo.Effective_Range[1]

        plotted_x = np.array([-30, -15, 0, 15, 30]) + pBase.X[0][central_x,central_y]
        plotted_y = np.array([-20, -10, 0, 10, 20]) + pBase.X[1][central_x,central_y]
        plotted_x, plotted_y = pBase.pos_mm_to_index_list(plotted_x,plotted_y)
        
        'fig1'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][:, plotted_y[k]] - pBase.X[0][central_x,0]
            plot_y = S_u[:,plotted_y[k]]
            axess[0][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], 
                               label = fr'$y-y_{{c}}$ = {pBase.X[1][0,plotted_y[k]]-pBase.X[1][central_x,central_y]:.0f} mm')

        'fig2'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][:, plotted_y[k]] - pBase.X[0][central_x,0]
            plot_y = S_v[:,plotted_y[k]]
            axess[1][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], 
                               label = fr'$y-y_{{c}}$ = {pBase.X[1][0,plotted_y[k]]-pBase.X[1][central_x,central_y]:.0f} mm')

        'fig3'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][:, plotted_y[k]] - pBase.X[0][central_x,0]
            plot_y = F_u[:,plotted_y[k]]
            axess[2][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], 
                               label = fr'$y-y_{{c}}$ = {pBase.X[1][0,plotted_y[k]]-pBase.X[1][central_x,central_y]:.0f} mm')
        axess[2][case_number].axhline(y=3, color= 'k', linestyle = '--',linewidth = 0.8)
        
        'fig4'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][:, plotted_y[k]] - pBase.X[0][central_x,0]
            plot_y = F_v[:,plotted_y[k]]
            axess[3][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], 
                               label = fr'$y-y_{{c}}$ = {pBase.X[1][0,plotted_y[k]]-pBase.X[1][central_x,central_y]:.0f} mm')
        axess[3][case_number].axhline(y=3, color= 'k', linestyle = '--',linewidth = 0.8)        

        'fig5'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],:] - pBase.X[1][central_x,central_y]
            plot_y = S_u[plotted_x[k],:]
            axess[4][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], 
                               label = fr'$x-x_{{c}}$ = {pBase.X[0][plotted_x[k],0]-pBase.X[0][central_x,central_y]:.0f} mm')

        
        'fig6'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],:] - pBase.X[1][central_x,central_y]
            plot_y = S_v[plotted_x[k],:]
            axess[5][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], 
                               label = fr'$x-x_{{c}}$ = {pBase.X[0][plotted_x[k],0]-pBase.X[0][central_x,central_y]:.0f} mm')

        'fig7'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],:] - pBase.X[1][central_x,central_y]
            plot_y = F_u[plotted_x[k],:]
            axess[6][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], 
                               label = fr'$x-x_{{c}}$ = {pBase.X[0][plotted_x[k],0]-pBase.X[0][central_x,central_y]:.0f} mm')
        axess[6][case_number].axhline(y=3, color= 'k', linestyle = '--',linewidth = 0.8)

        'fig8'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],:] - pBase.X[1][central_x,central_y]
            plot_y = F_v[plotted_x[k],:]
            axess[7][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], 
                               label = fr'$x-x_{{c}}$ = {pBase.X[0][plotted_x[k],0]-pBase.X[0][central_x,central_y]:.0f} mm')
        axess[7][case_number].axhline(y=3, color= 'k', linestyle = '--',linewidth = 0.8)


for fig_number in range(len(figs)):
    fig = figs[fig_number]
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(right=0.65)
    fig.subplots_adjust(hspace=0.7)
    fig.subplots_adjust(wspace=0.4)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.67, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()    
