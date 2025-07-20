''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/25  =
=========================
'''

import numpy as np
import matplotlib.pyplot as plt


from L01_modelspectrumRDT import Pao_AX, Pope_AX, k_range
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
Pao_AX.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(8), cm_to_inch(6))

fig_number = 2
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$k_{1}$ (m$^{-1}$)',r'$k_{1}$ (m$^{-1}$)']
ylables = [r'$E_{11}(k_{1})$',r'$E_{22}(k_2)/E_{11}(k_{1})$']
figtitles = ['E11','ratio_E22_E11']
xlims = [(1e-1,1e5)]
ylims = [(1e-8,1e0),(0,5)]
figformat = '.jpg'

for fig_id in range(fig_number):
    ax = axess[fig_id][0]
    axconfig = myaxconfig(ax = ax)
    axconfig.xlable = xlables[fig_id]
    axconfig.ylable = ylables[fig_id]
    # axconfig.xlim = xlims[0]
    axconfig.ylim = ylims[fig_id]
    axconfig.apply()

# -------------------------------------------------------------------------
# endregion
integral_L = 2e-2
Re_lamda = 50
epsilon = 4.5e4

k_range_long = k_range()
k_range_long.recommend_value(integral_L,Re_lamda)
k_range_trans = k_range()
k_range_trans.recommend_value(integral_L,Re_lamda)


Pope = Pope_AX(k_range_long, k_range_trans, L=integral_L, Re_lamda=Re_lamda, epsilon=epsilon)
Pope.cal_origin()
L_pope = Pope.cal_integral_scale(Pope.k_long,Pope.E11k1_origin)

'fig1'
ax = axess[0][0]
ax.set_xscale('log')
ax.set_yscale('log')
ax.plot(Pope.k_long, Pope.E11k1_origin,  color = 'k', label = 'Pope (origin)')

ax1 = axess[1][0]
ax1.set_xscale('log')
c = [1/3, 3]
for c_id in range(len(c)):
    Pope.cal_RDT_E11k1(c[c_id])
    Pope.cal_RDT_E22k2(c[c_id])
    ax.plot(Pope.k_long, Pope.E11k1, color = mycolors[c_id], linestyle = '-', label = f'c = {c[c_id]:.2f}')
    ax.plot(Pope.k_long, Pope.E22k2, color = mycolors[c_id], linestyle = '--', label = f'c = {c[c_id]:.2f}')

    ax1.plot(Pope.k_long, Pope.E22k2/Pope.E11k1, color = mycolors[c_id], linestyle = '-', label = f'c = {c[c_id]:.2f}')
    print(f'c_id:{c_id}')

# -------------------------------------------------------------------------
# region
for fig_id in range(fig_number):
    for ax in axess[fig_id]:
        ax.legend()
    fig = figs[fig_id]
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:], bbox_inches='tight', pad_inches=0.05)
plt.clf() 
# -------------------------------------------------------------------------
# endregion  