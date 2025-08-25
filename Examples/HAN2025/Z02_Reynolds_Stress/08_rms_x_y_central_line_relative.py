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
figsize_inch = (cm_to_inch(16), cm_to_inch(4.8))
# -------------------------------------------------------------------------
# endregion


fig_number = 2
figs, axess = generatefiglist(fig_number, 1, 2, figsize_inch)

xlables = [r'$x-x_{c}$ (mm)', r'$x-x_{c}$ (mm)']
ylables = [r'$\frac{u_{1, \mathrm{rms}}-u_{1, \mathrm{rms,avg}}}{u_{1, \mathrm{rms,avg}}}$', 
           r'$\frac{u_{2, \mathrm{rms}}-u_{2, \mathrm{rms,avg}}}{u_{2, \mathrm{rms,avg}}}$']
figtitles = ['rms_u_v_central_line','rms_u_v_central_line_y']
xlims = [(-60,60),(-60,60)]
xticks = [
    [-50,0,50],
    [-50,0,50]
]
ylims = [(-0.6,0.6),(-0.6,0.6)]
yticks = [
    [-0.5, 0, 0.5],
    [-0.5, 0, 0.5]
]
figformat = '.pdf'
filter_size = 8

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
        # axconfig.yticks = yticks[ax_num]
        axconfig.apply()


for case_number in range(len(cases)):
    rs = RS(cases[case_number])
    rs.load()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    
    fig_id = 0  
    'urms(x-xc,y-yc=0)'
    ax = axess[fig_id][0]
    plot_x = pBase.X[0][left:right,central_y] - pBase.X[0][central_x,central_y]
    u_rms_avg = np.sqrt(np.mean(rs.uu[left:right,bottom:up]))
    u_rms = np.sqrt(rs.uu)
    u_rms = nanmean_filter2d(u_rms,filter_size)
    plot_y = (u_rms[left:right,central_y] - u_rms_avg)/u_rms_avg
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    ax.axhline(y=0, color= 'k', linestyle = '--',linewidth = 0.8)    

    'vrms(x-xc,y-yc=0)'
    ax = axess[fig_id][1]
    plot_x = pBase.X[0][left:right,central_y] - pBase.X[0][central_x,central_y]
    v_rms_avg = np.sqrt(np.mean(rs.vv[left:right,bottom:up]))
    v_rms = np.sqrt(rs.vv)
    v_rms = nanmean_filter2d(v_rms,filter_size)
    plot_y = (v_rms[left:right,central_y] - v_rms_avg) / v_rms_avg
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    ax.axhline(y=0, color= 'k', linestyle = '--',linewidth = 0.8)  

    fig_id = 1
    'urms(x-xc,y-yc=0)'
    ax = axess[fig_id][0]
    plot_x = pBase.X[1][central_x,bottom:up] - pBase.X[1][central_x,central_y]
    u_rms_avg = np.sqrt(np.mean(rs.uu[left:right,bottom:up]))
    u_rms = np.sqrt(rs.uu)
    u_rms = nanmean_filter2d(u_rms,filter_size)
    plot_y = (u_rms[central_x,bottom:up] - u_rms_avg)/u_rms_avg
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    ax.axhline(y=0, color= 'k', linestyle = '--',linewidth = 0.8)    

    'vrms(x-xc,y-yc=0)'
    ax = axess[fig_id][1]
    plot_x = pBase.X[1][central_x,bottom:up] - pBase.X[1][central_x,central_y]
    v_rms_avg = np.sqrt(np.mean(rs.vv[left:right,bottom:up]))
    v_rms = np.sqrt(rs.vv)
    v_rms = nanmean_filter2d(v_rms,filter_size)
    plot_y = (v_rms[central_x,bottom:up] - v_rms_avg) / v_rms_avg
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    ax.axhline(y=0, color= 'k', linestyle = '--',linewidth = 0.8)      
      

        
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
