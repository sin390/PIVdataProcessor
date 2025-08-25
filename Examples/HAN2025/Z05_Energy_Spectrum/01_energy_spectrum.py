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
from G01_energy_spectrum import EnergySpectrum as ES

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
mycolors[6] = 'k'
# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(16), cm_to_inch(5.5))
# -------------------------------------------------------------------------
# endregion

fig_number = 2
fig_Nx = 2
fig_Ny = 1
figs, axess = generatefiglist(fig_number, fig_Ny, fig_Nx, figsize_inch)

xlables = [r'$k_x~\mathrm{(m^{-1})}$',
           r'$k_y~\mathrm{(m^{-1})}$']
ylables = [[r'$E_{u}(k_{x})~\mathrm{(m^3/s^2)}$', r'$k_x^{5/3}E_{u}~\mathrm{(m^{4/3}/s^2)}$'],
           [r'$E_{v}(k_{y})~\mathrm{(m^3/s^2)}$', r'$k_y^{5/3}E_{v}~\mathrm{(m^{4/3}/s^2)}$']]
figtitles = ['E11', 'E22']
xlims = [(0.5e2,1e4),(0.5e2,1e4)]
ylims = [[(1e-4,2e1), (1e2,1.5e4)],
         [(1e-4,2e1), (1e2,1.5e4)]]
figformat = '.pdf'
case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6', 'Mori et al.']

for fig_id in range(fig_number):
    for sub_fig_id in (range(fig_Nx*fig_Ny)):
        ax = axess[fig_id][sub_fig_id]
        axconfig = myaxconfig(ax = ax)
        axconfig.xlable = xlables[fig_id]
        axconfig.ylable = ylables[fig_id][sub_fig_id]
        axconfig.xlim = xlims[fig_id]
        axconfig.ylim = ylims[fig_id][sub_fig_id]
        axconfig.apply()

target = 5/3
for case_number in range(len(cases)):
    es = ES(cases[case_number])
    es.load()

    "fig1"
    fig_id = 0
    ax = axess[fig_id][0]
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(es.wavenumber_xdir,es.spec_xdir[0],linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    
    ax = axess[fig_id][1]
    ax.set_xscale('log')
    ax.set_yscale('log')    


    ax.plot(es.wavenumber_xdir, es.spec_xdir[0]*(es.wavenumber_xdir**target), color = mycolors[case_number])


    "fig2"
    fig_id = 1
    ax = axess[fig_id][0]
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.plot(es.wavenumber_ydir,es.spec_ydir[1],linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])

    ax = axess[fig_id][1]
    ax.set_xscale('log')
    ax.set_yscale('log') 
    ax.plot(es.wavenumber_ydir, es.spec_ydir[1]*(es.wavenumber_ydir**target), color = mycolors[case_number])

f_Eu = 'Eu_kx_x605mm.txt'
f_Ev = 'Ev_ky_x605mm.txt' 
k_x, Eu = np.loadtxt(f_Eu, unpack=True,skiprows=1)
k_y, Ev = np.loadtxt(f_Ev, unpack=True,skiprows=1)
fig_id = 0
ax = axess[fig_id][0]
ax.plot(k_x, Eu, color = 'k', label = r'Mori et al.')
ax = axess[fig_id][1]
ax.plot(k_x, Eu*(k_x**target), color = 'k', label = r'Mori et al.')

fig_id = 1
ax = axess[fig_id][0]
ax.plot(k_y, Ev, color = 'k', label = r'Mori et al.')
ax = axess[fig_id][1]
ax.plot(k_y, Ev*(k_y**target), color = 'k', label = r'Mori et al.')

for fig_number in range(len(figs)):
    fig = figs[fig_number]

    label_index = ['a','b','c','d','e','f']
    for i, ax in enumerate(axess[fig_number]):
        if i < len(label_index):
            ax.text(-0.25, 1.12, fr'$\textbf{{({label_index[i]})}}$',
                    transform=ax.transAxes,
                    fontsize=12, fontweight='bold',
                    va='top', ha='left')  
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(top = 0.9, bottom = 0.22, left = 0.1, right=0.78)
    fig.subplots_adjust(wspace=0.5)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.8, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()   