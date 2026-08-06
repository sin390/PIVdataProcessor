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
from Z21_Energy_Spectrum.G01_energy_spectrum import EnergySpectrum as ES
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL
from Z24_Probability_Distribution.G02_PDF_for_IS import PDF_for_IS as PDF

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/06_IS_PDF"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.08),
    right_legend=True,     # reserve legend column
    left=0.1,
    right=0.92,
    bottom=0.32,
    top=0.88,
    dpi=600,
    wspace=0.3
)

filter = 'gaussian'

'0'
filter_param = 1
fig_id = 0
for case_id, case in enumerate(A01.cases_select):
    pdf = PDF(A01.cases_select_w[case_id], filter, filter_param)
    pdf.load_result(1.5)
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id], label=A01.cases_select_labels[case_id])
print(A01.Lf_labels[filter_param-1])

'1'
filter_param = 4
fig_id = 1
for case_id, case in enumerate(A01.cases_select):
    pdf = PDF(A01.cases_select_w[case_id], filter, filter_param)
    pdf.load_result(1.5)
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id])
print(A01.Lf_labels[filter_param-1])

'2'
filter_param = 7
fig_id = 2
for case_id, case in enumerate(A01.cases_select):
    pdf = PDF(A01.cases_select_w[case_id], filter, filter_param)
    pdf.load_result(1.5)
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id])
print(A01.Lf_labels[filter_param-1])

for i in range(3):
    fig.set_panel_label(i)
    fig.set_axis(i,ylim=(0,0.8))
    fig.set_axis(i,xlim=(0,5),minor_xticks=None)
fig.set_label(0,xlabel=r'$\tilde I_S/\langle \tilde I_S\rangle$')
fig.set_label(1,xlabel=r'$\tilde I_S/\langle \tilde I_S\rangle$')
fig.set_label(2,xlabel=r'$\tilde I_S/\langle \tilde I_S\rangle$')
fig.set_label(0,labelpad=15, ylabel=r'$\mathrm{p.d.f}$')
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend(bbox_to_anchor=(-1,0.5))
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)