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
from Z25_Autocorrelation.G01_autocorrelation_TDM import AutoCorrelation as AC
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/03_ratio_dudx_Lf"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.06),
    right_legend=False,     # reserve legend column
    left=0.1,
    right=0.99,
    bottom=0.3,
    top=0.85,
    wspace=0.65,
    dpi=600
)

fig_id = 0
filter = 'gaussian'
for case_id, case in enumerate(A01.cases):
    rm = RM(case) 

    x=[]
    y=[]
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        x.append(2*np.pi/A01.Lf_coeff[filter_id])
        ac = AC(case,filter,filter_param)
        ac.load()
        ac.cal_L_thr(0.3679)
        y.append(ac.result_json.get(0)['L_thr_Is_x']/ac.result_json.get(0)['L_thr_Is_y'])
    fig.plot(fig_id,x,y,marker='^',markersize = 5,ifmarker=True, color=colors[case_id],label=A01.case_labels[case_id],xlog=True)
fig.plot(fig_id,[0,100],[1,1], color=colors[case_id],xlog=True)

fig_id = 1
filter = 'gaussian'
for case_id, case in enumerate(A01.cases):
    rm = RM(case) 
    Lfs = rm.result_table.get(2)['Lfs']
    x=[]
    y=[]
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        x.append(2*np.pi/A01.Lf_coeff[filter_id])
        ac = AC(case,filter,filter_param)
        ac.load()
        ac.cal_L_thr(0.3679)
        y.append(ac.result_json.get(0)['L_thr_Is_y'])
    fig.plot(fig_id,x,y,marker='^',markersize = 5,ifmarker=True, color=colors[case_id],xlog=True,ylog=True)




for i in range(3):
    fig.set_panel_label(i)

fig.set_axis(0,xlim=(10,110),ylim=(0,2))
# fig.set_axis(1,xlim=(10,110),ylim=(0,2))
# fig.set_axis(2,xlim=(10,110),ylim=(0,2))
fig.set_label(0,xlabel=r'$2\pi L_{u_1} /L_f $')
fig.set_label(1,xlabel=r'$2\pi L_{u_1} /L_f $')
fig.set_label(2,xlabel=r'$2\pi L_{u_1} /L_f $')
fig.set_label(0,
              ylabel=r'$\widetilde u_{1,\mathrm{rms}}/ \widetilde u_{2,\mathrm{rms}}$',
              labelpad= 15)
fig.set_label(1,
              ylabel=r'$\frac{\left( \partial \widetilde u_1 / \partial x_1 \right){\mathrm{rms}}}{\left( \partial \widetilde u_2 / \partial x_2 \right){\mathrm{rms}}}$',
              labelpad= 15)
fig.set_label(2,
              ylabel=r'$\frac{\left( \partial \widetilde u_1 / \partial x_2 \right){\mathrm{rms}}}{\left( \partial \widetilde u_2 / \partial x_1 \right){\mathrm{rms}}}$',
              labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.legend(bbox_to_anchor=(-1.5, 0.5), handlelength= 1.5, fontsize=16)
fig.add_legend_bottom_rowmajor_manual(x=0.46,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# fig.add_legend_inside(handlelength= 1.5,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
