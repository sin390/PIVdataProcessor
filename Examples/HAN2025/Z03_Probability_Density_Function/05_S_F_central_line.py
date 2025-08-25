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
figsize_inch = (cm_to_inch(12), cm_to_inch(6))
# -------------------------------------------------------------------------
# endregion

fig_number = 4
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$x~(\mathrm{mm})$', r'$x~(\mathrm{mm})$', r'$x~(\mathrm{mm})$', r'$x~(\mathrm{mm})$']
ylables = [r'$\mathrm{Skewness\ of}\ u_1$', 
           r'$\mathrm{Skewness\ of}\ u_2$', 
           r'$\mathrm{Flatness\ of}\ u_1$', 
           r'$\mathrm{Flatness\ of}\ u_2$']
figtitles = ['S-u-x','S-v-x','F-u-x','F-v-x']
xlims = [(-60,60),(-60,60),(-60,60),(-60,60)]
ylims = [(-0.1,0.1),(-0.1,0.1),(0,6),(0,6)]
yticks = [0,2,4,6]
figformat = '.pdf'
cases_title = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']

for axes_number in range(len(figs)):
    ax = axess[axes_number][0]
    axconfig = myaxconfig(ax = ax)
    axconfig.xlable = xlables[axes_number]
    axconfig.ylable = ylables[axes_number]
    axconfig.xlim = xlims[axes_number]
    axconfig.ylim = ylims[axes_number]
    if axes_number in [2,3]:
        axconfig.yticks = yticks
    axconfig.apply()

for case_number in range(len(cases)):
    sf = SF(cases[case_number])
    sf.load()
    kernel_size = 8
    S_u = nanmean_filter2d(sf.S_u,kernel_size=kernel_size)
    F_u = nanmean_filter2d(sf.F_u,kernel_size=kernel_size)
    S_v = nanmean_filter2d(sf.S_v,kernel_size=kernel_size)
    F_v = nanmean_filter2d(sf.F_v,kernel_size=kernel_size)
        
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]

    'fig1'
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = S_u[left:right,central_y]
    axess[0][0].plot(plot_x, plot_y, linestyle = '-', color = mycolors[case_number], 
                        label = cases_title[case_number])

    'fig2'
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = S_v[left:right,central_y]
    axess[1][0].plot(plot_x, plot_y, linestyle = '-', color = mycolors[case_number], 
                        label = cases_title[case_number])

    'fig3'
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = F_u[left:right,central_y]
    axess[2][0].plot(plot_x, plot_y, linestyle = '-', color = mycolors[case_number], 
                        label = cases_title[case_number])

    
    'fig4'
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = F_v[left:right,central_y]
    axess[3][0].plot(plot_x, plot_y, linestyle = '-', color = mycolors[case_number], 
                        label = cases_title[case_number]) 
axess[0][0].axhline(y=0, color= 'k', linestyle = '--',linewidth = 0.8)
axess[1][0].axhline(y=0, color= 'k', linestyle = '--',linewidth = 0.8) 
axess[2][0].axhline(y=3, color= 'k', linestyle = '--',linewidth = 0.8)
axess[3][0].axhline(y=3, color= 'k', linestyle = '--',linewidth = 0.8)   

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