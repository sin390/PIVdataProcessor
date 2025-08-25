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
figsize_inch = (cm_to_inch(16), cm_to_inch(4.8))
# -------------------------------------------------------------------------
# endregion


fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 2, figsize_inch)

xlables = [r'$x~(\mathrm{mm})$', r'$x~(\mathrm{mm})$']
ylables = [r'$S_u$', 
           r'$F_u$']
figtitles = ['F_and_S_for_u1_central_line']
xlims = [(-60,60),(-60,60)]
xticks = [
    [-50,0,50],
    [-50,0,50]
]
ylims = [(-0.1,0.1),(0,6)]
yticks = [
    [-0.10,-0.05,0,0.05,0.10],
    [0,2,4,6]
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
    sf = SF(cases[case_number]+'_sub1')
    sf.load()
    sub1_S_u = sf.S_u
    sub1_F_u = sf.F_u
    sf = SF(cases[case_number]+'_sub2')
    sf.load()
    sub2_S_u = sf.S_u
    sub2_F_u = sf.F_u   
    S_u_for_uncertainty = (sub1_S_u - sub2_S_u)**2
    F_u_for_uncertainty = (sub1_F_u - sub2_F_u)**2
    S_u_uncertainty = np.sqrt(nanmean_filter2d(S_u_for_uncertainty, filter_size))
    F_u_uncertainty = np.sqrt(nanmean_filter2d(F_u_for_uncertainty, filter_size))    

    sf = SF(cases[case_number])
    sf.load()
    kernel_size = 8
    S_u = nanmean_filter2d(sf.S_u,kernel_size=kernel_size)
    F_u = nanmean_filter2d(sf.F_u,kernel_size=kernel_size)

    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    errorbar_x,_ = pBase.pos_mm_to_index_list([-25,0,25],[0,0,0])

    fig_id = 0

    'S of u1(x,y=0)'
    ax = axess[fig_id][0]
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = S_u[left:right,central_y]
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    ax.axhline(y=0, color= 'k', linestyle = '--',linewidth = 0.8) 
    err_x = [pBase.X[0][xi,central_y] for xi in errorbar_x]
    err_y = [S_u[xi, central_y] for xi in errorbar_x]
    yerr = [S_u_uncertainty[xi, central_y]/2 for xi in errorbar_x]
    ax.errorbar(err_x, err_y, yerr=yerr, fmt='none',  color=mycolors[case_number],
                        capsize=2, elinewidth=0.5, markersize=2)  
    'F of u1(x,y=0)'
    ax = axess[fig_id][1]
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = F_u[left:right,central_y]
    ax.plot(plot_x,plot_y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    ax.axhline(y=3, color= 'k', linestyle = '--',linewidth = 0.8)   
    err_x = [pBase.X[0][xi,central_y] for xi in errorbar_x]
    err_y = [F_u[xi, central_y] for xi in errorbar_x]
    yerr = [F_u_uncertainty[xi, central_y]/2 for xi in errorbar_x]
    ax.errorbar(err_x, err_y, yerr=yerr, fmt='none',  color=mycolors[case_number],
                        capsize=2, elinewidth=0.5, markersize=2)  
        

        
for fig_number in range(len(figs)):
    fig = figs[fig_number]

    label_index = ['a','b','c','d','e','f']
    for i, ax in enumerate(axess[fig_number]):
        if i < len(label_index):
            if i == 0:
                ax.text(-0.22, 1.2, fr'$\textbf{{({label_index[i]})}}$',
                        transform=ax.transAxes,
                        fontsize=12, fontweight='bold',
                        va='top', ha='left') 
            elif i == 1:
                ax.text(-0.3, 1.2, fr'$\textbf{{({label_index[i]})}}$',
                        transform=ax.transAxes,
                        fontsize=12, fontweight='bold',
                        va='top', ha='left') 
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(top = 0.85, bottom = 0.22, left = 0.1, right=0.8)
    fig.subplots_adjust(wspace=0.55)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.82, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()    
