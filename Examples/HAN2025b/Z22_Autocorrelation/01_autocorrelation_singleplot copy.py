''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/02/05  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Q01_Plot.C00_cfg_for_cases import colors, linewidths

import numpy as np
from ZZZ_Result_Manager.A01_cases import cases, cases_f, cases_w, cases_select, case_labels
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from ZZZ_Result_Manager.A01_cases import cases_select
from G01_autocorrelation import AutoCorrelation as AC

quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,4), right_legend=True, hspace=0.5, wspace=0.5, panel_offset=(-0.2,1.1))
','
cases_select = cases_w
case_labels = ['Case 1L', 'Case 2L', 'Case 3L', 'Case 4L', 'Case 5L']

fig_id = 0
for case_id, case in enumerate(cases_select):
    ac = AC(case)
    ac.load()
    x = ac.r_xdir
    y = ac.autocorr_xdir[0]
    fig.plot(fig_id,x,y, color=colors[case_id], label= case_labels[case_id])
    x = ac.fitting_part[1]
    y = ac.fitting_part[0]
    fig.plot(fig_id,x,y, color=colors[case_id], linestyle = '-.')
fig_id = 1
for case_id, case in enumerate(cases_select):
    ac = AC(case)
    ac.load()
    x = ac.r_ydir
    y = ac.autocorr_ydir[1]
    fig.plot(fig_id,x,y, color=colors[case_id])
    x = ac.fitting_part[3]
    y = ac.fitting_part[2]
    fig.plot(fig_id,x,y, color=colors[case_id], linestyle = '-.')


fig.set_axis(0,xlim=(0,200),ylim=(0,1))
fig.set_axis(1,xlim=(0,200),ylim=(0,1))
fig.set_label(0,ylabel='$f_u$')
fig.set_label(0,xlabel=r'$r~\mathrm{(mm)}$')
fig.set_label(1,ylabel='$f_v$')
fig.set_label(1,xlabel=r'$r~\mathrm{(mm)}$')
for fig_id in range(2):
    fig.set_panel_label(fig_id)

fig.set_margins(right=0.93)
fig.legend(bbox_to_anchor=(0.8,0.5))
fig.save(getplotpath()+"/autocorrelation.png")
