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
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/06_omega_s_norm_across_case"
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

fig_id = 0
filter = 'gaussian'
filter_id = 1
for case_id, case in enumerate(A01.cases[:-1]):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]   
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y,label=A01.case_labels[case_id], color=colors[case_id])
print(A01.Lf_label[filter_id-1])

fig_id = 1
filter = 'gaussian'
filter_id = 5
for case_id, case in enumerate(A01.cases[:-1]):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]   
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y,color=colors[case_id])
print(A01.Lf_label[filter_id-1])

fig_id = 2
filter = 'gaussian'
filter_id = 9
for case_id, case in enumerate(A01.cases[:-1]):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]   
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y,color=colors[case_id])
print(A01.Lf_label[filter_id-1])

for i in range(3):
    fig.set_panel_label(i)
    fig.set_axis(i,xlim=(-5,5),xticks=[-4,-2,0,2,4])
    fig.set_axis(i,ylim=(-0.3,1.1))
fig.set_label(0,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(1,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(2,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(0,labelpad=15, ylabel=r'$\left\langle\widetilde{\omega}_S \right\rangle_\mathrm{norm}$')
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.add_legend_bottom_rowmajor_manual(x=0.53,y=0.04,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
