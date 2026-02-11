'''
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09
=========================
'''

import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from Q01_Plot.L03_cmap import white_turbo
from Q01_Plot.L02_cloud_plot import CloudFigure, add_length_line
from Q01_Plot.L00_tools import quickset,getplotpath 
from Z02_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL

from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DR
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, cases_w, cases_select

# -------------------------------
# region initialization
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
figsize_inch = (14,8)
# endregion
# -------------------------------

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/avg_I_S_BRF"

global_min = -0.05
global_max = 1
mag_max = [0.0 for _ in range(3)]
mag_min = [0.0 for _ in range(3)]

CF = CloudFigure(
    nrows=1, ncols=2,
    figsize=figsize_inch,
    cmap='turbo'
)

case_id = 0
filter = 'gaussian'
filter_param = 1

case = cases_select[case_id]
sl = SL(case, filter, filter_param)
sl.load_result()

Lf = sl.result_json.get(0)['Lf_in_mm']
ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
ujump = sl.result_json.get(0)['jump_u']

'0'
fig_id = 0

X = sl.X_BRF[0]/Lf
Y = sl.X_BRF[1]/Lf
U = sl.avg_u_BRF[0]
V = sl.avg_u_BRF[1]
I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']
mag = (sl.avg_Is_BRF-I_s_avg)/(sl.avg_Is_BRF[ic,jc]-I_s_avg)
mag_max[fig_id] = np.nanmax(mag)
mag_min[fig_id] = np.nanmin(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max)

s = 3 
X0 = X[ic, :][::s]
Y0 = Y[ic, :][::s]
U0 = (U[ic, :] / ujump)[::s]
V0 = (V[ic, :] / ujump)[::s]

CF.add_quiver(fig_id, X0, Y0, U0, V0, stride=1, scale=3, width=0.004)

'1'
fig_id = 1

X = sl.X_BRF[0]/Lf
Y = sl.X_BRF[1]/Lf

mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]
mag_max[fig_id] = np.nanmax(mag)
mag_min[fig_id] = np.nanmin(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max)



'End'
for i in range(2):
    CF.set_equal_axis(i)
    CF.set_panel_label(i)
CF.set_axis(0, xlim=(-4.5,4.5), ylim=(-4.5,4.5), xlabel=r'$\boldsymbol{\zeta}_{x}/L_{F}$',
            ylabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$',
            xticks=[-4,-2,0,2,4], yticks=[-4,-2,0,2,4])
CF.set_axis(1, xlim=(-4.5,4.5), ylim=(-4.5,4.5), xlabel=r'$\boldsymbol{\zeta}_{x}/L_{F}$',
            ylabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$',
            xticks=[-4,-2,0,2,4], yticks=[-4,-2,0,2,4])


# Colorbar
CF.add_colorbar(
    label=r'$<\widetilde{I_S}>_\mathrm{norm}, <\widetilde{\omega}_S>_\mathrm{norm}$',
    position=[0.25, 0.10, 0.5, 0.03]
)

# Margins
CF.set_margins(left=0.07, right=0.93, top=0.95, bottom=0.3)
CF.set_spacing(wspace=0.30, hspace=0.10)

# Save
CF.save(result_fig + figformat)
print(mag_max)
print(mag_min)