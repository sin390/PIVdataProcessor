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
result_fig = f"{fig_path}/04_delta_u_delta_s"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=2,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.06),
    right_legend=False,     # reserve legend column
    left=0.12,
    right=0.98,
    bottom=0.18,
    top=0.85,
    wspace=0.25,
    dpi=600
)

fig_id = 0
for case_id, case in enumerate(A01.cases_select):
    rm = RM(case) 
    eta = rm.result_table.get(3)['eta']
    viscosity = rm.result_table.get(3)['kinetic_viscosity']
    eps = rm.result_table.get(3)['eps']
    velocity_eta = (viscosity*eps)**(0.25)
    x=[]
    y=[]
    for Lf_id, _ in enumerate(A01.coeffs_to_eta):
        sl = SL(A01.cases_select_w[case_id],'gaussian',Lf_id+1)
        sl.load_result(None)
        jump_u = sl.result_json.get(0)['jump_u']
        delta_s_in_m = sl.result_json.get(0)['delta_s_in_mm']/1000
        x.append(delta_s_in_m/eta)
        y.append(jump_u/velocity_eta)

    fig.plot(fig_id,x,y,label=A01.cases_select_labels[case_id],marker='^',markersize = 5,ifmarker=True, color=colors[case_id])


fig_id = 1
for case_id, case in enumerate(A01.cases_select):
    rm = RM(case) 
    eta = rm.result_table.get(3)['eta']
    viscosity = rm.result_table.get(3)['kinetic_viscosity']
    eps = rm.result_table.get(3)['eps']
    velocity_eta = (viscosity*eps)**(0.25)
    x=[]
    y=[]
    for Lf_id, _ in enumerate(A01.coeffs_to_eta):
        sl = SL(A01.cases_select_w[case_id],'gaussian',Lf_id+1)
        sl.load_result(None)
        jump_u = sl.result_json.get(0)['jump_u']
        delta_s_in_m = sl.result_json.get(0)['delta_s_in_mm']/1000
        x.append(delta_s_in_m/eta)
        tmp = (eps*delta_s_in_m)**(1/3)
        y.append(jump_u/tmp) 
    fig.plot(fig_id,x,y, color=colors[case_id],marker='^',markersize = 5,ifmarker=True,)

for i in range(2):
    fig.set_panel_label(i)

fig.set_axis(0,xlim=(0,60),ylim=(0,8))
fig.set_axis(1,xlim=(0,60),ylim=(0,3))
fig.set_label(0,xlabel=r'$\delta_S/\eta$')
fig.set_label(0,ylabel=r'$\Delta u/u_\eta$',labelpad= 15)
fig.set_label(1,xlabel=r'$\delta_S/\eta$')
fig.set_label(1,ylabel=r'$\Delta u/(\varepsilon \delta_s)^{1/3}$',labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.legend(bbox_to_anchor=(-2, 0.5), handlelength= 1.5)
fig.add_legend_inside(handlelength= 1.5,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
