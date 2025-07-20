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

from Z06_Autocorrelation.G01_autocorrelation import AutoCorrelation as AC

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
cases_sub1 = [case + '_sub1' for case in cases]
cases_sub2 = [case + '_sub2' for case in cases]

reporter = GT(if_save_in_S02 = False)
# reporter.rm_and_create_directory(reporter.result_path)
logfile = '/06_Integral_Length.txt'
reporter.GTreport('',logfile=logfile,ifinit=True)

for case_number in range(len(cases)):
    sub1 = AC(cases_sub1[case_number])
    sub1.load()
    S11_sub1 = sub1.Integral_length[0]

    
    sub2 = AC(cases_sub2[case_number])
    sub2.load()
    S11_sub2 = sub2.Integral_length[0]
    uncertainty = np.sqrt((S11_sub1 - S11_sub2)**2)

    reporter.GTreport(f'Case: {cases[case_number]}', logfile = logfile)
    reporter.GTreport(f'Uncertainty of L1 : {uncertainty:.4f}', logfile = logfile)

    S11_sub1 = sub1.Integral_length[1]
    S11_sub2 = sub2.Integral_length[1]
    uncertainty = np.sqrt((S11_sub1 - S11_sub2)**2)
    reporter.GTreport(f'Uncertainty of L2 : {uncertainty:.4f}', logfile = logfile)
