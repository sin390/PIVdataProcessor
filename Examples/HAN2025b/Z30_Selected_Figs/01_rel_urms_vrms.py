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
from Z13_Reynolds_Stress.G01_reynolds_stress import ReynoldsStress as RS

import ZZZ_Result_Manager.A01_cases as A01

figformat = ".png"
fig_path = getplotpath()
result_fig = f"{fig_path}/01_rel_urms_vrms"

norm = Normalize(vmin=-25, vmax=25)
p = 60

quickset()
cf = CloudFigure(
    nrows=2,
    ncols=3,
    figsize=(31,18),    
    figsize_unit="cm",
    cmap='bwr',
    panel_fontsize= 20,
    panel_offset=(-0.2,1.05),

    # margins must be reserved manually
    left=0.07,
    right=0.98,
    bottom=0.22,
    top=0.95,
    dpi=600,
    wspace=0.2,hspace=0.2
)



case_id = 0
rs = RS(A01.cases_select_w[case_id])
rs.load()
central_x, central_y = pBase.CaseInfo.Central_Position_Grid
left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]

urms = np.sqrt(rs.uu)
vrms = np.sqrt(rs.vv)
avg_urms = np.nanmean(urms[left:right,bottom:up])
avg_vrms = np.nanmean(vrms[left:right,bottom:up])
# rel_urms = (urms-avg_urms)/avg_urms*100
# rel_vrms = (vrms-avg_vrms)/avg_vrms*100
rel_urms = nanmean_filter2d((urms-avg_urms)/avg_urms*100)
rel_vrms = nanmean_filter2d((vrms-avg_vrms)/avg_vrms*100)

print(A01.cases_select_w[case_id],'urms',np.max(rel_urms[left:right,bottom:up]),np.min(rel_urms[left:right,bottom:up]))
print(A01.cases_select_w[case_id],'vrms',np.max(rel_vrms[left:right,bottom:up]),np.min(rel_vrms[left:right,bottom:up]))
fig_id = 0
cf.add_cloud(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_urms[left:right,bottom:up],
    method="imshow",
    norm=norm,
    rasterized=True,    # PDF size friendly
    aspect="equal",
)
cf.add_contour(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_urms[left:right,bottom:up],
    levels=(-15,-5,5,15),
    colors="k",
    linewidths=1.2,
)

fig_id = 3
cf.add_cloud(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_vrms[left:right,bottom:up],
    method="imshow",
    norm=norm,
    rasterized=True,    # PDF size friendly
    aspect="equal",
)
cf.add_contour(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_vrms[left:right,bottom:up],
    levels=(-15,-5,5,15),
    colors="k",
    linewidths=1.2,
)

case_id = 1
rs = RS(A01.cases_select_w[case_id])
rs.load()
central_x, central_y = pBase.CaseInfo.Central_Position_Grid
left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]

urms = np.sqrt(rs.uu)
vrms = np.sqrt(rs.vv)
avg_urms = np.nanmean(urms[left:right,bottom:up])
avg_vrms = np.nanmean(vrms[left:right,bottom:up])

# rel_urms = (urms-avg_urms)/avg_urms*100
# rel_vrms = (vrms-avg_vrms)/avg_vrms*100
rel_urms = nanmean_filter2d((urms-avg_urms)/avg_urms*100)
rel_vrms = nanmean_filter2d((vrms-avg_vrms)/avg_vrms*100)

print(A01.cases_select_w[case_id],'urms',np.max(rel_urms[left:right,bottom:up]),np.min(rel_urms[left:right,bottom:up]))
print(A01.cases_select_w[case_id],'vrms',np.max(rel_vrms[left:right,bottom:up]),np.min(rel_vrms[left:right,bottom:up]))
fig_id = 1
cf.add_cloud(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_urms[left:right,bottom:up],
    method="imshow",
    norm=norm,
    rasterized=True,    # PDF size friendly
    aspect="equal",
)
cf.add_contour(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_urms[left:right,bottom:up],
    levels=(-15,-5,5,15),
    colors="k",
    linewidths=1.2,
)

fig_id = 4
cf.add_cloud(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_vrms[left:right,bottom:up],
    method="imshow",
    norm=norm,
    rasterized=True,    # PDF size friendly
    aspect="equal",
)
cf.add_contour(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_vrms[left:right,bottom:up],
    levels=(-15,-5,5,15),
    colors="k",
    linewidths=1.2,
)
case_id = 2
rs = RS(A01.cases_select_w[case_id])
rs.load()
central_x, central_y = pBase.CaseInfo.Central_Position_Grid
left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]

urms = np.sqrt(rs.uu)
vrms = np.sqrt(rs.vv)
avg_urms = np.nanmean(urms[left:right,bottom:up])
avg_vrms = np.nanmean(vrms[left:right,bottom:up])
# rel_urms = (urms-avg_urms)/avg_urms*100
# rel_vrms = (vrms-avg_vrms)/avg_vrms*100
rel_urms = nanmean_filter2d((urms-avg_urms)/avg_urms*100)
rel_vrms = nanmean_filter2d((vrms-avg_vrms)/avg_vrms*100)

print(A01.cases_select_w[case_id],'urms',np.max(rel_urms[left:right,bottom:up]),np.min(rel_urms[left:right,bottom:up]))
print(A01.cases_select_w[case_id],'vrms',np.max(rel_vrms[left:right,bottom:up]),np.min(rel_vrms[left:right,bottom:up]))
fig_id = 2
cf.add_cloud(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_urms[left:right,bottom:up],
    method="imshow",
    norm=norm,
    rasterized=True,    # PDF size friendly
    aspect="equal",
)
cf.add_contour(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_urms[left:right,bottom:up],
    levels=(-15,-5,5,15),
    colors="k",
    linewidths=1.2,
)

fig_id = 5
cf.add_cloud(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_vrms[left:right,bottom:up],
    method="imshow",
    norm=norm,
    rasterized=True,    # PDF size friendly
    aspect="equal",
)
cf.add_contour(
    index=fig_id,
    X=pBase.X[0,left:right,bottom:up]/p,
    Y=pBase.X[1,left:right,bottom:up]/p,
    field=rel_vrms[left:right,bottom:up],
    levels=(-15,-5,5,15),
    colors="k",
    linewidths=1.2,
)

cf.add_colorbar(
    mappable_index=0,
    label = r"$\Delta(u_\mathrm{rms})~(\mathrm{\%})$"+r"$, \Delta(v_\mathrm{rms})~(\mathrm{\%})$",
    orientation="horizontal",
    position=(0.25, 0.1, 0.5, 0.035),  # [left, bottom, width, height]
    fontsize=20,
    label_coords=(0.5, -1.6),
    ticks=(-25,-15,-5,5,15,25),
    tick_params=dict(length= 18)
)

for i in range(6):
    cf.set_axis(index=i, xlim = (-1,1), ylim = (-0.6,0.6),subticks=2)
    cf.set_panel_label(i)
cf.set_axis(0,ylabel=r'$y/p$')
cf.set_axis(3,ylabel=r'$y/p$')
cf.set_axis(3,xlabel=r'$x/p$')
cf.set_axis(4,xlabel=r'$x/p$')
cf.set_axis(5,xlabel=r'$x/p$')
cf.save(result_fig + figformat)
