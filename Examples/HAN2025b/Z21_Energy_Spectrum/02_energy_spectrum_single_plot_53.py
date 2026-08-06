''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/02/05  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Q01_Plot.C00_cfg_for_cases import colors, linewidths
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
import numpy as np
from ZZZ_Result_Manager.A01_cases import cases, cases_f, cases_select, cases_select_labels, cases_select_w
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from ZZZ_Result_Manager.A01_cases import cases_select
from Z21_Energy_Spectrum.G01_energy_spectrum import EnergySpectrum as ES
from Z21_Energy_Spectrum.G02_model_spectrum import Pope_Spectrum as PS
from Z21_Energy_Spectrum.G02_model_spectrum import k53_line as k53

quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,4), right_legend=True, hspace=0.5, wspace=0.6, panel_offset=(-0.2,1.1))
','

ps = PS(1,200,1)
arr = np.logspace(0.01, 10, 100)
k_pope = arr * ps.eta 
E_pope = ps.model_spectrum(k_pope)

fig_id = 0
slope=2
for case_id, case in enumerate(cases_select):
    es = ES(cases_select_w[case_id])
    es.load()
    rm = RM(cases_select[case_id])
    eps = rm.result_table.get(11)['eps']
    eta = rm.result_table.get(11)['eta']
    kinetic_viscosity = rm.result_table.get(11)['kinetic_viscosity']
    x = es.wavenumber_xdir*eta
    y = es.spec_xdir[0]/(kinetic_viscosity**(5/4) * eps**(1/4)) * x**slope
    fig.plot(fig_id,x,y, color=colors[case_id], label= cases_select_labels[case_id])

# x,y = k53(1.1e-2,1e0,2e3)
# fig.plot(fig_id,x,y, color='k')

fig_id = 1
for case_id, case in enumerate(cases_select):
    es = ES(cases_select_w[case_id])
    es.load()
    rm = RM(cases_select[case_id])
    eps = rm.result_table.get(11)['eps']
    eta = rm.result_table.get(11)['eta']
    kinetic_viscosity = rm.result_table.get(11)['kinetic_viscosity']
    x = es.wavenumber_ydir*eta
    y = es.spec_ydir[1]/(kinetic_viscosity**(5/4) * eps**(1/4))* x**slope
    fig.plot(fig_id,x,y, color=colors[case_id])

# x,y = k53(1.1e-2,1e0,2e3)
# fig.plot(fig_id,x,y, color='k')

# fig.set_axis(0,xlim=(1e-2,2e0),ylim=(1e-2,1e4),xlog=True,ylog=True)
# fig.set_axis(1,xlim=(1e-2,2e0),ylim=(1e-2,1e4),xlog=True,ylog=True)
fig.set_axis(0,xlim=(1e-2,2e0),xlog=True,ylog=True)
fig.set_axis(1,xlim=(1e-2,2e0),xlog=True,ylog=True)
fig.set_label(0,ylabel=r'$E_u(\nu ^5 \varepsilon)^{-1/4}$')
fig.set_label(0,xlabel=r'$k_x\eta$')
fig.set_label(1,ylabel=r'$E_v(\nu ^5 \varepsilon)^{-1/4}$')
fig.set_label(1,xlabel=r'$k_y\eta$')
for fig_id in range(2):
    fig.set_panel_label(fig_id)

fig.set_margins(right=0.93)
fig.legend(bbox_to_anchor=(0.8,0.5))
fig.save(getplotpath()+"/energy_spectrum.png")
