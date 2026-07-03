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
from Q01_Plot.C00_cfg_for_cases import colors, linewidths, markers, linestyles, markersizes
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath

import ZZZ_Result_Manager.A01_cases as A01
from Z04_Velocity_Gradient.G01_dissipation_rate import DissipationRate as DR
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

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

cases_sub1 = [case + '_even' for case in A01.cases]
cases_sub2 = [case + '_odd' for case in A01.cases]

fig_id = 0
filter = 'gaussian'
for case_id, case in enumerate(A01.cases[:-1]):
    rm = RM(case) 
    eta = rm.result_table.get(1)['eta']
    viscosity = rm.result_table.get(1)['kinetic_viscosity']
    eps = rm.result_table.get(1)['dissipationRate']
    velocity_eta = (viscosity*eps)**(0.25)
    x=[]
    y=[]

    yerr = []
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        x.append(A01.Lf_coeff[filter_id])
        dr = DR(case, filter, filter_param)
        y.append(dr.result_json.get(0)['urms']/dr.result_json.get(0)['vrms'])

        dr = DR(cases_sub1[case_id], filter, filter_param)
        value_sub1 = dr.result_json.get(0)['urms']/dr.result_json.get(0)['vrms']
        dr = DR(cases_sub2[case_id], filter, filter_param)
        value_sub2 = dr.result_json.get(0)['urms']/dr.result_json.get(0)['vrms']
        yerr.append(np.abs(value_sub1-value_sub2)/2)
        
    fig.plot(fig_id,x,y,marker=markers[case_id],label=A01.case_labels[case_id],markersize = markersizes[case_id],ifmarker=True, color=colors[case_id],
             yerr=yerr,capsize=5,capthick=0.5, markerfacecolor='none')


fig.set_axis(0,xlim=(0,0.4),ylim=(0,2.5))
fig.set_label(0,xlabel=r'$L_F/L_{u}$')
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
