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
import numpy as np
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL
from ZZZ_Result_Manager.A01_cases import cases, cases_f, cases_select, case_labels
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM


quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,3), right_legend=True, wspace=0.6,panel_offset=(-0.2,1.1))
','

'0'
fig_id = 0
filter = 'gaussian'
filter_param = 1
for case_id, case in enumerate(cases_select):
    sl = SL(case, filter, filter_param)
    sl.load_result()
    rm = RM(cases[case_id])
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = (sl.avg_Is_BRF-I_s_avg)/(sl.avg_Is_BRF[ic,jc]-I_s_avg)

    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y,label=case_labels[case_id], color=colors[case_id])



'1'
fig_id = 1
filter = 'gaussian'
filter_param = 1
for case_id, case in enumerate(cases_select):
    sl = SL(case, filter, filter_param)
    sl.load_result()
    rm = RM(cases[case_id])
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = (sl.avg_Is_BRF-I_s_avg)/(sl.avg_Is_BRF[ic,jc]-I_s_avg)

    x = sl.X_BRF[0,:,jc]/Lf
    y = mag[:,jc]
    fig.plot(fig_id,x,y, color=colors[case_id])

fig.set_label(0,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(0,ylabel=r'$<\widetilde{I_S}>_\mathrm{norm}$')
fig.set_label(1,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(1,ylabel=r'$<\widetilde{I_S}>_\mathrm{norm}$')
fig.set_axis(0,xlim=(-5,5),ylim=(-0.3,1.1))
fig.set_axis(1,xlim=(-5,5),ylim=(-0.3,1.1))
for fig_id in range(2):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.8)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/dis_norm_I_s.png")
