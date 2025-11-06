''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/07  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.A01_toolbox import nanmean_filter2d, WriteHandler
from pivdataprocessor.A02_pltcfg import quickset, getplotpath


# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()

# -------------------------------------------------------------------------
# endregion

# -------------------------------------------------------------------------
# main
# region

cases = ['Case01XY_Z0_Ethanol', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
filter_range = 8

data_handler = WriteHandler(['y(mm)','v_avg(m/s)','err_v_avg(m/s)','-err_v_avg(m/s)'])
for case_number in range(len(cases)):
    pBase.load_case(cases[case_number]+'_sub1')
    avg_U_sub1 = pBase.avg_U.copy()
    pBase.load_case(cases[case_number]+'_sub2')
    avg_U_sub2 = pBase.avg_U.copy()
    for_uncertainty = (avg_U_sub1 - avg_U_sub2)**2
    U_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[0], filter_range))
    V_uncertainty = np.sqrt(nanmean_filter2d(for_uncertainty[1], filter_range))   
    pBase.load_case(cases[case_number])

    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]

    plotted_x = np.array([-30, -15, 0, 15, 30]) 
    plotted_y = np.array([-20, -10, 0, 10, 20])
    plotted_x, plotted_y = pBase.pos_mm_to_index_list(plotted_x,plotted_y)

    case_dir = fig_path+f'/{cases[case_number]}'
    pBase.rm_and_create_directory(case_dir)

    for k in range(len(plotted_x)):
        plot_x = pBase.X[1][plotted_x[k],bottom:up]
        plot_y = pBase.avg_U[1][plotted_x[k],bottom:up]
        yerr = V_uncertainty[plotted_x[k],bottom:up]/2
        data_handler.loaddata([plot_x,plot_y,yerr,-yerr])
        data_handler.write(case_dir+f'/x={round(pBase.X[0][plotted_x[k],0])}.txt')

