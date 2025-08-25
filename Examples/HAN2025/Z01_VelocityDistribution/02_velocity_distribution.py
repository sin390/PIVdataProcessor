''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/07  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.A01_toolbox import nanmean_filter2d
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, generatefiglist, myaxconfig, mycolors


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
colors = mycolors
styles = [['-','-','-'],['--','--','--']]

# -------------------------------------------------------------------------
# main
# region

figs, axess = generatefiglist(4, 3, 2, figsize_inch)

xlables = [r'$x~(\mathrm{mm})$', r'$x~(\mathrm{mm})$', r'$y~(\mathrm{mm})$', r'$y~(\mathrm{mm})$']
ylables = [r'$\langle U_{1} \rangle$ (m/s)', 
           r'$\langle U_{2} \rangle$ (m/s)', 
           r'$\langle U_{1} \rangle$ (m/s)', 
           r'$\langle U_{2} \rangle$ (m/s)']
figtitles = ['avg_U1-x','avg_U2-x','avg_U1-y','avg_U2-y']
figformat = '.pdf'
xlims = [(-60,60),(-60,60),(-40,40),(-40,40)]
ylims = [(-50,50),(-50,50),(-50,50),(-50,50)]
# case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']
fit_order = 3

filter_range = 8

for i in range(3):
    for j in range(2):
        case_number = i*2+j
        pBase.load_case(cases[case_number]+'_sub1')
        avg_U_sub1 = pBase.avg_U.copy()
        pBase.load_case(cases[case_number]+'_sub2')
        avg_U_sub2 = pBase.avg_U.copy()
        for_uncertainty = (avg_U_sub1 - avg_U_sub2)**2
        U_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[0], filter_range))
        V_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[1], filter_range))   
        pBase.load_case(cases[case_number])
        for axes_number in range(len(figs)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax = ax)
            # axconfig.title = case_titles[case_number]
            if i == 2:
                axconfig.xlable = xlables[axes_number]
            if j == 0:
                axconfig.ylable = ylables[axes_number]
            axconfig.xlim = xlims[axes_number]
            axconfig.ylim = ylims[axes_number]
            axconfig.apply()
        
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom,up = pBase.CaseInfo.Effective_Range[1]

        plotted_x = np.array([-30, -15, 0, 15, 30]) 
        plotted_y = np.array([-20, -10, 0, 10, 20])
        plotted_x, plotted_y = pBase.pos_mm_to_index_list(plotted_x,plotted_y)

        'fig1'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][left:right, plotted_y[k]]
            plot_y = pBase.avg_U[0][left:right, plotted_y[k]]
            axess[0][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k],
                               label = fr'$y = {round(pBase.X[1][0,plotted_y[k]])}~\mathrm{{mm}}$')
    
            errorbar_x,_ = pBase.pos_mm_to_index_list([-25,0,25],[0,0,0])
            err_x = [pBase.X[0][xi,plotted_y[k]] for xi in errorbar_x]
            err_y = [pBase.avg_U[0][xi, plotted_y[k]] for xi in errorbar_x]
            yerr = [U_uncertainty[xi, plotted_y[k]]/2 for xi in errorbar_x]
            axess[0][case_number].errorbar(err_x, err_y, yerr=yerr, fmt='none', color=mycolors[k],
                               capsize=2, elinewidth=0.5, markersize=2)

 

        'fig2'
        for k in range(len(plotted_y)):
            plot_x = pBase.X[0][left:right, plotted_y[k]]
            plot_y = pBase.avg_U[1][left:right, plotted_y[k]]
            axess[1][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k],
                               label = fr'$y = {round(pBase.X[1][0,plotted_y[k]])}~\mathrm{{mm}}$')
            
     
  

        'fig3'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],bottom:up]
            plot_y = pBase.avg_U[0][plotted_x[k],bottom:up]
            axess[2][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k],
                               label = fr'$x = {round(pBase.X[0][plotted_x[k],0])}~\mathrm{{mm}}$')
   

        'fig4'
        for k in range(len(plotted_x)):
            plot_x = pBase.X[1][plotted_x[k],bottom:up]
            plot_y = pBase.avg_U[1][plotted_x[k],bottom:up]
            axess[3][case_number].plot(plot_x, plot_y, linestyle = '-', color = mycolors[k],
                               label = fr'$x = {round(pBase.X[0][plotted_x[k],0])}~\mathrm{{mm}}$')
            _,errorbar_y = pBase.pos_mm_to_index_list([0,0,0],[-12.5,0,12.5])
            err_x = [pBase.X[1][plotted_x[k],yi] for yi in errorbar_y]
            err_y = [pBase.avg_U[1][plotted_x[k], yi] for yi in errorbar_y]
            yerr = [V_uncertainty[plotted_x[k], yi]/2 for yi in errorbar_y]
            axess[3][case_number].errorbar(err_x, err_y, yerr=yerr, fmt='none', color=mycolors[k],
                               capsize=2, elinewidth=0.5, markersize=2)


      


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

# -------------------------------------------------------------------------
# endregion