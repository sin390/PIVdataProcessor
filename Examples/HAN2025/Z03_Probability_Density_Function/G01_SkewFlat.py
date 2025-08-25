''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/17  =
=========================
'''

import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import WelfordStatisticsCalculator as WSC
from pivdataprocessor.A01_toolbox import shift_field

class SkewFlat(pTS):
    
    def __init__(self, casename):
        super().__init__(casename)
        self.casename = pBase.CaseInfo.CaseName
        Nx, Ny = pBase.CaseInfo.Nx, pBase.CaseInfo.Ny
        self.S_and_F_u = WSC((Nx,Ny))
        self.S_and_F_v = WSC((Nx,Ny))
        self.S_u = pBase.get_a_container(0)
        self.F_u = pBase.get_a_container(0)
        self.S_v = pBase.get_a_container(0)
        self.F_v = pBase.get_a_container(0)


    def calculate(self):
        pBase.rm_and_create_directory(self.result_path)
        for run_id in range(len(pBase.frame_numbers_in_runs)):
            for frame_id in range(pBase.frame_numbers_in_runs[run_id]):
                pBase.base_load_data_all(run_id,frame_id)
                self.S_and_F_u.add_point(pBase.fluc_U[0])
                self.S_and_F_v.add_point(pBase.fluc_U[1])
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

    def load(self):
        self.S_u = self.load_nparray_from_bin(self.S_u, self.result_path+'/S_u.bin')
        self.F_u = self.load_nparray_from_bin(self.F_u, self.result_path+'/F_u.bin')
        self.S_v = self.load_nparray_from_bin(self.S_v, self.result_path+'/S_v.bin')
        self.F_v = self.load_nparray_from_bin(self.F_v, self.result_path+'/F_v.bin')

if __name__ == "__main__":
    cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
    cases = [case + '_sub1' for case in cases]    
    for case_id in range(len(cases)):
        target_cases = SkewFlat(cases[case_id])
        target_cases.calculate()