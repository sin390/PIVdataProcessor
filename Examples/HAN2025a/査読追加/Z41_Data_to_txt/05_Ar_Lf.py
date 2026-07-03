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

figformat = ".png"
fig_path = getplotpath()


wh = WH(['coef_eta',r'$L_f/\eta$',r'$A_R$'])


fig_id = 0
case_id = 0
coeffs = []
x=[]
y=[]
for Lf_id, _ in enumerate(A01.coeffs_to_eta):
    sl = SL(A01.cases[case_id],'gaussian',Lf_id+1)
    sl.load_result(None)
    coeffs.append(A01.coeffs_to_eta[Lf_id])
    eta = sl.result_json.get(0)['eta']
    Lf = sl.result_json.get(0)['Lf_in_mm']/1000
    Ar = sl.result_json.get(0)['AR']
    x.append(Lf/eta)
    y.append(Ar)

wh.loaddata([coeffs, x, y])
wh.write(fig_path+f'/{A01.cases[case_id]}.txt')




