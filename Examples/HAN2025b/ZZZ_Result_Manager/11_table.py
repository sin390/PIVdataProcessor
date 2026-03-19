import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases_select, cases_select_f, cases_select_w
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
from ZZZ_Result_Manager.A01_cases import cases, cases_select
from Z13_Reynolds_Stress.G01_reynolds_stress import ReynoldsStress as RS
from Z10_Mean_Flow.G01_fitted_slope import FittedSlope as FS

result_id = 11

for case_id, case in enumerate(cases_select):
    rm = RM(case)  

    rs = RS(cases_select_w[case_id])
    rs.load()
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    dx_w = pBase.X[0,1,1]-pBase.X[0,0,0]
    urms = np.sqrt(rs.uu)
    vrms = np.sqrt(rs.vv)
    avg_urms = np.nanmean(urms[left:right,bottom:up])
    avg_vrms = np.nanmean(vrms[left:right,bottom:up])
    rm.result_table.set(result_id, urms=avg_urms, vrms=avg_vrms)

    pBase.load_case(cases_select_w[case_id])
    avg_U = np.nanmean(pBase.avg_U[0][left:right,bottom:up])
    avg_V = np.nanmean(pBase.avg_U[1][left:right,bottom:up])
    rm.result_table.set(result_id, avg_U=avg_U, avg_V=avg_V)


    ds = DS(cases_select_f[case_id], 'gaussian',-1)
    eta = ds.result_json.get(0)['eta']
    viscosity = ds.result_json.get(0)['kinematic_viscosity']
    eps = ds.result_json.get(0)['DissipationRate']
    rm.result_table.set(result_id, eps=eps, kinetic_viscosity=viscosity,eta=eta)    

    dudx_rms = ds.result_json.get(0)['dudx_rms']
    lamda = avg_urms/dudx_rms
    Re_lamda =avg_urms*lamda/viscosity
    rm.result_table.set(result_id, lamda=lamda, Re_lamda=Re_lamda)   

    pBase.load_case(cases_select_f[case_id])
    dx_f = pBase.X[0,1,1]-pBase.X[0,0,0]
    rm.result_table.set(result_id, relative_resolution_f=2*dx_f/1000/eta)

    pBase.load_case(cases_select_w[case_id])
    dx_w = pBase.X[0,1,1]-pBase.X[0,0,0]
    rm.result_table.set(result_id, relative_resolution_w=2*dx_w/1000/eta)