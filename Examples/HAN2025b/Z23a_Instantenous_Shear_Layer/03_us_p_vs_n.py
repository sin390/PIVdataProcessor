''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/03/20  =
=========================
'''

import numpy as np
import matplotlib.pyplot as plt
from Q01_Plot.L01_piv_plot import PlotFigure 
from Q01_Plot.C00_cfg_for_cases import colors, linewidths
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath

from ZZZ_Result_Manager.A01_cases import cases_select, cases_select_f,cases_select_w, coeffs_to_eta,cases_select_labels
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from Z23a_Instantenous_Shear_Layer.T01_local_toolbox import power_law_fit
from Z23a_Instantenous_Shear_Layer.G01_instantenous_shear_layer import ShearLayer as SL
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/03_us_p_vs_n"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=1,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.16,1.06),
    right_legend=True,     # reserve legend column
    left=0.3,
    right=0.7,
    bottom=0.18,
    top=0.85,
    wspace=0.6,
    dpi=600
)

fig_id = 0
for case_id, case in enumerate(cases_select):
    ds = DS(cases_select_f[case_id], 'gaussian',-1)
    eta = ds.result_json.get(0)['eta']*1000
    
    n_s = []
    p_s = []
    for n in [i for i in range(1,10)]:
        x = []
        y = []
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
            # y_tmp /= (v_jump_array[0]**n_list[n-1])

            x.append(Lf/eta)
            y.append(y_tmp)
            p,_,y_fit = power_law_fit(x,y)

        n_s.append(n)
        p_s.append(p)
    fig.plot(fig_id,n_s,p_s,label=cases_select_labels[case_id], color=colors[case_id], marker='^',markersize = 5,ifmarker=True)

fig.set_axis(0,xlim=(0,10),ylim=(-3,2),xticks=[0,2,4,6,8,10],minor_xticks=1)
fig.set_label(0,xlabel=r'$n$')
fig.set_label(0,ylabel=r'$p$',labelpad=12)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend(bbox_to_anchor=(-2.2, 0.5), handlelength= 1.5, fontsize=16)
# fig.add_legend_inside(handlelength= 1.5,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)