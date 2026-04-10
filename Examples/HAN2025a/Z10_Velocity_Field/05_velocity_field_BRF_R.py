'''
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09
=========================
'''

import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from Q01_Plot.L02_cloud_plot import CloudFigure, add_length_line
from Q01_Plot.L00_tools import quickset,getplotpath 
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from Z01_Filtered_Velocity_Field.H01_gaussian_params import selected_k1L1, k1L1_label, gaussian_id, gaussian_bp_id, L11_cases, cases
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL
import matplotlib.colors as mcolors
from Z10_Velocity_Field.T01_local_toolbox import add_open_arc_one_arrow


# -------------------------------
# region initialization
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
figsize_inch = (14,8)
# endregion
# -------------------------------

case_id =2
filter_id = 2
figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/avg_omega_BRF"



global_min = -3
global_max = 3
mag_max = [0.0 for _ in range(3)]
mag_min = [0.0 for _ in range(3)] 
norm = mcolors.TwoSlopeNorm(vmin=global_min, vcenter=0.0, vmax=global_max)
CF = CloudFigure(
    nrows=1, ncols=2,
    figsize=figsize_inch,
    # cmap="turbo"
    cmap="seismic"
)


'0'
fig_id = 0
filter = 'gaussian_bp'
filter_param = gaussian_bp_id[filter_id]
Lf = 2*np.pi/selected_k1L1[filter_id]/L11_cases[case_id]
sl = SL(cases[case_id], filter, filter_param)
sl.load_result()

X = sl.X_BRF[0]/Lf
Y = sl.X_BRF[1]/Lf
U = sl.avg_u_BRF[0]
V = sl.avg_u_BRF[1]
mag = sl.avg_omega_r_BRF/sl.td.result_json.get(0)['avg_intensity_RR']
mag_max[fig_id] = np.nanmax(mag)
mag_min[fig_id] = np.nanmin(mag)
CF.add_cloud(fig_id, X, Y, mag,  interpolation="bicubic",    norm = norm)

'1'
fig_id = 1
filter = 'gaussian'

filter_param = gaussian_id[2]
Lf = 2*np.pi/selected_k1L1[filter_id]/L11_cases[case_id]
sl = SL(cases[case_id], filter, filter_param)
sl.load_result()
X = sl.X_BRF[0]/Lf
Y = sl.X_BRF[1]/Lf
ic, jc = len(X[:,0])//2, len(X[0,:])//2
U = sl.avg_u_BRF[0]
V = sl.avg_u_BRF[1]
mag = sl.avg_omega_r_BRF/sl.td.result_json.get(0)['avg_intensity_RR']
mag_max[fig_id] = np.nanmax(mag)
mag_min[fig_id] = np.nanmin(mag)
CF.add_cloud(fig_id, X, Y, mag, interpolation="bicubic",    norm = norm)


'End'
for i in range(2):
    CF.set_equal_axis(i)
    CF.set_panel_label(i)
CF.set_axis(0, xlim=(-2.5,2.5), ylim=(-2.5,2.5), xlabel=r'$\boldsymbol{\zeta}_{x}/L_{F}$',
            ylabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$',
            xticks=[-2,-1,0,1,2], yticks=[-2,-1,0,1,2])
CF.set_axis(1, xlim=(-2.5,2.5), ylim=(-2.5,2.5), xlabel=r'$\boldsymbol{\zeta}_{x}/L_{F}$',
            ylabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$',
            xticks=[-2,-1,0,1,2], yticks=[-2,-1,0,1,2])


# Colorbar
CF.add_colorbar(
    label=r'$\widehat{\omega}_\mathrm{R}/(\widehat{I}_\mathrm{R})_\mathrm{avg}, \widetilde{\omega}_\mathrm{R}/(\widetilde{I}_\mathrm{R})_\mathrm{avg}$',
    position=[0.25, 0.10, 0.5, 0.03]
)

# Margins
CF.set_margins(left=0.07, right=0.93, top=0.95, bottom=0.3)
CF.set_spacing(wspace=0.30, hspace=0.10)

# Save
CF.save(result_fig + figformat)
print(mag_max)
print(mag_min)