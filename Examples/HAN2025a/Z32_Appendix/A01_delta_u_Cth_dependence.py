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

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/A01_Cth_dependence"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=1,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.16,1.06),
    right_legend=True,     # reserve legend column
    left=0.33,
    right=0.73,
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
Cth_label = [rf'$C_{{th}} = {Cths[i]:.1f}$' for i in range(len(Cths))]
print(A01.Lf_label[filter_id])

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

    fig.plot(fig_id,x,y, color=colors[curve_id],label=Cth_label[curve_id],
             marker=markers[curve_id],markersize = markersizes[curve_id],ifmarker=True, markerfacecolor='none')


fig.set_axis(0,xlim=(0,0.25),ylim=(0,3))
fig.set_label(0,xlabel=r'$\delta_S/L_u$')
fig.set_label(0,ylabel=r'$(\Delta u/u_{\mathrm{rms}})/(\delta_S/L_{u})^{1/3}$',labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend(bbox_to_anchor=(-2.0, 0.5), handlelength= 2.2, fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
