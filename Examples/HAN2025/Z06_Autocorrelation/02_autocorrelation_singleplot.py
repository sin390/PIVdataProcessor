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

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06', 'Mori465']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(8), cm_to_inch(9))
# -------------------------------------------------------------------------
# endregion

fig_number = 1
figs, axess = generatefiglist(fig_number, 2, 1, figsize_inch)

xlables = [r'$r$ (mm)',r'$r$ (mm)']
ylables = [r'$f_1(r)$',r'$f_2(r)$']
figtitles = ['autocorrelation']
xlims = [(0,100)]
ylims = [(-0.2,1)]
figformat = '.jpg'
mycolors[6] = 'k'
case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6', 'Mori et al.']

for axes_number in range(len(axess)):
    for axes_id in range(len(axess[axes_number])):
        ax = axess[axes_number][axes_id]
        axconfig = myaxconfig(ax = ax)
        # axconfig.title = cases[case_number]
        axconfig.xlable = xlables[axes_id]
        axconfig.ylable = ylables[axes_id]
        axconfig.ylim = ylims[axes_number]
        axconfig.xlim = xlims[axes_number]
        axconfig.apply()

for case_number in range(len(cases)):
    ac = AC(cases[case_number])
    ac.load()

    'fig1'
    fig_id = 0
    'subplot1'
    axess[fig_id][0].plot(ac.r_xdir,ac.autocorr_xdir[0], linestyle = '-', color = mycolors[case_number],
                            label = case_titles[case_number])
    axess[fig_id][0].plot(ac.fitting_part[1],ac.fitting_part[0], linestyle = '-.', color = mycolors[case_number])
    'subplot2'
    axess[fig_id][1].plot(ac.r_ydir,ac.autocorr_ydir[1],  linestyle = '-', color = mycolors[case_number],
                        label = case_titles[case_number])    
    axess[fig_id][1].plot(ac.fitting_part[3],ac.fitting_part[2], linestyle = '-.', color = mycolors[case_number])



for fig_number in range(len(figs)):
    fig = figs[fig_number]
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(right=0.65)
    fig.subplots_adjust(hspace=0.7)
    fig.subplots_adjust(wspace=0.4)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.67, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()    
