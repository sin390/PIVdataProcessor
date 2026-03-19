''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/03/16  =
=========================
'''

import numpy as np
import matplotlib.pyplot as plt
from Q01_Plot.L01_piv_plot import PlotFigure 
from Q01_Plot.C00_cfg_for_cases import colors, linewidths
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath

import ZZZ_Result_Manager.A01_cases as A01
from Z13_Reynolds_Stress.G01_reynolds_stress import ReynoldsStress as RS
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/10_dis_urms_vrms"
quickset()

p = 60

fig = PlotFigure(
    nrows=1,
    ncols=2,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.06),
    right_legend=True,     # reserve legend column
    left=0.1,
    right=1,
    bottom=0.18,
    top=0.85,
    wspace=0.6,
    dpi=600
)

for case_id, case in enumerate(A01.cases_select):
    rs = RS(A01.cases_select_w[case_id])
    rs.load()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]

    urms = np.sqrt(rs.uu)
    vrms = np.sqrt(rs.vv)

    fig_id = 0
    x = pBase.X[1, central_x, bottom:up]/p
    y = urms[central_x, bottom:up]
    fig.plot(fig_id,x,y, color=colors[case_id], label= A01.cases_select_labels[case_id])

    fig_id = 1
    x = pBase.X[1, central_x, bottom:up]/p
    y = vrms[central_x, bottom:up]
    fig.plot(fig_id,x,y, color=colors[case_id])


for i in range(2):
    fig.set_panel_label(i)

fig.set_axis(0,xlim=(-0.6,0.6),ylim=(0, 1.2),xticks=[-0.5,0,0.5], yticks=[0,0.5,1.0])
fig.set_axis(1,xlim=(-0.6,0.6),ylim=(0, 1.2),xticks=[-0.5,0,0.5], yticks=[0,0.5,1.0])
fig.legend(bbox_to_anchor=(-2.4, 0.5), handlelength= 1.5)
fig.set_label(0,ylabel=r'$u_{\mathrm{rms}}~\mathrm{(m/s)}$',labelpad=15)
fig.set_label(0,xlabel=r'$y/p$')
fig.set_label(1,ylabel=r'$v_{\mathrm{rms}}~\mathrm{(m/s)}$',labelpad=15)
fig.set_label(1,xlabel=r'$y/p$')
fig.save(result_fig + figformat)
