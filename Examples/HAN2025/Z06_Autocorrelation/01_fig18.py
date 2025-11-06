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
from G01_autocorrelation import AutoCorrelation as AC

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist
from pivdataprocessor.A01_toolbox import WriteHandler, nanmean_filter1d

cases = ['Case01XY_Z0_Ethanol', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)

# -------------------------------------------------------------------------
# endregion

ws_fu_measured = WriteHandler(['r(mm)','f_u','f_u_uncertainty','-f_u_uncertainty'])
ws_fv_measured = WriteHandler(['r(mm)','f_y','f_y_uncertainty','-f_y_uncertainty'])
ws_fu_fitted = WriteHandler(['r(mm)','f_u'])
ws_fv_fitted = WriteHandler(['r(mm)','f_v'])

for case_number in range(len(cases)):
    ac = AC(cases[case_number]+'_sub1')
    ac.load()
    sub1_Fu = ac.autocorr_xdir[0].copy()
    sub1_Fv = ac.autocorr_ydir[1].copy()
    print(f"Processing {cases[case_number]}: sub1_Fu length = {len(sub1_Fu)}, sub1_Fv length = {len(sub1_Fv)}")
    ac = AC(cases[case_number]+'_sub2')
    ac.load()
    sub2_Fu = ac.autocorr_xdir[0].copy()
    sub2_Fv = ac.autocorr_ydir[1].copy()
    print(f"Processing {cases[case_number]}: sub2_Fu length = {len(sub2_Fu)}, sub2_Fv length = {len(sub2_Fv)}")
    F_u_len = min(len(sub1_Fu),len(sub2_Fu))
    F_v_len = min(len(sub1_Fv),len(sub2_Fv))  
    F_u_for_uncertainty = (sub1_Fu[:F_u_len] - sub2_Fu[:F_u_len])**2
    F_v_for_uncertainty = (sub1_Fv[:F_v_len] - sub2_Fv[:F_v_len])**2
    F_u_uncertainty = np.sqrt(nanmean_filter1d(F_u_for_uncertainty, 8))/2
    F_v_uncertainty = np.sqrt(nanmean_filter1d(F_v_for_uncertainty, 8))/2
    ac = AC(cases[case_number])
    ac.load()
    print(f"Processing {cases[case_number]}: ac.r_xdir length = {len(ac.r_xdir)}, ac.r_ydir length = {len(ac.r_ydir)}")
    target_len = len(ac.r_xdir)
    current_len = len(F_u_uncertainty)
    if current_len < target_len:
        pad_len = target_len - current_len
        F_u_uncertainty = np.concatenate([F_u_uncertainty, np.full(pad_len, np.nan)])
    target_len = len(ac.r_ydir)
    current_len = len(F_v_uncertainty)
    if current_len < target_len:
        pad_len = target_len - current_len
        F_v_uncertainty = np.concatenate([F_v_uncertainty, np.full(pad_len, np.nan)])

    pBase.rm_and_create_directory(fig_path+f'/{cases[case_number]}')
    ws_fu_measured.loaddata([ac.r_xdir,ac.autocorr_xdir[0],F_u_uncertainty,-F_u_uncertainty])
    ws_fu_measured.write(fig_path+f'/{cases[case_number]}/fu_measured_part.txt')
    ws_fu_fitted.loaddata([ac.fitting_part[1],ac.fitting_part[0]])
    ws_fu_fitted.write(fig_path+f'/{cases[case_number]}/fu_fitted_part.txt')
    ws_fv_measured.loaddata([ac.r_ydir,ac.autocorr_ydir[1],F_v_uncertainty,-F_v_uncertainty])
    ws_fv_measured.write(fig_path+f'/{cases[case_number]}/fv_measured_part.txt')
    ws_fv_fitted.loaddata([ac.fitting_part[3],ac.fitting_part[2]])
    ws_fv_fitted.write(fig_path+f'/{cases[case_number]}/fv_fitted_part.txt')