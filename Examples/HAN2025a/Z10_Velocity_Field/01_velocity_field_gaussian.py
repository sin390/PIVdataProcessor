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
from Z01_Filtered_Velocity_Field.H01_gaussian_params import selected_k1L1, k1L1_label, gaussian_id, gaussian_bp_id, L11_cases

# -------------------------------
# region initialization
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
figsize_inch = (16,6)
# endregion
# -------------------------------

case = 'Case03'
L11 = L11_cases[3-1] 
run_id = 4
frame_id = 3
figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/instantaneous_velocity_gaussian"

global_min = 0
global_max = 60
Label = ['' for _ in range(3)]
mag_max = [0.0 for _ in range(3)]

CF = CloudFigure(
    nrows=1, ncols=3,
    figsize=figsize_inch,
    cmap="turbo"
)

'0'
fig_id = 0
vfh = VFH(case, 'gaussian', -1)
vfh.load_X()
vfh.load_field(run_id,frame_id)
e_range = vfh.effctive_range
left,right = e_range[0]
bottom,up = e_range[1]

X = vfh.X[0][left:right,bottom:up]
Y = vfh.X[1][left:right,bottom:up]
U = vfh.u[0][left:right,bottom:up]
V = vfh.u[1][left:right,bottom:up]
mag = np.sqrt(U**2 + V**2)
mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, interpolation="bicubic")

'1'
fig_id = 1
filter_id = 3
vfh = VFH(case, 'gaussian', gaussian_id[filter_id-1])
print(k1L1_label[filter_id-1])
vfh.load_X()
vfh.load_field(run_id,frame_id)
e_range = vfh.effctive_range
left,right = e_range[0]
bottom,up = e_range[1]

X = vfh.X[0][left:right,bottom:up]
Y = vfh.X[1][left:right,bottom:up]
U = vfh.u[0][left:right,bottom:up]
V = vfh.u[1][left:right,bottom:up]
mag = np.sqrt(U**2 + V**2)
mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, interpolation="bicubic")
ax = CF.axes[fig_id]
Lf = 2*np.pi/(selected_k1L1[filter_id-1]/L11)*1000
print(Lf)
add_length_line(
    ax,
    x0=-35, y0=-20.0,  
    L=Lf,
    angle_deg=0,       
    color="w",
    lw=1.0,
)

'2'
fig_id = 2
filter_id = 5
vfh = VFH(case, 'gaussian', gaussian_id[filter_id-1])
print(k1L1_label[filter_id-1])
vfh.load_X()
vfh.load_field(run_id,frame_id)
e_range = vfh.effctive_range
left,right = e_range[0]
bottom,up = e_range[1]

X = vfh.X[0][left:right,bottom:up]
Y = vfh.X[1][left:right,bottom:up]
U = vfh.u[0][left:right,bottom:up]
V = vfh.u[1][left:right,bottom:up]
mag = np.sqrt(U**2 + V**2)
mag_max[fig_id] = np.max(mag)
Lf = 2*np.pi/(selected_k1L1[filter_id-1]/L11)*1000
print(Lf)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, interpolation="bicubic")
ax = CF.axes[fig_id]
add_length_line(
    ax,
    x0=-30, y0=-15.0,   
    L=Lf,
    angle_deg=0,       
    color="w",
    lw=1.0,
)


'End'
for i in range(3):
    CF.set_equal_axis(i)
    CF.set_axis(i, xlim=(-45,45), ylim=(-28,28), xlabel=r'$x~\mathrm{(mm)}$',
                ylabel=r'$y~\mathrm{(mm)}$' if i%3==0 else None,
                xticks=[-40,-20,0,20,40], yticks=[-20,0,20])

    CF.set_panel_label(i,Label[i])



# Colorbar
CF.add_colorbar(
    label=r'$|\mathbf{u}|, |\widetilde{\mathbf{u}}|~\mathrm{(m/s)}$',
    position=[0.25, 0.10, 0.5, 0.03]
)

# Margins
CF.set_margins(left=0.07, right=0.93, top=0.95, bottom=0.22)
CF.set_spacing(wspace=0.30, hspace=0.10)

# Save
CF.save(result_fig + figformat)
print(mag_max)