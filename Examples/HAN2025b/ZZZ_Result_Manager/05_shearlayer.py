from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
from ZZZ_Result_Manager.A01_cases import cases, cases_select, coeffs_to_eta
from Z22_Autocorrelation.G01_autocorrelation import AutoCorrelation as AC
from Z23_Shear_Layer.G01_shear_layer import ShearLayer as SL

results_id = 5
for coeff_id,coeff in enumerate(coeffs_to_eta):
    coeff_id += 1
    result_id = results_id*10 + coeff_id
    for case_id, case in enumerate(cases):
        rm = RM(case)
        case_select = cases_select[case_id]
        
        sl = SL(case_select, 'gaussian', coeff_id)
        
        sl.load_result(None)
        Lf_in_mm = sl.result_json.get(0)['Lf_in_mm']

        eps = sl.result_json.get(0)['eps']
        eta = sl.result_json.get(0)['eta']
        nu = sl.result_json.get(0)['nu']
        L_x = sl.result_json.get(0)['L_x']
        L_y = sl.result_json.get(0)['L_y']
        AR = sl.result_json.get(0)['AR']
        delta_s_in_mm = sl.result_json.get(0)['delta_s_in_mm']
        jump_u = sl.result_json.get(0)['jump_u']
        I_S_avg = sl.result_json.get(0)['I_S_avg']

        # rm.result_table.set(result_id, Lf_in_mm=Lf_in_mm, eps=eps, eta=eta, L_x=L_x, L_y=L_y, AR=AR, delta_s_in_mm=delta_s_in_mm, jump_u=jump_u)

        tau_eta = eta**2 / nu
        rm.result_table.set(result_id, I_S_avg_tau = I_S_avg * tau_eta)
        ratio_Lx = L_x/Lf_in_mm
        ratio_Ly = L_y/Lf_in_mm
        rm.result_table.set(result_id, ratio_Lx = ratio_Lx, ratio_Ly = ratio_Ly)
        Ar = L_x/L_y
        rm.result_table.set(result_id, Ar = Ar)
        ratio_delta_s = delta_s_in_mm / Lf_in_mm
        rm.result_table.set(result_id, ratio_delta_s = ratio_delta_s)
        nom_u_jump = jump_u / (eps*delta_s_in_mm/1000)**(1/3)
        rm.result_table.set(result_id, nom_u_jump = nom_u_jump)

        N_sample = sl.result_json.get(0)['identified_LSL_number']
        rm.result_table.set(result_id, N_sample = N_sample)


