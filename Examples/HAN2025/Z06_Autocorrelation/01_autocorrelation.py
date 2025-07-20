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
from G01_autocorrelation import AutoCorrelation as AC

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(16), cm_to_inch(12))
# -------------------------------------------------------------------------
# endregion

fig_number = 1
figs, axess = generatefiglist(fig_number, 3, 2, figsize_inch)

xlables = [r'$r$ (mm)']
ylables = [r'$f_i(r)$']
figtitles = ['autocorrelation']
xlims = [(0,100)]
ylims = [(-0.2,1)]
figformat = '.eps'
case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']

for i in range(3):
    for j in range(2):
        case_number = i*2+j

        ac = AC(cases[case_number])
        ac.load()

        for axes_number in range(len(axess)):
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

        'fig1'
        fig_id = 0
        axess[fig_id][case_number].plot(ac.r_xdir,ac.autocorr_xdir[0], linestyle = '-', color = mycolors[0],
                                label = r'$f_1(r)$')
        axess[fig_id][case_number].plot(ac.fitting_part[1],ac.fitting_part[0], linewidth=0.8, linestyle = '-.', color = mycolors[0])
        axess[fig_id][case_number].plot(ac.r_ydir,ac.autocorr_ydir[1],  linestyle = '-', color = mycolors[1],
                                label = r'$f_2(r)$')
        axess[fig_id][case_number].plot(ac.fitting_part[3],ac.fitting_part[2], linewidth=0.8, linestyle = '-.', color = mycolors[1])
        ref_ac = AC('Mori465')
        ref_ac.load()
        axess[fig_id][case_number].plot(ref_ac.r_xdir,ref_ac.autocorr_xdir[0], linewidth=0.8, linestyle = '-', color = 'k')

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
    fig.subplots_adjust(left=0.1, right=0.8, top=0.94, bottom=0.1, wspace=0.32, hspace=0.6)


    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.82, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:])
plt.clf()    