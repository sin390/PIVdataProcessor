''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/25  =
=========================
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator

from G01_modelspectrumRDT import RDT_Axis_Symmetric_Strain
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
RDT_Axis_Symmetric_Strain.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(16), cm_to_inch(5.5))

fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 2, figsize_inch)

xlables = [r'$k_{1}~(\mathrm{m^{-1}})$']
ylables = [r'$E_{11}(k_{1})~(\mathrm{m^{3}s^{-2}})$',r'$E_{11}(k_{1})/k_{1}^{-5/3}$']
figtitles = ['E11']
xlims = [(1e1,1e5)]
xtricks = [1e2, 1e3, 1e4, 1e5]
ylims = [(1e-7,1e-1),(1e-3,1e3)]
figformat = '.pdf'
for fig_id in range(fig_number):
    for ax_id in range(2):
        ax = axess[fig_id][ax_id]
        axconfig = myaxconfig(ax = ax)
        axconfig.xlable = xlables[0]
        axconfig.ylable = ylables[ax_id]
        axconfig.xlim = xlims[0]
        axconfig.xticks = xtricks
        axconfig.ylim = ylims[ax_id]
        axconfig.apply()

# -------------------------------------------------------------------------
# endregion
cases = ['Re_300']
Pope = RDT_Axis_Symmetric_Strain(casename = cases[0])
Pope.load_origin()
Pope.load_E11k1(c=0.25)

'fig1'
ax = axess[0][0]
ax.set_xscale('log')
ax.set_xticks([1e1, 1e2, 1e3, 1e4, 1e5])
ax.set_yscale('log')
ax.set_yticks([1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1])
ax.plot(Pope.k_long, Pope.E11k1_origin*2,  color = 'k', label = 'Initial (isotropic)')
ax.plot(Pope.k_long, Pope.E11k1*2, color = mycolors[0], label = 'RDT (c=0.25)')

f_ori = 'E11_origin.txt'   # 对应 cal_origin_polar 输出
f_rdt = 'E11k1_RDT.txt'      # 对应 cal_RDT_E11k1_polar 输出
k_ori, E11_ori = np.loadtxt(f_ori, unpack=True)
k_rdt, E11_rdt = np.loadtxt(f_rdt, unpack=True)
ax.plot(k_ori, E11_ori, linestyle = '-.', color = 'k', label = 'Initial(fortran)')
ax.plot(k_rdt, E11_rdt, linestyle = '-.', color = mycolors[0], label = 'RDT(fortran)')
ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
# x_ref = 2e2  # 参考点的 x 坐标
# y_ref_m53 = 1e-2  # 参考点的 y 坐标
# y_ref_m2 = 0.8e-2  # 参考点的 y 坐标
# # 生成一系列 x 点用于画线（注意要在合适的范围内）
# x_fit = np.logspace(np.log10(x_ref), np.log10(x_ref * 20), 100)

# # 对应斜率线的 y 值
# y_m53 = y_ref_m53 * (x_fit / x_ref) ** (-5/3)
# y_m2  = y_ref_m2 * (x_fit / x_ref) ** (-2)

# ax.plot(x_fit, y_m53, 'k--')

ax = axess[0][1]
ax.set_xscale('log')
ax.set_xticks([1e1, 1e2, 1e3, 1e4, 1e5])
ax.set_yscale('log')
target = 5/3
ax.plot(Pope.k_long, Pope.E11k1_origin*(Pope.k_long)**target,  color = 'k', label = 'Initial')
ax.plot(Pope.k_long, Pope.E11k1*(Pope.k_long)**target, color = mycolors[0], label = 'RDT')
ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
ax.plot(k_ori, E11_ori*(k_ori)**target, linestyle = '-.', color = 'k', label = 'Initial(fortran)')
ax.plot(k_rdt, E11_rdt*(k_rdt)**target, linestyle = '-.', color = mycolors[0], label = 'RDT(fortran)')

for fig_number in range(len(figs)):
    fig = figs[fig_number]

    label_index = ['a','b','c','d','e','f']
    for i, ax in enumerate(axess[fig_number]):
        if i < len(label_index):
            ax.text(-0.35, 1.12, fr'$\textbf{{({label_index[i]})}}$',
                    transform=ax.transAxes,
                    fontsize=12, fontweight='bold',
                    va='top', ha='left')  
    handles, labels = [], []
    for line in axess[fig_number][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(top = 0.9, bottom = 0.22, left = 0.1, right=0.72)
    fig.subplots_adjust(wspace=0.5)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.73, 0.5), borderaxespad=0)
    # fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()   