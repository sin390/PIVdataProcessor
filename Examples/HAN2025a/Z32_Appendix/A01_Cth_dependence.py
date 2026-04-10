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
result_fig = f"{fig_path}/A01_Cth_dependence"
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
    wspace=0.5
)

plotted_filter_param = [1,2,3,4,5,6,7]

fig_id = 0
filter = 'gaussian'
case_id = 0
filter_id = 4
Cths = [1,1.5,2,2.5,3]
Cth_label = [rf'$C_{{th}} = {Cths[i]:.2f}$' for i in range(len(Cths))]
print(A01.Lf_label[filter_id])

for curve_id, Cth in enumerate(Cths):
    sl = SL(A01.cases[case_id], filter, filter_id+1)
    sl.load_result(Cth=Cth)
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]   
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y,label=Cth_label[curve_id], color=colors[curve_id])

fig_id = 1
rm = RM(A01.cases[case_id]) 
urms = rm.result_table.get(1)['urms']
for curve_id, Cth in enumerate(Cths):
    sl = SL(A01.cases[case_id], filter, filter_id+1)
    sl.load_result(Cth=Cth)
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    jump_u = sl.result_json.get(0)['jump_u']
    mag = sl.avg_u_BRF[0]/jump_u 
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y, color=colors[curve_id])

fig_id = 2
rm = RM(A01.cases[case_id])
L11 = rm.result_table.get(1)['L11']
urms1 = rm.result_table.get(1)['urms']
for curve_id, Cth in enumerate(Cths):
    x=[]
    y=[]
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        sl = SL(A01.cases[case_id],'gaussian',filter_param)
        sl.load_result(None,Cth)
        jump_u = sl.result_json.get(0)['jump_u']
        delta_s_in_m = sl.result_json.get(0)['delta_s_in_mm']/1000
        x.append(delta_s_in_m/L11)
        tmp = (urms1**3/L11*delta_s_in_m)**(1/3)
        y.append(jump_u/tmp) 

    fig.plot(fig_id,x,y, color=colors[curve_id],marker='^',markersize = 4,ifmarker=True)

for i in range(3):
    fig.set_panel_label(i)
fig.set_axis(0,xlim=(-5,5),ylim=(-0.3,1.1))
fig.set_axis(1,xlim=(-5,5),ylim=(-1,1))
fig.set_axis(2,xlim=(0,0.25),ylim=(0,3))
fig.set_label(0,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(0,labelpad=15, ylabel=r'$\left\langle\widetilde{\omega}_S \right\rangle_\mathrm{norm}$')
fig.set_label(1,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(1,labelpad=15, ylabel=r'$\left\langle\widetilde{u}_{\boldsymbol{\zeta}_x} \right\rangle/\Delta u$')
fig.set_label(2,xlabel=r'$\delta_S/\eta$')
fig.set_label(2,ylabel=r'$\Delta u(u_{1,\mathrm{rms}}^3L_{u_1}^{-1} \delta_s)^{-1/3}$',labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.add_legend_bottom_rowmajor_manual(x=0.6,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
