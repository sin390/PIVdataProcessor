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

filter_size = 3
comment = ['Note:',
           '    <uv>/urmsvrms(1) - filter first, then calculate the ratio',
         '    <uv>/urmsvrms(2) - calculate the ratio first, then filter']
ws = WriteHandler(['x(mm)','<uv>/urmsvrms(1)','<uv>/urmsvrms(2)'],comment=comment)

fig, ax = plt.subplots(figsize=(8,6))
for case_number in range(len(cases)):
    rs = RS(cases[case_number])
    rs.load()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    

    'urms(x,y=0)'
    plot_x = pBase.X[0][left:right,central_y]
    urms = np.sqrt(rs.uu)
    vrms = np.sqrt(rs.vv)
    uv = rs.uv

    ratio1 = nanmean_filter2d(uv,filter_size) / (nanmean_filter2d(urms,filter_size) * nanmean_filter2d(vrms,filter_size))
    ratio2 = nanmean_filter2d(uv / (urms * vrms), filter_size)
    ws.loaddata([plot_x,\
                 ratio1[left:right,central_y],ratio2[left:right,central_y]])
    ws.write(fig_path+f'/{cases[case_number]}.txt')
    'Plotting'
    ax.plot(plot_x, ratio1[left:right,central_y], label='<uv>/urmsvrms (filter first)', color=mycolors[0])
    ax.plot(plot_x, ratio2[left:right,central_y], label='<uv>/urmsvrms (calc first)', color=mycolors[1], linestyle='--')
plt.show()