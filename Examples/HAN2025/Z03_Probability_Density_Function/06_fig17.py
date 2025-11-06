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
from pivdataprocessor.A01_toolbox import nanmean_filter2d, WriteHandler
from pivdataprocessor.A02_pltcfg import getplotpath

from G01_SkewFlat import SkewFlat as SF

cases = ['Case01XY_Z0_Ethanol', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
# -------------------------------------------------------------------------
# endregion

ws = WriteHandler(['x(mm)','S_u1','err_S_u1','-err_S_u1','F_u1','err_F_u1','-err_F_u1'])

filter_size = 8

for case_number in range(len(cases)):
    sf = SF(cases[case_number]+'_sub1')
    sf.load()
    sub1_S_u = sf.S_u
    sub1_F_u = sf.F_u
    sf = SF(cases[case_number]+'_sub2')
    sf.load()
    sub2_S_u = sf.S_u
    sub2_F_u = sf.F_u   
    S_u_for_uncertainty = (sub1_S_u - sub2_S_u)**2
    F_u_for_uncertainty = (sub1_F_u - sub2_F_u)**2
    S_u_uncertainty = np.sqrt(nanmean_filter2d(S_u_for_uncertainty, filter_size))
    F_u_uncertainty = np.sqrt(nanmean_filter2d(F_u_for_uncertainty, filter_size))    

    sf = SF(cases[case_number])
    sf.load()
    kernel_size = 8
    S_u = nanmean_filter2d(sf.S_u,kernel_size=kernel_size)
    F_u = nanmean_filter2d(sf.F_u,kernel_size=kernel_size)

    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    errorbar_x,_ = pBase.pos_mm_to_index_list([-25,0,25],[0,0,0])

    plot_x = pBase.X[0][left:right,central_y]
    plot_y1 = S_u[left:right,central_y]
    plot_err_y1 = S_u_uncertainty[left:right,central_y]/2
    plot_y2 = F_u[left:right,central_y]
    plot_err_y2 = F_u_uncertainty[left:right,central_y]/2
    ws.loaddata([plot_x,plot_y1,plot_err_y1,-plot_err_y1,\
                 plot_y2,plot_err_y2,-plot_err_y2])
    ws.write(fig_path + f'/{cases[case_number]}.txt')

