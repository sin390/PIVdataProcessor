''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/16  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Q01_Plot.C00_cfg_for_cases import case_titles, colors, linewidths
from pivdataprocessor.A01_toolbox import ProbabilityDensity as PD
import numpy as np
from Z22_Probability_Distribution.G03_PDF_TDM_relative_intensity import PDF_TDM_relative_intensity as PDF
from Z01_Filtered_Velocity_Field.H01_gaussian_params import selected_k1L1, k1L1_label, gaussian_id, gaussian_bp_id, L11_cases, cases
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,3), right_legend=True, wspace=0.3, panel_offset=(-0.2,1.1))
','

filter = 'gaussian_bp'
filter_param = gaussian_bp_id[2]

fig_id = 0
for case_id, case in enumerate(cases):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_S_omega_x
    y = pdf.PDF_S_omega_y
    fig.plot(fig_id,x,y, color=colors[case_id], label= case_titles[case_id], linewidth = linewidths[case_id])

fig_id = 1
filter = 'gaussian_bp'
for case_id, case in enumerate(cases):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_R_omega_x
    y = pdf.PDF_R_omega_y
    fig.plot(fig_id,x,y, color=colors[case_id], linewidth = linewidths[case_id])

ax = fig.ax_target(fig_id)
axins = inset_axes(
    ax,
    width="60%",      # inset 宽度（相对父轴）
    height="60%",     # inset 高度
    loc="upper right" # 位置
)
for case_id, case in enumerate(cases):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_R_omega_x
    y = pdf.PDF_R_omega_y
    axins.plot(x,y, color=colors[case_id], linewidth = linewidths[case_id])
axins.set_xlim(-0.1, 1)
axins.set_ylim(0, 1)

fig.set_axis(0,xlim=(-0.1,4),ylim=(0,1))
fig.set_axis(1,xlim=(-0.1,4),ylim=(0,100))
fig.set_label(0,ylabel='$\mathrm{PDF}$')
fig.set_label(0,xlabel='$\widehat{I}_\mathrm{S}/|\widehat{\omega}|_\mathrm{avg}$')
fig.set_label(1,xlabel='$\widehat{I}_\mathrm{R}/|\widehat{\omega}|_\mathrm{avg}$')

for fig_id in range(2):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.8)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/PDF_intensity_Cases.png")
