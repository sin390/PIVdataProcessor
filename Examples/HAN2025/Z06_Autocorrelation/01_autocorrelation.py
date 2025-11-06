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
from pivdataprocessor.A01_toolbox import nanmean_filter1d

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
figformat = '.pdf'
case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']

for i in range(3):
    for j in range(2):
        case_number = i*2+j
        ac = AC(cases[case_number]+'_sub1')
        ac.load()
        sub1_Fu = ac.autocorr_xdir[0].copy()
        sub1_Fv = ac.autocorr_ydir[1].copy()
        ac = AC(cases[case_number]+'_sub2')
        ac.load()
        sub2_Fu = ac.autocorr_xdir[0].copy()
        sub2_Fv = ac.autocorr_ydir[1].copy()
        F_u_len = min(len(sub1_Fu),len(sub2_Fu))
        F_v_len = min(len(sub1_Fv),len(sub2_Fv))  
        F_u_for_uncertainty = (sub1_Fu[:F_u_len] - sub2_Fu[:F_u_len])**2
        F_v_for_uncertainty = (sub1_Fv[:F_v_len] - sub2_Fv[:F_v_len])**2
        F_u_uncertainty = np.sqrt(nanmean_filter1d(F_u_for_uncertainty, 8))/2
        F_v_uncertainty = np.sqrt(nanmean_filter1d(F_v_for_uncertainty, 8))/2
  
        ac = AC(cases[case_number])
        ac.load()

        target_len = len(ac.r_xdir)
        current_len = len(F_u_uncertainty)
        if current_len < target_len:
            pad_len = target_len - current_len
            F_u_uncertainty = np.concatenate([F_u_uncertainty, np.full(pad_len, np.nan)])
        target_len = len(ac.r_ydir)
        current_len = len(F_v_uncertainty)
        if current_len < target_len:
            pad_len = target_len - current_len
            F_v_uncertainty = np.concatenate([F_v_uncertainty, np.full(pad_len, np.nan)])

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
        axess[fig_id][case_number].errorbar(ac.r_xdir[::2],ac.autocorr_xdir[0][::2], yerr=F_u_uncertainty[::2]/2, fmt='none',  color=mycolors[0],
                            capsize=2, elinewidth=0.5, markersize=2)
        axess[fig_id][case_number].plot(ac.fitting_part[1],ac.fitting_part[0], linewidth=0.8, linestyle = '-.', color = mycolors[0])
        axess[fig_id][case_number].plot(ac.r_ydir,ac.autocorr_ydir[1],  linestyle = '-', color = mycolors[1],
                                label = r'$f_2(r)$')
        axess[fig_id][case_number].plot(ac.fitting_part[3],ac.fitting_part[2], linewidth=0.8, linestyle = '-.', color = mycolors[1])
        axess[fig_id][case_number].errorbar(ac.r_ydir[::2],ac.autocorr_ydir[1][::2], yerr=F_v_uncertainty[::2]/2, fmt='none',  color=mycolors[1],
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
    fig.subplots_adjust(left=0.1, right=0.8, top=0.94, bottom=0.1, wspace=0.32, hspace=0.6)


    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.82, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:])
plt.clf()    