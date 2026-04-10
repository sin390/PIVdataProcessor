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

import ZZZ_Result_Manager.A01_cases as A01
from Z11_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from Z23a_Instantenous_Shear_Layer.T01_local_toolbox import power_law_fit
from Z23a_Instantenous_Shear_Layer.G01_instantenous_shear_layer import ShearLayer as SL

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
for case_id, case in enumerate(A01.cases):
    rm = RM(A01.cases[case_id])
    eta = rm.result_table.get(1)['eta']
    Lfs_in_mm = rm.result_table.get(2)['Lfs']
    n_s = []
    p_s = []
    for n in [i for i in range(1,10)]:
        x = []
        y = []
        for filter_id, filter_param in enumerate(A01.gaussian_id):
            sl = SL(A01.cases[case_id],'gaussian',filter_param)
            sl.load_result(None)
            n_list = sl.result_json.get(1)['n_list']
            index = n_list.index(n)
            v_jump_array = sl.result_json.get(1)['v_jump_array'] 
    
            Lf = Lfs_in_mm[filter_id]/1000
            y_tmp = v_jump_array[index]
            # y_tmp /= (v_jump_array[0]**n_list[n-1])

            x.append(Lf/eta)
            y.append(y_tmp)
            p,_,y_fit = power_law_fit(x,y)

        n_s.append(n)
        p_s.append(p)
    fig.plot(fig_id,n_s,p_s,label=A01.case_labels[case_id], color=colors[case_id], marker='^',markersize = 5,ifmarker=True)

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