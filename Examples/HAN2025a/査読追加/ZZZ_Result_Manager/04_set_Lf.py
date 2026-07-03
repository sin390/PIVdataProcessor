from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, coeffs_to_eta
from Z22_Autocorrelation.G01_autocorrelation import AutoCorrelation as AC

result_id = 4


for case_id, case in enumerate(cases): 

    rm = RM(case)
    eta = rm.result_table.get(1)['eta']
    for filter_id,coeff in enumerate(coeffs_to_eta): 
        Lf_in_mm = coeff*eta*1000
        filter_id += 1
        rm.result_table.set(result_id*10 + filter_id, Lf_in_mm=Lf_in_mm)
