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
figsize_inch = (cm_to_inch(12), cm_to_inch(6))
# -------------------------------------------------------------------------
# endregion


fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$x~(\mathrm{mm})$']
ylables = [r'$k_t~(\mathrm{m}^{2}/\mathrm{s}^{2})$']
figtitles = ['kt_central_line']
xlims = [(-60,60)]
xticks = [[-50,0,50]]
ylims = [(0,1000)]
yticks = [
    [0, 200,400,600,800]
]
figformat = '.pdf'
filter_size = 8

case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']

for axes_number in range(len(axess)):
    ax_num = 0
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
    rs = RS(cases[case_number])
    rs.load()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    
    fig_id = 0
    
    ax = axess[fig_id][0]
    plot_x = pBase.X[0][left:right,central_y]
    kt = rs.k2
    kt = nanmean_filter2d(kt,filter_size)
    plot_y = kt[left:right,central_y]
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    

        
for fig_id in range(fig_number):
    fig = figs[fig_id]
    handles, labels = [], []
    for line in axess[fig_id][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(top = 0.9, left = 0.15, right=0.65,bottom=0.2)
    fig.subplots_adjust(wspace=0.4, hspace=0.5)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.67, 0.5), borderaxespad=0)
    fig = figs[fig_id]
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:])
plt.clf()      