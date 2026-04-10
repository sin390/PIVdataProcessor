''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/12/08  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Z22_Probability_Distribution.G01_PDF_for_e2x_Kolar import PDF_for_e2x
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import params, params_mori
from pivdataprocessor.A01_toolbox import ProbabilityDensity as PD
import numpy as np

quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(16,6), right_legend=True, wspace=0.5)
''

case = 'Case03'

col_id = 0
for ft_id in params[col_id][:-1]:
    pdf = PDF_for_e2x(case, 'gaussian', ft_id)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    scale = pdf.td.vfh.scale_in_grid
    fig.plot(col_id,x,y, label = f'$C_L = {scale:.1f}$',marker=None)

col_id = 1
for ft_id in params[col_id][:-1]:
    pdf = PDF_for_e2x(case, 'gaussian_bp', ft_id)
    pdf.load_result()
    x = pdf.PDF_x
    y = pdf.PDF_y
    scale = pdf.td.vfh.scale_in_grid
    fig.plot(col_id,x,y, label = f'$C_L = ({scale[0]:.1f},{scale[1]:.1f})$',marker=None)

# col_id = 2
# for ft_id in params[col_id][:-1]:
#     pdf = PDF_for_e2x(case, 'wavelet', ft_id)
#     pdf.load_result()
#     x = pdf.PDF_x
#     y = pdf.PDF_y
#     scale = pdf.td.vfh.scale_in_grid
#     fig.plot(col_id,x,y, label = f'$C_L \propto {scale}$',marker=None)


for i in range(2):
    # fig.set_axis(i, xlim = (0,90),ylim = (-0.005,0.04),xticks = [0,45,90], minor_xticks=15)
    fig.set_axis(i, xlim = (0,360),ylim = (0,0.02),xticks = [i*45 for i in range(9)],minor_xticks=15)
    fig.set_axis(i, xlim = (0,180),ylim = (0,0.01),xticks = [i*45 for i in range(5)],minor_xticks=15)

fig.set_margins(right=0.8)
fig.set_margins(top = 0.5, bottom=0.2)
fig.panel_offset = (-0.22,1.12)
fig.set_panel_label(0, "Gaussian")
fig.set_panel_label(1, "Gaussian_bp")
# fig.set_panel_label(2, "Wavelet")

fig.set_label(0,ylabel='$\mathrm{P.D.F}$')
# fig.set_label(2,ylabel='$\mathrm{P.D.F}$')
fig.set_label(0,xlabel=r'$\alpha$'+'$(\mathrm{deg})$')
fig.set_label(1,xlabel=r'$\alpha$'+'$(\mathrm{deg})$')

fig.legend(bbox_to_anchor=(0.7,0.5))
# fig.add_legend_inside()

fig.save(getplotpath()+"/figure1.jpg")
fig.show()
