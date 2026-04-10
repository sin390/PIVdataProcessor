''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/02/20  =
=========================
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from pivdataprocessor.A01_toolbox import nanmean_filter2d
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath
from Q01_Plot.L02_cloud_plot import CloudFigure  
from Z11_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD
import ZZZ_Result_Manager.A01_cases as A01

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/A1_ins_TDM"

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
cf = CloudFigure(
    nrows=1,
    ncols=3,
    figsize=(31,10),    
    figsize_unit="cm",
    cmap=cmap,
    panel_fontsize= 20,
    panel_offset=(-0.1,1.05),

    # margins must be reserved manually
    left=0.07,
    right=0.98,
    bottom=0.22,
    top=1.15,
    dpi=600,
    wspace=0.2
)

global_min = 0
global_max = 10
mag_max = [0.0 for _ in range(3)]
mag_min = [0.0 for _ in range(3)]


case_id = 1
filter_id = 7
run_id = 5
frame_id = 5
print(A01.Lf_label[filter_id-1])

td = TD(A01.cases[case_id], 'gaussian', filter_id)
td.load_avg()
td.cal_frame(run_id,frame_id)
e_range = td.effctive_range
left,right,bottom,up = td.vfh.unpackrange(e_range)
X = td.X[0][left:right,bottom:up]
Y = td.X[1][left:right,bottom:up]

'0'
fig_id = 0
mag = td.intensity_shear[left:right,bottom:up]/td.result_json.get(0)['avg_intensity_SH'] 
mag_max[fig_id] = np.max(mag)
cf.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, method='imshow', interpolation="bicubic")

'1'
fig_id = 1
mag = td.intensity_elongation[left:right,bottom:up]/td.result_json.get(0)['avg_intensity_EL'] 
mag_max[fig_id] = np.max(mag)
cf.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, method='imshow', interpolation="bicubic")

'2'
fig_id = 2
mag = td.intensity_rotation[left:right,bottom:up]/td.result_json.get(0)['avg_intensity_RR'] 
mag_max[fig_id] = np.max(mag)
cf.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, method='imshow', interpolation="bicubic")

cf.add_colorbar(
    mappable_index=0,
    label = r'$\widetilde{I_S}, \widetilde{I_E}, \widetilde{I_R}~\mathrm{(s^{-1})}$',
    orientation="horizontal",
    position=(0.25, 0.2, 0.5, 0.044),  # [left, bottom, width, height]
    fontsize=20,
    label_coords=(0.53, -2.6),
    ticks=(0,2500,5000,7500,10000,12500),
    tick_params=dict(length=12)
)

for i in range(3):
    cf.set_equal_axis(i)
    cf.set_axis(index=i, xlim = (-40,40), ylim = (-23,23),xticks=[-40,-20,0,20,40],yticks=[-20,0,20],subticks=2)
    cf.set_panel_label(i)

cf.set_axis(0,xlabel=r'$x~\mathrm{(mm)}$',ylabel=r'$y~\mathrm{(mm)}$')
cf.set_axis(1,xlabel=r'$x~\mathrm{(mm)}$')
cf.set_axis(2,xlabel=r'$x~\mathrm{(mm)}$')
cf.save(result_fig + figformat)

print(mag_max)
print(mag_min)