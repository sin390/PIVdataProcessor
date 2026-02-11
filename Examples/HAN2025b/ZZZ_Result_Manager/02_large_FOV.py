from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
import numpy as np
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, cases_f, cases_w
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
from Z22_Autocorrelation.G01_autocorrelation import AutoCorrelation as AC
from Z25_Skew_Flat.G01_SkewFlat import SkewFlat as SF1
from Z25_Skew_Flat.G02_SkewFlat_dudx import SkewFlat as SF2
from Z10_Mean_Flow.G01_fitted_slope import FittedSlope as FS

result_id = 2

for case_id, case in enumerate(cases):
    rm = RM(case)
    case_c = cases_w[case_id]
    print(case, case_c)
    ds = DS(case_c, 'gaussian', -1)

    fov_x = ds.vfh.X[0,-1,-1]-ds.vfh.X[0,0,0]
    fov_y = ds.vfh.X[1,-1,-1]-ds.vfh.X[1,0,0]
    rm.result_table.set(result_id, fov_x = fov_x, fov_y=fov_y)

    runs = len(ds.vfh.frames_in_runs)
    frames = sum(ds.vfh.frames_in_runs)
    rm.result_table.set(result_id, runs=runs, frames=frames)

    ac = AC(case_c)
    L11 = ac.result_json.get(0)['L11_x']/1000
    L22 = ac.result_json.get(0)['L22_y']/1000
    rm.result_table.set(result_id,L11 = L11, L22 = L22, ratio_L11_L22 = L11/L22)

    urms = ds.result_json.get(0)['urms']
    vrms = ds.result_json.get(0)['vrms']
    rm.result_table.set(result_id, urms = urms, vrms = vrms, ratio_urms_vrms = urms/vrms)

    ratio_dudx_dvdy_rms = ds.result_json.get(0)['ratio_dudx_dvdy_rms']
    rm.result_table.set(result_id, ratio_dudx_dvdy_rms = ratio_dudx_dvdy_rms)

    kinematic_viscosity = ds.result_json.get(0)['kinematic_viscosity']
    eta = ds.result_json.get(0)['eta']
    eps = ds.result_json.get(0)['DissipationRate']
    eps_nor = eps * L22 / vrms**3 
    rm.result_table.set(result_id, eps_nor = eps_nor)

    rm.result_table.set(result_id, Re_lambda_x = ds.result_json.get(0)['Re_lambda_x'])
    rm.result_table.set(result_id, Re_lambda_y = ds.result_json.get(0)['Re_lambda_y'])

    sf1 = SF1(case_c,'gaussian',-1)
    sf2 = SF2(case_c,'gaussian',-1)
    rm.result_table.set(result_id, F_u = sf1.result_json.get(0)['avg_F_u'])
    rm.result_table.set(result_id, F_v = sf1.result_json.get(0)['avg_F_v'])
    rm.result_table.set(result_id, F_dudx = sf2.result_json.get(0)['avg_F_dudx'])
    rm.result_table.set(result_id, F_dvdy = sf2.result_json.get(0)['avg_F_dvdy'])

    resolution = 2*ds.vfh.dX_in_m[0]
    resolution_eta = resolution/eta
    rm.result_table.set(result_id, resolution_eta = resolution_eta)

    fs = FS(case_c)
    rm.result_table.set(result_id, S_avg = fs.result_json.get(0)['S_avg'])
    rm.result_table.set(result_id, A11_nor = fs.result_json.get(0)['A11_nor'])
    rm.result_table.set(result_id, A22_nor = fs.result_json.get(0)['A22_nor'])
    rm.result_table.set(result_id, A12_nor = fs.result_json.get(0)['A12_nor'])
    rm.result_table.set(result_id, A21_nor = fs.result_json.get(0)['A21_nor'])
    rm.result_table.set(result_id, A11_A22 = fs.result_json.get(0)['A11_A22'])

