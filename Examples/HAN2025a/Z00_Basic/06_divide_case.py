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
sub_case_extension = ['_sub1', '_sub2']

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

        
import shutil

def divide_case_by_odd_even_full(case: str):
    """
    将 case 按 run 的奇偶编号分成两个子 case
    偶数 run -> case_even
    奇数 run -> case_odd
    """
    # 1. 加载原 case
    pBase.load_case(case)
    root_raw_data_path = pBase.get_paths()['RawData'] + "/csv"
    root_case_info_file = pBase.get_paths()['CaseInfo']
    root_frames_in_runs = pBase.frame_numbers_in_runs.copy()  # 每个元素是该 run 的 frame 数量
    num_runs = len(root_frames_in_runs)

    # 2. 定义子 case 名称
    sub_case_names = [case + "_even", case + "_odd"]

    for i, sub_case in enumerate(sub_case_names):
        # 3. 创建子 case
        pBase.create_case(sub_case)
        shutil.copy(root_case_info_file, pBase.get_paths()['CaseInfo'])
        pBase.load_case(sub_case)

        # 4. 更新 YAML 中 case 名
        pBase.CaseInfo.CaseName = sub_case
        pBase.CaseInfo.to_yaml(pBase.get_paths()['CaseInfo'])

        # 5. 选择奇偶 run
        if i == 0:
            run_indices = [r for r in range(num_runs) if r % 2 == 0]  # 偶数 run 编号
        else:
            run_indices = [r for r in range(num_runs) if r % 2 == 1]  # 奇数 run 编号

        # 对应 frame 数量
        selected_frames = [root_frames_in_runs[r] for r in run_indices]
        pBase.frame_numbers_in_runs = selected_frames

        # 6. 复制 run 数据
        target_raw_data_path = pBase.get_paths()['RawData'] + "/csv"
        for sub_run_number, run_idx in enumerate(run_indices):
            src_run_path = root_raw_data_path + pBase.Paths.Run_path_rootword + f'{run_idx:02d}'
            dst_run_path = target_raw_data_path + pBase.Paths.Run_path_rootword + f'{sub_run_number:02d}'
            # 创建目标目录并复制
            pBase.rm_and_create_directory(dst_run_path, ifcreate=True)
            shutil.copytree(src_run_path, dst_run_path, dirs_exist_ok=True)

        # 7. 预处理数据
        pBase.preprocess_data(sub_case)


from ZZZ_Result_Manager.A01_cases import cases,cases_appendix
# for case in cases[:-1]:
for case in cases_appendix:
    divide_case_by_odd_even_full(case)