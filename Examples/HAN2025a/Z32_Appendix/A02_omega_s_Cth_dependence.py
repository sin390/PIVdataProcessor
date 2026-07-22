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
from Q01_Plot.C00_cfg_for_cases import colors, linewidths, markers, markersizes
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath

import ZZZ_Result_Manager.A01_cases as A01
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

linestyles = [
    '-',
    (6, (19, 3)),                  # 长破线，24
    (3.5, (14, 3, 2, 3)),            # 一点划线，24
    (3, (11, 3, 2, 3, 2, 3)),       
    '-',
    (6, (19, 3)),                  # 长破线，24
    (3.5, (14, 3, 2, 3)),           # 一点划线，24
    (3, (11, 3, 2, 3, 2, 3)),  
]

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/A01_Cth_dependence"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=2,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.06),
    right_legend=True,     # reserve legend column
    left=0.12,
    right=0.88,
    bottom=0.18,
    top=0.85,
    wspace=0.6,
    dpi=600
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
    fig.plot(fig_id,x,y,label=Cth_label[curve_id], color=colors[curve_id],linestyle = linestyles[curve_id])

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
    fig.plot(fig_id,x,y, color=colors[curve_id],linestyle = linestyles[curve_id])


for i in range(2):
    fig.set_panel_label(i)
fig.set_axis(0,xlim=(-3,3),ylim=(-0.3,1.1))
fig.set_axis(1,xlim=(-3,3),ylim=(-1,1))
fig.set_label(0,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(1,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(0,labelpad=15, ylabel=r'$\overline{\widetilde{\omega}_S}/ (\overline{\widetilde{\omega}_S})_0$')
fig.set_label(1,labelpad=15, ylabel=r"$\overline{\tilde{u}'_1}/u_{\mathrm{rms}}$")
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend(bbox_to_anchor=(-2.0, 0.5), handlelength= 2.2, fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
