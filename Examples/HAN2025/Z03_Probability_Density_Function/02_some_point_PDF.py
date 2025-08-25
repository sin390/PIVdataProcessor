''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/10  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.A01_toolbox import ProbabilityDensity as PD
from pivdataprocessor.A01_toolbox import shift_field
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(12), cm_to_inch(14))
# -------------------------------------------------------------------------
# endregion

fig_number = 2
figs, axess = generatefiglist(fig_number, 3, 1, figsize_inch)

cases_title = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']
xlables = [r'$u_{1}/u_{1,\mathrm{rms}}$', r'$u_{2}/u_{2,\mathrm{rms}}$']
ylables = [r'PDF', r'PDF']
figtitles = ['PDF-u','PDF-v']
xlims = [(-5,5),(-5,5)]
ylims = [(0,0.5),(0,0.5)]
figformat = '.pdf'

for axes_number in range(len(axess)):
    for i in range(3):
        ax = axess[axes_number][i]
        axconfig = myaxconfig(ax = ax)
        if i == 2:
            axconfig.xlable = xlables[axes_number]
        axconfig.ylable = ylables[axes_number]
        axconfig.xlim = xlims[axes_number]
        axconfig.ylim = ylims[axes_number]
        axconfig.apply()



for case_number in range(len(cases)):
    pBase.load_case(cases[case_number])
    Nx, Ny = pBase.CaseInfo.Nx, pBase.CaseInfo.Ny

    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]

    plotted_x = np.array([0, 15, 30])
    plotted_y = np.array([0, 0, 0 ])
    plotted_x, plotted_y = pBase.pos_mm_to_index_list(plotted_x,plotted_y)

    PDF_u = [PD() for _ in range(len(plotted_x))]
    PDF_v = [PD() for _ in range(len(plotted_x))]

    for run_id in range(len(pBase.frame_numbers_in_runs)):
        for frame_id in range(pBase.frame_numbers_in_runs[run_id]):
            pBase.base_load_data_all(run_id,frame_id)
            for tmp_i in range(len(PDF_u)):
                PDF_u[tmp_i].add_point([pBase.fluc_U[0][plotted_x[tmp_i],plotted_y[tmp_i]]])
                PDF_v[tmp_i].add_point([pBase.fluc_U[1][plotted_x[tmp_i],plotted_y[tmp_i]]])
    for tmp_i in range(len(PDF_u)):
        PDF_u[tmp_i].process()
        PDF_u[tmp_i].normalize()
        PDF_v[tmp_i].process()
        PDF_v[tmp_i].normalize()
    
    for pos_number in range(len(plotted_x)):           
        'fig1'
        axess[0][pos_number].plot(PDF_u[pos_number].KDE_x, PDF_u[pos_number].KDE_y, linestyle='-', color = mycolors[case_number],\
                                    label = cases_title[case_number])
        'fig2'
        axess[1][pos_number].plot(PDF_v[pos_number].KDE_x, PDF_v[pos_number].KDE_y, linestyle='-', color = mycolors[case_number],\
                                    label = cases_title[case_number])     
    

for pos_number in range(len(plotted_x)):
    gauss_x = np.linspace(-5,5,100)
    gauss_pdf = norm.pdf(gauss_x, loc = 0, scale = 1)
    axess[0][pos_number].plot(gauss_x, gauss_pdf, linestyle = '-.', color = 'k', linewidth = 0.8)
    axess[1][pos_number].plot(gauss_x, gauss_pdf, linestyle = '-.', color = 'k', linewidth = 0.8)

for fig_number in range(len(figs)):
    fig = figs[fig_number]

    label_index = ['a','b','c','d','e','f']
    for i, ax in enumerate(axess[fig_number]):
        if i < len(label_index):
            ax.text(-0.2, 1.2, fr'$\textbf{{({label_index[i]})}}$',
                    transform=ax.transAxes,
                    fontsize=12, fontweight='bold',
                    va='top', ha='left')  
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(top = 0.95, left = 0.2, right=0.65, bottom=0.08)
    fig.subplots_adjust(wspace=0.4, hspace=0.5)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.67, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()    
