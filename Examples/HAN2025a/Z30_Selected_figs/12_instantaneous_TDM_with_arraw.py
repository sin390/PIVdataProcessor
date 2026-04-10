''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/16  =
=========================
'''

from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath
import ZZZ_Result_Manager.A01_cases as A01

from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
import numpy as np
from Q01_Plot.L02_cloud_plot import CloudFigure, add_length_line
from Z11_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

from matplotlib.colors import LinearSegmentedColormap
colors = [
    (1.0,1.0,1.0),   # white
    # (0.0,1.0,1.0),   # cyan
    (0.0,0.3,1.0),   # blue
    (1.0,1.0,0.0),   # yellow
    (1.0,0.4,0.0),   # orange
    (1.0,0.0,0.0),   # red
    (0.6,0.0,0.8)    # purple
]
cmap = LinearSegmentedColormap.from_list(
    "piv_style",
    colors,
    N=256
)

quickset()
CF = CloudFigure(
    nrows=1, ncols=1,
    figsize=(31,10),    
    # cmap='turbo',
    cmap=cmap,
    hspace= 0.3,
    wspace= 0.5
)

case_id = 0
case = A01.cases[case_id]


filter_id = 7
run_id = 5
frame_id = 18

figformat = ".jpg"
fig_path = getplotpath()
result_fig = f"{fig_path}/instantaneous_TDM"

global_min = 0
global_max = 12000
Label = ['' for _ in range(3)]
mag_max = [0.0 for _ in range(3)]


td = TD(case, 'gaussian', filter_id)
td.cal_frame(run_id,frame_id)

e_range = td.effctive_range
left,right,bottom,up = VFH.unpackrange(e_range)
X = td.X[0][left:right,bottom:up]
Y = td.X[1][left:right,bottom:up]

'0'
fig_id = 0
mag = td.intensity_shear[left:right,bottom:up]
mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, method='imshow', interpolation="bicubic")
'End'

# Colorbar
cbar = CF.add_colorbar(
    label=r'$\widetilde I_\mathrm{S}~\mathrm{(s^{-1})}$',
    position=[0.3, 0.10, 0.4, 0.03],
    label_coords = (-0.15,1.8),
    fontsize=16
)

# Margins
CF.set_margins(left=0.07, right=0.93, top=0.95, bottom=0.35)
CF.set_axis(0,xlim=(-35,35),ylim=(-20,20),yticks=[-20,0,20])
# CF.set_spacing(wspace=0.30, hspace=0.10)
CF.set_equal_axis(0)
CF.set_axis(0,xlabel=r'$x~\mathrm{(mm)}$', ylabel=r'$y~\mathrm{(mm)}$')
# Save
CF.save(result_fig + figformat)
print(A01.Lf_label[filter_id-1])
print(mag_max)