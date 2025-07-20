''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2024/06/25  =
=========================
'''

''' 
===================================================================
=====     Warning     ===     Warning     ===     Warning     =====
=.                                                               .=
>  Be certain that you are clear about what you are trying to do  <
===================================================================
'''

import os
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase

def clean_dirs(target_cases, ifBin, ifProcessed_data, ifPlots):
    if len(target_cases)==0:
        casebase = pBase.Paths.Working_path + pBase.Paths.Case_foldername
        target_cases = [
            name for name in os.listdir(casebase)
            if os.path.isdir(os.path.join(casebase, name))
        ]
    if ifBin == True:
        for case in target_cases:
            pBase.load_case(case)
            path = pBase.get_paths()['RawData'] + '/bin'
            pBase.rm_and_create_directory(path, ifcreate=False)
    if ifProcessed_data == True:
        for case in target_cases:
            pBase.load_case(case)
            path = pBase.get_paths()['ProcessedData']
            pBase.rm_and_create_directory(path, ifcreate=False)
    if ifPlots == True:
        path = pBase.Paths.Working_path + pBase.Paths.Plot_foldername
        pBase.rm_and_create_directory(path, ifcreate=False)

if __name__ == "__main__":
    target_cases = []  # empty means all
    clean_dirs(target_cases, ifBin = True, ifProcessed_data = False, ifPlots = False)