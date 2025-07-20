''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/07/08  =
=========================
'''

import numpy as np
import os
from dataclasses import dataclass
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L01_base import GeneralDataHandler as GDH
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import scalar_field_5points_stencil
from scipy.ndimage import gaussian_filter
from Z21_Filtered_Velocity_Field.G00_filter_option import FilterOptionInfo as FOI

@dataclass
class FilteredVelocityFieldInfo(GDH):
    Lf_in_mm: float = 0.5
    sigma_in_grid: tuple[float,float] = (0.5, 0.5)
    truncate_coef: float = 1.0
    truncate_range_in_grid: tuple[float,float] = (2.0, 2.0)
    Effective_Range: tuple[tuple[int, int], tuple[int, int]] = ((0, 0), (0, 0))

class FilteredVelocityField(pTS):
    def __init__(self, casename, filter_option = None, ifinit = False, ifcleandir = False):
        '''
        filter_option:s
            (Lf_in_mm, truncate_coef) for Gaussian filter
        '''
        super().__init__(casename)
        if ifcleandir == True:
            self.rm_and_create_directory(self.result_path)
        self.info = FilteredVelocityFieldInfo()
        if filter_option is not None:
            self.result_path = self.result_path + f'/_{int(filter_option[0]*1000)}_{int(filter_option[1]*1000)}'
            self.info.Lf_in_mm = float(filter_option[0])

            sigma_x = float(filter_option[0] / np.sqrt(12.0) / pBase.dX[0])
            sigma_y = float(filter_option[0] / np.sqrt(12.0) / pBase.dX[1])
            self.info.sigma_in_grid = (sigma_x, sigma_y)

            self.info.truncate_coef = float(filter_option[1])
            truncate_x = float(filter_option[1] * sigma_x)
            truncate_y = float(filter_option[1] * sigma_y)
            self.info.truncate_range_in_grid = (truncate_x, truncate_y)
 
            import math
            range_x_left = max(math.ceil(truncate_x), pBase.CaseInfo.Effective_Range[0][0])
            range_x_right = min(pBase.CaseInfo.Nx - math.ceil(truncate_x), pBase.CaseInfo.Effective_Range[0][1])
            range_y_bottom = max(math.ceil(truncate_y), pBase.CaseInfo.Effective_Range[1][0])
            range_y_top = min(pBase.CaseInfo.Ny - math.ceil(truncate_y), pBase.CaseInfo.Effective_Range[1][1])
            self.info.Effective_Range = ((range_x_left, range_x_right), (range_y_bottom, range_y_top))

        self.filtered_fluc_U = self.get_a_container(1)
        self.filtered_fluc_dUdX = self.get_a_container(2)
        if ifinit == True:
            self.info.to_yaml(self.result_path +'/info.yaml')
            pBase.rm_and_create_directory(self.result_path)
        self.info = self.info.from_yaml(self.result_path +'/info.yaml')        


    def calculate(self):
        dx_in_m = self.dX/1000
        for run_ID in range(len(pBase.frame_numbers_in_runs)):
            save_run_path = self.result_path + f'/Run_{run_ID}'
            os.mkdir(save_run_path)
            for frame_ID in range(pBase.frame_numbers_in_runs[run_ID]):
                save_frame_path = save_run_path + f'/Frame_{frame_ID}'
                os.mkdir(save_frame_path)
                pBase.base_load_data_all(run_ID, frame_ID)
                for i in range(2):
                    self.filtered_fluc_U[i] = gaussian_filter(pBase.fluc_U[i], sigma=self.info.sigma_in_grid, truncate=self.info.truncate_coef)
                    self.filtered_fluc_dUdX[i] = scalar_field_5points_stencil(pBase.fluc_U[i], dx_in_m[0], dx_in_m[1])
                self.save_nparray_to_bin(self.filtered_fluc_U, save_frame_path + f'/filtered_fluc_U.bin')
                self.save_nparray_to_bin(self.filtered_fluc_dUdX, save_frame_path + f'/filtered_fluc_dUdX.bin')


    def load(self, run_ID = 0, frame_ID = 0):
        save_run_path = self.result_path + f'/Run_{run_ID}'
        save_frame_path = save_run_path + f'/Frame_{frame_ID}'
        self.filtered_fluc_U = self.load_nparray_from_bin(self.filtered_fluc_U, save_frame_path + '/filtered_fluc_U.bin')
        self.filtered_fluc_dUdX = self.load_nparray_from_bin(self.filtered_fluc_dUdX, save_frame_path + '/filtered_fluc_dUdX.bin')

if __name__ == "__main__":
    # cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
    cases = ['Case01']
    for case_id in range(len(cases)):
        FO = FOI(cases[case_id])
        FO.load()
        FV = FilteredVelocityField(cases[case_id],ifinit=True, ifcleandir=True)
        for filter_option_id in range(FO.option_list_shape.total_options):
            FV = FilteredVelocityField(cases[case_id],(FO.option_list[0, filter_option_id], FO.option_list[1, filter_option_id]))
            FV.calculate()