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
from Z24_Probability_Distribution.G01_PDF_for_e2x_Kolar import PDF_for_e2x as PDF
from ZZZ_Result_Manager.A01_cases import cases, cases_f, cases_w, cases_select, case_labels
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

quickset()
nrows = 2
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,8), right_legend=True, hspace=0.5, wspace=0.6, panel_offset=(-0.2,1.1))
','


filter = 'gaussian'

'0'
filter_param = 4
fig_id = 0
for case_id, case in enumerate(cases_select):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id], label= case_labels[case_id])

'1'
filter_param = 3
fig_id = 1
for case_id, case in enumerate(cases_select):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id])

'2'
filter_param = 2
fig_id = 2
for case_id, case in enumerate(cases_select):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id])

'3'
filter_param = 1
fig_id = 3
for case_id, case in enumerate(cases_select):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id])


fig.set_label(2,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(3,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(0,ylabel=r'$\mathrm{p.d.f.}$')
fig.set_label(2,ylabel=r'$\mathrm{p.d.f.}$')
fig.set_axis(0,xlim=(0,180),ylim=(0.0,0.008),xticks=[0,45,90,135,180])
fig.set_axis(1,xlim=(0,180),ylim=(0.0,0.008),xticks=[0,45,90,135,180])
fig.set_axis(2,xlim=(0,180),ylim=(0.0,0.008),xticks=[0,45,90,135,180])
fig.set_axis(3,xlim=(0,180),ylim=(0.0,0.008),xticks=[0,45,90,135,180])
for fig_id in range(4):
    fig.set_panel_label(fig_id)


fig.set_margins(right=0.92)
fig.legend(bbox_to_anchor=(0.8,0.5))
fig.save(getplotpath()+"/PDF_alpha_Cases.png")
