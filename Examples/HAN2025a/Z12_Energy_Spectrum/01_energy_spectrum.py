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

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Z11_Dissipation_Rate')))
# pyright: reportMissingImports=false
from G01_dissipation_rate import DissipationRate as DR

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from G01_energy_spectrum import EnergySpectrum as ES
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['All100','Grad','AntiGrad','Shear']
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

xlabels = [r'$k_x\eta$',
           r'$k_y\eta$']
ylabels = [r'$E_{11}(k_{x})/(\epsilon\nu^{5})^{1/4}$',
           r'$E_{22}(k_{y})/(\epsilon\nu^{5})^{1/4}$']
figtitles = ['E11', 'E22']
xlims = [(1e-3,1e1),(1e-3,1e1)]
ylims = [(1e-4,1e6), (1e-4,1e6)]
figformat = '.jpg'
case_titles = ['All100','Grad','AntiGrad','Shear']
for fig_id in range(fig_number):
    ax = axess[fig_id][0]
    axconfig = myaxconfig(ax = ax)
    axconfig.xlable = xlabels[fig_id]
    axconfig.ylable = ylabels[fig_id]
    axconfig.xlim = xlims[fig_id]
    axconfig.ylim = ylims[fig_id]
    axconfig.apply()


kinetic_viscosity = np.zeros(len(cases))
eta = np.zeros(len(cases))
epsilons = np.zeros(len(cases))
for case_number in range(len(cases)):
    dr = DR(cases[case_number])
    dr.load()
    kinetic_viscosity[case_number] = dr.Result.Kinematic_viscosity
    eta[case_number] = dr.Result.eta
    epsilons[case_number] = dr.Result.DissipationRate

for case_number in range(len(cases)):
    es = ES(cases[case_number])
    es.load()

    "fig1"
    fig_id = 0
    ax = axess[fig_id][0]
    ax.set_xscale('log')
    ax.set_yscale('log')
    x = es.wavenumber_xdir*eta[case_number]
    y = es.spec_xdir[0]/(kinetic_viscosity[case_number]**(5/4) * epsilons[case_number]**(1/4))
    ax.plot(x,y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    

    "fig2"
    fig_id = 1
    ax = axess[fig_id][0]
    ax.set_xscale('log')
    ax.set_yscale('log')
    x = es.wavenumber_ydir*eta[case_number]
    y = es.spec_ydir[1]/(kinetic_viscosity[case_number]**(5/4) * epsilons[case_number]**(1/4))
    ax.plot(x,y,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])

fig_id = 0
ax = axess[fig_id][0]
x1, y1 = 0.05, 1e3
x2 = 0.5
y2 = y1 * (x2 / x1)**(-5/3)
ax.plot([x1, x2], [y1, y2], 'k--', linewidth=1, label=r'$-5/3 law$')
fig_id = 1
ax = axess[fig_id][0]
ax.plot([x1, x2], [y1, y2], 'k--', linewidth=1, label=r'$-5/3 law$')

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