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

# pyright: reportMissingImports=false
from G01_fitted_slope import FittedSlope as FS
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist
from pivdataprocessor.A01_toolbox import nanmean_filter2d

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(33), cm_to_inch(19))
# -------------------------------------------------------------------------
# endregion


fig_number = 2
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$-\frac{\partial \overline{U}_1}{\partial x_1} \, (\mathrm{s}^{-1})$',
           r'$-\frac{\partial \overline{U}_1}{\partial x_1} \, (\mathrm{s}^{-1})$']
ylables = [r'$\xi$',r'$\eta$']

figtitles = ['xi-S11','eta-S11']
ylims = [(0,0.2),(0,0.2)]
xlims = [(0,1100),(0,1100)]
figformat = '.jpg'

lines = ['-','-','-','-.','-.','-.']


for case_number in range(len(cases)):
    rs = RS(cases[case_number])
    rs.load()
    fs = FS(cases[case_number])
    fs.load_fitted()
    invariant_xi = rs.invariant_xi
    invariant_eta = rs.invariant_eta
    invariant_xi = nanmean_filter2d(rs.invariant_xi,kernel_size=7)
    invariant_eta = nanmean_filter2d(rs.invariant_eta,kernel_size=7)
    for axes_number in range(len(axess)):
        ax = axess[axes_number]
        axconfig = myaxconfig(ax = ax)
        # axconfig.title = cases[case_number]
        axconfig.xlable = xlables[axes_number]
        axconfig.ylable = ylables[axes_number]
        axconfig.ylim = ylims[axes_number]
        axconfig.xlim = xlims[axes_number]
        axconfig.apply()
    
    central_x, central_y = pBase.CaseInfo.Central_Position_Flow
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]


    'fig1'
    plot_x = fs.fit_avg_dUdX[0][0][left:right,central_y]*(-1000)
    plot_y = invariant_xi[left:right,central_y]
    axess[0].plot(plot_x, plot_y, linestyle = lines[case_number], color = mycolors[case_number], label = f'{cases[case_number]}')


    'fig2'
    plot_x = fs.fit_avg_dUdX[0][0][left:right,central_y]*(-1000)
    plot_y = invariant_eta[left:right,central_y]
    axess[1].plot(plot_x, plot_y, linestyle = lines[case_number], color = mycolors[case_number], label = f'{cases[case_number]}')


    
    for axes_number in range(len(figs)):
        ax = axess[axes_number]
        ax.legend()


for fig_id in range(fig_number):
    fig = figs[fig_id]
    fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format='jpg')
plt.clf()       