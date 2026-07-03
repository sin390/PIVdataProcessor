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
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL

linestyles = [
    '-',
    (6, (19, 3)),                  # 长破线，24
    (3.5, (14, 3, 2, 3)),            # 一点划线，24
    (3, (11, 3, 2, 3, 2, 3)),       
    '-',
    (6, (19, 3)),                  # 长破线，24
    (3.5, (14, 3, 2, 3)),           # 一点划线，24
    (3, (11, 3, 2, 3, 2, 3)),  
]

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/10_Ar_angle"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.08),
    right_legend=False,     # reserve legend column
    left=0.07,
    right=0.98,
    bottom=0.3,
    top=0.85,
    dpi=600,
    wspace=0.3
)

cases_sub1 = [case + '_even' for case in A01.cases]
cases_sub2 = [case + '_odd' for case in A01.cases]

fig_id = 0
filter = 'gaussian'
filter_id = 1
for case_id, case in enumerate(A01.cases[:-1]):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    x = []
    y = []
    yerr = []
    for deg in A01.degs:
        sl = SL(case, filter, filter_id)
        sl.load_result(deg)
        AR = sl.result_json.get(0)['AR']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(AR)

        sl = SL(cases_sub1[case_id], filter, filter_id)
        sl.load_result(deg)        
        value_sub1 = sl.result_json.get(0)['AR']
        sl = SL(cases_sub2[case_id], filter, filter_id)
        sl.load_result(deg)        
        value_sub2 = sl.result_json.get(0)['AR']
        yerr.append(np.abs(value_sub1-value_sub2)/2)
    fig.plot(fig_id,x,y,label=A01.case_labels[case_id], color=colors[case_id],linestyle = linestyles[case_id],
            yerr=yerr,elinewidth=0.5)
print(A01.Lf_label[filter_id-1])

fig_id = 1
filter = 'gaussian'
filter_id = 5
for case_id, case in enumerate(A01.cases[:-1]):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    x = []
    y = []
    yerr = []
    for deg in A01.degs:
        sl.load_result(deg)
        AR = sl.result_json.get(0)['AR']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(AR)

        sl = SL(cases_sub1[case_id], filter, filter_id)
        sl.load_result(deg)        
        value_sub1 = sl.result_json.get(0)['AR']
        sl = SL(cases_sub2[case_id], filter, filter_id)
        sl.load_result(deg)        
        value_sub2 = sl.result_json.get(0)['AR']
        yerr.append(np.abs(value_sub1-value_sub2)/2)
    fig.plot(fig_id,x,y,color=colors[case_id], yerr=yerr, elinewidth=0.5,linestyle = linestyles[case_id])
print(A01.Lf_label[filter_id-1])

fig_id = 2
filter = 'gaussian'
filter_id = 9
for case_id, case in enumerate(A01.cases[:-1]):
    sl = SL(case, filter, filter_id)
    sl.load_result()
    x = []
    y = []
    yerr = []
    for deg in A01.degs:
        sl.load_result(deg)
        AR = sl.result_json.get(0)['AR']
        x.append((deg[0][0]+deg[0][1])/2)
        y.append(AR)
 
        sl = SL(cases_sub1[case_id], filter, filter_id)
        sl.load_result(deg)        
        value_sub1 = sl.result_json.get(0)['AR']
        sl = SL(cases_sub2[case_id], filter, filter_id)
        sl.load_result(deg)        
        value_sub2 = sl.result_json.get(0)['AR']
        yerr.append(np.abs(value_sub1-value_sub2)/2) 
    fig.plot(fig_id,x,y,color=colors[case_id], yerr=yerr, elinewidth=0.5,linestyle = linestyles[case_id])
print(A01.Lf_label[filter_id-1])


for i in range(3):
    fig.set_panel_label(i)
    fig.set_axis(i,ylim=(3,8))
    fig.set_axis(i,xlim=(0,180),xticks=[0,45,90,135,180],minor_xticks=None)
fig.set_label(0,xlabel=r'$\theta~\mathrm{(deg.)}$')
fig.set_label(1,xlabel=r'$\theta~\mathrm{(deg.)}$')
fig.set_label(2,xlabel=r'$\theta~\mathrm{(deg.)}$')
fig.set_label(0,labelpad=15, ylabel=r'$A_R$')
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.legend(bbox_to_anchor=(-1.8, 0.5), handlelength= 1.5)
fig.legend_bottom(
    ncol=7,
    y=0.05,
    fontsize=16,
    columnspacing=1.4,
    handlelength=2.2,
)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
