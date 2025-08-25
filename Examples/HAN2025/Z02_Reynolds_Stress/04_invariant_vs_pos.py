''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Z01_VelocityDistribution')))

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from G01_reynolds_stress import ReynoldsStress as RS


from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist
from pivdataprocessor.A01_toolbox import nanmean_filter2d

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


fig_number = 2
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$x~(\mathrm{mm})$',r'$x~(\mathrm{mm})$']
ylables = [r'$\xi$',r'$\eta$']

figtitles = ['xi-x','eta-x']
ylims = [(0,0.3),(0,0.3)]
xlims = [(-60,60),(-60,60)]
xticks = [
    [-50,0,50],
    [-50,0,50]
]
figformat = '.pdf'
cases_title = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6', 'Mori et al.']
mycolors[6] = 'k'

for axes_number in range(len(figs)):
    ax = axess[axes_number][0]
    axconfig = myaxconfig(ax = ax)
    axconfig.xlable = xlables[axes_number]
    axconfig.ylable = ylables[axes_number]
    axconfig.xlim = xlims[axes_number]
    axconfig.xticks = xticks[axes_number]
    axconfig.ylim = ylims[axes_number]
    axconfig.apply()

for case_number in range(len(cases)):
    rs = RS(cases[case_number]+'_sub1')
    rs.load()
    sub1_xi = rs.invariant_xi.copy()
    sub1_eta = rs.invariant_eta.copy()
    rs = RS(cases[case_number]+'_sub2')
    rs.load()
    sub2_xi = rs.invariant_xi.copy()
    sub2_eta = rs.invariant_eta.copy()
    xi_for_uncertainty = (sub1_xi - sub2_xi)**2
    eta_for_uncertainty = (sub1_eta - sub2_eta)**2
    xi_uncertainty = np.sqrt(nanmean_filter2d(xi_for_uncertainty, kernel_size=8))
    eta_uncertainty = np.sqrt(nanmean_filter2d(eta_for_uncertainty, kernel_size=8))

    rs = RS(cases[case_number])
    rs.load()

    invariant_xi = nanmean_filter2d(rs.invariant_xi,kernel_size=8)
    invariant_eta = nanmean_filter2d(rs.invariant_eta,kernel_size=8)
    # invariant_xi = rs.invariant_xi
    # invariant_eta = rs.invariant_eta  
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    errorbar_x,_ = pBase.pos_mm_to_index_list([-25,0,25],[0,0,0])

    'fig1'
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = invariant_xi[left:right,central_y]
    axess[0][0].plot(plot_x, plot_y,  color = mycolors[case_number], label = f'{cases_title[case_number]}')

    'fig2'
    plot_x = pBase.X[0][left:right,central_y]
    if cases[case_number] == 'Mori465':
        plot_x = plot_x - pBase.X[0][central_x,central_y]
    plot_y = invariant_eta[left:right,central_y]
    axess[1][0].plot(plot_x, plot_y,  color = mycolors[case_number], label = f'{cases_title[case_number]}')
    err_x = [pBase.X[0][xi,central_y] for xi in errorbar_x]
    err_y = [invariant_eta[xi, central_y] for xi in errorbar_x]
    yerr = [eta_uncertainty[xi, central_y]/2 for xi in errorbar_x]
    axess[1][0].errorbar(err_x, err_y, yerr=yerr, fmt='none', linestyle='none', color=mycolors[case_number],
                        capsize=2, elinewidth=0.5, markersize=2)    
    print(f'Case: {cases[case_number]}, uu_avg: {np.nanmean(rs.uu[left:right, bottom:up]):.3f}')
    print(f'Case: {cases[case_number]}, vv_avg: {np.nanmean(rs.vv[left:right, bottom:up]):.3f}')
    print(f'Case: {cases[case_number]}, kt_avg: {np.nanmean(rs.k2[left:right, bottom:up]):.3f}')
    print(f'Case: {cases[case_number]}, ratio_uu_vv_avg: {np.nanmean(rs.uu[left:right, bottom:up])/np.nanmean(rs.vv[left:right, bottom:up]):.3f}')
    print(f'Case: {cases[case_number]}, eta_avg: {np.nanmean(rs.invariant_eta[left:right, bottom:up]):.3f}')


for fig_id in range(len(figs)):
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