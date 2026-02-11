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
import matplotlib.pyplot as plt
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from Z10_Mean_Flow.G01_fitted_slope import FittedSlope as FS

from ZZZ_Result_Manager.A01_cases import cases, case_labels


quickset()
plt.rcParams.update({
    "axes.grid": False
})
nrows = 2
ncols = 2
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(14,7), 
                 wspace = 0.6, hspace = 0.5,right_legend=True, panel_offset=(-0.2,1.1))
','

p = 60
x_0 = 0
y_0 = 0
x_1 = 30
y_1 = 15

fig_id = 0
# dUdX-x
for case_id, case in enumerate(cases):
    fs = FS(case)
    fs.load_fitted()
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= fs.effctive_range[0]
    bottom, up = fs.effctive_range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = fs.fit_avg_dUdX[0][0][left:right,i_y[0]]*1000
    fig.plot(fig_id,x,y,color=colors[case_id],label=case_labels[case_id])
    
    x = pBase.X[0][left:right,i_y[1]]
    y = fs.fit_avg_dUdX[0][0][left:right,i_y[1]]*1000
    fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')

fig_id = 1
# dUdY-x
for case_id, case in enumerate(cases):
    fs = FS(case)
    fs.load_fitted()
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= fs.effctive_range[0]
    bottom, up = fs.effctive_range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = fs.fit_avg_dUdX[0][1][left:right,i_y[0]]*1000
    fig.plot(fig_id,x,y,color=colors[case_id])
    
    x = pBase.X[0][left:right,i_y[1]]
    y = fs.fit_avg_dUdX[0][1][left:right,i_y[1]]*1000
    fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.')  

fig_id = 2
# dVdX-x
for case_id, case in enumerate(cases):
    fs = FS(case)
    fs.load_fitted()
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= fs.effctive_range[0]
    bottom, up = fs.effctive_range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = fs.fit_avg_dUdX[1][0][left:right,i_y[0]]*1000
    fig.plot(fig_id,x,y,color=colors[case_id])
    
    x = pBase.X[0][left:right,i_y[1]]
    y = fs.fit_avg_dUdX[1][0][left:right,i_y[1]]*1000
    fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.') 

fig_id = 3
# dVdY-x
for case_id, case in enumerate(cases):
    fs = FS(case)
    fs.load_fitted()
    i_x, i_y = pBase.pos_mm_to_index_list([x_0, x_1], [y_0, y_1])
    left, right= fs.effctive_range[0]
    bottom, up = fs.effctive_range[1]

    x = pBase.X[0][left:right,i_y[0]]
    y = fs.fit_avg_dUdX[0][1][left:right,i_y[0]]*1000
    fig.plot(fig_id,x,y,color=colors[case_id])
    
    x = pBase.X[0][left:right,i_y[1]]
    y = fs.fit_avg_dUdX[0][1][left:right,i_y[1]]*1000
    fig.plot(fig_id,x,y,color=colors[case_id], linewidth = 0.5, linestyle='-.') 


fig.set_label(0,ylabel=r'$<\partial U/\partial x>~\mathrm{(s^{-1})}$')
fig.set_label(1,ylabel=r'$<\partial U/\partial y>~\mathrm{(s^{-1})}$')
fig.set_label(2,ylabel=r'$<\partial V/\partial x>~\mathrm{(s^{-1})}$')
fig.set_label(3,ylabel=r'$<\partial V/\partial y>~\mathrm{(s^{-1})}$')
fig.set_label(2,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_label(3,xlabel=r'$x~\mathrm{(mm)}$')
fig.set_axis(0,xlim=(-60,60),ylim=(-30,10))
fig.set_axis(1,xlim=(-60,60),ylim=(-10,30))
fig.set_axis(2,xlim=(-60,60),ylim=(-20,20))
fig.set_axis(3,xlim=(-60,60),ylim=(-10,30))
for fig_id in range(4):
    fig.set_panel_label(fig_id)
fig.set_margins(right=0.83)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/dis_x_avg_gradient.png")
