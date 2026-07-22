import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from A01_cases import cases, case_labels, Lf_coeff
from A01_cases import cases_appendix

rm_case01 = RM('Case01')
table_case01 = rm_case01.result_table

result_id = 2
for case_id, case in enumerate(cases_appendix):
    rm = RM(case)
    L1 = rm_case01.result_table.get(1)['L11']
    Lf = L1 * Lf_coeff * 1000
    rm.result_table.set(result_id, Lfs=list(Lf))

result_id = 1
for case_id, case in enumerate(cases_appendix):
    rm = RM(case)
    rm.result_table.set(result_id, urms = table_case01.get(1)['urms'], vrms = table_case01.get(1)['vrms'], kt = table_case01.get(1)['kt'])
    rm.result_table.set(result_id, Re_lambda = table_case01.get(1)['Re_lambda'], Lambda = table_case01.get(1)['Lambda'])
    rm.result_table.set(result_id, L11 = table_case01.get(1)['L11'], L22 = table_case01.get(1)['L22'], ratio_L11_L22 = table_case01.get(1)['ratio_L11_L22'])
    rm.result_table.set(result_id, dissipationRate = table_case01.get(1)['dissipationRate'], eta = table_case01.get(1)['eta'], kinetic_viscosity = table_case01.get(1)['kinetic_viscosity'])
