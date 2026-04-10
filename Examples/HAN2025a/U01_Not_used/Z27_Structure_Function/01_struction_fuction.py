''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from G01_struction_fuction import StructureFunction as SF

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01','Case01F_x0','Case01F_x15', 'Case01F_x30','Case01LowRe', 'Case01LowReF_x0','Mori_465']
cases = ['Case04', 'Case04F_x0', 'Case04F_x15','Case04F_x30','Mori_465']
mycolors[len(cases)-1] = 'k'
markers = ['o','s','^','D','v','P','*']
markersize = 2
# cases = cases + ['Case04', 'Case04F_x0', 'Case04F_x15','Case04F_x30']
# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(20), cm_to_inch(12))
# -------------------------------------------------------------------------
# endregion

fig_number = 2
fig_Nx = 2
fig_Ny = 2
figs, axess = generatefiglist(fig_number, fig_Ny, fig_Nx, figsize_inch)

xlables = [r'$r~\mathrm{(mm)}$',
           r'$r~\mathrm{(mm)}$']
ylables = [[r'$(\Delta u)^2(r)~\mathrm{(m^2/s^2)}$', r'$r^{-2/3}(\Delta u)^2(r)~\mathrm{(m^{4/3}/s^2)}$',
            r'$r^{-3/3}(\Delta u)^2(r)~\mathrm{(m^1/s^2)}$',r'$r^{-4/3}(\Delta u)^2(r)~\mathrm{(m^{2/3}/s^2)}$'],
           [r'$(\Delta v)^2(r)~\mathrm{(m^2/s^2)}$', r'$r^{-2/3}(\Delta v)^2(r)~\mathrm{(m^{4/3}/s^2)}$',
            r'$r^{-3/3}(\Delta v)^2(r)~\mathrm{(m^1/s^2)}$',r'$r^{-4/3}(\Delta v)^2(r)~\mathrm{(m^{2/3}/s^2)}$']]
figtitles = ['(Du)2', '(Dv)2']
xlims = [(0.5e2,3e4),(0.5e2,3e4)]
ylims = [[(1e-4,2e1), (1e2,1.5e4)],
         [(1e-4,2e1), (1e2,1.5e4)]]
figformat = '.jpg'
case_titles = cases

for fig_id in range(fig_number):
    for sub_fig_id in (range(fig_Nx*fig_Ny)):
        ax = axess[fig_id][sub_fig_id]
        axconfig = myaxconfig(ax = ax)
        axconfig.xlable = xlables[fig_id]
        axconfig.ylable = ylables[fig_id][sub_fig_id]
        # axconfig.xlim = xlims[fig_id]
        # axconfig.ylim = ylims[fig_id][sub_fig_id]
        axconfig.apply()

targets = [-2/3,-3/3,-4/3]
for case_number in range(len(cases)):
    sf = SF(cases[case_number])
    sf.load()
    shift = 1
    "fig1"
    fig_id = 0
    plot_x = sf.r_xdir
    plot_y = sf.sf_xdir[0]
    ax = axess[fig_id][0]
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(plot_x, plot_y, linestyle = '-', color = mycolors[case_number], marker = markers[case_number],
            markersize = markersize, label = case_titles[case_number])

    ax = axess[fig_id][1]
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(plot_x, plot_y*(plot_x**targets[0]), color = mycolors[case_number], marker = markers[case_number],
            markersize = markersize)

    ax = axess[fig_id][2]
    ax.set_xscale('log')
    ax.set_yscale('log')    
    ax.plot(plot_x, plot_y*(plot_x**targets[1]), color = mycolors[case_number], marker = markers[case_number],
            markersize = markersize)


    ax = axess[fig_id][3]
    ax.set_xscale('log')
    ax.set_yscale('log')    
    ax.plot(plot_x, plot_y*(plot_x**targets[2]), color = mycolors[case_number], marker = markers[case_number],
            markersize = markersize)

    "fig2"
    fig_id = 1
    ax = axess[fig_id][0]
    ax.set_xscale('log')
    ax.set_yscale('log')

    plot_x = sf.r_ydir
    plot_y = sf.sf_ydir[1]
    ax.plot(plot_x, plot_y, linestyle = '-', color = mycolors[case_number], marker = markers[case_number],
            markersize = markersize, label = case_titles[case_number])

    ax = axess[fig_id][1]
    ax.set_xscale('log')
    ax.set_yscale('log') 
    ax.plot(plot_x, plot_y*(plot_x**targets[0]), color = mycolors[case_number], marker = markers[case_number],
            markersize = markersize)

    ax = axess[fig_id][2]
    ax.set_xscale('log')
    ax.set_yscale('log') 
    ax.plot(plot_x, plot_y*(plot_x**targets[1]), color = mycolors[case_number], marker = markers[case_number],
            markersize = markersize)
    ax = axess[fig_id][3]
    ax.set_xscale('log')
    ax.set_yscale('log') 
    ax.plot(plot_x, plot_y*(plot_x**targets[2]), color = mycolors[case_number], marker = markers[case_number],
            markersize = markersize)

for fig_number in range(len(figs)):
    fig = figs[fig_number]

    label_index = ['a','b','c','d','e','f']
    for i, ax in enumerate(axess[fig_number]):
        if i < len(label_index):
            ax.text(-0.1, 1.12, fr'$\textbf{{({label_index[i]})}}$',
                    transform=ax.transAxes,
                    fontsize=12, fontweight='bold',
                    va='top', ha='left')  
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(top = 0.9, bottom = 0.22, left = 0.1, right=0.78)
    fig.subplots_adjust(wspace=0.5, hspace=0.4)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.78, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()   