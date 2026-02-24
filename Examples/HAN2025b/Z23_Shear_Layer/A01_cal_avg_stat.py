''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.1         =
= Date:     2026/01/21  =
=========================
'''

import numpy as np
from pivdataprocessor.A01_toolbox import ProbabilityDensity as PD
from pivdataprocessor.A01_toolbox import float_precsion
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL
from Z23_Shear_Layer.T02_find_crossing import find_threshold_crossings_quadratic_minimal

from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, cases_f,cases_select, coeffs_to_eta
from ZZZ_Result_Manager.A01_cases import degs

degs += [None,]
for filter_id,coeff in enumerate(coeffs_to_eta):
    filter_id += 1
    log_id = 40 + filter_id
    for case_id, case in enumerate(cases_select):
        sl = SL(case, 'gaussian', filter_id)
        rm = RM(cases[case_id])
        Lf_in_mm = rm.result_table.get(log_id)['Lf_in_mm']
        eps = rm.result_table.get(3)['eps']
        eta = rm.result_table.get(3)['eta']
        nu = rm.result_table.get(3)['kinetic_viscosity']
        I_S_avg = sl.td.result_json.get(0)['avg_intensity_SH']      
        for deg in degs:
            sl.load_result(deg)
            X = sl.X_BRF[0]
            ic, jc = len(X[:,0])//2, len(X[0,:])//2
            norm_I_S = (sl.avg_Is_BRF-I_S_avg) / (sl.avg_Is_BRF[ic,jc]-I_S_avg)
            L_x = find_threshold_crossings_quadratic_minimal(sl.X_BRF[0,:,jc],norm_I_S[:,jc],ic=ic,thr=0.1)
            L_y = find_threshold_crossings_quadratic_minimal(sl.X_BRF[1,ic,:],norm_I_S[ic,:],ic=jc,thr=0.1)    
            AR = L_x/L_y
            norm_omega_s = sl.avg_omega_s_BRF/sl.avg_omega_s_BRF[ic,jc]
            delta_s_in_mm = find_threshold_crossings_quadratic_minimal(sl.X_BRF[1,ic,:],norm_omega_s[ic,:],ic=jc,thr=0.5)  
            jump_u = delta_s_in_mm / 1000 * sl.avg_omega_s_BRF[ic,jc]
            sl.result_json.set(0, Lf_in_mm=Lf_in_mm, eps = eps, eta = eta, nu = nu)
            sl.result_json.set(0, ic = ic , jc=jc)
            sl.result_json.set(0, Lf_in_mm=Lf_in_mm, AR=AR, delta_s_in_mm=delta_s_in_mm, jump_u=jump_u)
            sl.result_json.set(0, L_x=L_x, L_y=L_y)
            sl.result_json.set(0, I_S_avg=I_S_avg)




