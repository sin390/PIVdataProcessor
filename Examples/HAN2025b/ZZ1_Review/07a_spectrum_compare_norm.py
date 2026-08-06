''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/05/30  =
=========================
'''

import numpy as np
import matplotlib.pyplot as plt
from Q01_Plot.L01_piv_plot import PlotFigure 
from Q01_Plot.C00_cfg_for_cases import colors, linewidths
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath
from scipy.interpolate import interp1d

import ZZZ_Result_Manager.A01_cases as A01
from Z21_Energy_Spectrum.G01_energy_spectrum import EnergySpectrum as ES
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/07_spectrum_compare"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=1,
    figsize=(31, 9),      # cm, physical size is sacred
    figsize_unit="cm",
    right_legend=True,     # reserve legend column
    left=0.33,
    right=0.73,
    bottom=0.20,
    dpi=600
)


fig_id = 0
# for case_id, case in enumerate(A01.cases_select):
case_id = 2

ds = DS(A01.cases_select_f[case_id], 'gaussian',0)
eta = ds.result_json.get(0)['eta']
viscosity = ds.result_json.get(0)['kinematic_viscosity']
eps = ds.result_json.get(0)['DissipationRate']

es = ES(A01.cases_select_f[case_id])
es.load()

k1 = es.wavenumber_xdir
E11 = es.spec_xdir[0]

k2 = es.wavenumber_ydir
E22 = es.spec_ydir[1]

# fig.plot(fig_id,k1,E11,  yerr=errorE11/2, color=colors[0], label= r'$E_u(k_x)$',xlog=True,ylog=True)
# fig.plot(fig_id,k2,E22,  yerr=errorE22/2, color=colors[1], label= r'$E_v(k_y)$',xlog=True,ylog=True)
fig.plot(fig_id,k1*eta, E11/(viscosity**(5/4) * eps**(1/4)),  color=colors[0], label= r'$E_u(k_x)$',xlog=True,ylog=True)
fig.plot(fig_id,k2*eta, E22/(viscosity**(5/4) * eps**(1/4)),  color=colors[1], label= r'$E_v(k_y)$',xlog=True,ylog=True)

# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.add_legend_inside(loc="upper right",handlelength=1.5,fontsize=16)
fig.legend(bbox_to_anchor=(-0.8,0.5))
# fig.set_axis(0,xlim=(5e1,5e3))
fig.set_axis(0,xlim=(1e-2,5e0))
fig.set_label(0,ylabel=r'$E\nu ^{-5/4} \varepsilon^{-1/4}$')
fig.set_label(0,xlabel=r'$k_x\eta, k_y\eta$')

# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)

