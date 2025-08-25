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
from G01_fitted_slope import FittedSlope
from pivdataprocessor.A01_toolbox import nanmean_filter2d
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(16), cm_to_inch(4.8))
# -------------------------------------------------------------------------
# endregion


fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 2, figsize_inch)

xlables = [r'$x~(\mathrm{mm})$', r'$y~(\mathrm{mm})$']
ylables = [r'$-S_{11}~(\mathrm{s}^{-1})$', 
           r'$S_{22}~(\mathrm{s}^{-1})$']
figtitles = ['avg_slope']
xlims = [(-60,60),(-40,40)]
xticks = [
    [-50,0,50],
    [-25,0,25]
]
ylims = [(0,1200),(0,1200)]
yticks = [
    [0, 250,500,750,1000],
    [0, 250,500,750,1000]
]
figformat = '.pdf'


case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']

for axes_number in range(len(axess)):
    for i in range(2):
        ax_num = i
        ax = axess[axes_number][ax_num]
        axconfig = myaxconfig(ax = ax)
        axconfig.xlable = xlables[ax_num]
        axconfig.ylable = ylables[ax_num]
        axconfig.xlim = xlims[ax_num]
        axconfig.xticks = xticks[ax_num]
        axconfig.ylim = ylims[ax_num]
        axconfig.yticks = yticks[ax_num]
        axconfig.apply()


for case_number in range(len(cases)):
    fs = FittedSlope(cases[case_number])
    fs.load_fitted()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    
    fig_id = 0
    
    'S11(x,y=0)'
    ax = axess[fig_id][0]
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = fs.fit_avg_dUdX[0][0][left:right,central_y] * (-1000)
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    
    'S22(x=0,y)'
    ax = axess[fig_id][1]
    plot_x = pBase.X[1][central_x,bottom:up]
    plot_y = fs.fit_avg_dUdX[1][1][central_x,bottom:up] * 1000
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
      

        
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
    fig.subplots_adjust(top = 0.9, bottom = 0.22, left = 0.12, right=0.8)
    fig.subplots_adjust(wspace=0.5)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.82, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()    
