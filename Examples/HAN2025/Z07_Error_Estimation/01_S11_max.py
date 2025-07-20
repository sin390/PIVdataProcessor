''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/07/19  =
=========================
'''

import numpy as np
from Z01_VelocityDistribution.G01_fitted_slope import FittedSlope as FS
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
cases_sub1 = [case + '_sub1' for case in cases]
cases_sub2 = [case + '_sub2' for case in cases]

reporter = GT(if_save_in_S02 = False)
# reporter.rm_and_create_directory(reporter.result_path)
logfile = '/01_S11_max.txt'
reporter.GTreport('',logfile=logfile,ifinit=True)

for case_number in range(len(cases)):
    sub1 = FS(cases_sub1[case_number])
    sub1.load_fitted()
    left,right = sub1.effctive_range[0]
    bottom,up = sub1.effctive_range[1]
    S11_sub1 = sub1.fit_avg_dUdX[0,0,left:right, bottom:up].copy()
    S11_sub1 = np.abs(S11_sub1)*1000
    S11_sub1_max = np.nanmax(S11_sub1)
    
    sub2 = FS(cases_sub2[case_number])
    sub2.load_fitted()
    S11_sub2 = sub2.fit_avg_dUdX[0,0,left:right, bottom:up].copy()
    S11_sub2 = np.abs(S11_sub2)*1000
    S11_sub2_max = np.nanmax(S11_sub2)

    uncertainty = np.sqrt((S11_sub1_max - S11_sub2_max)**2)

    reporter.GTreport(f'Case: {cases[case_number]}', logfile = logfile)
    reporter.GTreport(f'Uncertainty of |S11|max : {uncertainty:.4f}', logfile = logfile)
