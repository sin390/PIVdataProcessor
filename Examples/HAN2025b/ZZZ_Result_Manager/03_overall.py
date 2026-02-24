from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, cases_f, cases_w
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
from ZZZ_Result_Manager.A01_cases import cases, cases_select
from Z22_Autocorrelation.G01_autocorrelation import AutoCorrelation as AC
from Z10_Mean_Flow.G01_fitted_slope import FittedSlope as FS

result_id = 3

for case_id, case in enumerate(cases):
    rm = RM(case)
    case_select = cases_select[case_id]
    print(case, case_select)    

    ds = DS(case_select, 'gaussian',-1)

    urms = ds.result_json.get(0)['urms']
    vrms = ds.result_json.get(0)['vrms']
    ratio_urms_vrms = ds.result_json.get(0)['ratio_uv_rms']
    rm.result_table.set(result_id, urms=urms, vrms=vrms, ratio_urms_vrms=ratio_urms_vrms)

    ac = AC(case_select)
    Lx = ac.result_json.get(0)['L11_x']/1000
    Ly = ac.result_json.get(0)['L22_y']/1000
    ratio_Lx_Ly = Lx/Ly
    rm.result_table.set(result_id, Lx=Lx, Ly=Ly, ratio_Lx_Ly = ratio_Lx_Ly)

    lamda_x = ds.result_json.get(0)['lambda_x']
    lamda_y = ds.result_json.get(0)['lambda_y']
    rm.result_table.set(result_id, lamda_x=lamda_x, lamda_y=lamda_y)

    eta = ds.result_json.get(0)['eta']
    rm.result_table.set(result_id, eta=eta)
    Re_lamda_x = ds.result_json.get(0)['Re_lambda_x']
    Re_lamda_y = ds.result_json.get(0)['Re_lambda_y']
    rm.result_table.set(result_id, Re_lamda_x=Re_lamda_x, Re_lamda_y=Re_lamda_y)

    ratio_dudx_dvdy_rms = ds.result_json.get(0)['ratio_dudx_dvdy_rms']
    rm.result_table.set(result_id, ratio_dudx_dvdy_rms = ratio_dudx_dvdy_rms)

    fs = FS(case_select)
    A = fs.result_json.get(0)['S_avg']
    A_T_Lx = A*Lx/urms
    A_T_Ly = A*Ly/vrms
    rm.result_table.set(result_id, A_T_Lx=A_T_Lx, A_T_Ly=A_T_Ly)

    T_Lx = Lx/urms
    T_Ly = Ly/vrms
    rm.result_table.set(result_id, T_Lx=T_Lx, T_Ly=T_Ly)


    eps = ds.result_json.get(0)['DissipationRate']
    kinetic_viscosity = ds.result_json.get(0)['kinematic_viscosity']
    rm.result_table.set(result_id, eps=eps, kinetic_viscosity = kinetic_viscosity)
    C_eps_x = eps*Lx/(urms**3)
    C_eps_y = eps*Ly/(vrms**3)
    rm.result_table.set(result_id, C_eps_x=C_eps_x, C_eps_y=C_eps_y)

    relative_resolution = ds.result_json.get(0)['dx_over_eta']
    rm.result_table.set(result_id, relative_resolution=relative_resolution)