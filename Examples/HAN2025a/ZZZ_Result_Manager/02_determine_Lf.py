import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from A01_cases import cases, case_labels, Lf_coeff


result_id = 2

for case_id, case in enumerate(cases[:-1]):
    rm = RM(case)
    L1 = rm.result_table.get(1)['L11']
    Lf = L1 * Lf_coeff * 1000
    dx = rm.result_table.get(1)['resolution']/2*1000
    eta = rm.result_table.get(1)['eta']*1000
    rm.result_table.set(result_id, Lfs=list(Lf))
    # print(f'{case_labels[case_id]}:{Lf/dx}')

