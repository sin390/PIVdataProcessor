''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as swc

class ReynoldsStress(pTS):
    def __init__(self, casename):
        super().__init__(casename)

        self.uu = self.get_a_container(0)
        self.vv = self.get_a_container(0)
        self.uv = self.get_a_container(0)
        self.k2 = self.get_a_container(0)
        self.b = self.get_a_container(2)

        self.invariant_eta = self.get_a_container(0)
        self.invariant_xi = self.get_a_container(0)
        self.__cal_uu = swc(self.uu.shape)
        self.__cal_vv = swc(self.vv.shape)
        self.__cal_uv = swc(self.uv.shape)
        self.__cal_k2 = swc(self.k2.shape)
    
    def calculate(self):
        pBase.rm_and_create_directory(self.result_path)
        for run_ID in range(len(pBase.frame_numbers_in_runs)):
            for frame_ID in range(pBase.frame_numbers_in_runs[run_ID]):
                pBase.base_load_data_all(run_ID,frame_ID)
                self.__cal_uu.add_point(pBase.fluc_U[0]*pBase.fluc_U[0])
                self.__cal_vv.add_point(pBase.fluc_U[1]*pBase.fluc_U[1])
                self.__cal_uv.add_point(pBase.fluc_U[0]*pBase.fluc_U[1])
                self.__cal_k2.add_point((pBase.fluc_U[0]*pBase.fluc_U[0]+ 2*pBase.fluc_U[1]*pBase.fluc_U[1])/2)
        self.uu = self.__cal_uu.get_mean()
        self.uv = self.__cal_uv.get_mean()
        self.vv = self.__cal_vv.get_mean()
        self.k2 = self.__cal_k2.get_mean()

        b11 = self.uu/(2*self.k2) - 1/3
        b22 = self.vv/(2*self.k2) - 1/3
        b12 = self.uv/(2*self.k2)
        b33 = b22

        self.b[0][0] = b11
        self.b[0][1] = b12
        self.b[1][0] = b12
        self.b[1][1] = b22

        self.invariant_eta = b11*b11 + b22*b22 + b33*b33 + 2*(b12*b12)
        self.invariant_eta = np.sqrt(self.invariant_eta/6)
        self.invariant_xi = b11*b11*b11 + b22*b22*b22 + b33*b33*b33 + 3*b11*b12*b12 + 3*b22*b12*b12
        self.invariant_xi = np.cbrt(self.invariant_xi/6)
        self.__scalars()
        self.__save()

    def __scalars(self):
        self.report(f'Avg_uu = {np.nanmean(self.uu)}')
        self.report(f'Avg_vv = {np.nanmean(self.vv)}')
        self.report(f'Avg_uv = {np.nanmean(self.uv)}')
        self.report(f'Avg_k2 = {np.nanmean(self.k2)}')
        self.report(f'Avg_xi = {np.nanmean(self.invariant_xi)}')
        self.report(f'Avg_xi = {np.nanmean(self.invariant_eta)}')

    def __save(self):
        self.save_nparray_to_bin(self.uu, self.result_path+'/uu.bin')
        self.save_nparray_to_bin(self.uv, self.result_path+'/uv.bin')
        self.save_nparray_to_bin(self.vv, self.result_path+'/vv.bin')
        self.save_nparray_to_bin(self.k2, self.result_path+'/k2.bin')
        self.save_nparray_to_bin(self.invariant_eta, self.result_path+'/eta.bin')
        self.save_nparray_to_bin(self.invariant_xi, self.result_path+'/xi.bin')
        self.save_nparray_to_bin(self.b, self.result_path+'/b.bin')
    
    def load(self):
        self.uu = self.load_nparray_from_bin(self.uu, self.result_path+'/uu.bin')
        self.uv = self.load_nparray_from_bin(self.uv, self.result_path+'/uv.bin')
        self.vv = self.load_nparray_from_bin(self.vv, self.result_path+'/vv.bin')
        self.k2 = self.load_nparray_from_bin(self.k2, self.result_path+'/k2.bin')
        self.invariant_eta = self.load_nparray_from_bin(self.invariant_eta, self.result_path+'/eta.bin')
        self.invariant_xi = self.load_nparray_from_bin(self.invariant_xi, self.result_path+'/xi.bin')
        self.b = self.load_nparray_from_bin(self.b, self.result_path+'/b.bin')

if __name__ == "__main__":
    cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
    cases = [case + '_sub2' for case in cases]
    for case_id in range(len(cases)):
        RS = ReynoldsStress(cases[case_id])
        RS.calculate()
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom, up = pBase.CaseInfo.Effective_Range[1]        
        RS.report(f'k2,avg = {np.nanmean(RS.k2[left:right,bottom:up])} (m2/s2)')