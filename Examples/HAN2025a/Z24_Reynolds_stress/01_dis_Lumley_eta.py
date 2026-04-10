''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/19  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Q01_Plot.C00_cfg_for_cases import case_titles, colors, linewidths
import numpy as np
from Z24_Reynolds_stress.G01_reynolds_stress import ReynoldsStress as RS
from Z01_Filtered_Velocity_Field.H01_gaussian_params import selected_k1L1, k1L1_label, gaussian_id, gaussian_bp_id, L11_cases, cases


quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,3), right_legend=True, wspace=0.6,panel_offset=(-0.2,1.1))
','

case = 'Case06'

'0'
fig_id = 0
filter = 'gaussian'
for curve_id in range(len(gaussian_id)):
    filter_id = 4-curve_id
    filter_param = gaussian_id[filter_id]
    rs = RS(case, filter, filter_param)
    rs.load()
    central_X, central_Y = rs.vfh.central_pos_grid
    left,right,bottom,up = rs.vfh.unpackrange(rs.vfh.effctive_range)
    x = rs.vfh.X[0,left:right,central_Y]
    y = rs.invariant_eta[left:right,central_Y]
    fig.plot(fig_id,x,y, label=k1L1_label[filter_id],color=colors[curve_id])
    

'1'
fig_id = 1
filter = 'gaussian_bp'
for curve_id in range(len(gaussian_bp_id)):
    filter_id = 4-curve_id
    filter_param = gaussian_bp_id[filter_id]
    rs = RS(case, filter, filter_param)
    rs.load()
    central_X, central_Y = rs.vfh.central_pos_grid
    left,right,bottom,up = rs.vfh.unpackrange(rs.vfh.effctive_range)
    x = rs.vfh.X[0,left:right,central_Y]
    y = rs.invariant_eta[left:right,central_Y]
    fig.plot(fig_id,x,y, color=colors[curve_id])

fig.set_label(0,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_label(0,ylabel=r'$\widetilde{B}_2$')
fig.set_label(1,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_label(1,ylabel=r'$\widehat{B}_2$')
fig.set_axis(0,xlim=(-50,50),ylim=(0,0.2))
fig.set_axis(1,xlim=(-50,50),ylim=(0,0.2))
for fig_id in range(2):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.8)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/dis_Lumley_eta.png")
