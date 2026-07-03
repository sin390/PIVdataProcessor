''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/19  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Q01_Plot.C00_cfg_for_cases import colors
import matplotlib.pyplot as plt
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.A01_cases import cases
from pivdataprocessor.A01_toolbox import nanmean_filter2d
import numpy as np
from Z02_Reynolds_Stress.G01_reynolds_stress import ReynoldsStress as RS

quickset()
plt.rcParams.update({
    "axes.grid": False
})
nrows = 2
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,12), 
                 wspace = 0.7, hspace = 0.5,right_legend=True)
','

filter_range = 8

x_0 = 0
y_0 = 0
x_1 = 20
y_1 = 15

fig_id = 0
# U-x
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    rs = RS(case)
    rs.load()
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = np.sqrt(rs.uu[left:right,i_y[0]])
    fig.plot(fig_id,x,y,color=colors[case_id])

    # fig.shade(fig_id,x,y,y_err,color=colors[case_id],label=case_labels[case_id],fill_alpha=0.5,center_lw=0.5)
    x = pBase.X[0][left:right,i_y[1]]
    y = np.sqrt(rs.uu[left:right,i_y[1]])
    fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')

fig_id = 1
# U-y
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    rs = RS(case)
    rs.load()

    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[1][i_x[0],bottom:up]
    y = np.sqrt(rs.uu[i_x[0],bottom:up])
    fig.plot(fig_id,x,y,color=colors[case_id])

    # fig.shade(fig_id,x,y,y_err,color=colors[case_id],label=case_labels[case_id],fill_alpha=0.5,center_lw=0.5)
    x = pBase.X[1][i_x[1],bottom:up]
    y = np.sqrt(rs.uu[i_x[1],bottom:up])
    fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')


fig_id = 2
# V-x
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    rs = RS(case)
    rs.load()
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = np.sqrt(rs.vv[left:right,i_y[0]])
    fig.plot(fig_id,x,y,color=colors[case_id])

    # fig.shade(fig_id,x,y,y_err,color=colors[case_id],label=case_labels[case_id],fill_alpha=0.5,center_lw=0.5)
    x = pBase.X[0][left:right,i_y[1]]
    y = np.sqrt(rs.vv[left:right,i_y[1]])
    fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')

fig_id = 3
# V-y
for case_id, case in enumerate(cases):
    pBase.load_case(case)
    rs = RS(case)
    rs.load()

    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    x = pBase.X[1][i_x[0],bottom:up]
    y = np.sqrt(rs.vv[i_x[0],bottom:up])
    fig.plot(fig_id,x,y,color=colors[case_id])

    # fig.shade(fig_id,x,y,y_err,color=colors[case_id],label=case_labels[case_id],fill_alpha=0.5,center_lw=0.5)
    x = pBase.X[1][i_x[1],bottom:up]
    y = np.sqrt(rs.vv[i_x[1],bottom:up])
    fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')



fig.set_label(0,ylabel=r'$u_{rms}$')
fig.set_label(2,ylabel=r'$v_{rms}$')
fig.set_label(2,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_label(3,xlabel=r'$y~\mathrm{(mm)}$')
fig.set_axis(0,xlim=(-40,40),ylim=(0,30),yticks=[0,20])
fig.set_axis(1,xlim=(-20,20),ylim=(0,30),yticks=[0,20])
fig.set_axis(2,xlim=(-40,40),ylim=(0,30),yticks=[0,20])
fig.set_axis(3,xlim=(-20,20),ylim=(0,30),yticks=[0,20])
for fig_id in range(4):
    fig.set_panel_label(fig_id)
fig.set_margins(left=0.15,right=1,bottom=0.2,top=0.95)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/02_dis_fluc_u_rms.png")
fig.show()