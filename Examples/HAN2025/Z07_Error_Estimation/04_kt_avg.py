''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/07/19  =
=========================
'''

import numpy as np
from Z02_Reynolds_Stress.G01_reynolds_stress import ReynoldsStress as RS
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT


cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
cases_sub1 = [case + '_sub1' for case in cases]
cases_sub2 = [case + '_sub2' for case in cases]

reporter = GT(if_save_in_S02 = False)
# reporter.rm_and_create_directory(reporter.result_path)
logfile = '/04_kt_avg.txt'
reporter.GTreport('',logfile=logfile,ifinit=True)

for case_number in range(len(cases)):
    sub1 = RS(cases_sub1[case_number])
    sub1.load()
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    S11_sub1 = sub1.k2[left:right, bottom:up].copy()
    
    sub2 = RS(cases_sub2[case_number])
    sub2.load()
    S11_sub2 = sub2.k2[left:right, bottom:up].copy()

    uncertainty = np.sqrt(np.average((S11_sub1 - S11_sub2)**2))

    reporter.GTreport(f'Case: {cases[case_number]}', logfile = logfile)
    reporter.GTreport(f'Uncertainty of kt_avg : {uncertainty:.4f}', logfile = logfile)