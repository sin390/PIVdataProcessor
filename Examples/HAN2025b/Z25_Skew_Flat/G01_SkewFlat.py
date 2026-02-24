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
        self.S_and_F_u = WSC(self.vfh.X[0].shape)
        self.S_and_F_v = WSC(self.vfh.X[0].shape)
        self.S_u = np.zeros_like(self.vfh.X[0])
        self.F_u = np.zeros_like(self.vfh.X[0])
        self.S_v = np.zeros_like(self.vfh.X[0])
        self.F_v = np.zeros_like(self.vfh.X[0])
        self.effctive_range = self.vfh.effctive_range

    def calculate(self):
        self.rm_and_create_directory(self.result_path)
        for run_id in range(len(self.vfh.frames_in_runs)):
            for frame_id in range(self.vfh.frames_in_runs[run_id]):
                self.vfh.load_field(run_id,frame_id)
                self.S_and_F_u.add_point(self.vfh.u[0])
                self.S_and_F_v.add_point(self.vfh.u[1])
        self.S_u = self.S_and_F_u.get_skewness()
        self.F_u = self.S_and_F_u.get_flatness()
        self.S_v = self.S_and_F_v.get_skewness()
        self.F_v = self.S_and_F_v.get_flatness()

        self.__save()    

    def __save(self):
        self.save_nparray_to_bin(self.S_u, self.result_path+'/S_u.bin')
        self.save_nparray_to_bin(self.F_u, self.result_path+'/F_u.bin')
        self.save_nparray_to_bin(self.S_v, self.result_path+'/S_v.bin')
        self.save_nparray_to_bin(self.F_v, self.result_path+'/F_v.bin')
        left,right = self.effctive_range[0]
        bottom,up = self.effctive_range[1]
        self.result_json.set(0,avg_S_u= np.nanmean(self.S_u[left:right,bottom:up]))
        self.result_json.set(0,avg_F_u= np.nanmean(self.F_u[left:right,bottom:up]))
        self.result_json.set(0,avg_S_v= np.nanmean(self.S_v[left:right,bottom:up]))
        self.result_json.set(0,avg_F_v= np.nanmean(self.F_v[left:right,bottom:up]))
    def load(self):
        self.S_u = self.load_nparray_from_bin(self.S_u, self.result_path+'/S_u.bin')
        self.F_u = self.load_nparray_from_bin(self.F_u, self.result_path+'/F_u.bin')
        self.S_v = self.load_nparray_from_bin(self.S_v, self.result_path+'/S_v.bin')
        self.F_v = self.load_nparray_from_bin(self.F_v, self.result_path+'/F_v.bin')

if __name__ == "__main__":
    import ZZZ_Result_Manager.A01_cases as A01
    cases = A01.cases_f+A01.cases_w
    for case_id in range(len(cases)):
        target_cases = SkewFlat(cases[case_id],'gaussian',-1)
        target_cases.calculate()