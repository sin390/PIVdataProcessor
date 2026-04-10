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
rm = RM(case)
Lfs = rm.result_table.get(2)['Lfs']
plotted_filter_param = [2,3,4,5,6,7,8]
filter = 'gaussian'

fig_id = 0
filter = 'gaussian'
filter_id = 5
for case_id, case in enumerate(A01.cases):
    ac = AC(case, filter, filter_id)
    ac.load()
    Lf = Lfs[filter_id]
    x = ac.r_xdir/Lf
    y = ac.autocorr_xdir[0]
    fig.plot(fig_id,x,y, label=A01.case_labels[case_id],color=colors[case_id])

fig_id = 1
filter = 'gaussian'
filter_id = 5
for case_id, case in enumerate(A01.cases):
    ac = AC(case, filter, filter_id)
    ac.load()
    Lf = Lfs[filter_id]
    x = ac.r_xdir/Lf
    y = ac.autocorr_xdir[1]
    fig.plot(fig_id,x,y,color=colors[case_id])

for i in range(2):
    fig.set_panel_label(i)

fig.set_axis(0,xlim = (0,4),ylim=(0,1.2))
fig.set_axis(1,xlim = (0,4),ylim=(0,1.2))
# fig.set_label(0,xlabel=r'$x~\mathrm{(mm)}$')
# fig.set_label(0,ylabel=r'$\widetilde{I}_\mathrm{S}~\mathrm{(s^{-1})}$',labelpad=12)
# fig.set_label(1,xlabel=r'$x~\mathrm{(mm)}$')
# fig.set_label(1,ylabel=r'$\widetilde{I}_\mathrm{R}~\mathrm{(s^{-1})}$',labelpad=12)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend(bbox_to_anchor=(-2.6, 0.5), handlelength= 1.5, fontsize=16)
# fig.add_legend_inside(handlelength= 1.5,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
