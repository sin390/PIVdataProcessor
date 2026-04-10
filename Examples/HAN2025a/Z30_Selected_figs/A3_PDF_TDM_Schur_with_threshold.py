''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/16  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Q01_Plot.C00_cfg_for_cases import colors, linewidths
from pivdataprocessor.A01_toolbox import ProbabilityDensity as PD
import numpy as np
from Z22_Probability_Distribution.G02a_PDF_TDM_Schur_with_threshold import PDF_TDM_Schur as PDF
from Z22_Probability_Distribution.G02a_PDF_TDM_Schur_with_threshold import thresholds
from ZZZ_Result_Manager.A01_cases import cases, gaussian_id

quickset()
fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.07),
    right_legend=False,     # reserve legend column
    left=0.08,
    right=0.98,
    bottom=0.32,
    top=0.88,
    dpi=600,
    wspace=0.3
)

case = 'Case02'
filter = 'gaussian'
filter_id = 5

fig_id = 0
for th_id, threshold in enumerate(thresholds):
    pdf = PDF(case, filter, filter_id, threshold)
    pdf.load_result()
    x = pdf.PDF_S_NN_x
    y = pdf.PDF_S_NN_y
    fig.plot(fig_id,x,y, color=colors[th_id],label='$C_{th,I}=$'+f'{threshold}')

fig_id = 1
for th_id, threshold in enumerate(thresholds):
    pdf = PDF(case, filter, filter_id, threshold)
    pdf.load_result()
    x = pdf.PDF_E_NS_x
    y = pdf.PDF_E_NS_y
    fig.plot(fig_id,x,y, color=colors[th_id])

fig_id = 2
for th_id, threshold in enumerate(thresholds):
    pdf = PDF(case, filter, filter_id, threshold)
    pdf.load_result()
    x = pdf.PDF_R_NO_x
    y = pdf.PDF_R_NO_y
    fig.plot(fig_id,x,y, color=colors[th_id])

fig.set_axis(0,xlim=(0,1.5),ylim=(0,120),minor_yticks=25)
fig.set_axis(1,xlim=(0,1.5),ylim=(0,40),minor_yticks=10)
fig.set_axis(2,xlim=(0,1.5),ylim=(0,4),minor_yticks=1)

fig.set_label(0,ylabel='$\mathrm{p.d.f.}$')
fig.set_label(0,xlabel='$\widetilde{I}_\mathrm{S}/\widetilde{I}_\mathrm{NN}$')
fig.set_label(1,xlabel='$\widetilde{I}_\mathrm{E}/\widetilde{I}_\mathrm{N,S}$')
fig.set_label(2,xlabel='$\widetilde{I}_\mathrm{R}/\widetilde{I}_\mathrm{N,\Omega}$')
for fig_id in range(3):
    fig.set_panel_label(fig_id)
# fig.legend(bbox_to_anchor=(0.7,0.5))
fig.add_legend_bottom_rowmajor_manual(x=0.55,y=0.05,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
fig.save(getplotpath()+"/A3_PDF_TDM_Schur_with_threshold.png")
