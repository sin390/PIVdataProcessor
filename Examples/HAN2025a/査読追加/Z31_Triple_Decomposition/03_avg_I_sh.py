''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/16  =
=========================
'''

from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath
from Z02_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
import numpy as np
from Q01_Plot.L02_cloud_plot import CloudFigure, add_length_line
from G01_triple_decomposition import TripleDecomposition as TD
from ZZZ_Result_Manager.A01_cases import cases, cases_f

quickset()
CF = CloudFigure(
    nrows=1, ncols=2,
    figsize=(16,6),
    cmap="turbo",
    hspace= 0.3,
    wspace= 0.5
)

case = cases_f[1]
print(case)
figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/instantaneous_TDM_with_arraw"

global_min = 0
global_max = 100
Label = ['' for _ in range(3)]
mag_max = [0.0 for _ in range(3)]


td = TD(case, 'gaussian', 2)
td.load_avg()
e_range = td.effctive_range
left,right,bottom,up = VFH.unpackrange(e_range)
X = td.X[0][left:right,bottom:up]
Y = td.X[1][left:right,bottom:up]

'0'
fig_id = 0
mag = td.avg_intensity_shear[left:right,bottom:up]
mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, interpolation="bicubic")
ax = CF.axes[fig_id]
'1'
fig_id = 1
mag = mag = td.avg_intensity_shear[left:right,bottom:up]
mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, interpolation="bicubic")


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