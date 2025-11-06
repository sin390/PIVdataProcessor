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
from G01_fitted_slope import FittedSlope
from pivdataprocessor.A01_toolbox import nanmean_filter2d, WriteHandler
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01XZ_Y00', 'Case01XZ_Y20']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
# -------------------------------------------------------------------------
# endregion


xlables = [r'$x~(\mathrm{mm})$', r'$y~(\mathrm{mm})$']
ylables = [r'$-S_{11}~(\mathrm{s}^{-1})$', 
           r'$S_{22}~(\mathrm{s}^{-1})$']
figtitles = ['avg_slope']

wh_x_central = WriteHandler(['x(mm)','-A11(s-1)','err_-A11(s-1)'])
wh_y_central = WriteHandler(['z(mm)','A33(s-1)','err_A33(s-1)'])
filter_range = 8

for case_number in range(len(cases)):
    fs = FittedSlope(cases[case_number]+'_sub1')
    fs.load_fitted()
    S11_sub1 = fs.fit_avg_dUdX[0][0] * (-1000)
    S22_sub1 = fs.fit_avg_dUdX[1][1] * 1000
    
    fs = FittedSlope(cases[case_number]+'_sub2')
    fs.load_fitted()
    S11_sub2 = fs.fit_avg_dUdX[0][0] * (-1000)
    S22_sub2 = fs.fit_avg_dUdX[1][1] * 1000
    
    for_uncertainty = (S11_sub1 - S11_sub2)**2
    S11_err = np.sqrt(nanmean_filter2d(for_uncertainty, filter_range))  
    for_uncertainty = (S22_sub1 - S22_sub2)**2
    S22_err = np.sqrt(nanmean_filter2d(for_uncertainty, filter_range))
 
    fs = FittedSlope(cases[case_number])
    fs.load_fitted()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    
    fig_id = 0
    
    'S11(x,y=0)'
    plot_x = pBase.X[0][left:right,central_y]
    plot_y = fs.fit_avg_dUdX[0][0][left:right,central_y] * (-1000)
    yerr = S11_err[left:right,central_y]/2
    wh_x_central.loaddata([plot_x,plot_y,yerr])
    wh_x_central.write(fig_path+f'/{cases[case_number]}_-A11.txt')
    
    'S22(x=0,y)'
    plot_x = pBase.X[1][central_x,bottom:up]
    plot_y = fs.fit_avg_dUdX[1][1][central_x,bottom:up] * 1000
    yerr = S22_err[central_x,bottom:up]/2
    wh_y_central.loaddata([plot_x,plot_y,yerr])
    wh_y_central.write(fig_path+f'/{cases[case_number]}_A33.txt')


    plt.plot(plot_x, plot_y, 'o', markersize=4, label=f'{cases[case_number]}')
    plt.errorbar(plot_x, plot_y, yerr=yerr, fmt='o', markersize=4, label=f'{cases[case_number]}')
plt.xlabel(xlables[fig_id])
plt.ylabel(ylables[fig_id])
plt.title(figtitles[fig_id])
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
