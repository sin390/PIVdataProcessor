import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, case_labels


Temp = np.array([299, 289, 288, 288, 288, 290])
press = np.array([102000,102000,102000,102000,102000,102000])
Rho = press/287.05/Temp

Mu0 = 1.724e-5
T0 = 273
S = 110.4
Mu = Mu0* ((Temp/T0)**1.5)*(T0+S)/(Temp+S)
Upsilon = Mu/Rho

urms1 = np.array([16.63, 18.36, 19.54, 28.11, 27.65, 29.53])
vrms1 = np.array([11.36, 12.32, 12.43, 17.84, 17.27, 17.88])

k2 = (urms1**2 + vrms1**2+ vrms1**2)/2
urms = np.sqrt(k2*2/3)

L11 = np.array([27.62, 30.33, 35.17, 28.87, 33.39, 34.86])/1000
L22 = np.array([22.27, 20.06, 19.65, 18.60, 17.80, 17.33])/1000
L = (L11+L22+L22)/3

A=1
dissipationRate = A *urms**3/L

TimeL = L/urms

S11_avg = np.array([665, 640, 600, 830, 700, 730])
S22_avg = np.array([335, 321, 303, 413, 349, 359])
S = (S11_avg + 2*S22_avg + 2*S22_avg)/3

Lambda = np.sqrt(10*(Mu/Rho)*k2/dissipationRate)
eta = (Mu/Rho)**(3/4)*dissipationRate**(-1/4)

Re_lambda = Rho* urms * Lambda /Mu

SL = S11_avg*TimeL


result_id = 1
for case_id, case in enumerate(cases[:-1]):
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

