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
from ZZZ_Result_Manager.A01_cases import cases, cases_w
from pivdataprocessor.A01_toolbox import nanmean_filter2d
import numpy as np

cases = cases_w
case_labels = ['Case 1L', 'Case 2L', 'Case 3L', 'Case 4L', 'Case 5L']
quickset()
plt.rcParams.update({
    "axes.grid": False
})
nrows = 2
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(5,5), 
                 wspace = 1, hspace = 1,right_legend=True)
','

filter_range = 8

p = 60
x_0 = 0
y_0 = 0
x_1 = 30
y_1 = 15

fig_id = 0
# U-x
for case_id, case in enumerate(cases):
    pBase.load_case(case+'_sub1')
    avg_U_sub1 = pBase.avg_U.copy()
    pBase.load_case(case+'_sub2')
    avg_U_sub2 = pBase.avg_U.copy()
    for_uncertainty = (avg_U_sub1 - avg_U_sub2)**2
    U_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[0], filter_range))
    V_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[1], filter_range)) 

    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = pBase.avg_U[0][left:right,i_y[0]]
    # fig.plot(fig_id,x,y,color=colors[case_id],label=case_labels[case_id])

    y_err = U_uncertainty[left:right,i_y[0]]/2
    fig.errorbar(fig_id,x,y,y_err,color=colors[case_id],label=case_labels[case_id],capsize=1,capthick=0.5,every=10)
    # fig.shade(fig_id,x,y,y_err,color=colors[case_id],label=case_labels[case_id],fill_alpha=0.5,center_lw=0.5)
    # x = pBase.X[0][left:right,i_y[1]]
    # y = pBase.avg_U[0][left:right,i_y[1]]
    # fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')

fig_id = 1
# U-y
for case_id, case in enumerate(cases):
    pBase.load_case(case+'_sub1')
    avg_U_sub1 = pBase.avg_U.copy()
    pBase.load_case(case+'_sub2')
    avg_U_sub2 = pBase.avg_U.copy()
    for_uncertainty = (avg_U_sub1 - avg_U_sub2)**2
    U_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[0], filter_range))
    V_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[1], filter_range)) 
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[1][i_x[0],bottom:up]
    y = pBase.avg_U[0][i_x[0],bottom:up]
    y_err = U_uncertainty[i_x[0],bottom:up]/2
    # fig.plot(fig_id,x,y,color=colors[case_id])
    fig.errorbar(fig_id,x,y,y_err,color=colors[case_id],capsize=1,capthick=0.5,every=10)
    # fig.shade(fig_id,x,y,y_err,color=colors[case_id],fill_alpha=0.5,center_lw=0.5)
    # x = pBase.X[1][i_x[1],bottom:up]
    # y = pBase.avg_U[0][i_x[1],bottom:up]
    # fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')    

fig_id = 2
# V-x
for case_id, case in enumerate(cases):
    pBase.load_case(case+'_sub1')
    avg_U_sub1 = pBase.avg_U.copy()
    pBase.load_case(case+'_sub2')
    avg_U_sub2 = pBase.avg_U.copy()
    for_uncertainty = (avg_U_sub1 - avg_U_sub2)**2
    U_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[0], filter_range))
    V_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[1], filter_range)) 
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = pBase.avg_U[1][left:right,i_y[0]]
    y_err = V_uncertainty[left:right,i_y[0]]/2
    # fig.plot(fig_id,x,y,color=colors[case_id])
    fig.errorbar(fig_id,x,y,y_err,color=colors[case_id],capsize=1,capthick=0.5,every=10)
    # fig.shade(fig_id,x,y,y_err,color=colors[case_id],fill_alpha=0.5,center_lw=0.5)

    # x = pBase.X[0][left:right,i_y[1]]
    # y = pBase.avg_U[1][left:right,i_y[1]]
    # fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')   

fig_id = 3
# V-y
for case_id, case in enumerate(cases):
    pBase.load_case(case+'_sub1')
    avg_U_sub1 = pBase.avg_U.copy()
    pBase.load_case(case+'_sub2')
    avg_U_sub2 = pBase.avg_U.copy()
    for_uncertainty = (avg_U_sub1 - avg_U_sub2)**2
    U_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[0], filter_range))
    V_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[1], filter_range)) 
    pBase.load_case(case)
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[1][i_x[0],bottom:up]
    y = pBase.avg_U[1][i_x[0],bottom:up]
    y_err = V_uncertainty[i_x[0],bottom:up]/2
    # fig.plot(fig_id,x,y,color=colors[case_id])
    fig.errorbar(fig_id,x,y,y_err,color=colors[case_id],capsize=1,capthick=0.5,every=10)
    # fig.shade(fig_id,x,y,y_err,color=colors[case_id],label=case_labels[case_id],fill_alpha=0.5,center_lw=0.5)
    # x = pBase.X[1][i_x[1],bottom:up]
    # y = pBase.avg_U[1][i_x[1],bottom:up]
    # fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')   


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
fig.set_margins(left=0,right=1,bottom=0,top=1)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/dis_avg_velocity.jpg")
fig.show()