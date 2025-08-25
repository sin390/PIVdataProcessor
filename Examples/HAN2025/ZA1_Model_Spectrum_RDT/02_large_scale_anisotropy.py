''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/06/02  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np

from G03_large_scale_anisotropy import LargeScaleAnisotropy as LSA
from G02_RDT_integral import RDT_integral_calculator as RIC
from G01_modelspectrumRDT import RDT_Axis_Symmetric_Strain
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
LSA.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(12), cm_to_inch(9))
# endregion

# -------------------------------------------------------------------------
# region
fig_number = 2
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$c$', r'$\overline{u_{1}^2}/\overline{u_{2}^2}$']
ylables = [r'$\overline{u_{1}^2}/\overline{u_{2}^2}$', r'$L_{11}/L_{22}$']
figtitles = ['c-uu_vv','uu_vv-L11_L22']
xlims = [(0,100)]
ylims = [(-0.2,1)]
figformat = '.jpg'

for fig_id in range(fig_number):
    for ax in axess[fig_id]:
        axconfig = myaxconfig(ax = ax)
        axconfig.xlable = xlables[fig_id]
        axconfig.ylable = ylables[fig_id]
        # axconfig.xlim = xlims[fig_id]
        # axconfig.ylim = ylims[fig_id]
        axconfig.apply()
# endregion

# -------------------------------------------------------------------------
# region

cases = ['Re_100']
Pope = RDT_Axis_Symmetric_Strain(casename = cases[0])
Pope.load_origin()
Pope.load_E11k1(c=0.5)
Pope.load_E22k2(c=0.5)
dk = Pope.k_range_long.dk
test_c = [0.5]
u11 = np.sum(Pope.k_long*Pope.E11k1*dk)
u22 = np.sum(Pope.k_long*Pope.E22k2*dk)
test_ratio = [u11/u22]

'fig1'
ax = axess[0][0]




# analytical solution
c = np.linspace(1.01,10,50)
alpha2 = 1 - c**(-3)
alpha = np.sqrt(alpha2)
uu = 3.0/(4.0*c**2)
uu *= (1+alpha2)/(2*alpha**3)*np.log((1+alpha)/(1-alpha)) - alpha**(-2)
vv = 3.0/(4.0*c**2)
vv *= 1.0/(2*alpha2)-(1-alpha2)/(4*alpha**3)*np.log((1+alpha)/(1-alpha))
vv += 3.0*c/4


ax.plot(c, uu/vv, label = r'Analytical solution (Bachelor)')

ric = RIC()
c = np.logspace(-1, 1, 100)
uu_vv_ric = c.copy()
L11_L22_ric = c.copy()
for i in range(len(c)):
    ric.calculate(c[i])
    uu_vv_ric[i]=ric.u11u22
    L11_L22_ric[i] = ric.L11L22
ax.plot(c, uu_vv_ric, label = r'Numerical solution (Han)', linestyle = '-.')
ax.plot(test_c, test_ratio, 'o', color='red', label = r'RDT (Han)')

'fig2'
uu_vv_org = [2.01, 2.26, 2.50, 2.47, 2.55, 2.71]
L11_L22_org = [1.05, 1.54, 1.82, 1.53, 1.81, 1.92]
uu_vv_rm = [1.25, 1.55, 1.55, 1.54, 1.75, 1.77]
L11_L22_rm = [0.42, 0.69, 0.70, 0.60, 0.83, 0.85]
uu_vv_rm2 = [1.18, 1.30, 1.30, 1.34, 1.46, 1.49]
L11_L22_rm2 = [0.29, 0.40, 0.40, 0.38, 0.53, 0.55]
plt.plot(1, 1, 'o', color='red')
ax = axess[1][0]
ax.plot(uu_vv_org,L11_L22_org, marker='x', linestyle = 'None', label= 'experiment')
ax.plot(uu_vv_ric,L11_L22_ric, label = 'Numerical solution (Han)')
ax.plot()
# endregion

# -------------------------------------------------------------------------
# region
for fig_id in range(fig_number):
    for ax in axess[fig_id]:
        ax.legend()
    fig = figs[fig_id]
    fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format='jpg')
plt.clf()
# endregion
