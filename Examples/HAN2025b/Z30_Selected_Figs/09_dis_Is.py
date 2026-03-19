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
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL

import ZZZ_Result_Manager.A01_cases as A01

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/09_dis_Is"

quickset()
cf = CloudFigure(
    nrows=1,
    ncols=3,
    figsize=(31,15),    
    figsize_unit="cm",
    cmap='bwr',
    panel_fontsize= 20,
    panel_offset=(-0.1,1.02),

    # margins must be reserved manually
    left=0.07,
    right=0.98,
    bottom=0.22,
    top=1,
    dpi=600,
    wspace=0.2
)

global_min = 0
global_max = 1
mag_max = [0.0 for _ in range(3)]
mag_min = [0.0 for _ in range(3)]
s = 4 
filter_id = 7

fig_id = 0
case_id = fig_id
sl = SL(A01.cases_select_w[case_id], 'gaussian', filter_id)
sl.load_result()

Lf = sl.result_json.get(0)['Lf_in_mm']
ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
ujump = sl.result_json.get(0)['jump_u']
X = sl.X_BRF[0]/Lf
Y = sl.X_BRF[1]/Lf
U = sl.avg_u_BRF[0]
V = sl.avg_u_BRF[1]
I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']
mag = (sl.avg_Is_BRF)/(sl.avg_Is_BRF[ic,jc])
mag_max[fig_id] = np.nanmax(mag)
mag_min[fig_id] = np.nanmin(mag)
cf.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, aspect="equal")

X0 = X[ic, :][::s]
Y0 = Y[ic, :][::s]
U0 = (U[ic, :] / ujump)[::s]
V0 = (V[ic, :] / ujump)[::s]
cf.add_quiver(fig_id, X0, Y0, U0, V0, stride=1, scale=3, width=0.004)

fig_id = 1
case_id = fig_id
sl = SL(A01.cases_select_w[case_id], 'gaussian', filter_id)
sl.load_result()

Lf = sl.result_json.get(0)['Lf_in_mm']
ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
ujump = sl.result_json.get(0)['jump_u']
X = sl.X_BRF[0]/Lf
Y = sl.X_BRF[1]/Lf
U = sl.avg_u_BRF[0]
V = sl.avg_u_BRF[1]
I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']
mag = (sl.avg_Is_BRF)/(sl.avg_Is_BRF[ic,jc])
mag_max[fig_id] = np.nanmax(mag)
mag_min[fig_id] = np.nanmin(mag)
cf.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, aspect="equal")

X0 = X[ic, :][::s]
Y0 = Y[ic, :][::s]
U0 = (U[ic, :] / ujump)[::s]
V0 = (V[ic, :] / ujump)[::s]
cf.add_quiver(fig_id, X0, Y0, U0, V0, stride=1, scale=3, width=0.004)

fig_id = 2
case_id = fig_id
sl = SL(A01.cases_select_w[case_id], 'gaussian', filter_id)
sl.load_result()

Lf = sl.result_json.get(0)['Lf_in_mm']
ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
ujump = sl.result_json.get(0)['jump_u']
X = sl.X_BRF[0]/Lf
Y = sl.X_BRF[1]/Lf
U = sl.avg_u_BRF[0]
V = sl.avg_u_BRF[1]
I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']
mag = (sl.avg_Is_BRF)/(sl.avg_Is_BRF[ic,jc])
mag_max[fig_id] = np.nanmax(mag)
mag_min[fig_id] = np.nanmin(mag)
cf.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, aspect="equal")

X0 = X[ic, :][::s]
Y0 = Y[ic, :][::s]
U0 = (U[ic, :] / ujump)[::s]
V0 = (V[ic, :] / ujump)[::s]
cf.add_quiver(fig_id, X0, Y0, U0, V0, stride=1, scale=3, width=0.004)


cf.add_colorbar(
    mappable_index=0,
    label = r'$\left\langle\widetilde{I_S}\right\rangle / \left\langle\widetilde{I_S}\right\rangle_{(0,0)}$',
    orientation="horizontal",
    position=(0.25, 0.15, 0.5, 0.035),  # [left, bottom, width, height]
    fontsize=20,
    label_coords=(0.53, -1.8),
    ticks=(0,0.25,0.5,0.75,1.0),
    tick_params=dict(length=14)
)

for i in range(3):
    cf.set_axis(index=i, xlim = (-5,5), ylim = (-5,5),xticks=[-4,-2,0,2,4],yticks=[-4,-2,0,2,4],subticks=2)
    cf.set_panel_label(i)

cf.set_axis(0,xlabel=r'$\boldsymbol{\zeta}_{x}/L_{F}$',ylabel=r'$\boldsymbol{\zeta}_{y}/L_{F}$')
cf.set_axis(1,xlabel=r'$\boldsymbol{\zeta}_{x}/L_{F}$')
cf.set_axis(2,xlabel=r'$\boldsymbol{\zeta}_{x}/L_{F}$')
cf.save(result_fig + figformat)

print(mag_max)
print(mag_min)