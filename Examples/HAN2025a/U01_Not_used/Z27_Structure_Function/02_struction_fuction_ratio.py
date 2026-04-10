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
from G01_struction_fuction import StructureFunction as SF

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

# cases = ['Case01', 'Case01F_x0', 'Case01F_x15', 'Case01F_x30']
# cases = cases+['Case04', 'Case04F_x0', 'Case04F_x15','Case04F_x30']
linestyles = ['-' for _ in range(10)]+['-.' for _ in range(4)]
# for i in range(4):
#     mycolors[i+4] = mycolors[i]
cases = ['Case01','Case01F_x0','Case01F_x15', 'Case01F_x30','Case01LowRe', 'Case01LowReF_x0','Mori_465']
# cases = ['Case04', 'Case04F_x0', 'Case04F_x15','Case04F_x30','Mori_465']
mycolors[len(cases)-1] = 'k'
markers = ['o','s','^','D','v','P','*']
markersize = 2
# for i in [0,4]:
#     linestyles[i] = '--'
# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(14), cm_to_inch(7))
# -------------------------------------------------------------------------
# endregion

fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$2\pi /r~\mathrm{(m^{-1})}$']
ylables = [r'$(\Delta u)^2/(\Delta v)^2$']
figtitles = ['Du2_Dv2_Ratio']
xlims = [(0.8e2,5e4)]
ylims = [(0,2.5)]
figformat = '.jpg'

case_titles = cases
for fig_id in range(fig_number):
    ax = axess[fig_id][0]
    axconfig = myaxconfig(ax = ax)
    axconfig.xlable = xlables[fig_id]
    axconfig.ylable = ylables[fig_id]
    axconfig.xlim = xlims[fig_id]
    axconfig.ylim = ylims[fig_id]
    axconfig.apply()

for case_number in range(len(cases)):
    sf = SF(cases[case_number])
    sf.load()

    fig_id = 0
    ax = axess[fig_id][0]    
    
    r1 = sf.r_xdir
    Du2 = sf.sf_xdir[0]
    f1 = interp1d(np.log(r1), np.log(Du2), kind='cubic', fill_value="extrapolate")

    r2 = sf.r_ydir
    Dv2 = sf.sf_ydir[1]
    f2 = interp1d(np.log(r2), np.log(Dv2), kind='cubic', fill_value="extrapolate")

    left = np.max([r1[0], r2[0]])
    right = np.min([r1[-1], r2[-1]])
    r = np.logspace(np.log10(left), np.log10(right), 50)

    Du2_uni = np.exp(f1(np.log(r)))
    Dv2_uni = np.exp(f2(np.log(r)))

    ax.set_xscale('log')
    stat = 0
    ax.plot(2*np.pi/r[stat:]*1000, Du2_uni[stat:] / Dv2_uni[stat:], 
            linestyle=linestyles[case_number], color=mycolors[case_number], 
            marker=markers[case_number], markersize=markersize,
            label=case_titles[case_number])
    ax.axhline(1, linestyle='-.', linewidth=0.8, color='k')


for fig_number in range(len(figs)):
    fig = figs[fig_number]
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(right=0.6,bottom = 0.15,top=0.9)
    fig.subplots_adjust(hspace=0.7)
    fig.subplots_adjust(wspace=0.3)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.62, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()  