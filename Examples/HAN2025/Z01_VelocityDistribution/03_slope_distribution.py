''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/08  =
=========================
'''
import matplotlib.pyplot as plt
import numpy as np


from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.A01_toolbox import moving_average
from pivdataprocessor.A01_toolbox import nanmean_filter2d
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, generatefiglist, myaxconfig, mycolors
from G01_fitted_slope import FittedSlope


# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(16), cm_to_inch(12))
# -------------------------------------------------------------------------
# endregion

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']   
figs, axess = generatefiglist(10, 3, 2, figsize_inch)

xlables = [r'$x-x_{c}$ (mm)', r'$x-x_{c}$ (mm)', r'$x-x_{c}$ (mm)', r'$x-x_{c}$ (mm)',
           r'$y-y_{c}$ (mm)', r'$y-y_{c}$ (mm)', r'$y-y_{c}$ (mm)', r'$y-y_{c}$ (mm)',
           r'$x-x_{c}$ (mm)', r'$y-y_{c}$ (mm)',]
ylables = [r'$-S_{11}~(\mathrm{s}^{-1})$', 
           r'$S_{21}~(\mathrm{s}^{-1})$',
           r'$S_{12}~(\mathrm{s}^{-1})$',
           r'$S_{22}~(\mathrm{s}^{-1})$',
           r'$-S_{11} ~(\mathrm{s}^{-1})$',
           r'$S_{21}~(\mathrm{s}^{-1})$',
           r'$S_{12}~(\mathrm{s}^{-1})$',
           r'$S_{22}~(\mathrm{s}^{-1})$',
           r'$-{S_{22}}/{S_{11}}$',
           r'$-{S_{22}}/{S_{11}}$']

figtitles = ['S11-x','S21-x','S12-x','S22-x',
             'S11-y','S21-y','S12-y','S22-y',
             'ratio_S22_S11-x','ratio_S22_S11-y']
xlims = [(-60,60),(-60,60),(-60,60),(-60,60),
         (-40,40),(-40,40),(-40,40),(-40,40),
         (-60,60),(-40,40)]
ylims = [(0,1200),(-600,600),(-600,600),(0,1200),
         (0,1200),(-600,600),(-600,600),(0,1200),
         (0,1),(0,1)]
figformat = '.eps'



for i in range(3):
    for j in range(2):
        case_number = i*2+j
        fitted_case = FittedSlope(cases[case_number])
        fitted_case.load_fitted()

        for axes_number in range(len(figs)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax = ax)
            # axconfig.title = cases[case_number]
            if i == 2:
                axconfig.xlable = xlables[axes_number]
            if j == 0:
                axconfig.ylable = ylables[axes_number]
            axconfig.xlim = xlims[axes_number]
            axconfig.ylim = ylims[axes_number]
            axconfig.apply()
        
        central_x, central_y = pBase.CaseInfo.Central_Position_Flow
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom,up = pBase.CaseInfo.Effective_Range[1]

        plotted_x = np.array([-30, -15, 0, 15, 30]) + pBase.X[0][central_x,central_y]
        plotted_y = np.array([-20, -10, 0, 10, 20]) + pBase.X[1][central_x,central_y]
        plotted_x, plotted_y = pBase.pos_mm_to_index_list(plotted_x,plotted_y)


        'fig1'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][left:right, plotted_y[k]] - pBase.X[0][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[0][0][left:right,plotted_y[k]] * (-1000)
            axess[0][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], 
                               label = fr'$y-y_{{c}}$ = {pBase.X[1][0,plotted_y[k]]-pBase.X[1][central_x,central_y]:.0f} mm')
            avg_value = np.mean(plot_y[:])
            # axess[0][case_number].axhline(y = avg_value, linestyle = '-.', color = mycolors[k])
            # print(avg_value)

            
        
        'fig2'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][left:right, plotted_y[k]] - pBase.X[0][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[1][0][left:right,plotted_y[k]] * (1000)
            axess[1][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], label = fr'$y-y_{{c}}$ = {pBase.X[1][0,plotted_y[k]]-pBase.X[1][central_x,central_y]:.0f} mm')
            

        'fig3'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][left:right, plotted_y[k]] - pBase.X[0][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[0][1][left:right,plotted_y[k]] * (1000)
            axess[2][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], label = fr'$y-y_{{c}}$ = {pBase.X[1][0,plotted_y[k]]-pBase.X[1][central_x,central_y]:.0f} mm')
            

        'fig4'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][left:right, plotted_y[k]] - pBase.X[0][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[1][1][left:right,plotted_y[k]] * (1000)
            axess[3][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], label = fr'$y-y_{{c}}$ = {pBase.X[1][0,plotted_y[k]]-pBase.X[1][central_x,central_y]:.0f} mm')
            
               
        'fig5'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],bottom:up] - pBase.X[1][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[0][0][plotted_x[k],bottom:up] * (-1000)
            axess[4][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], label = fr'$x-x_{{c}}$ = {pBase.X[0][plotted_x[k],0]-pBase.X[0][central_x,central_y]:.0f} mm')
            avg_value = np.mean(plot_y[:])
            # axess[4][case_number].axhline(y = avg_value, linestyle = '-.', color = mycolors[k])            


        'fig6'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],bottom:up] - pBase.X[1][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[1][0][plotted_x[k],bottom:up] * (1000)
            axess[5][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], label = fr'$x-x_{{c}}$ = {pBase.X[0][plotted_x[k],0]-pBase.X[0][central_x,central_y]:.0f} mm')
            

        'fig7'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],bottom:up] - pBase.X[1][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[0][1][plotted_x[k],bottom:up] * (1000)
            axess[6][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], label = fr'$x-x_{{c}}$ = {pBase.X[0][plotted_x[k],0]-pBase.X[0][central_x,central_y]:.0f} mm')
            

        'fig8'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],bottom:up] - pBase.X[1][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[1][1][plotted_x[k],bottom:up] * (1000)
            axess[7][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], label = fr'$x-x_{{c}}$ = {pBase.X[0][plotted_x[k],0]-pBase.X[0][central_x,central_y]:.0f} mm')

        'fig9'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][left:right, plotted_y[k]] - pBase.X[0][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[1][1][left:right,plotted_y[k]] * (-1) / fitted_case.fit_avg_dUdX[0][0][left:right,plotted_y[k]]
            axess[8][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], label = fr'$y-y_{{c}}$ = {pBase.X[1][0,plotted_y[k]]-pBase.X[1][central_x,central_y]:.0f} mm')
        axess[8][case_number].axhline(y=0.5, color= 'k', linestyle = '--',linewidth = 0.8)

        'fig10'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],bottom:up] - pBase.X[1][central_x,central_y]
            plot_y = fitted_case.fit_avg_dUdX[1][1][plotted_x[k],bottom:up] * (-1) / fitted_case.fit_avg_dUdX[0][0][plotted_x[k],bottom:up]
            axess[9][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k], label = fr'$x-x_{{c}}$ = {pBase.X[0][plotted_x[k],0]-pBase.X[0][central_x,central_y]:.0f} mm')
        axess[9][case_number].axhline(y=0.5, color= 'k', linestyle = '--',linewidth = 0.8)
            

for fig_id in range(len(figs)):
    fig = figs[fig_id]
    label_index = ['a','b','c','d','e','f']
    for i, ax in enumerate(axess[fig_id]):
        if i < len(label_index):
            ax.text(-0.25, 1.25, fr'$\textbf{{({label_index[i]})}}$',
                    transform=ax.transAxes,
                    fontsize=12, fontweight='bold',
                    va='top', ha='left')  
    handles, labels = [], []
    for line in axess[fig_id][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(left=0.1, right=0.7, top=0.95, bottom=0.1, wspace=0.32, hspace=0.6)


    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.72, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:])
plt.clf()    