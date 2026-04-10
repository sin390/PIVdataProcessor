''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.1         =
= Date:     2025/12/01  =
=========================
'''

import numpy as np
import pywt

from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from pivdataprocessor.A01_toolbox import float_precsion
from Z01_Filtered_Velocity_Field.G01_filter_manager import FilterManager as FM
from pivdataprocessor.A01_toolbox import scalar_field_5points_stencil

wavelet_length = {'db3':6, 'db4':8}

class WaveletTransform(GT):
    def __init__(self, case_name='unnamed'):
        self.case_name = case_name
        super().__init__(case_name)
        self.param_table_wt = PT(self.result_path +"/" + case_name + ".json")
        self.dx_in_m = np.zeros((2,), dtype=float_precsion)


    def init(self, wavelet = 'db3', max_level = 4, mark_margin = 2):
        self.param_table_wt.data = {}
        self.param_table_wt.save()
        self.param_table_wt.set(0, wavelet = wavelet, max_level = max_level)
        self.fm = FM(self.case_name)
        self.fm.load_X()
        Nx = self.fm.filter_param_table.get(0)['Nx']
        Ny = self.fm.filter_param_table.get(0)['Ny']

        L_unit = 2.0 ** max_level
        Nx_wt = int((Nx // L_unit) * L_unit)
        Ny_wt = int((Ny // L_unit) * L_unit)
        self.param_table_wt.set(0, Nx_wt = Nx_wt, Ny_wt = Ny_wt)

        crop_x = Nx - Nx_wt
        crop_y = Ny - Ny_wt
        left_x  = crop_x // 2
        right_x = Nx - (crop_x - left_x)
        bottom_y = crop_y // 2
        top_y = Ny - (crop_y - bottom_y)
        self.param_table_wt.set(0, range_in_original_X = [[left_x,right_x],[bottom_y,top_y]])
        self.param_table_wt.set(0, effective_range = [[mark_margin,Nx_wt-mark_margin],[mark_margin,Ny_wt-mark_margin]])
        self.param_table_wt.set(0, frames_in_runs = self.fm.filter_param_table.get(0)['frames_in_runs'])
        central_pos_grid = self.fm.filter_param_table.get(0)['central_pos_grid']
        central_pos_grid_wt = [central_pos_grid[0] - left_x, central_pos_grid[0] - bottom_y]
        self.param_table_wt.set(0, central_pos_grid = central_pos_grid_wt)

        self.X = np.zeros((2,Nx_wt,Ny_wt), dtype = float_precsion)
        self.u = np.zeros((2,Nx_wt,Ny_wt), dtype = float_precsion)
        self.dudx = np.zeros((2,2,Nx_wt,Ny_wt), dtype = float_precsion)
        self.X = self.fm.X[:,left_x:right_x,bottom_y:top_y].copy()
        self.save_nparray_to_bin(self.X, self.result_path+'/X_wt.bin')
        self.load_X()

    def load_X(self):
        Nx_wt = self.param_table_wt.get(0)['Nx_wt']
        Ny_wt = self.param_table_wt.get(0)['Ny_wt']
        self.X = np.zeros((2,Nx_wt,Ny_wt))
        self.X = self.load_nparray_from_bin(self.X, self.result_path+'/X_wt.bin')
        self.u = np.zeros((2,Nx_wt,Ny_wt))
        self.dudx = np.zeros((2,2,Nx_wt,Ny_wt))
        for i in range(2):
            self.dx_in_m[i] = (self.X[i,1,1] - self.X[i,0,0])/1000        


    def calculate_all_and_save(self):
        wavelet = self.param_table_wt.get(0)['wavelet']
        max_level = self.param_table_wt.get(0)['max_level']
        def extract_swt_band(coeffs, j_target):
            new_coeffs = []
            j_in_pywt = max_level-j_target
            for j in range(len(coeffs)):
                (cA, (cH, cV, cD)) = coeffs[j]
                
                if j == j_in_pywt:
                    new_cA = np.zeros_like(cA)
                    new_cH = cH
                    new_cV = cV
                    new_cD = cD
                else:
                    new_cA = np.zeros_like(cA)
                    new_cH = np.zeros_like(cH)
                    new_cV = np.zeros_like(cV)
                    new_cD = np.zeros_like(cD)

                new_coeffs.append((new_cA, (new_cH, new_cV, new_cD)))
            return new_coeffs

        self.empty_directory(self.result_path)
        frames_in_runs = self.fm.filter_param_table.get(0)['frames_in_runs']
        left, right = self.param_table_wt.get(0)['range_in_original_X'][0]
        bottom, up  = self.param_table_wt.get(0)['range_in_original_X'][1]
        for run_id in range(len(frames_in_runs)):
            for frame_id in range(frames_in_runs[run_id]):
                self.fm.load_field(0,run_id,frame_id, if_cal_du=False)
                coeffs_u = pywt.swt2(self.fm.u[0][left:right, bottom:up], wavelet, level=max_level)
                coeffs_v = pywt.swt2(self.fm.u[1][left:right, bottom:up], wavelet, level=max_level)
                for level_id in range(1,max_level+1):
                    coeffs_u_j = extract_swt_band(coeffs_u, level_id)
                    coeffs_v_j = extract_swt_band(coeffs_v, level_id)
                    self.u[0] = pywt.iswt2(coeffs_u_j, wavelet)
                    self.u[1] = pywt.iswt2(coeffs_v_j, wavelet)
                    self.save_field(level_id,run_id,frame_id)
        Nx_wt = self.param_table_wt.get(0)['Nx_wt']
        Ny_wt = self.param_table_wt.get(0)['Ny_wt']
        e_left,e_right = self.param_table_wt.get(0)['effective_range'][0]
        e_bottom,e_up = self.param_table_wt.get(0)['effective_range'][1]
        for level_id in range(1,max_level+1):
            margin = (wavelet_length[wavelet]-1) * 2 ** (level_id-1)
            e_left = max(e_left,margin)
            e_bottom = max(e_bottom,margin)
            e_right = min(e_right,Nx_wt-margin)
            e_up = min(e_up,Ny_wt-margin)
            self.param_table_wt.set(level_id, effective_range = [[e_left,e_right],[e_bottom,e_up]])
            self.param_table_wt.set(level_id, scale_in_grid = 2 ** level_id)
            


    def save_field(self, level_id , run_id, frame_id):
        path = self.path_rule(level_id, run_id, frame_id)
        self.make_sure_directory(path)
        self.save_nparray_to_bin(self.u, path+'/u_wt.bin')

    def load_field(self, lever_id , run_id, frame_id, if_cal_du = True):
        path = self.path_rule(lever_id, run_id, frame_id)
        self.u = self.load_nparray_from_bin(self.u, path+'/u_wt.bin')
        if if_cal_du == True:
            for i in range(2):
                self.dudx[i] = scalar_field_5points_stencil(self.u[i], self.dx_in_m[0], self.dx_in_m[1])

    def path_rule(self, level_id, run_id = None, frame_id = None) -> str:
        result = self.result_path + f'/{level_id}'
        if frame_id != None:
            result += f'/Run{run_id}'
            if frame_id !=None:
                result += f'/Frame{frame_id}'
        return result

if __name__ == "__main__":
    cases = ['Case03']
    for case in cases:
        wt = WaveletTransform(case)
        wt.init(wavelet='db3', max_level=4)
        wt.calculate_all_and_save()

# if __name__ == "__main__":
#     cases = ['Mori_465']
#     for case in cases:
#         wt = WaveletTransform(case)
#         wt.init(wavelet='db3', max_level=4)
#         wt.calculate_all_and_save()
