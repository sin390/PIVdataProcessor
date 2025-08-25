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

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
mycolors[6] = 'k'
# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(12), cm_to_inch(7))
# -------------------------------------------------------------------------
# endregion

fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$k~\mathrm{(m^{-1})}$']
ylables = [r'$E_{u}(k_x)/E_{v}(k_y)$']
figtitles = ['E11_E22']
xlims = [(0.8e2,1e4)]
ylims = [(0.5,2)]
figformat = '.pdf'
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

    fig_id = 0
    ax = axess[fig_id][0]    
    k1 = es.wavenumber_xdir
    E11 = es.spec_xdir[0]
    f1 = interp1d(k1, E11, kind='cubic', fill_value="extrapolate")    
    k2 = es.wavenumber_ydir
    E22 = es.spec_ydir[1]
    f2 = interp1d(k2, E22, kind='cubic', fill_value="extrapolate")

    left = np.max([k1[0],k2[0]])
    right = np.min([k1[-1],k2[-1]])
    k = np.linspace(left,right,100)
    E11_uni = f1(k)
    E22_uni = f2(k)
    ax.set_xscale('log')
    stat = 0
    ax.plot(k[stat:], E11_uni[stat:]/E22_uni[stat:] ,linestyle = '-', color = mycolors[case_number], label = case_titles[case_number])
    ax.axhline(1, linestyle = '-.', linewidth = 0.8, color = 'k')

f_EuEv = 'EuEv_Ratio_x605mm.txt'
k, EuEv = np.loadtxt(f_EuEv, unpack=True,skiprows=1)

fig_id = 0
ax = axess[fig_id][0]
ax.plot(k, EuEv, color = 'k', label = r'Mori et al.')


for fig_number in range(len(figs)):
    fig = figs[fig_number]
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(right=0.7,bottom = 0.15,top=0.9)
    fig.subplots_adjust(hspace=0.7)
    fig.subplots_adjust(wspace=0.3)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.72, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()  