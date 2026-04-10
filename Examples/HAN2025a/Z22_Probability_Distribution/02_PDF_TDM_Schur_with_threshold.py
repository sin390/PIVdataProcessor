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
from Z22_Probability_Distribution.G02a_PDF_TDM_Schur_with_threshold import PDF_TDM_Schur as PDF
from Z22_Probability_Distribution.G02a_PDF_TDM_Schur_with_threshold import thresholds
from Z01_Filtered_Velocity_Field.H01_gaussian_params import selected_k1L1, k1L1_label, gaussian_id, gaussian_bp_id, L11_cases, cases

quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,3), right_legend=True, wspace=0.5,panel_offset=(-0.2,1.1))
','

case = 'Case03'
filter = 'gaussian_bp'
filter_id = gaussian_bp_id[2]

fig_id = 0
for th_id, threshold in enumerate(thresholds):
    pdf = PDF(case, filter, filter_id, threshold)
    pdf.load_result()
    x = pdf.PDF_E_NS_x
    y = pdf.PDF_E_NS_y
    fig.plot(fig_id,x,y, color=colors[th_id], linewidth = linewidths[0],label='$C_{th,I}=$'+f'{threshold}')


fig_id = 1
for th_id, threshold in enumerate(thresholds):
    pdf = PDF(case, filter, filter_id, threshold)
    pdf.load_result()
    x = pdf.PDF_R_NO_x
    y = pdf.PDF_R_NO_y
    fig.plot(fig_id,x,y, color=colors[th_id], linewidth = linewidths[0])

fig.set_axis(0,xlim=(-0.1,1.5),ylim=(0,30))
fig.set_axis(1,xlim=(-0.1,1.5),ylim=(0,3))

fig.set_label(0,ylabel='$\mathrm{PDF}$')
fig.set_label(0,xlabel='$\widehat{I}_\mathrm{E}/\widehat{I}_\mathrm{N,S}$')
fig.set_label(1,xlabel='$\widehat{I}_\mathrm{R}/\widehat{I}_\mathrm{N,\Omega}$')
for fig_id in range(2):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.8)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/PDF_TDM_Schur_threshold.png")
