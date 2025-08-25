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
from G01_reynolds_stress import ReynoldsStress as RS
from pivdataprocessor.A01_toolbox import nanmean_filter2d
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


fig_number = 4
figs, axess = generatefiglist(fig_number, 2, 2, figsize_inch)

xlables = [r'$x-x_{c}$ (mm)', r'$x-x_{c}$ (mm)', r'$y-y_{c}$ (mm)', r'$y-y_{c}$ (mm)']
ylables = [r'$R_{11}~(\mathrm{m}^{2}/\mathrm{s}^{2})$', r'$R_{22}~(\mathrm{m}^{2}/\mathrm{s}^{2})$', 
           r'$R_{12}~(\mathrm{m}^{2}/\mathrm{s}^{2})$', r'$k_t~(\mathrm{m}^{2}/\mathrm{s}^{2})$']
figtitles = ['R_11','R_22','R_12','k_t']
xlims = [(-60,60),(-60,60),(-40,40),(-40,40)]
xticks = [
    [-50,0,50],
    [-50,0,50],
    [-25,0,25],
    [-25,0,25]
]
ylims = [(0,1200),(0,500),(-500,500),(0,1200)]
yticks = [
    [0, 250,500,750,1000],
    [0, 100,200,300,400],
    [-400,0,400],
    [0, 250,500,750,1000]
]
figformat = '.pdf'

plotted_x_r = np.array([0, 30])
plotted_y_r = np.array([0, 20])

filter_size = 8

case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']

for axes_number in range(len(axess)):
    for i in range(2):
        for j in range(2):
            ax_num = i*2+j
            ax = axess[axes_number][ax_num]
            axconfig = myaxconfig(ax = ax)
            axconfig.xlable = xlables[ax_num]
            if j == 0 :
                axconfig.ylable = ylables[axes_number]
            axconfig.xlim = xlims[ax_num]
            axconfig.xticks = xticks[ax_num]
            axconfig.ylim = ylims[axes_number]
            axconfig.yticks = yticks[axes_number]
            axconfig.apply()


for case_number in range(len(cases)):
    rs = RS(cases[case_number])
    rs.load()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    
    plotted_x = plotted_x_r + pBase.X[0][central_x,central_y]
    plotted_y = plotted_y_r + pBase.X[1][central_x,central_y]
    plotted_x, plotted_y = pBase.pos_mm_to_index_list(plotted_x,plotted_y)

    'fig1'
    fig_id = 0
    for j in range(2):
        uu = nanmean_filter2d(rs.uu,filter_size)
        plot_x = pBase.X[0][left:right, plotted_y[j]] - pBase.X[0][central_x,0]
        plot_y = uu[left:right, plotted_y[j]]
        axess[fig_id][j].plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])

        plot_x = pBase.X[1][plotted_x[j],bottom:up] - pBase.X[1][0,central_y]
        plot_y = uu[plotted_x[j],bottom:up]
        axess[fig_id][2+j].plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])

    'fig2'
    fig_id = 1
    for j in range(2):
        vv = nanmean_filter2d(rs.vv,filter_size)
        plot_x = pBase.X[0][left:right, plotted_y[j]] - pBase.X[0][central_x,0]
        plot_y = vv[left:right, plotted_y[j]]
        axess[fig_id][j].plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
        plot_x = pBase.X[1][plotted_x[j],bottom:up] - pBase.X[1][0,central_y]
        plot_y = vv[plotted_x[j],bottom:up]
        axess[fig_id][2+j].plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])    

    'fig3'
    fig_id = 2
    for j in range(2):
        uv = nanmean_filter2d(rs.uv,filter_size)
        plot_x = pBase.X[0][left:right, plotted_y[j]] - pBase.X[0][central_x,0]
        plot_y = uv[left:right, plotted_y[j]]
        axess[fig_id][j].plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
        plot_x = pBase.X[1][plotted_x[j],bottom:up] - pBase.X[1][0,central_y]
        plot_y = uv[plotted_x[j],bottom:up]
        axess[fig_id][2+j].plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])

    'fig4'
    fig_id = 3
    for j in range(2):
        k2 = nanmean_filter2d(rs.k2,filter_size)
        plot_x = pBase.X[0][left:right, plotted_y[j]] - pBase.X[0][central_x,0]
        plot_y = k2[left:right, plotted_y[j]]
        axess[fig_id][j].plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
        plot_x = pBase.X[1][plotted_x[j],bottom:up] - pBase.X[1][0,central_y]
        plot_y = k2[plotted_x[j],bottom:up]
        axess[fig_id][2+j].plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
        

        
for fig_number in range(len(figs)):
    fig = figs[fig_number]

    label_index = ['a','b','c','d','e','f']
    for i, ax in enumerate(axess[fig_number]):
        if i < len(label_index):
            ax.text(-0.2, 1.1, fr'$\textbf{{({label_index[i]})}}$',
                    transform=ax.transAxes,
                    fontsize=12, fontweight='bold',
                    va='top', ha='left')  
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(top = 0.95, left = 0.12, right=0.8)
    fig.subplots_adjust(wspace=0.4, hspace=0.5)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.82, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()    
