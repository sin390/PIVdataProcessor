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
from Z11_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/02_dis_I"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=2,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.16,1.06),
    right_legend=True,     # reserve legend column
    left=0.1,
    right=0.95,
    bottom=0.18,
    top=0.85,
    wspace=0.6,
    dpi=600
)

case_id = 2
case = A01.cases[case_id]
plotted_filter_param = [2,3,4,5,6,7,8]
filter = 'gaussian'

fig_id = 0
for curve_id, filter_param in enumerate(plotted_filter_param):
    filter_id = filter_param-1
    td = TD(case, filter, filter_param)
    td.load_avg()
    central_X, central_Y = td.vfh.central_pos_grid
    left,right,bottom,up = td.vfh.unpackrange(td.vfh.effctive_range)
    x = td.vfh.X[0,left:right,central_Y]
    y = td.avg_intensity_shear[left:right,central_Y]
    fig.plot(fig_id,x,y, label=A01.Lf_label[filter_id],color=colors[curve_id])


fig_id = 1
for curve_id, filter_param in enumerate(plotted_filter_param):
    filter_id = filter_param-1
    td = TD(case, filter, filter_param)
    td.load_avg()
    central_X, central_Y = td.vfh.central_pos_grid
    left,right,bottom,up = td.vfh.unpackrange(td.vfh.effctive_range)
    x = td.vfh.X[0,left:right,central_Y]
    y = td.avg_intensity_rotation[left:right,central_Y]
    fig.plot(fig_id,x,y,color=colors[curve_id])

for i in range(2):
    fig.set_panel_label(i)

fig.set_axis(0,xlim=(-50,50),ylim=(0,5000))
fig.set_axis(1,xlim=(-50,50),ylim=(0,1200))
fig.set_label(0,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_label(0,ylabel=r'$\widetilde{I}_\mathrm{S}~\mathrm{(s^{-1})}$',labelpad=12)
fig.set_label(1,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_label(1,ylabel=r'$\widetilde{I}_\mathrm{R}~\mathrm{(s^{-1})}$',labelpad=12)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend(bbox_to_anchor=(-2.6, 0.5), handlelength= 1.5, fontsize=16)
# fig.add_legend_inside(handlelength= 1.5,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
