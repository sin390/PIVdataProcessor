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

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/08_Ar_Lf"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.07),
    right_legend=False,     # reserve legend column
    left=0.06,
    right=0.98,
    bottom=0.32,
    top=0.88,
    dpi=600,
    wspace=0.4
)

fig_id = 0
for case_id, case in enumerate(A01.cases):
    x=[]
    y=[]
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        sl = SL(A01.cases[case_id],'gaussian',filter_param)
        sl.load_result(None)
        eta = sl.result_json.get(0)['eta']
        Lf = sl.result_json.get(0)['Lf_in_mm']/1000
        Ar = sl.result_json.get(0)['AR']
        x.append(Lf/eta)
        y.append(Ar)

    fig.plot(fig_id,x,y,label=A01.case_labels[case_id], color=colors[case_id], marker='^',markersize = 5,ifmarker=True,)

fig_id = 1
for case_id, case in enumerate(A01.cases):
    x=[]
    y=[]
    for filter_id, filter_param in enumerate(A01.gaussian_id): 
        sl = SL(A01.cases[case_id],'gaussian',filter_param)
        sl.load_result(None)
        eta = sl.result_json.get(0)['eta']
        Lf = sl.result_json.get(0)['Lf_in_mm']/1000
        Lx = sl.result_json.get(0)['L_x']/1000
        x.append(Lf/eta)
        y.append(Lx/Lf)

    fig.plot(fig_id,x,y, color=colors[case_id],marker='^',markersize = 5,ifmarker=True,)

fig_id = 2
for case_id, case in enumerate(A01.cases):
    x=[]
    y=[]
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        sl = SL(A01.cases[case_id],'gaussian',filter_param)
        sl.load_result(None)
        eta = sl.result_json.get(0)['eta']
        Lf = sl.result_json.get(0)['Lf_in_mm']/1000
        Ly = sl.result_json.get(0)['L_y']/1000
        x.append(Lf/eta)
        y.append(Ly/Lf)

    fig.plot(fig_id,x,y, color=colors[case_id],marker='^',markersize = 5,ifmarker=True,)

for i in range(3):
    fig.set_panel_label(i)

fig.set_axis(0,xlim=(0,1200),ylim=(0,8),minor_yticks=1)
fig.set_axis(1,xlim=(0,1200),ylim=(0,8),minor_yticks=1)
fig.set_axis(2,xlim=(0,1200),ylim=(0,2),minor_yticks=1)
# fig.set_axis(1,xlim=(10,40),ylim=(0,3))

fig.set_label(0,xlabel=r'$L_f/\eta$')
fig.set_label(1,xlabel=r'$L_f/\eta$')
fig.set_label(2,xlabel=r'$L_f/\eta$')
fig.set_label(0,ylabel=r'$A_R$',labelpad= 15)
fig.set_label(1,ylabel=r'$L_x/L_f$',labelpad= 15)
fig.set_label(2,ylabel=r'$L_y/L_f$',labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.legend(bbox_to_anchor=(-2.2, 0.5), handlelength= 1.5, fontsize=16)
fig.add_legend_bottom_rowmajor_manual(x=0.46,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
