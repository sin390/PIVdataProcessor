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
from ZZZ_Result_Manager.A01_cases import cases
from Z02_Reynolds_Stress.G01_reynolds_stress import ReynoldsStress as RS
# -------------------------------
# region initialization
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
figsize_inch = (16,8)
# endregion
# -------------------------------


figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/01_reynolds_stress_field"

global_min = 0
global_max = 20
mag_max = [0.0 for _ in range(3)]

CF = CloudFigure(
    nrows=1, ncols=2,
    figsize=figsize_inch,
    cmap="turbo"
)

Label = [r'$u_{\mathrm{rms}}$',r'$v_{\mathrm{rms}}$']

'0'
fig_id = 0

case = cases[0]
rs = RS(case)
rs.load()
left, right = pBase.CaseInfo.Effective_Range[0]
bottom, up = pBase.CaseInfo.Effective_Range[1]
X = pBase.X[0][left:right,bottom:up]
Y = pBase.X[1][left:right,bottom:up]
mag = np.sqrt(rs.uu[left:right,bottom:up])

mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, interpolation="bicubic")


'0'
fig_id = 1

case = cases[-1]
print(case)
rs = RS(case)
rs.load()
left, right = pBase.CaseInfo.Effective_Range[0]
bottom, up = pBase.CaseInfo.Effective_Range[1]
X = pBase.X[0][left:right,bottom:up]
Y = pBase.X[1][left:right,bottom:up]
mag = np.sqrt(rs.vv[left:right,bottom:up])

mag_max[fig_id] = np.max(mag)
CF.add_cloud(fig_id, X, Y, mag, vmin=global_min, vmax=global_max, interpolation="bicubic")

'End'
for i in range(2):
    CF.set_equal_axis(i)
    CF.set_axis(i, xlim=(-40,40), ylim=(-25,25), xlabel=r'$x~\mathrm{(mm)}$',
                ylabel=r'$y~\mathrm{(mm)}$' if i%3==0 else None,
                xticks=[-40,-20,0,20,40], yticks=[-20,0,20])

    CF.set_panel_label(i,Label[i])


# Colorbar
CF.add_colorbar(
    label=r'$u_{\mathrm{rms}}, v_{\mathrm{rms}}~\mathrm{(m/s)}$',
    position=[0.25, 0.10, 0.5, 0.03],
    label_coords=(1.25,1)
    
)

# Margins
CF.set_margins(left=0.12, right=0.93, top=0.95, bottom=0.4)
CF.set_spacing(wspace=0.30, hspace=0.10)

# Save
CF.save(result_fig + figformat)
print(mag_max)