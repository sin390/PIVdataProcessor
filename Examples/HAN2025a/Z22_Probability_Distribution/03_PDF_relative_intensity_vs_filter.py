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

quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,3), right_legend=True, wspace=0.3, panel_offset=(-0.2,1.1))
','

filter = 'gaussian'
filter_id = gaussian_id[2]
case = 'Case03'

fig_id = 0
filter = 'gaussian_bp'
for curve_id in range(len(gaussian_id)):
    filter_id = 4-curve_id
    filter_param = gaussian_bp_id[filter_id]
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_S_omega_x
    y = pdf.PDF_S_omega_y
    fig.plot(fig_id,x,y, color=colors[curve_id], label= k1L1_label[filter_id])

fig_id = 1
filter = 'gaussian_bp'
for curve_id in range(len(gaussian_bp_id)):
    filter_id = 4-curve_id
    filter_param = gaussian_bp_id[filter_id]
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_R_omega_x
    y = pdf.PDF_R_omega_y
    fig.plot(fig_id,x,y, color=colors[curve_id])




fig.set_axis(0,xlim=(0,4),ylim=(0,1))
fig.set_axis(1,xlim=(0,4),ylim=(0,1))
fig.set_label(0,ylabel='$\mathrm{PDF}$')
fig.set_label(0,xlabel='$\widehat{I}_\mathrm{S}/|\widehat{\omega}|_\mathrm{avg}$')
fig.set_label(1,xlabel='$\widehat{I}_\mathrm{R}/|\widehat{\omega}|_\mathrm{avg}$')

for fig_id in range(2):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.8)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/PDF_TDM_Schur.png")
