from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases,case_labels

result_id = 0
for case_id, case in enumerate(cases):
    rm = RM(case)
    rm.clean()
    rm.result_table.set(0, case = case, case_label = case_labels[case_id])