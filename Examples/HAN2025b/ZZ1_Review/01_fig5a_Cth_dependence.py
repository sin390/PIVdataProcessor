''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/05/28  =
=========================
'''

import numpy as np
import matplotlib.pyplot as plt
from Q01_Plot.L01_piv_plot import PlotFigure 
from Q01_Plot.C00_cfg_for_cases import colors, linewidths
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath

import ZZZ_Result_Manager.A01_cases as A01
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/01_fig5a_Cth_dependence"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.05),
    right_legend=False,     # reserve legend column
    left=0.08,
    right=0.98,
    bottom=0.32,
    top=0.9,
    dpi=600,
    wspace=0.3
)

case_id = 2

fig_id = 0
filter = 'gaussian'
C_th = 2
for Lf_id, _ in enumerate(A01.coeffs_to_eta):
    sl = SL(A01.cases_select_w[case_id], filter, Lf_id+1)
    sl.load_result(None, Cth=C_th)
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]   
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y,label=A01.Lf_labels[Lf_id], color=colors[Lf_id])

fig_id = 1
filter = 'gaussian'
C_th = 3
for Lf_id, _ in enumerate(A01.coeffs_to_eta):
    sl = SL(A01.cases_select_w[case_id], filter, Lf_id+1)
    sl.load_result(None, Cth=C_th)
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]   
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y, color=colors[Lf_id])

fig_id = 2
filter = 'gaussian'
C_th = 4
for Lf_id, _ in enumerate(A01.coeffs_to_eta):
    sl = SL(A01.cases_select_w[case_id], filter, Lf_id+1)
    sl.load_result(None, Cth=C_th)
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]   
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y, color=colors[Lf_id])


for i in range(3):
    fig.set_panel_label(i)
    fig.set_axis(i, xlim=(-4,4), ylim=(-0.3,1.1))
fig.set_label(0,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(1,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(2,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(0,labelpad=15, ylabel=r'$\overline{\widetilde{\omega}_S}/ (\overline{\widetilde{\omega}_S})_0$')
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.add_legend_bottom_rowmajor_manual(x=0.5,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
