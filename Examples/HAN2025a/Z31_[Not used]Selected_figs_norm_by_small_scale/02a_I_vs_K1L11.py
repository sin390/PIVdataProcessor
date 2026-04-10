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
from Z11_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD1
from Z11_Triple_Decomposition.G02_triple_decomposition_order_3 import TripleDecomposition as TD3
from Z11_Triple_Decomposition.G03_triple_decomposition_order_5 import TripleDecomposition as TD5
from Z11_Triple_Decomposition.G04_triple_decomposition_order_7 import TripleDecomposition as TD7
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/02a_I_vs_K1L11"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=2,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.06),
    right_legend=True,     # reserve legend column
    left=0.12,
    right=0.98,
    bottom=0.22,
    top=0.85,
    wspace=0.8,
    dpi=600
)

fig_id = 0
for case_id, case in enumerate(A01.cases):
    rm = RM(case) 
    eta = rm.result_table.get(1)['eta']
    viscosity = rm.result_table.get(1)['kinetic_viscosity']
    eps = rm.result_table.get(1)['dissipationRate']
    tau = (eta**2/eps)**(1/3)
    Lfs = rm.result_table.get(2)['Lfs']
    x=[]
    y=[]
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        td = TD1(case,'gaussian',filter_param)
        td.load_avg()
        Lf = Lfs[filter_id]/1000
        avg = td.result_json.get(0)['avg_intensity_SH']
        x.append(Lf/eta)
        y.append(avg*(Lf)*(Lf/eta)**(-1/3))

    fig.plot(fig_id,x,y,label=A01.case_labels[case_id],marker='^',markersize = 5,ifmarker=True, color=colors[case_id],xlog=True,ylog=True)

fig_id = 1
for case_id, case in enumerate(A01.cases):
    rm = RM(case) 
    eta = rm.result_table.get(1)['eta']
    viscosity = rm.result_table.get(1)['kinetic_viscosity']
    eps = rm.result_table.get(1)['dissipationRate']
    tau = (eta**2/eps)**(1/3)
    Lfs = rm.result_table.get(2)['Lfs']
    x=[]
    y=[]
    for filter_id, filter_param in enumerate(A01.gaussian_id):
        td = TD1(case,'gaussian',filter_param)
        td.load_avg()
        Lf = Lfs[filter_id]/1000
        avg = td.result_json.get(0)['avg_intensity_RR']
        x.append(Lf/eta)
        y.append(avg*(Lf)*(Lf/eta)**(-1/3))
    fig.plot(fig_id,x,y,marker='^',markersize = 5,ifmarker=True, color=colors[case_id],xlog=True,ylog=True)



for i in range(2):
    fig.set_panel_label(i)

fig.set_axis(0,xlog=True,ylog=True,ylim=(5e-1,2e1),xlim=(90,2e3))
# fig.set_axis(1,xlog=True,ylog=True,ylim=(5e-1,2e1),xlim=(90,2e3))
fig.set_axis(1,xlog=True,ylog=True,ylim=(5e-2,2e0),xlim=(90,2e3))
fig.set_label(0,xlabel=r'$L_f/\eta$')
fig.set_label(1,xlabel=r'$L_f/\eta$')
# fig.set_label(2,xlabel=r'$L_f/\eta$')
fig.set_label(0,ylabel=r'$(\widetilde{I}_\mathrm{S}L_f)_\mathrm{avg} (L_f/\eta)^{-1/3}$',labelpad= 15)
fig.set_label(1,ylabel=r'$(\widetilde{I}_\mathrm{R}L_f)_\mathrm{avg}(L_f/\eta)^{-1/3}$',labelpad= 15)
# fig.set_label(2,ylabel=r'$\widetilde{I}_\mathrm{R,avg} L_f(L_f/\eta)^{1/3}$',labelpad= 15)
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend(bbox_to_anchor=(-2.6, 0.5), handlelength= 1.5, fontsize=16)
# fig.add_legend_inside(handlelength= 1.5,fontsize=16)
# fig.add_legend_bottom_rowmajor_manual(x=0.46,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
