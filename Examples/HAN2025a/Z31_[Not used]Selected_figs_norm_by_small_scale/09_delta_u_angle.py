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
result_fig = f"{fig_path}/09_delta_u_angle"
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
    bottom=0.32,
    top=0.88,
    dpi=600,
    wspace=0.3
)


fig_id = 0
filter = 'gaussian'
filter_id = 1
for case_id, case in enumerate(A01.cases):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    eps = sl.result_json.get(0)['eps']
    delta_s_in_mm = sl.result_json.get(0)['delta_s_in_mm']
    Lf = sl.result_json.get(0)['Lf_in_mm']
    nor_tmp = (eps*delta_s_in_mm/1000)**(1/3)
    x = []
    y = []
    for deg in A01.degs:
        sl.load_result(deg)
        jump_u = sl.result_json.get(0)['jump_u']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(jump_u/nor_tmp)
    fig.plot(fig_id,x,y,label=A01.case_labels[case_id], color=colors[case_id])
print(A01.Lf_label[filter_id-1])

fig_id = 1
filter = 'gaussian'
filter_id = 5
for case_id, case in enumerate(A01.cases):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    eps = sl.result_json.get(0)['eps']
    delta_s_in_mm = sl.result_json.get(0)['delta_s_in_mm']
    Lf = sl.result_json.get(0)['Lf_in_mm']
    nor_tmp = (eps*delta_s_in_mm/1000)**(1/3)
    x = []
    y = []
    for deg in A01.degs:
        sl.load_result(deg)
        jump_u = sl.result_json.get(0)['jump_u']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(jump_u/nor_tmp)
    fig.plot(fig_id,x,y,color=colors[case_id])
print(A01.Lf_label[filter_id-1])

fig_id = 2
filter = 'gaussian'
filter_id = 9
for case_id, case in enumerate(A01.cases):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    eps = sl.result_json.get(0)['eps']
    delta_s_in_mm = sl.result_json.get(0)['delta_s_in_mm']
    Lf = sl.result_json.get(0)['Lf_in_mm']
    nor_tmp = (eps*delta_s_in_mm/1000)**(1/3)
    x = []
    y = []
    for deg in A01.degs:
        sl.load_result(deg)
        jump_u = sl.result_json.get(0)['jump_u']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(jump_u/nor_tmp)
    fig.plot(fig_id,x,y,color=colors[case_id])
print(A01.Lf_label[filter_id-1])

for i in range(3):
    fig.set_panel_label(i)
    fig.set_axis(i,ylim=(0,3))
    fig.set_axis(i,xlim=(0,180),xticks=[0,45,90,135,180],minor_xticks=None)
fig.set_label(0,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(1,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(2,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(0,labelpad=15, ylabel=r'$\Delta u/(\varepsilon \delta_s)^{1/3}$')
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.add_legend_bottom_rowmajor_manual(x=0.46,y=0.04,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
