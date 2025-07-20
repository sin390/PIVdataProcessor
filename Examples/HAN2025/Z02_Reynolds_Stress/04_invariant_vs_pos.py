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

xlables = [r'$x-x_{c}$ (mm)',r'$x-x_{c}$ (mm)']
ylables = [r'$\xi$',r'$\eta$']

figtitles = ['xi-xc','eta-xc']
ylims = [(0,0.2),(0,0.2)]
xlims = [(-60,60),(-60,60)]
figformat = '.eps'
cases_title = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']

for axes_number in range(len(figs)):
    ax = axess[axes_number][0]
    axconfig = myaxconfig(ax = ax)
    axconfig.xlable = xlables[axes_number]
    axconfig.ylable = ylables[axes_number]
    axconfig.xlim = xlims[axes_number]
    axconfig.ylim = ylims[axes_number]
    axconfig.apply()

for case_number in range(len(cases)):
    rs = RS(cases[case_number])
    rs.load()

    invariant_xi = nanmean_filter2d(rs.invariant_xi,kernel_size=8)
    invariant_eta = nanmean_filter2d(rs.invariant_eta,kernel_size=8)
    
    central_x, central_y = pBase.CaseInfo.Central_Position_Flow
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]


    'fig1'
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = invariant_xi[left:right,central_y]
    axess[0][0].plot(plot_x, plot_y,  color = mycolors[case_number], label = f'{cases_title[case_number]}')

    'fig2'
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = invariant_eta[left:right,central_y]
    axess[1][0].plot(plot_x, plot_y,  color = mycolors[case_number], label = f'{cases_title[case_number]}')

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