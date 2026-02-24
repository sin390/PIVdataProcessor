from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, cases_f, cases_w, coeffs_to_eta
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
from ZZZ_Result_Manager.A01_cases import cases, cases_select
from Z22_Autocorrelation.G01_autocorrelation import AutoCorrelation as AC
from Z10_Mean_Flow.G01_fitted_slope import FittedSlope as FS

result_id = 4


for case_id, case in enumerate(cases):
    rm = RM(case)
    case_select = cases_select[case_id]
    print(case, case_select)    

    ds = DS(case_select, 'gaussian',-1)
    eta = ds.result_json.get(0)['eta']
    for filter_id,coeff in enumerate(coeffs_to_eta): 
        Lf_in_mm = coeff*eta*1000
        filter_id += 1
        rm.result_table.set(result_id*10 + filter_id, Lf_in_mm=Lf_in_mm)
