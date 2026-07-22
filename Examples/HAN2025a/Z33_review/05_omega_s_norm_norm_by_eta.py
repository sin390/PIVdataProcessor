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
from Q01_Plot.C00_cfg_for_cases import colors, linewidths, linestyles
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath

import ZZZ_Result_Manager.A01_cases as A01
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

linestyles = [
    '-',
    (4, (19, 3)),                  # 长破线，24
    (1.5, (14, 3, 2, 3)),            # 一点划线，24
    (1, (11, 3, 2, 3, 2, 3)),       
    '-',
    (4, (19, 3)),                  # 长破线，24
    (1.5, (14, 3, 2, 3)),           # 一点划线，24
    (1, (11, 3, 2, 3, 2, 3)),  
]


figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/05_omega_s_norm"
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

external_files = [
    './Z33_review/external_data/Case_FanW_All100_60.0.txt',
    # './Z33_review/external_data/all100_70.txt',
    # './Z33_review/external_data/all100_80.txt'
]
external_labels = [r'$L_F=60\eta$',r'$L_F=70\eta$',r'$L_F=80\eta$']
external_markers = ['D','^','s','p']
external_marker_size = [3,5,4,5]

plotted_filter_param = [1,2,3,4,5,6,7]

fig_id = 0
filter = 'gaussian'
case_id = 0
print(A01.cases_appendix[case_id])
for curve_id, filter_param in enumerate(plotted_filter_param):
    filter_id = filter_param-1
    sl = SL(A01.cases_appendix[case_id], filter, filter_param)
    sl.load_result()
    Lf = sl.result_json.get(0)['Lf_in_mm']
    eta = sl.result_json.get(0)['eta']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]   
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    fig.plot(fig_id,x,y,label=rf'$L_{{F}} = {Lf/1000/eta:.0f}\eta$', linestyle = linestyles[curve_id], color=colors[curve_id])

pinths = [1,3,4]
for file_id, file in enumerate(external_files):
    print(file)
    data = np.loadtxt(file, skiprows=1, delimiter=',')
    x,y = data.T
    fig.plot(fig_id,x[::pinths[file_id]],y[::pinths[file_id]], ifmarker=True, marker = external_markers[file_id],markersize = external_marker_size[file_id], 
             linestyle = 'None', color=colors[-1])

fig.set_axis(0,xlim=(-3,3),ylim=(-0.3,1.1))
fig.set_label(0,xlabel=r'$\zeta_{2}/L_{F}$')
# fig.set_label(2,xlabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
fig.set_label(0,labelpad=15, ylabel=r'$\overline{\widetilde{\omega}_S}/ (\overline{\widetilde{\omega}_S})_0$')
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
# fig.add_legend_bottom_rowmajor_manual(x=0.46,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
fig.legend(bbox_to_anchor=(-2, 0.5),handlelength=2.2)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
