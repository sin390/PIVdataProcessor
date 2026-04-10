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
from Z22_Probability_Distribution.G01_PDF_for_e2x_Kolar import PDF_for_e2x as PDF
from Z01_Filtered_Velocity_Field.H01_gaussian_params import selected_k1L1, k1L1_label, gaussian_id, gaussian_bp_id, L11_cases, cases
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

quickset()
nrows = 2
ncols = 3
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(16,8), right_legend=False, hspace=0.5, wspace=0.5, panel_offset=(-0.2,1.1))
','
ax_5= fig.ax_target(5)
ax_5.remove()

filter = 'gaussian'
filter_param = gaussian_id[4]

fig_id = 0
for case_id, case in enumerate(cases):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id], label= case_titles[case_id], linewidth = linewidths[case_id])

fig_id = 1
filter_param = gaussian_id[3]
for case_id, case in enumerate(cases):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id], linewidth = linewidths[case_id])

fig_id = 2
filter_param = gaussian_id[2]
for case_id, case in enumerate(cases):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id], linewidth = linewidths[case_id])

fig_id = 3
filter_param = gaussian_id[1]
for case_id, case in enumerate(cases):
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id], linewidth = linewidths[case_id])

fig_id = 4
filter_param = gaussian_id[0]
for case_id, case in enumerate(cases):
    if case == 'Mori_465':
        continue
    pdf = PDF(case, filter, filter_param)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    fig.plot(fig_id,x,y, color=colors[case_id], linewidth = linewidths[case_id])


fig.set_axis(0,xlim=(0,180),ylim=(0.002,0.008),xticks=[0,45,90,135,180])
fig.set_axis(1,xlim=(0,180),ylim=(0.002,0.008),xticks=[0,45,90,135,180])
fig.set_axis(2,xlim=(0,180),ylim=(0.002,0.008),xticks=[0,45,90,135,180])
fig.set_axis(3,xlim=(0,180),ylim=(0.002,0.008),xticks=[0,45,90,135,180])
fig.set_axis(4,xlim=(0,180),ylim=(0.002,0.008),xticks=[0,45,90,135,180])
fig.set_label(0,ylabel='$\mathrm{PDF}$')
fig.set_label(3,ylabel='$\mathrm{PDF}$')
for i in [2,3,4]:
    fig.set_label(i,xlabel=r'$\alpha~\mathrm{(deg)}$')

# fig.set_label(0,xlabel='$\widehat{I}_\mathrm{S}/|\widehat{\omega}|_\mathrm{avg}$')
# fig.set_label(1,xlabel='$\widehat{I}_\mathrm{R}/|\widehat{\omega}|_\mathrm{avg}$')

for fig_id in range(5):
    fig.set_panel_label(fig_id)
fig.set_margins(right=1)
fig.legend(bbox_to_anchor=(0.8,0.2))
fig.save(getplotpath()+"/PDF_alpha_Cases_Gaussian.png")
