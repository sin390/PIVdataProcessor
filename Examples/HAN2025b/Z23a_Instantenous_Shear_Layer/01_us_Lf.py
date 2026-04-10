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
from Z23a_Instantenous_Shear_Layer.G01_instantenous_shear_layer import ShearLayer as SL
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/01_us_Lf"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.07),
    right_legend=False,     # reserve legend column
    left=0.1,
    right=0.98,
    bottom=0.32,
    top=0.88,
    dpi=600,
    wspace=0.3
)

fig_id = 0
for case_id, case in enumerate(A01.cases):
    x=[]
    y=[]
    n = 1
    rm = RM(A01.cases[case_id])
    eta = rm.result_table.get(1)['eta']
    Lfs_in_mm = rm.result_table.get(2)['Lfs']
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        sl = SL(A01.cases[case_id],'gaussian',filter_param)
        sl.load_result(None)
        n_list = sl.result_json.get(1)['n_list']
        index = n_list.index(n)
        v_jump_array = sl.result_json.get(1)['v_jump_array'] 
 
        Lf = Lfs_in_mm[filter_id]/1000
        y_tmp = v_jump_array[index]
        # y_tmp /= (v_jump_array[0]**n_list[n-1])
        y_tmp = y_tmp/(Lf/eta)**(n/3)
        x.append(Lf/eta)
        y.append(y_tmp)

    fig.plot(fig_id,x,y,label=A01.case_labels[case_id], color=colors[case_id], marker='^',markersize = 5,ifmarker=True)

fig_id = 1
for case_id, case in enumerate(A01.cases):
    x=[]
    y=[]
    n = 3
    rm = RM(A01.cases[case_id])
    eta = rm.result_table.get(1)['eta']
    Lfs_in_mm = rm.result_table.get(2)['Lfs']
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        sl = SL(A01.cases[case_id],'gaussian',filter_param)
        sl.load_result(None)
        n_list = sl.result_json.get(1)['n_list']
        index = n_list.index(n)
        v_jump_array = sl.result_json.get(1)['v_jump_array'] 
 
        Lf = Lfs_in_mm[filter_id]/1000
        y_tmp = v_jump_array[index]
        # y_tmp /= (v_jump_array[0]**n_list[n-1])
        y_tmp = y_tmp/(Lf/eta)**(n/3)
        x.append(Lf/eta)
        y.append(y_tmp)

    fig.plot(fig_id,x,y, color=colors[case_id],marker='^',markersize = 5,ifmarker=True)

fig_id = 2
for case_id, case in enumerate(A01.cases):
    x=[]
    y=[]
    n = 5
    rm = RM(A01.cases[case_id])
    eta = rm.result_table.get(1)['eta']
    Lfs_in_mm = rm.result_table.get(2)['Lfs']
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        sl = SL(A01.cases[case_id],'gaussian',filter_param)
        sl.load_result(None)
        n_list = sl.result_json.get(1)['n_list']
        index = n_list.index(n)
        v_jump_array = sl.result_json.get(1)['v_jump_array'] 
 
        Lf = Lfs_in_mm[filter_id]/1000
        y_tmp = v_jump_array[index]
        # y_tmp /= (v_jump_array[0]**n_list[n-1])
        y_tmp = y_tmp/(Lf/eta)**(n/3)
        x.append(Lf/eta)
        y.append(y_tmp)

    fig.plot(fig_id,x,y, color=colors[case_id],marker='^',markersize = 5,ifmarker=True)

text = [f'$n=1$','$n=3$','$n=5$']
for i in range(3):
    fig.set_panel_label(i,text[i])

fig.set_axis(0,xlim=(0,1200),ylim=(0,5))
fig.set_axis(1,xlim=(0,1200),ylim=(0,100))
fig.set_axis(2,xlim=(0,1200),ylim=(0,10000))
# fig.set_axis(1,xlim=(10,40),ylim=(0,3))

fig.set_label(0,xlabel=r'$L_f/\eta$')
fig.set_label(1,xlabel=r'$L_f/\eta$')
fig.set_label(2,xlabel=r'$L_f/\eta$')
fig.set_label(0,ylabel=r'$\left\langle {u_S}^n\right\rangle/(L_f/\eta)^{n/3}$',labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.legend(bbox_to_anchor=(-2.2, 0.5), handlelength= 1.5, fontsize=16)
fig.add_legend_bottom_rowmajor_manual(x=0.46,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
