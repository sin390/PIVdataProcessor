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


fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 2, figsize_inch)

xlables = [r'$x~(\mathrm{mm})$', r'$x~(\mathrm{mm})$']
ylables = [r'$u_{1,\,\mathrm{rms}}~\mathrm{(m/s)}$', 
           r'$u_{2,\,\mathrm{rms}}~\mathrm{(m/s)}$']
figtitles = ['rms_u_v_central_line']
xlims = [(-60,60),(-60,60)]
xticks = [
    [-50,0,50],
    [-50,0,50]
]
ylims = [(0,45),(0,45)]
yticks = [
    [0, 10,20,30,40],
    [0, 10,20,30,40]
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
        axconfig.yticks = yticks[ax_num]
        axconfig.apply()



for case_number in range(len(cases)):
    rs = RS(cases[case_number]+'_sub1')
    rs.load()
    sub1_urms = np.sqrt(rs.uu)
    sub1_vrms = np.sqrt(rs.vv)
    rs = RS(cases[case_number]+'_sub2')
    rs.load()
    sub2_urms = np.sqrt(rs.uu)
    sub2_vrms = np.sqrt(rs.vv)
    urms_for_uncertainty = (sub1_urms - sub2_urms)**2
    vrms_for_uncertainty = (sub1_vrms - sub2_vrms)**2
    urms_uncertainty = np.sqrt(nanmean_filter2d(urms_for_uncertainty, filter_size))
    vrms_uncertainty = np.sqrt(nanmean_filter2d(vrms_for_uncertainty, filter_size))

    rs = RS(cases[case_number])
    rs.load()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    errorbar_x,_ = pBase.pos_mm_to_index_list([-25,0,25],[0,0,0])
    fig_id = 0
    
    'urms(x,y=0)'
    ax = axess[fig_id][0]
    plot_x = pBase.X[0][left:right,central_y]
    urms = np.sqrt(rs.uu)
    urms = nanmean_filter2d(urms,filter_size)
    plot_y = urms[left:right,central_y]
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    err_x = [pBase.X[0][xi,central_y] for xi in errorbar_x]
    err_y = [urms[xi, central_y] for xi in errorbar_x]
    yerr = [urms_uncertainty[xi, central_y]/2 for xi in errorbar_x]
    ax.errorbar(err_x, err_y, yerr=yerr, fmt='none',  color=mycolors[case_number],
                        capsize=2, elinewidth=0.5, markersize=2)    
    'vrms(x,y=0)'
    ax = axess[fig_id][1]
    plot_x = pBase.X[0][left:right,central_y]
    vrms = np.sqrt(rs.vv)
    vrms = nanmean_filter2d(vrms,filter_size)
    plot_y = vrms[left:right,central_y]
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    err_x = [pBase.X[0][xi,central_y] for xi in errorbar_x]
    err_y = [vrms[xi, central_y] for xi in errorbar_x]
    yerr = [vrms_uncertainty[xi, central_y]/2 for xi in errorbar_x]
    ax.errorbar(err_x, err_y, yerr=yerr, fmt='none', color=mycolors[case_number],
                        capsize=2, elinewidth=0.5, markersize=2)       

        
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
