''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/19  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Q01_Plot.C00_cfg_for_cases import case_titles, colors, linewidths
import matplotlib.pyplot as plt
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.A01_cases import cases, cases_w, cases_f
from pivdataprocessor.A01_toolbox import nanmean_filter2d
import numpy as np


case_labels = ['Case 1L', 'Case 2L', 'Case 3L', 'Case 4L', 'Case 5L']
case_f_labels = ['Case 1S', 'Case 2S', 'Case 3S', 'Case 4S', 'Case 5S']
quickset()
plt.rcParams.update({
    "axes.grid": False
})
nrows = 2
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,7), 
                 wspace = 0.5, hspace = 0.5,right_legend=True, panel_offset=(-0.2,1.1))
','

filter_range = 8

p = 60
x_0 = 0
y_0 = 0
x_1 = 30
y_1 = 15

fig_id = 0
# U-x
cases = cases_w
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = pBase.avg_U[0][left:right,i_y[0]]
    fig.plot(fig_id,x,y,color=colors[case_id],label=case_labels[case_id])
cases = cases_f
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = pBase.avg_U[0][left:right,i_y[0]]
    fig.plot(fig_id,x,y,color=colors[case_id],linestyle = '-.',label=case_f_labels[case_id])

fig_id = 1
# U-y
cases = cases_w
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[1][i_x[0],bottom:up]
    y = pBase.avg_U[0][i_x[0],bottom:up]
    fig.plot(fig_id,x,y,color=colors[case_id])
cases = cases_f
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[1][i_x[0],bottom:up]
    y = pBase.avg_U[0][i_x[0],bottom:up]
    fig.plot(fig_id,x,y,color=colors[case_id],linestyle = '-.',)

fig_id = 2
# V-x
cases = cases_w
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = pBase.avg_U[1][left:right,i_y[0]]
    fig.plot(fig_id,x,y,color=colors[case_id])

cases = cases_f
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = pBase.avg_U[1][left:right,i_y[0]]
    fig.plot(fig_id,x,y,color=colors[case_id],linestyle = '-.')

fig_id = 3
# V-y
cases = cases_w
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[1][i_x[0],bottom:up]
    y = pBase.avg_U[1][i_x[0],bottom:up]
    fig.plot(fig_id,x,y,color=colors[case_id])
cases = cases_f
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[1][i_x[0],bottom:up]
    y = pBase.avg_U[1][i_x[0],bottom:up]
    fig.plot(fig_id,x,y,color=colors[case_id],linestyle = '-.')


fig.set_label(0,ylabel=r'$<U>~\mathrm{(m/s)}$')
fig.set_label(2,ylabel=r'$<V>~\mathrm{(m/s)}$')
fig.set_label(2,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_label(3,xlabel=r'$y~\mathrm{(mm)}$')
fig.set_axis(0,xlim=(-60,60),ylim=(-6,2))
fig.set_axis(1,xlim=(-40,40),ylim=(-6,2))
fig.set_axis(2,xlim=(-60,60),ylim=(-3,1))
fig.set_axis(3,xlim=(-40,40),ylim=(-3,1))
for fig_id in range(4):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.8)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/dis_avg_velocity.png")
