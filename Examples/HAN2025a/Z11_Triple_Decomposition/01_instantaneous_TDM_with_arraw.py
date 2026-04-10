''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/16  =
=========================
'''

from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
import numpy as np
from Q01_Plot.L02_cloud_plot import CloudFigure, add_length_line
from G01_triple_decomposition import TripleDecomposition as TD
from Z01_Filtered_Velocity_Field.H01_gaussian_params import selected_k1L1, k1L1_label, gaussian_id, gaussian_bp_id, L11_cases

quickset()
CF = CloudFigure(
    nrows=1, ncols=2,
    figsize=(16,6),
    cmap="turbo",
    hspace= 0.3,
    wspace= 0.5
)

case = 'Case03'
L11 = L11_cases[3-1] 
run_id = 4
frame_id = 3
figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/instantaneous_TDM_with_arraw"

global_min = 0
global_max = 4000
Label = ['' for _ in range(3)]
mag_max = [0.0 for _ in range(3)]

filter_id = 5
Lf = 2*np.pi/(selected_k1L1[filter_id-1]/L11)*1000
print(Lf)

td = TD(case, 'gaussian_bp', gaussian_bp_id[filter_id-1])
print(k1L1_label[filter_id-1])
td.cal_frame(run_id,frame_id)
e_range = td.effctive_range
left,right,bottom,up = VFH.unpackrange(e_range)
X = td.X[0][left:right,bottom:up]
Y = td.X[1][left:right,bottom:up]

'0'
fig_id = 0
mag = td.intensity_rotation[left:right,bottom:up]
mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, interpolation="bicubic")
ax = CF.axes[fig_id]
add_length_line(
    ax,x0=-28, y0=-16.0,
    L=Lf,angle_deg=0,       
    color="w",lw=1.0)
'1'
fig_id = 1
mag = td.intensity_shear[left:right,bottom:up]
mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, interpolation="bicubic")
td.load_avg()
td.cal_and_identify_SH_layer_frame(run_id,frame_id)
mask = td.identified_pos
XI, YI = np.where(mask)   # YI=row=y,  XI=col=x
ax = CF.axes[fig_id]
CF.add_quiver(fig_id,td.X[0][XI, YI],td.X[1][XI, YI],
              td.Q[0,1,XI,YI],td.Q[1,1,XI,YI],
              scale=20, width=0.005, color='r', headwidth=3, headlength=3, headaxislength=3)
add_length_line(
    ax,x0=-28, y0=-16.0,
    L=Lf,angle_deg=0,       
    color="w",lw=1.0)

'End'
for i in range(2):
    CF.set_axis(i, xlim=(-31.5,31.5), ylim=(-19,19), xlabel=r'$x~\mathrm{(mm)}$',
                ylabel=r'$y~\mathrm{(mm)}$' if i%2==0 else None,
                xticks=[-30,-15,0,15,30], yticks=[-15,0,15])
    CF.set_equal_axis(i)
    CF.set_panel_label(i,Label[i])

# Colorbar
CF.add_colorbar(
    label=r'$\widehat I_\mathrm{R},\widehat I_\mathrm{S}~\mathrm{(s^{-1})}$',
    position=[0.25, 0.10, 0.5, 0.03]
)

# Margins
CF.set_margins(left=0.07, right=0.93, top=0.95, bottom=0.35)
CF.set_spacing(wspace=0.30, hspace=0.10)

# Save
CF.save(result_fig + figformat)

print(mag_max)