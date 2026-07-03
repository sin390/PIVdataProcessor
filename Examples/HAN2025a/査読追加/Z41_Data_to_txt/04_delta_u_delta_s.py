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
wh = WH(['coef_eta',r'$\delta_S/\eta$',r'$\Delta u/(\varepsilon \delta_s)^{1/3}$'])
case_id = 0
case = A01.cases[case_id]
print(case)


rm = RM(case) 
eta = rm.result_table.get(1)['eta']
viscosity = rm.result_table.get(1)['kinetic_viscosity']
eps = rm.result_table.get(1)['dissipationRate']
velocity_eta = (viscosity*eps)**(0.25)
coefs = []
x=[]
y=[]
for Lf_id, _ in enumerate(A01.coeffs_to_eta):
    sl = SL(A01.cases[case_id],'gaussian',Lf_id+1)
    sl.load_result(None)
    coefs.append(A01.coeffs_to_eta[Lf_id])
    jump_u = sl.result_json.get(0)['jump_u']
    delta_s_in_m = sl.result_json.get(0)['delta_s_in_mm']/1000
    x.append(delta_s_in_m/eta)
    tmp = (eps*delta_s_in_m)**(1/3)
    y.append(jump_u/tmp)

wh.loaddata([coefs, x, y])
wh.write(fig_path+f'/{case}.txt')