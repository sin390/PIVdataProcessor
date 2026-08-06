''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/05/28  =
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
from Z24_Probability_Distribution.G01_PDF_for_e2x_Kolar import PDF_for_e2x as PDF

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/02_fig9a_Cth_dependence"
quickset()

fig = PlotFigure(
    nrows=1,
    ncols=3,
    figsize=(31, 10),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.08),
    right_legend=False,     # reserve legend column
    left=0.1,
    right=0.98,
    bottom=0.32,
    top=0.88,
    dpi=600,
    wspace=0.3
)

case_id = 2

fig_id = 0
filter = 'gaussian'
cth = 2
for Lf_id, _ in enumerate(A01.coeffs_to_eta):
    pdf = PDF(A01.cases_select_w[case_id], filter, Lf_id+1)
    pdf.load_result(coef_threshold=cth)
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y,label=A01.Lf_labels[Lf_id], color=colors[Lf_id])

fig_id = 1
filter = 'gaussian'
cth = 3
for Lf_id, _ in enumerate(A01.coeffs_to_eta):
    pdf = PDF(A01.cases_select_w[case_id], filter, Lf_id+1)
    pdf.load_result(coef_threshold=cth)
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y,color=colors[Lf_id])


fig_id = 2
filter = 'gaussian'
cth = 4
for Lf_id, _ in enumerate(A01.coeffs_to_eta):
    pdf = PDF(A01.cases_select_w[case_id], filter, Lf_id+1)
    pdf.load_result(coef_threshold=cth)
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y,color=colors[Lf_id])


for i in range(3):
    fig.set_panel_label(i)
    fig.set_axis(i,ylim=(0,0.01),yticks=[0,0.005,0.01])
    fig.set_axis(i,xlim=(0,180),xticks=[0,45,90,135,180],minor_xticks=None)
fig.set_label(0,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(1,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(2,xlabel=r'$\theta~\mathrm{(deg)}$')
fig.set_label(0,labelpad=15, ylabel=r'$\mathrm{p.d.f}$')
# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.add_legend_bottom_rowmajor_manual(x=0.5,y=0.04,ncol=7,xpad=0.14,handlelength=0.02,fontsize=16)
# ---------------------------
# save & show
# ---------------------------
fig.save(result_fig + figformat)
