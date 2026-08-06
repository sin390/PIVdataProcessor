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

import ZZZ_Result_Manager.A01_cases as A01
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from Z13a_Lowpass_Reynolds_stress.G01_reynolds_stress import ReynoldsStress as RS
from ZZZ_Result_Manager.A01_cases import cases_select, cases_select_f, cases_select_w, coeffs_to_eta


figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/03_ratio_urms_Lf"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=1,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.16,1.06),
    right_legend=True,     # reserve legend column
    left=0.33,
    right=0.73,
    bottom=0.18,
    top=0.85,
    wspace=0.6,
    dpi=600
)

# cases_sub1 = [case + '_even' for case in A01.cases]
# cases_sub2 = [case + '_odd' for case in A01.cases]

fig_id = 0
filter = 'gaussian'
for case_id, case in enumerate(cases_select):
    x=[]
    y=[]

    yerr = []
    for coeff_id, coeff in enumerate(coeffs_to_eta):
        x.append(A01.coeffs_to_eta[coeff_id])
        coeff_id += 1
        rs = RS(cases_select_w[case_id], filter, coeff_id)
        y.append(rs.result_json.get(0)['avg_urms']/rs.result_json.get(0)['avg_vrms'])

        # dr = DR(cases_sub1[case_id], filter, filter_param)
        # value_sub1 = dr.result_json.get(0)['urms']/dr.result_json.get(0)['vrms']
        # dr = DR(cases_sub2[case_id], filter, filter_param)
        # value_sub2 = dr.result_json.get(0)['urms']/dr.result_json.get(0)['vrms']
        # yerr.append(np.abs(value_sub1-value_sub2)/2)
        
    fig.plot(fig_id,x,y,label=A01.cases_select_labels[case_id], color=colors[case_id],
             marker='^',markersize = 5,ifmarker=True,)
    # fig.plot(fig_id,x,y,marker=markers[case_id],label=A01.case_labels[case_id],markersize = markersizes[case_id],ifmarker=True, color=colors[case_id],
    #          yerr=yerr,capsize=5,capthick=0.5, markerfacecolor='none')


fig.set_axis(0,xlim=(0,100),ylim=(0,2))
fig.set_label(0,xlabel=r'$L_F/\eta$')
fig.set_label(0,
              ylabel=r'$\tilde u_{\mathrm{rms}}/ \tilde v_{\mathrm{rms}}$',
              labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend(bbox_to_anchor=(-2.2, 0.5), handlelength= 1.5, fontsize=16)
# fig.add_legend_bottom_rowmajor_manual(x=0.46,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# fig.add_legend_inside(handlelength= 1.5,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
