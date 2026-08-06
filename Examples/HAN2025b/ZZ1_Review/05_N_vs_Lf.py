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


figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/05_N_vs_Lf"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=1,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    # panel_fontsize= 20,
    panel_offset=(-0.12,1.08),
    right_legend=False,     # reserve legend column
    left=0.32,
    right=0.72,
    bottom=0.18,
    top=0.88,
    dpi=600,
    wspace=0.3
)

fig_id = 0
for case_id, case in enumerate(A01.cases_select):
    x=[]
    y=[]
    for Lf_id, _ in enumerate(A01.coeffs_to_eta):
        sl = SL(A01.cases_select_w[case_id],'gaussian',Lf_id+1)
        sl.load_result(None)
        eta = sl.result_json.get(0)['eta']
        Lf = sl.result_json.get(0)['Lf_in_mm']/1000
        N_layer = sl.result_json.get(0)['identified_LSL_number']
        x.append(Lf/eta)
        y.append(N_layer)

    fig.plot(fig_id,x,y,label=A01.cases_select_labels[case_id], color=colors[case_id],marker='^',markersize = 5,ifmarker=True,)


fig.set_axis(0,xlim=(0,90),ylim=(1e3,1e6),ylog=True)
# fig.set_axis(0,xlim=(0,90),ylim=(0.8e4,1e6),ylog=True)
# fig.set_axis(1,xlim=(10,40),ylim=(0,3))

fig.set_label(0,xlabel=r'$L_F/L_u$')
fig.set_label(0,ylabel=r'$N_{S}$',labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.add_legend_inside(handlelength=1.5,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)    