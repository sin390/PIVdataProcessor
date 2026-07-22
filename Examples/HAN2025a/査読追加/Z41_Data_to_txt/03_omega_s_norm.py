''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/02/20  =
=========================
'''

import numpy as np
import matplotlib.pyplot as plt
from Q01_Plot.L01_piv_plot import PlotFigure 
from Q01_Plot.C00_cfg_for_cases import colors, linewidths
from Q01_Plot.L00_tools import rm_and_create_directory, quickset, getplotpath
from pivdataprocessor.A01_toolbox import WriteHandler as WH

import ZZZ_Result_Manager.A01_cases as A01
from Z32_Shear_Layer.G01_shear_layer import ShearLayer as SL
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

figformat = ".jpg"
fig_path = getplotpath()

wh = WH([r'$zeta2/LF$',r'$norm_omega_s$'])

filter = 'gaussian'
case_id = 0
for Lf_id, _ in enumerate(A01.coeffs_to_eta):
    sl = SL(A01.cases[case_id], filter, Lf_id+1)
    sl.load_result()
    Lf = sl.result_json.get(0)['Lf_in_mm']
    ic, jc = sl.result_json.get(0)['ic'],sl.result_json.get(0)['jc']
    I_s_avg = sl.td.result_json.get(0)['avg_intensity_SH']    
    mag = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]   
    x = sl.X_BRF[1,ic,:]/Lf
    y = mag[ic,:]
    wh.loaddata([x, y])
    wh.write(fig_path+f'/{A01.cases[case_id]}_{A01.coeffs_to_eta[Lf_id]}.txt')



