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

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/10_Ar_angle"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.08),
    right_legend=False,     # reserve legend column
    left=0.07,
    right=0.98,
    bottom=0.3,
    top=0.85,
    dpi=600,
    wspace=0.3
)

fig_id = 0
filter = 'gaussian'
filter_id = 1
for case_id, case in enumerate(A01.cases):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    x = []
    y = []
    for deg in A01.degs:
        sl.load_result(deg)
        AR = sl.result_json.get(0)['AR']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(AR)
    fig.plot(fig_id,x,y,label=A01.case_labels[case_id], color=colors[case_id])
print(A01.Lf_label[filter_id-1])

fig_id = 1
filter = 'gaussian'
filter_id = 5
for case_id, case in enumerate(A01.cases):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    x = []
    y = []
    for deg in A01.degs:
        sl.load_result(deg)
        AR = sl.result_json.get(0)['AR']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(AR)
    fig.plot(fig_id,x,y,color=colors[case_id])
print(A01.Lf_label[filter_id-1])

fig_id = 2
filter = 'gaussian'
filter_id = 9
for case_id, case in enumerate(A01.cases):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    x = []
    y = []
    for deg in A01.degs:
        sl.load_result(deg)
        AR = sl.result_json.get(0)['AR']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(AR)
    fig.plot(fig_id,x,y,color=colors[case_id])
print(A01.Lf_label[filter_id-1])


for i in range(3):
    fig.set_panel_label(i)
    fig.set_axis(i,ylim=(0,8))
    fig.set_axis(i,xlim=(0,180),xticks=[0,45,90,135,180],minor_xticks=None)
fig.set_label(0,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(1,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(2,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(0,labelpad=15, ylabel=r'$A_R$')
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.legend(bbox_to_anchor=(-1.8, 0.5), handlelength= 1.5)
fig.add_legend_bottom_rowmajor_manual(x=0.46,y=0.04,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
