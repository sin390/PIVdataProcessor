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
from Z21_Energy_Spectrum.G01_Spectrum_1D import EnergySpectrum as ES
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/01_energy_spectrum"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=2,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.16,1.06),
    right_legend=True,     # reserve legend column
    left=0.1,
    right=1,
    bottom=0.18,
    top=0.85,
    wspace=0.6,
    dpi=600
)

fig_id = 0
for case_id, case in enumerate(A01.cases):
    es = ES(case, filter='gaussian', filter_id= -1)
    es.load()
    
    rm = RM(case)
    urms1 = rm.result_table.get(1)['urms']
    L11 = rm.result_table.get(1)['L11']
    y = es.spec_xdir[0]
    x = es.wavenumber_xdir
    y_nom = urms1**2 * L11
    x_nom = L11
    x = x * x_nom
    y = y / y_nom
    y = x**(5/3) * y
    fig.plot(fig_id,x,y,xlog=True,ylog=True, label= A01.case_labels[case_id],color=colors[case_id],marker='^',markersize = 4,ifmarker=True,)
    

fig_id = 1
for case_id, case in enumerate(A01.cases):
    es = ES(case, filter='gaussian', filter_id= -1)
    es.load()
    y = es.spec_xdir[0]
    x = es.wavenumber_xdir
    rm = RM(case)
    epsilon = rm.result_table.get(1)['dissipationRate']
    Upsilon = rm.result_table.get(1)['kinetic_viscosity']
    eta = rm.result_table.get(1)['eta']
    y_nom = epsilon*(Upsilon**5)
    y_nom = y_nom**(1/4)
    x_nom = eta
    x = x * x_nom
    y = y / y_nom
    y = x**(5/3) * y
    fig.plot(fig_id,x,y,xlog=True,ylog=True,color=colors[case_id],marker='^',markersize = 4,ifmarker=True,)


for i in range(2):
    fig.set_panel_label(i)

fig.set_axis(0,xlog=True,ylog=True,xlim=(1.5e0,3e2),ylim=(0.4e-1, 1.2e0))
fig.set_axis(1,xlim=(0.5e-3,1e-1),ylim=(0.5e-1, 1.5e0))
fig.set_label(0,xlabel=r'$k_1L_{u_1}$')
fig.set_label(0,ylabel=r'$(k_1L_{u_1})^{5/3}E_{u_1}/(u_{1,\mathrm{rms}}^2L_{u_1})$',labelpad= 8)
fig.set_label(1,xlabel=r'$k_1\eta$')
fig.set_label(1,ylabel=r'$(k_1\eta)^{5/3}E_{u_1}/(\varepsilon ^{2/3}\eta^{5/3})$',labelpad= 8)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend(bbox_to_anchor=(-2, 0.5), handlelength= 1.5)
# fig.add_legend_inside(handlelength= 1.5,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
