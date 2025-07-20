''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.A01_toolbox import float_precsion
from G02_POD_quarter import POD

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist


# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(33), cm_to_inch(19))
# -------------------------------------------------------------------------
# endregion

fig_number = 2
figs, axess = generatefiglist(fig_number, 2, 3, figsize_inch)

xlables = [r'$x$ (mm)']
ylables = [r'$y$ (mm)']
axtitles = ['Origin', 'Mode 1', 'Mode 2', 'Mode 1+2', 'Residuals', 'all moodes']

cases = ['Case03', 'Case06']
runs = [2,4]
frames = [10,50]
xlims = [(-50,50)]
ylims = [(-35,35)]
figformat = '.jpg'

for i in range(2):
    for j in range(3):
        case_number = i*3+j 
        for axes_number in range(len(axess)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax = ax)
            axconfig.title = axtitles[case_number]
            axconfig.xlable = xlables[0]
            axconfig.ylable = ylables[0]
            axconfig.ylim = ylims[0]
            axconfig.xlim = xlims[0]
            axconfig.apply()


global_min = 0
global_max = 60
first_quiv = None
step = 3 
scale_factor = 1000 

for case_id in range(fig_number):
    'origin'
    pBase.load_case(cases[case_id])
    pBase.base_load_data_all(runs[case_id], frames[case_id])
    central_x, central_y = pBase.CaseInfo.Central_Position_Flow
    left, right = pBase.CaseInfo.Effective_Range[0]
    bottom, up = pBase.CaseInfo.Effective_Range[1]

    'Origin'
    sub_fig_id = 0
    ax = axess[case_id][sub_fig_id]
    X = pBase.X[0][left:right, bottom:up]
    Y = pBase.X[1][left:right, bottom:up]
    U = pBase.fluc_U[0][left:right, bottom:up]
    V = pBase.fluc_U[1][left:right, bottom:up]
    magnitude = np.sqrt(U**2 + V**2)
    quiv = ax.quiver(X[::step, ::step], Y[::step, ::step],
                        U[::step, ::step], V[::step, ::step],
                        magnitude[::step, ::step],
                        cmap='viridis', clim=(global_min, global_max), scale=scale_factor)

    first_quiv = quiv

    pod = POD(cases[case_id])
    pod.PODload()
    X = pod.POD_X[0]
    Y = pod.POD_X[1]

    'Mode 1'
    sub_fig_id = 1
    ax = axess[case_id][sub_fig_id]
    pod_uv = pod.reconstruct(1)
    frame_id = pod.cal_assemble_frame_ID(runs[case_id],frames[case_id])
    plot_uv = pod_uv[:,:,:,frame_id]
    U = plot_uv[0]
    V = plot_uv[1]
    magnitude = np.sqrt(U**2 + V**2)
    quiv = ax.quiver(X[::step, ::step], Y[::step, ::step],
                        U[::step, ::step], V[::step, ::step],
                        magnitude[::step, ::step],
                        cmap='viridis', clim=(global_min, global_max), scale=scale_factor)

    'Mode 2'
    sub_fig_id = 2
    ax = axess[case_id][sub_fig_id]
    pod_uv = pod.reconstruct(2,1)
    frame_id = pod.cal_assemble_frame_ID(runs[case_id],frames[case_id])
    plot_uv = pod_uv[:,:,:,frame_id]
    U = plot_uv[0]
    V = plot_uv[1]
    magnitude = np.sqrt(U**2 + V**2)
    quiv = ax.quiver(X[::step, ::step], Y[::step, ::step],
                        U[::step, ::step], V[::step, ::step],
                        magnitude[::step, ::step],
                        cmap='viridis', clim=(global_min, global_max), scale=scale_factor)    

    'Mode 1+2'
    sub_fig_id = 3
    ax = axess[case_id][sub_fig_id]
    pod_uv = pod.reconstruct(2)
    frame_id = pod.cal_assemble_frame_ID(runs[case_id],frames[case_id])
    plot_uv = pod_uv[:,:,:,frame_id]
    U = plot_uv[0]
    V = plot_uv[1]
    magnitude = np.sqrt(U**2 + V**2)
    quiv = ax.quiver(X[::step, ::step], Y[::step, ::step],
                        U[::step, ::step], V[::step, ::step],
                        magnitude[::step, ::step],
                        cmap='viridis', clim=(global_min, global_max), scale=scale_factor)  
    
    'Remove 1+2'
    sub_fig_id = 4
    ax = axess[case_id][sub_fig_id]
    pod_uv = pod.removemodes(2)
    plot_uv = pod_uv[:,:,:,frame_id]
    U = plot_uv[0]
    V = plot_uv[1]
    magnitude = np.sqrt(U**2 + V**2)
    quiv = ax.quiver(X[::step, ::step], Y[::step, ::step],
                        U[::step, ::step], V[::step, ::step],
                        magnitude[::step, ::step],
                        cmap='viridis', clim=(global_min, global_max), scale=scale_factor)  
    'All modes'
    sub_fig_id = 5
    ax = axess[case_id][sub_fig_id]
    pod_uv = pod.reconstruct(-1)
    frame_id = pod.cal_assemble_frame_ID(runs[case_id],frames[case_id])
    plot_uv = pod_uv[:,:,:,frame_id]
    U = plot_uv[0]
    V = plot_uv[1]
    magnitude = np.sqrt(U**2 + V**2)
    quiv = ax.quiver(X[::step, ::step], Y[::step, ::step],
                        U[::step, ::step], V[::step, ::step],
                        magnitude[::step, ::step],
                        cmap='viridis', clim=(global_min, global_max), scale=scale_factor)  

for fig_id in range(fig_number):
    fig = figs[fig_id]
    fig.tight_layout()
    fig.savefig(fig_path + '/' + cases[fig_id] + f'_{runs[fig_id]}' + f'_{frames[fig_id]}' +  figformat, format='jpg')
plt.clf()