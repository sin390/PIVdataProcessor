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
from pivdataprocessor.A02_pltcfg import  getplotpath, myaxconfig, mycolors, generatefiglist
from pivdataprocessor.A01_toolbox import nanmean_filter2d, WriteHandler

cases = ['Case01XY_Z0_Ethanol', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)

# -------------------------------------------------------------------------
# endregion


ws = WriteHandler(['x(mm)','eta','err_eta','-err_eta'])

for case_number in range(len(cases)):
    rs = RS(cases[case_number]+'_sub1')
    rs.load()
    sub1_xi = rs.invariant_xi.copy()
    sub1_eta = rs.invariant_eta.copy()
    rs = RS(cases[case_number]+'_sub2')
    rs.load()
    sub2_xi = rs.invariant_xi.copy()
    sub2_eta = rs.invariant_eta.copy()
    xi_for_uncertainty = (sub1_xi - sub2_xi)**2
    eta_for_uncertainty = (sub1_eta - sub2_eta)**2
    xi_uncertainty = np.sqrt(nanmean_filter2d(xi_for_uncertainty, kernel_size=8))
    eta_uncertainty = np.sqrt(nanmean_filter2d(eta_for_uncertainty, kernel_size=8))

    rs = RS(cases[case_number])
    rs.load()

    invariant_xi = nanmean_filter2d(rs.invariant_xi,kernel_size=8)
    invariant_eta = nanmean_filter2d(rs.invariant_eta,kernel_size=8)
    # invariant_xi = rs.invariant_xi
    # invariant_eta = rs.invariant_eta  
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]

    plot_x = pBase.X[0][left:right,central_y]
    plot_y = invariant_eta[left:right,central_y]
    ws.loaddata([plot_x, plot_y, eta_uncertainty[left:right,central_y]/2, -eta_uncertainty[left:right,central_y]/2])
    ws.write(fig_path+f'/{cases[case_number]}.txt')
    


