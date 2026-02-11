''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/17  =
=========================
'''

import numpy as np
from pivdataprocessor.A01_toolbox import WelfordStatisticsCalculator as WSC
from pivdataprocessor.A01_toolbox import shift_field
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from Z02_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH

class SkewFlat(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None):
        super().__init__(casename)
        assert filter in ('gaussian','gaussian_bp','wavelet')
        self.datasource = filter
        self.filter_id = filter_id
        self.vfh = VFH(casename, filter, filter_id)
        self.vfh.load_X()
        self.vfh.load_field(0,0)
        self.result_json = PT(self.result_path + self.vfh.middle_path()+"/result.json")
        self.result_path = self.result_path + self.vfh.middle_path()
        self.S_and_F_dudx = WSC(self.vfh.X[0].shape)
        self.S_and_F_dvdy = WSC(self.vfh.X[0].shape)
        self.S_dudx = np.zeros_like(self.vfh.X[0])
        self.F_dudx = np.zeros_like(self.vfh.X[0])
        self.S_dvdy = np.zeros_like(self.vfh.X[0])
        self.F_dvdy = np.zeros_like(self.vfh.X[0])
        self.effctive_range = self.vfh.effctive_range


    def calculate(self):
        self.rm_and_create_directory(self.result_path)
        for run_id in range(len(self.vfh.frames_in_runs)):
            for frame_id in range(self.vfh.frames_in_runs[run_id]):
                self.vfh.load_field(run_id,frame_id)
                self.S_and_F_dudx.add_point(self.vfh.dudx[0][0])
                self.S_and_F_dvdy.add_point(self.vfh.dudx[1][1])
        self.S_dudx = self.S_and_F_dudx.get_skewness()
        self.F_dudx = self.S_and_F_dudx.get_flatness()
        self.S_dvdy = self.S_and_F_dvdy.get_skewness()
        self.F_dvdy = self.S_and_F_dvdy.get_flatness()

        self.__save()    

    def __save(self):
        self.save_nparray_to_bin(self.S_dudx, self.result_path+'/S_dudx.bin')
        self.save_nparray_to_bin(self.F_dudx, self.result_path+'/F_dudx.bin')
        self.save_nparray_to_bin(self.S_dvdy, self.result_path+'/S_dvdy.bin')
        self.save_nparray_to_bin(self.F_dvdy, self.result_path+'/F_dvdy.bin')
        left,right = self.effctive_range[0]
        bottom,up = self.effctive_range[1]
        self.result_json.set(0,avg_S_dudx= np.nanmean(self.S_dudx[left:right,bottom:up]))
        self.result_json.set(0,avg_F_dudx= np.nanmean(self.F_dudx[left:right,bottom:up]))
        self.result_json.set(0,avg_S_dvdy= np.nanmean(self.S_dvdy[left:right,bottom:up]))
        self.result_json.set(0,avg_F_dvdy= np.nanmean(self.F_dvdy[left:right,bottom:up]))
    def load(self):
        self.S_dudx = self.load_nparray_from_bin(self.S_dudx, self.result_path+'/S_dudx.bin')
        self.F_dudx = self.load_nparray_from_bin(self.F_dudx, self.result_path+'/F_dudx.bin')
        self.S_dvdy = self.load_nparray_from_bin(self.S_dvdy, self.result_path+'/S_dvdy.bin')
        self.F_dvdy = self.load_nparray_from_bin(self.F_dvdy, self.result_path+'/F_dvdy.bin')

if __name__ == "__main__":
    import ZZZ_Result_Manager.A01_cases as A01
    cases = A01.cases_f+A01.cases_w
    for case_id in range(len(cases)):
        target_cases = SkewFlat(cases[case_id],'gaussian',-1)
        target_cases.calculate()