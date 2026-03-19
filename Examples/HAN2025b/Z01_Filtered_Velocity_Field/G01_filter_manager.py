''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.1         =
= Date:     2025/12/01  =
=========================
'''
import numpy as np
from scipy.ndimage import gaussian_filter
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import scalar_field_5points_stencil
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as WSC


class FilterManager(GT):
    def __init__(self, case_name:str = 'unnamed'):
        super().__init__(case_name)
        self.case_name = case_name
        self.filter_param_table = PT(self.result_path +"/" + case_name + ".json")
        self.dx_in_m = np.zeros((2,), dtype=float_precsion)



    def init_filter_param_table(self, sigma_in_dx = 0.5, truncate = 4):        
        init_id = 0
        self.filter_param_table.data = {}
        self.filter_param_table.save()
        pBase.load_case(self.case_name)
        self.filter_param_table.set(uid = init_id, Nx = pBase.CaseInfo.Nx, Ny = pBase.CaseInfo.Ny)
        self.filter_param_table.set(uid = init_id, dx_in_mm = pBase.dX[0], dy_im_mm = pBase.dX[1])
        self.filter_param_table.set(uid = init_id, central_pos_grid = pBase.CaseInfo.Central_Position_Grid)
        self.filter_param_table.set(uid = init_id, effective_range = pBase.CaseInfo.Effective_Range) 
        self.filter_param_table.set(uid = init_id, frames_in_runs = pBase.frame_numbers_in_runs)
        self.filter_param_table.set(uid = init_id, pre_filter_in_dx = sigma_in_dx)
        self.filter_param_table.set(uid = init_id, scale_in_grid = sigma_in_dx*np.sqrt(12))

        self.X = pBase.X
        self.save_nparray_to_bin(self.X, self.result_path+'/X.bin')
        self.load_X()

        self.rm_and_create_directory(self.path_rule(init_id))
        tmp_U = np.zeros(shape=(2, pBase.CaseInfo.Nx, pBase.CaseInfo.Ny), dtype=float_precsion)
        avg_U_cal = WSC(tmp_U.shape)
        for run_id in range(len(pBase.frame_numbers_in_runs)):
            for frame_id in range(pBase.frame_numbers_in_runs[run_id]):
                pBase.base_load_data_all(run_id,frame_id)
                for i in (0,1):
                    tmp_U[i] = self.nan_gaussian_filter(pBase.U[i],(sigma_in_dx, sigma_in_dx), truncate = truncate)
                    avg_U_cal.add_point(tmp_U)
        avg_U = avg_U_cal.get_mean()
    
        for run_id in range(len(pBase.frame_numbers_in_runs)):
            for frame_id in range(pBase.frame_numbers_in_runs[run_id]):
                pBase.base_load_data_all(run_id,frame_id)
                for i in (0,1):
                    tmp_U[i] = self.nan_gaussian_filter(pBase.U[i],(sigma_in_dx, sigma_in_dx), truncate = truncate)
                self.u = tmp_U - avg_U
                self.save_field(0,run_id,frame_id)

        origin_id = -1
        self.filter_param_table.set(uid = origin_id, effective_range = pBase.CaseInfo.Effective_Range)
        self.filter_param_table.set(uid = origin_id, scale_in_grid = 0)

        self.rm_and_create_directory(self.path_rule(origin_id))
        for run_id in range(len(pBase.frame_numbers_in_runs)):
            for frame_id in range(pBase.frame_numbers_in_runs[run_id]):
                pBase.base_load_data_all(run_id,frame_id)
                self.u = pBase.fluc_U
                self.save_field(origin_id,run_id,frame_id)
          
    def add_filter_param(self, id, Lf_in_mm:list, truncate_coef_in_Lf:float):
        self.filter_param_table.set(id, Lf_in_mm = Lf_in_mm, truncate_coef_in_Lf = truncate_coef_in_Lf)
        dx_in_mm = np.array(self.dx_in_m)*1000
        Lf_in_mm = np.array(Lf_in_mm)
  
        assert len(dx_in_mm) == len(Lf_in_mm)
        sigma_in_grid = Lf_in_mm / np.sqrt(12.0) / dx_in_mm
        truncate_in_gird = np.ceil(truncate_coef_in_Lf * Lf_in_mm / dx_in_mm)
        self.filter_param_table.set(id, sigma_in_grid=[sigma_in_grid[0],sigma_in_grid[1]], 
                                    truncate_in_gird=[truncate_in_gird[0],truncate_in_gird[1]])
        
        Effective_Range_base = self.filter_param_table.get(0)['effective_range']
        Nx = self.filter_param_table.get(0)['Nx']
        Ny = self.filter_param_table.get(0)['Ny']
        range_x_left = int(max(truncate_in_gird[0], Effective_Range_base[0][0]))
        range_x_right = int(min(Nx- truncate_in_gird[0], Effective_Range_base[0][1]))
        range_y_bottom = int(max(truncate_in_gird[1], Effective_Range_base[1][0]))
        range_y_top = int(min(Ny- truncate_in_gird[1], Effective_Range_base[1][1]))        
        effective_Range = [[range_x_left,range_x_right],[range_y_bottom,range_y_top]]   
        self.filter_param_table.set(id, effective_range = effective_Range)
        self.filter_param_table.set(id, scale_in_grid = Lf_in_mm[0]/dx_in_mm[0])

    def calculate_frame(self, filter_id, run_id, frame_id, if_cal_du = True, base = -1):
        base_path = self.path_rule(base, run_id, frame_id)
        base_u = self.load_nparray_from_bin(self.u, base_path+'/u.bin')
        sigma_in_grid = self.filter_param_table.get(filter_id)['sigma_in_grid']
        coef_truncate = self.filter_param_table.get(filter_id)['truncate_coef_in_Lf']
        for i in range(2):
            self.u[i] = self.nan_gaussian_filter(base_u[i], sigma=(sigma_in_grid[0], sigma_in_grid[1]), 
                                                 truncate = coef_truncate * np.sqrt(12.0))
        if if_cal_du == True:
            for i in range(2):
                self.dudx[i] = scalar_field_5points_stencil(self.u[i], self.dx_in_m[0], self.dx_in_m[1])
    
    def calculate_all_and_save(self, base = -1):
        ids = self.filter_param_table.ids()
        frames_in_runs = self.filter_param_table.get(0)['frames_in_runs']
        self.empty_directory(self.result_path,('0','-1'))

        for filter_id in ids:
            if filter_id in (0,-1):
                continue
            sigma_in_grid = self.filter_param_table.get(filter_id)['sigma_in_grid']
            coef_truncate = self.filter_param_table.get(filter_id)['truncate_coef_in_Lf']
            for run_id in range(len(frames_in_runs)):
                for frame_id in range(frames_in_runs[run_id]):
                    base_path = self.path_rule(base, run_id, frame_id)
                    base_u = self.load_nparray_from_bin(self.u, base_path+'/u.bin')
                    for i in range(2):
                        self.u[i] = self.nan_gaussian_filter(base_u[i], sigma=(sigma_in_grid[0], sigma_in_grid[1]), 
                                                            truncate = coef_truncate * np.sqrt(12.0))
                    self.save_field(filter_id, run_id, frame_id)

    
    def load_X(self):
        Nx = self.filter_param_table.get(0)['Nx']
        Ny = self.filter_param_table.get(0)['Ny']
        self.X = np.zeros((2,Nx,Ny))
        self.X = self.load_nparray_from_bin(self.X, self.result_path+'/X.bin')
        self.u = np.zeros((2,Nx,Ny))
        self.dudx = np.zeros((2,2,Nx,Ny))
        for i in range(2):
            self.dx_in_m[i] = (self.X[i,1,1] - self.X[i,0,0])/1000

    def save_field(self, filter_id , run_id, frame_id):
        path = self.path_rule(filter_id, run_id, frame_id)
        self.make_sure_directory(path)
        self.save_nparray_to_bin(self.u, path+'/u.bin')

    def load_field(self, filter_id , run_id, frame_id, if_cal_du = True):
        path = self.path_rule(filter_id, run_id, frame_id)
        self.u = self.load_nparray_from_bin(self.u, path+'/u.bin')
        if if_cal_du == True:
            for i in range(2):
                self.dudx[i] = scalar_field_5points_stencil(self.u[i], self.dx_in_m[0], self.dx_in_m[1])
    @staticmethod
    def nan_gaussian_filter(arr, sigma, truncate=4.0):
        nan_mask = np.isnan(arr)
        arr_copy = arr.copy()
        arr_copy[nan_mask] = 0.0

        weights = (~nan_mask).astype(float)
        smooth_data = gaussian_filter(arr_copy, sigma=sigma, truncate=truncate)
        smooth_weights = gaussian_filter(weights, sigma=sigma, truncate=truncate)

        with np.errstate(invalid='ignore', divide='ignore'):
            result = smooth_data / smooth_weights
            result[smooth_weights == 0] = np.nan
        return result
    
    def path_rule(self, filter_id, run_id = None, frame_id = None) -> str:
        result = self.result_path + f'/{filter_id}'
        if frame_id != None:
            result += f'/Run{run_id}'
            if frame_id !=None:
                result += f'/Frame{frame_id}'
        return result

# from ZZZ_Result_Manager.A01_cases import cases_f,cases_w
# if __name__ == "__main__":
#     from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
#     for case_id, case in enumerate(cases_f+cases_w):
#         fm = FilterManager(case)
#         fm.init_filter_param_table(sigma_in_dx=0.5)

from ZZZ_Result_Manager.A01_cases import cases_select_w,cases_select_f, cases_select, coeffs_to_eta
if __name__ == "__main__":
    from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
    for case_id, case in enumerate(cases_select):
        fm = FilterManager(cases_select_w[case_id])
        fm.init_filter_param_table(sigma_in_dx=0.5)

        ds = DS(cases_select_f[case_id], 'gaussian',-1)
        eta = ds.result_json.get(0)['eta']*1000
        for coeff_id, coeff in enumerate(coeffs_to_eta):
            coeff_id += 1
            fm.add_filter_param(coeff_id,[coeff*eta,coeff*eta],1)
        fm.calculate_all_and_save()