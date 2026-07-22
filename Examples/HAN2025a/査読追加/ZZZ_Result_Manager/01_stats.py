import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, case_labels


Temp = np.array([299, 289, 288, 288, 288, 290])
press = np.array([102000,102000,102000,102000,102000,102000])
Rho = press/287.05/Temp


Upsilon = np.array([1.6e-5,])

urms1 = np.array([0.4724970901835236])
vrms1 = np.array([0.41538546670800836])

k2 = (urms1**2 + vrms1**2+ vrms1**2)/2
urms = np.sqrt(k2*2/3)

L11 = np.array([57.17])/1000
L22 = np.array([45.10])/1000
L = (L11+L22+L22)/3

A=1
dissipationRate = A *urms**3/L

TimeL = L/urms


Lambda = np.sqrt(10*(Upsilon)*k2/dissipationRate)
eta = Upsilon**(3/4)*dissipationRate**(-1/4)

Re_lambda = urms * Lambda /Upsilon


result_id = 1
for case_id, case in enumerate(cases):
    rm = RM(case)
    rm.result_table.set(result_id, urms = urms1[case_id], vrms = vrms1[case_id], kt = k2[case_id])
    rm.result_table.set(result_id, Re_lambda = Re_lambda[case_id], Lambda = Lambda[case_id])
    rm.result_table.set(result_id, L11 = L11[case_id], L22 = L22[case_id], ratio_L11_L22 = L11[case_id]/L22[case_id])
    rm.result_table.set(result_id, dissipationRate = dissipationRate[case_id], eta = eta[case_id], kinetic_viscosity = Upsilon[case_id])
    pBase.load_case(case)
    pBase.base_load_data_all(0,0)
    dx = (pBase.X[0][1,0]-pBase.X[0][0,0])/1000
    rm.result_table.set(result_id, resolution = 2*dx)
    rm.result_table.set(result_id, resolution_to_Lambda = 2*dx/Lambda[case_id])
    rm.result_table.set(result_id, resolution_to_eta = 2*dx/eta[case_id])
