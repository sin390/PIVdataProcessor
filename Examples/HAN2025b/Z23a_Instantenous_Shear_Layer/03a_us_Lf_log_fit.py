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

from ZZZ_Result_Manager.A01_cases import cases_select, cases_select_f,cases_select_w, coeffs_to_eta,cases_select_labels
from Z23a_Instantenous_Shear_Layer.G01_instantenous_shear_layer import ShearLayer as SL
from Z23a_Instantenous_Shear_Layer.T01_local_toolbox import power_law_fit
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/02_us_Lf_log"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.07),
    right_legend=False,     # reserve legend column
    left=0.1,
    right=0.98,
    bottom=0.32,
    top=0.88,
    dpi=600,
    wspace=0.3
)

fig_id = 0
for case_id, case in enumerate(cases_select):
    x=[]
    y=[]
    n = 1
    ds = DS(cases_select_f[case_id], 'gaussian',-1)
    eta = ds.result_json.get(0)['eta']*1000
    for coeff_id, coeff in enumerate(coeffs_to_eta):
        coeff_id += 1
        filter_params = coeff_id
        sl = SL(cases_select_w[case_id],'gaussian',coeff_id)
        sl.load_result(None)
        n_list = sl.result_json.get(1)['n_list']

        index = n_list.index(n)
        v_jump_array = sl.result_json.get(1)['v_jump_array'] 
 
        Lf = eta * coeff/1000
        y_tmp = v_jump_array[index]

        x.append(Lf/eta)
        y.append(y_tmp)

    fig.plot(fig_id,x,y,label=cases_select_labels[case_id], color=colors[case_id], marker='^',markersize = 5,ifmarker=True,xlog=True,ylog=True)
    _,_,y_fit = power_law_fit(x,y)
    fig.plot(fig_id,x,y_fit, color=colors[case_id], linestyle = '-.', markersize = 5,xlog=True,ylog=True)

fig_id = 1
for case_id, case in enumerate(cases_select):
    x=[]
    y=[]
    n = 5
    ds = DS(cases_select_f[case_id], 'gaussian',-1)
    eta = ds.result_json.get(0)['eta']*1000
    for coeff_id, coeff in enumerate(coeffs_to_eta):
        coeff_id += 1
        filter_params = coeff_id
        sl = SL(cases_select_w[case_id],'gaussian',coeff_id)
        sl.load_result(None)
        n_list = sl.result_json.get(1)['n_list']

        index = n_list.index(n)
        v_jump_array = sl.result_json.get(1)['v_jump_array'] 
 
        Lf = eta * coeff/1000
        y_tmp = v_jump_array[index]

        x.append(Lf/eta)
        y.append(y_tmp)

    fig.plot(fig_id,x,y, color=colors[case_id], marker='^',markersize = 5,ifmarker=True,xlog=True,ylog=True)
    _,_,y_fit = power_law_fit(x,y)
    fig.plot(fig_id,x,y_fit, color=colors[case_id], linestyle = '-.', markersize = 5,xlog=True,ylog=True)

fig_id = 2
for case_id, case in enumerate(cases_select):
    x=[]
    y=[]
    n = 9
    ds = DS(cases_select_f[case_id], 'gaussian',-1)
    eta = ds.result_json.get(0)['eta']*1000
    for coeff_id, coeff in enumerate(coeffs_to_eta):
        coeff_id += 1
        filter_params = coeff_id
        sl = SL(cases_select_w[case_id],'gaussian',coeff_id)
        sl.load_result(None)
        n_list = sl.result_json.get(1)['n_list']

        index = n_list.index(n)
        v_jump_array = sl.result_json.get(1)['v_jump_array'] 
 
        Lf = eta * coeff/1000
        y_tmp = v_jump_array[index]

        x.append(Lf/eta)
        y.append(y_tmp)

    fig.plot(fig_id,x,y, color=colors[case_id], marker='^',markersize = 5,ifmarker=True,xlog=True,ylog=True)
    _,_,y_fit = power_law_fit(x,y)
    fig.plot(fig_id,x,y_fit, color=colors[case_id], linestyle = '-.', markersize = 5,xlog=True,ylog=True)
    
text = [f'$n=1$','$n=5$','$n=9$']
for i in range(3):
    fig.set_panel_label(i,text[i])

# fig.set_axis(0,xlim=(100,1300))
# fig.set_axis(1,xlim=(100,1300))
# fig.set_axis(2,xlim=(100,1300))
# fig.set_axis(1,xlim=(10,40),ylim=(0,3))

fig.set_label(0,xlabel=r'$L_f/\eta$')
fig.set_label(1,xlabel=r'$L_f/\eta$')
fig.set_label(2,xlabel=r'$L_f/\eta$')
fig.set_label(0,ylabel=r'$\left\langle {u_S}^n\right\rangle~\mathrm{(m/s)}$',labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.legend(bbox_to_anchor=(-2.2, 0.5), handlelength= 1.5, fontsize=16)
fig.add_legend_bottom_rowmajor_manual(x=0.46,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
