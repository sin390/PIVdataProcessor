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
from ZZZ_Result_Manager.A01_cases import cases, case_labels, cases_f, cases_w, cases_select
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

quickset()
CF = CloudFigure(
    nrows=1, ncols=1,
    figsize=(8,6),
    cmap="turbo",
    hspace= 0.3,
    wspace= 0.5
)

case_id = 0
case_s = cases_select[case_id]
case = cases[case_id]

rm = RM(case)
eta = rm.result_table.get(3)['eta']
nu = rm.result_table.get(3)['kinetic_viscosity']

filter_id = 1
run_id = 3
frame_id = 8

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/instantaneous_TDM_with_arraw"

global_min = 0
global_max = 1.05
Label = ['' for _ in range(3)]
mag_max = [0.0 for _ in range(3)]


td = TD(case_s, 'gaussian', filter_id)
td.cal_frame(run_id,frame_id)

e_range = td.effctive_range
left,right,bottom,up = VFH.unpackrange(e_range)
X = td.X[0][left:right,bottom:up]
Y = td.X[1][left:right,bottom:up]

'0'
fig_id = 0
mag = td.intensity_shear[left:right,bottom:up]/nu*eta**2
mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, method='imshow', interpolation="bicubic")
td.load_avg()
td.cal_and_identify_SH_layer_frame(run_id,frame_id,coef_threshold=1.5,maximum_window=5)
mask = td.identified_pos
XI, YI = np.where(mask)   # YI=row=y,  XI=col=x
ax = CF.axes[fig_id]

# CF.add_quiver(fig_id,td.X[0][XI, YI],td.X[1][XI, YI],
#               td.Q[0,1,XI,YI],td.Q[1,1,XI,YI],
#               scale=20, width=0.005, color='r', headwidth=3, headlength=3, headaxislength=3)

'End'

# Colorbar
cbar = CF.add_colorbar(
    label=r'$\widehat I_\mathrm{S}\tau_\eta$',
    position=[0.15, 0.10, 0.7, 0.03],
    label_coords = (-0.15,1.8)
)

# Margins
CF.set_margins(left=0.07, right=0.93, top=0.95, bottom=0.35)
CF.set_spacing(wspace=0.30, hspace=0.10)
CF.set_axis(0,xlabel=r'$x~\mathrm{(mm)}$', ylabel=r'$y~\mathrm{(mm)}$')
# Save
CF.save(result_fig + figformat)

print(mag_max)