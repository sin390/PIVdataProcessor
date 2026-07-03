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
from pivdataprocessor.A01_toolbox import nanmean_filter2d
import numpy as np
from Z12_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD
from ZZZ_Result_Manager.A01_cases import cases, cases_f


quickset()
nrows = 1
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,3), right_legend=True, wspace=0.8,panel_offset=(-0.2,1.1))
','


'0'
fig_id = 0
filter = 'gaussian'
filter_id = 1
for case_id, case in enumerate(cases_f):
    td = TD(case, filter, filter_id)
    td.load_avg()
    central_X, central_Y = td.vfh.central_pos_grid
    left,right,bottom,up = td.vfh.unpackrange(td.vfh.effctive_range)
    x = td.vfh.X[0,left:right,central_Y]
    y = td.avg_intensity_shear[left:right,central_Y]
    fig.plot(fig_id,x,y, label=case, color=colors[case_id])
    

'0'
fig_id = 0
filter = 'gaussian_bp'
filter_id = (1,2)
for case_id, case in enumerate(cases_f):
    td = TD(case, filter, filter_id)
    td.load_avg()
    central_X, central_Y = td.vfh.central_pos_grid
    left,right,bottom,up = td.vfh.unpackrange(td.vfh.effctive_range)
    x = td.vfh.X[0,left:right,central_Y]
    y = td.avg_intensity_shear[left:right,central_Y]
    fig.plot(fig_id,x,y,  color=colors[case_id])
    

fig.set_label(0,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_label(0,ylabel=r'$\widetilde{I}_\mathrm{S}~\mathrm{(s^{-1})}$')
fig.set_label(1,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_label(1,ylabel=r'$\widehat{I}_\mathrm{S}~\mathrm{(s^{-1})}$')
# fig.set_axis(0,xlim=(-50,50),ylim=(0,4000))
# fig.set_axis(1,xlim=(-50,50),ylim=(0,1000))
for fig_id in range(2):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.85)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/dis_I_sh.png")
