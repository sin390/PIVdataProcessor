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
logfile = '/05_Rii_avg.txt'
reporter.GTreport('',logfile=logfile,ifinit=True)

for case_number in range(len(cases)):
    sub1 = RS(cases_sub1[case_number])
    sub1.load()
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    R11_sub1 = sub1.uu[left:right, bottom:up].copy()
    R22_sub1 = sub1.vv[left:right, bottom:up].copy()
    
    sub2 = RS(cases_sub2[case_number])
    sub2.load()
    R11_sub2 = sub2.uu[left:right, bottom:up].copy()
    R22_sub2 = sub2.vv[left:right, bottom:up].copy()


    uncertainty_R11 = np.sqrt(np.average((R11_sub1 - R11_sub2)**2))
    uncertainty_R22 = np.sqrt(np.average((R22_sub1 - R22_sub2)**2))

    reporter.GTreport(f'Case: {cases[case_number]}', logfile = logfile)
    reporter.GTreport(f'Uncertainty of R11 : {uncertainty_R11:.4f}', logfile = logfile)
    reporter.GTreport(f'Uncertainty of R22 : {uncertainty_R22:.4f}', logfile = logfile)
    
    root = RS(cases[case_number])
    root.load()
    

    R11_root = np.average(root.uu[left:right, bottom:up])
    R22_root = np.average(root.vv[left:right, bottom:up])

    uncertainty_tmp = (uncertainty_R11/R11_root)**2 + (uncertainty_R22/R22_root)**2
    uncertainty_tmp = np.sqrt(uncertainty_tmp)
    uncertainty_ratio = R11_root/R22_root * uncertainty_tmp
    reporter.GTreport(f'R11/R22 : {R11_root/R22_root:.4f}', logfile = logfile)
    reporter.GTreport(f'Uncertainty of R11/R22 : {uncertainty_ratio:.4f}', logfile = logfile)
