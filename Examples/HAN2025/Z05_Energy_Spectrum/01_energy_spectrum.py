''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import numpy as np
from scipy.interpolate import interp1d

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from G01_energy_spectrum import EnergySpectrum as ES

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06', 'Mori465']
mycolors[6] = 'k'
# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(14), cm_to_inch(8))
# -------------------------------------------------------------------------
# endregion

fig_number = 2
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$k_x$ (m$^{-1}$)',
           r'$k_y$ (m$^{-1}$)']
ylables = [r'$E_{11}(k_{x})$',
           r'$E_{22}(k_{y})$']
figtitles = ['E11', 'E22']
xlims = [(0.5e2,1e4),(0.5e2,1e4)]
ylims = [(1e-4,1e1), (1e-4,1e1)]
figformat = '.eps'
case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6', 'Mori et al.']
for fig_id in range(fig_number):
    ax = axess[fig_id][0]
    axconfig = myaxconfig(ax = ax)
    axconfig.xlable = xlables[fig_id]
    axconfig.ylable = ylables[fig_id]
    axconfig.xlim = xlims[fig_id]
    axconfig.ylim = ylims[fig_id]
    axconfig.apply()

for case_number in range(len(cases)):
    es = ES(cases[case_number])
    es.load()

    "fig1"
    fig_id = 0
    ax = axess[fig_id][0]
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(es.wavenumber_xdir,es.spec_xdir[0],linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    
    'sub1'
    if case_number == 0:
        axins1 = inset_axes(ax,
                            width="25%", height="25%",  # 相对主图大小
                            loc='lower left',
                            bbox_to_anchor=(0.18, 0.15, 1, 1),
                            bbox_transform=ax.transAxes,
                            borderpad=0)
        axins1.set_xscale('log')
        axins1.set_yscale('log')    
        axins1.set_xlim(0.5e2,1e4)
        axins1.set_ylim(1e2,2e4)
        axins1.tick_params(labelsize=8)
        axins1.set_xlabel(r'$k_{x}$', fontsize=8)
        axins1.set_ylabel(r'$E_{11}(k_x)/k_x^{-5/3}$', fontsize=8)

    target = 5/3
    axins1.plot(es.wavenumber_xdir, es.spec_xdir[0]*(es.wavenumber_xdir**target), linewidth = 0.8, color = mycolors[case_number])

    'sub2'
    if case_number == 0:
        axins2 = inset_axes(ax,
                            width="25%", height="25%",  # 相对主图大小
                            loc='upper right',
                            bbox_to_anchor=(-0.05, -0.12, 1, 1),
                            bbox_transform=ax.transAxes,
                            borderpad=0)
        axins2.set_xscale('log')
        axins2.set_yscale('log')    
        axins2.set_xlim(0.5e2,1e4)
        axins2.set_ylim(1e3,1e5)
        axins2.tick_params(labelsize=8)
        axins2.set_xlabel(r'$k_{x}$', fontsize=8)
        axins2.set_ylabel(r'$E_{11}(k_{x})/k_{x}^{-2}$', fontsize=8)

    target = 2
    axins2.plot(es.wavenumber_xdir, es.spec_xdir[0]*(es.wavenumber_xdir**target), linewidth = 0.8, color = mycolors[case_number])

    "fig2"
    fig_id = 1
    ax = axess[fig_id][0]
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(es.wavenumber_ydir,es.spec_ydir[1],linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    'sub1'
    if case_number == 0:
        axins3 = inset_axes(ax,
                            width="25%", height="25%",  # 相对主图大小
                            loc='lower left',
                            bbox_to_anchor=(0.18, 0.15, 1, 1),
                            bbox_transform=ax.transAxes,
                            borderpad=0)
        axins3.set_xscale('log')
        axins3.set_yscale('log')    
        axins3.set_xlim(0.5e2,1e4)
        axins3.set_ylim(1e2,2e4)
        axins3.tick_params(labelsize=8)
        axins3.set_xlabel(r'$k_{y}$', fontsize=8)
        axins3.set_ylabel(r'$E_{22}(k_{y})/k_{y}^{-5/3}$', fontsize=8)

    target = 5/3
    axins3.plot(es.wavenumber_ydir, es.spec_ydir[1]*(es.wavenumber_ydir**target), linewidth = 0.8, color = mycolors[case_number])

    'sub2'
    if case_number == 0:
        axins4 = inset_axes(ax,
                            width="25%", height="25%",  # 相对主图大小
                            loc='upper right',
                            bbox_to_anchor=(-0.05, -0.12, 1, 1),
                            bbox_transform=ax.transAxes,
                            borderpad=0)
        axins4.set_xscale('log')
        axins4.set_yscale('log')    
        axins4.set_xlim(0.5e2,1e4)
        axins4.set_ylim(1e3,1e5)
        axins4.tick_params(labelsize=8)
        axins4.set_xlabel(r'$k_{y}$', fontsize=8)
        axins4.set_ylabel(r'$E_{11}(k_{y})/k_{y}^{-2}$', fontsize=8)

    target = 2
    axins4.plot(es.wavenumber_ydir, es.spec_ydir[1]*(es.wavenumber_ydir**target), linewidth = 0.8, color = mycolors[case_number])  



for fig_number in range(len(figs)):
    fig = figs[fig_number]
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(right=0.75,bottom = 0.15,top=0.95)
    fig.subplots_adjust(hspace=0.7)
    fig.subplots_adjust(wspace=0.3)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.78, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()  