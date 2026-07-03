''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/02/20  =
=========================
'''

import numpy as np
import matplotlib.pyplot as plt
from Q01_Plot.L01_piv_plot import PlotFigure 
from Q01_Plot.C00_cfg_for_cases import colors, linewidths
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath

import ZZZ_Result_Manager.A01_cases as A01
from Z21_Energy_Spectrum.G01_energy_spectrum import EnergySpectrum as ES
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/02_energy_spectra"
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
for case_id, case in enumerate(A01.cases_select):
    ds = DS(A01.cases_select_f[case_id], 'gaussian',0)
    eta = ds.result_json.get(0)['eta']
    viscosity = ds.result_json.get(0)['kinematic_viscosity']
    eps = ds.result_json.get(0)['DissipationRate']

    es = ES(A01.cases_select_w[case_id])
    es.load()

    x = es.wavenumber_xdir*eta
    y = es.spec_xdir[0]/(viscosity**(5/4) * eps**(1/4))
    fig.plot(fig_id,x,y, color=colors[case_id], label= A01.cases_select_labels[case_id],xlog=True,ylog=True)
ax = fig.get_ax(fig_id)
ax.axvspan(2*np.pi/80, 2*np.pi/20, alpha=0.2, color='gray')

model_x = np.array([1e-2,1e0])/eta
model_y = 0.49*eps**(2/3)*model_x**(-5/3)

x = model_x*eta
y = model_y/(viscosity**(5/4) * eps**(1/4))
line = fig.plot(fig_id,x,y, color='k', linestyle = '-.',linewidth = 0.8, xlog=True,ylog=True)
line.set_dashes([6,3])  

# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.add_legend_inside(loc="upper right",handlelength=1.5,fontsize=16)
fig.legend(bbox_to_anchor=(-0.8,0.5))
fig.set_label(0,ylabel=r'$E_u(\nu ^5 \varepsilon)^{-1/4}$')
fig.set_label(0,xlabel=r'$k_x\eta$')

# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
