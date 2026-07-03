from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, case_labels, cases_appendix

result_id = 0
# for case_id, case in enumerate(cases):
for case_id, case in enumerate(cases_appendix):
    rm = RM(case, ifdelete=True)
    rm = RM(case)
    rm.result_table.set(result_id, case = case, case_label = case_labels[case_id])