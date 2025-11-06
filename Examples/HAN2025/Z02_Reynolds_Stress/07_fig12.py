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
from G01_reynolds_stress import ReynoldsStress as RS
from pivdataprocessor.A01_toolbox import nanmean_filter2d, WriteHandler
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01XY_Z0_Ethanol', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
# -------------------------------------------------------------------------
# endregion


xlables = [r'$x~(\mathrm{mm})$', r'$x~(\mathrm{mm})$']
ylables = [r'$u_{1,\,\mathrm{rms}}~\mathrm{(m/s)}$', 
           r'$u_{2,\,\mathrm{rms}}~\mathrm{(m/s)}$']
figtitles = ['rms_u_v_central_line']
xlims = [(-60,60),(-60,60)]
xticks = [
    [-50,0,50],
    [-50,0,50]
]
ylims = [(0,45),(0,45)]
yticks = [
    [0, 10,20,30,40],
    [0, 10,20,30,40]
]
figformat = '.pdf'
filter_size = 8


ws = WriteHandler(['x(mm)','urms(m/s)','err_urms(m/s)','-err_urms(m/s)','vrms(m/s)','err_vrms(m/s)','-err_vrms(m/s)'])


for case_number in range(len(cases)):
    rs = RS(cases[case_number]+'_sub1')
    rs.load()
    sub1_urms = np.sqrt(rs.uu)
    sub1_vrms = np.sqrt(rs.vv)
    rs = RS(cases[case_number]+'_sub2')
    rs.load()
    sub2_urms = np.sqrt(rs.uu)
    sub2_vrms = np.sqrt(rs.vv)
    urms_for_uncertainty = (sub1_urms - sub2_urms)**2
    vrms_for_uncertainty = (sub1_vrms - sub2_vrms)**2
    urms_uncertainty = np.sqrt(nanmean_filter2d(urms_for_uncertainty, filter_size))
    vrms_uncertainty = np.sqrt(nanmean_filter2d(vrms_for_uncertainty, filter_size))

    rs = RS(cases[case_number])
    rs.load()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    errorbar_x,_ = pBase.pos_mm_to_index_list([-25,0,25],[0,0,0])
    

    'urms(x,y=0)'
    plot_x = pBase.X[0][left:right,central_y]
    urms = np.sqrt(rs.uu)
    urms = nanmean_filter2d(urms,filter_size)
    'vrms(x,y=0)'
    vrms = np.sqrt(rs.vv)
    vrms = nanmean_filter2d(vrms,filter_size)
    ws.loaddata([plot_x,\
                 urms[left:right,central_y],urms_uncertainty[left:right,central_y]/2,-urms_uncertainty[left:right,central_y]/2,\
                 vrms[left:right,central_y],vrms_uncertainty[left:right,central_y]/2,-vrms_uncertainty[left:right,central_y]/2])
    ws.write(fig_path+f'/{cases[case_number]}.txt')