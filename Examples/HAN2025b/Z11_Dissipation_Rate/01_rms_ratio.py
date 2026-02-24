''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/19  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Q01_Plot.C00_cfg_for_cases import case_titles, colors, linewidths, cases
import numpy as np
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DR
from Z01_Filtered_Velocity_Field.H01_gaussian_params import selected_k1L1, k1L1_label, gaussian_id, gaussian_bp_id, L11_cases, cases

quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,3), right_legend=True, wspace=0.8,panel_offset=(-0.2,1.1))
','

'0'
fig_id = 0
filter = 'gaussian_bp'
for case_id, case in enumerate(cases):
    x = []
    y = []
    for filter_id, filter_param in enumerate(gaussian_bp_id):
        x.append(selected_k1L1[filter_id])
        dr = DR(case, filter, filter_param)
        y.append(dr.result_json.get(0)['urms']/dr.result_json.get(0)['vrms'])
    fig.plot(fig_id,x,y, marker='+', ifmarker= True, label=case_titles[case_id], color=colors[case_id])        

'1'
fig_id = 1
filter = 'gaussian_bp'
for case_id, case in enumerate(cases):
    x = []
    y = []
    for filter_id, filter_param in enumerate(gaussian_bp_id):
        x.append(selected_k1L1[filter_id])
        dr = DR(case, filter, filter_param)
        y.append(dr.result_json.get(0)['dudx_rms']/dr.result_json.get(0)['dvdy_rms'])
    fig.plot(fig_id,x,y, marker='+', ifmarker= True, color=colors[case_id])    


fig.set_label(0,xlabel=r'$k_1L_{u_1}$')
fig.set_label(0,ylabel=r'$\widehat u_{1,\mathrm{rms}}/\widehat u_{2,\mathrm{rms}}$')
fig.set_label(1,xlabel=r'$k_1L_{u_1}$')
fig.set_label(1,ylabel=r'$\frac{\left( \partial \widehat u_1 / \partial x_1 \right){\mathrm{rms}}}{\left( \partial \widehat u_2 / \partial x_2 \right){\mathrm{rms}}}$')
fig.set_axis(0,xlim=(0,120),ylim=(0.9,1.3))
fig.set_axis(1,xlim=(0,120),ylim=(0.9,1.3))
for fig_id in range(2):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.85)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/rms_ratio.png")
