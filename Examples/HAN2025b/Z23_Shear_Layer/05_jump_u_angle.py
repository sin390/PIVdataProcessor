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
from ZZZ_Result_Manager.A01_cases import cases, cases_w, cases_select, degs, case_labels

quickset()
nrows = 2
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,8), right_legend=True, hspace=0.5, wspace=0.6,panel_offset=(-0.2,1.1))
','

filter = 'gaussian'
filter_params = 3

'0'
fig_id = 0
filter_params = 4
for case_id, case in enumerate(cases_select):
    sl = SL(case, filter, filter_params)
    sl.load_result(None)
    eps = sl.result_json.get(0)['eps']
    delta_s_in_mm = sl.result_json.get(0)['delta_s_in_mm']
    Lf = sl.result_json.get(0)['Lf_in_mm']
    nor_tmp = (eps*delta_s_in_mm/1000)**(1/3)
    x = []
    y = []
    for deg in degs:
        sl.load_result(deg)
        jump_u = sl.result_json.get(0)['jump_u']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(jump_u/nor_tmp)
    fig.plot(fig_id,x,y,label=case_labels[case_id], color=colors[case_id])

'1'
fig_id = 1
filter_params = 3
for case_id, case in enumerate(cases_select):
    sl = SL(case, filter, filter_params)
    sl.load_result(None)
    eps = sl.result_json.get(0)['eps']
    delta_s_in_mm = sl.result_json.get(0)['delta_s_in_mm']
    Lf = sl.result_json.get(0)['Lf_in_mm']
    nor_tmp = (eps*delta_s_in_mm/1000)**(1/3)
    x = []
    y = []
    for deg in degs:
        sl.load_result(deg)
        jump_u = sl.result_json.get(0)['jump_u']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(jump_u/nor_tmp)
    fig.plot(fig_id,x,y, color=colors[case_id])

'2'
fig_id = 2
filter_params = 2
for case_id, case in enumerate(cases_select):
    sl = SL(case, filter, filter_params)
    sl.load_result(None)
    eps = sl.result_json.get(0)['eps']
    delta_s_in_mm = sl.result_json.get(0)['delta_s_in_mm']
    Lf = sl.result_json.get(0)['Lf_in_mm']
    nor_tmp = (eps*delta_s_in_mm/1000)**(1/3)
    x = []
    y = []
    for deg in degs:
        sl.load_result(deg)
        jump_u = sl.result_json.get(0)['jump_u']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(jump_u/nor_tmp)
    fig.plot(fig_id,x,y, color=colors[case_id])

'3'
fig_id = 3
filter_params = 1
for case_id, case in enumerate(cases_select):
    sl = SL(case, filter, filter_params)
    sl.load_result(None)
    eps = sl.result_json.get(0)['eps']
    delta_s_in_mm = sl.result_json.get(0)['delta_s_in_mm']
    Lf = sl.result_json.get(0)['Lf_in_mm']
    nor_tmp = (eps*delta_s_in_mm/1000)**(1/3)
    x = []
    y = []
    for deg in degs:
        sl.load_result(deg)
        jump_u = sl.result_json.get(0)['jump_u']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(jump_u/nor_tmp)
    fig.plot(fig_id,x,y, color=colors[case_id])


fig.set_label(2,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(3,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(0,ylabel=r'$(u_{jump}|_\theta)/(\varepsilon \delta_s)^{1/3}$')
fig.set_label(2,ylabel=r'$(u_{jump}|_\theta)/(\varepsilon \delta_s)^{1/3}$')
fig.set_axis(0,xlim=(0,180),ylim=(1,3.2),xticks=[0,45,90,135,180])
fig.set_axis(1,xlim=(0,180),ylim=(1,3.2),xticks=[0,45,90,135,180])
fig.set_axis(2,xlim=(0,180),ylim=(1,3.2),xticks=[0,45,90,135,180])
fig.set_axis(3,xlim=(0,180),ylim=(1,3.2),xticks=[0,45,90,135,180])
for fig_id in range(4):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.8)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/jump_u_angle.png")
