''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/07/18  =
=========================
'''

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L01_base import CaseInfoClass as CI
import copy, shutil, os

divide_number = 2
sub_case_extension = [f'_sub{i+1}' for i in range(divide_number)]

def divide_case(case:str):
    pBase.load_case(case)
    root_raw_data_path = pBase.get_paths()['RawData'] + "/bin"
    root_case_info_file = pBase.get_paths()['CaseInfo']
    root_frames_in_runs = pBase.frame_numbers_in_runs.copy()
    d_run = len(root_frames_in_runs) // divide_number
    for i in range(divide_number):
        pBase.create_case(case + sub_case_extension[i])
        shutil.copy(root_case_info_file, pBase.get_paths()['CaseInfo'])
        pBase.load_case(case + sub_case_extension[i])
        pBase.CaseInfo.CaseName = case + sub_case_extension[i]
        pBase.CaseInfo.to_yaml(pBase.get_paths()['CaseInfo'])
        
        if i == divide_number - 1:
            run_numbers = len(root_frames_in_runs) - i * d_run
            run_start = i * d_run
        else:
            run_numbers = d_run
            run_start = i * d_run
        
        pBase.frame_numbers_in_runs = root_frames_in_runs[run_start:run_start+run_numbers]
        target_raw_data_path = pBase.get_paths()['RawData'] + "/bin"
        for sub_run_number in range(run_numbers):
            src_run_path = root_raw_data_path + pBase.Paths.Run_path_rootword + f'{run_start+sub_run_number}'
            dst_run_path = target_raw_data_path + pBase.Paths.Run_path_rootword + f'{sub_run_number}'
            pBase.rm_and_create_directory(dst_run_path,ifcreate = False)
            shutil.copytree(src_run_path,dst_run_path)
        pBase.preprocess_data(case + sub_case_extension[i], ifbin = True)

def delete_sub_case(case:str):
    for i in range(divide_number):
        pBase.load_case(case)
        root_path = pBase.get_paths()['CurrentCase'] + sub_case_extension[i]
        pBase.rm_and_create_directory(root_path, ifcreate=False)


cases = ['Case01','Case02','Case03','Case04','Case05','Case06']
cases = ['Mori465']
for case in cases:
    delete_sub_case(case)
    # divide_case(case)
