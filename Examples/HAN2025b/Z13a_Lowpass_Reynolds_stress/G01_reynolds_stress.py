''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/12/05  =
=========================
'''

import numpy as np

from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as swc
from Z02_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT

class ReynoldsStress(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None):
        super().__init__(casename)
        assert filter in ('gaussian','gaussian_bp','wavelet')
        self.datasource = filter
        self.filter_id = filter_id
        self.vfh = VFH(casename, filter, filter_id)
        self.vfh.load_X()
        self.vfh.load_field(0,0)
        self.frames_in_runs = self.vfh.frames_in_runs

        self.result_json = PT(self.result_path + self.vfh.middle_path()+"/result.json")

        self.X = self.vfh.X
        self.effctive_range = self.vfh.effctive_range

        self.uu = np.zeros_like(self.vfh.X[0])
        self.vv = np.zeros_like(self.vfh.X[0])
        self.uv = np.zeros_like(self.vfh.X[0])
        self.k2 = np.zeros_like(self.vfh.X[0])

        self.urms = np.zeros_like(self.vfh.X[0])
        self.vrms = np.zeros_like(self.vfh.X[0])

        self.invariant_eta = np.zeros_like(self.vfh.X[0])

        self.__cal_uu = swc(self.uu.shape)
        self.__cal_vv = swc(self.vv.shape)
        self.__cal_uv = swc(self.uv.shape)
        self.__cal_k2 = swc(self.k2.shape)

    
    
    def calculate(self):
        result_path = self.result_path + self.vfh.middle_path()
        self.rm_and_create_directory(result_path)
        for run_ID in range(len(self.frames_in_runs)):
            for frame_ID in range(self.frames_in_runs[run_ID]):
                self.vfh.load_field(run_ID,frame_ID)
                frame_u = self.vfh.u
                self.__cal_uu.add_point(frame_u[0]*frame_u[0])
                self.__cal_vv.add_point(frame_u[1]*frame_u[1])
                self.__cal_uv.add_point(frame_u[0]*frame_u[1])
                self.__cal_k2.add_point((frame_u[0]*frame_u[0]+ 2*frame_u[1]*frame_u[1])/2)
        self.uu = self.__cal_uu.get_mean()
        self.uv = self.__cal_uv.get_mean()
        self.vv = self.__cal_vv.get_mean()
        self.k2 = self.__cal_k2.get_mean()

        self.urms = np.sqrt(self.uu)
        self.vrms = np.sqrt(self.vv)

        b11 = self.uu/(2*self.k2) - 1/3
        b22 = self.vv/(2*self.k2) - 1/3
        b12 = self.uv/(2*self.k2)
        b33 = b22

        self.invariant_eta = b11*b11 + b22*b22 + b33*b33 + 2*(b12*b12)
        self.invariant_eta = np.sqrt(self.invariant_eta/6)

        self.__scalars()
        self.__save()

    def __scalars(self):
        left, right, bottom, up = VFH.unpackrange(self.effctive_range)
        avg_urms = np.nanmean(self.urms[left:right,bottom:up])
        avg_vrms = np.nanmean(self.vrms[left:right,bottom:up])
        self.result_json.set(0, scale_in_grid = self.vfh.scale_in_grid)
        self.result_json.set(0, avg_urms = avg_urms) 
        self.result_json.set(0, avg_vrms = avg_vrms)
        self.result_json.set(0, avg_uv_rms_ratio = avg_urms/avg_vrms)
        self.result_json.set(0, avg_k2 = np.nanmean(self.k2[left:right,bottom:up]))

    def __save(self):
        result_path = self.result_path + self.vfh.middle_path()
        self.save_nparray_to_bin(self.uu, result_path+'/uu.bin')
        self.save_nparray_to_bin(self.uv, result_path+'/uv.bin')
        self.save_nparray_to_bin(self.vv, result_path+'/vv.bin')
        self.save_nparray_to_bin(self.k2, result_path+'/k2.bin')
        self.save_nparray_to_bin(self.urms, result_path+'/urms.bin')
        self.save_nparray_to_bin(self.vrms, result_path+'/vrms.bin')
        self.save_nparray_to_bin(self.invariant_eta, result_path+'/eta.bin')

    
    def load(self):
        result_path = self.result_path + self.vfh.middle_path()
        self.uu = self.load_nparray_from_bin(self.uu, result_path+'/uu.bin')
        self.uv = self.load_nparray_from_bin(self.uv, result_path+'/uv.bin')
        self.vv = self.load_nparray_from_bin(self.vv, result_path+'/vv.bin')
        self.k2 = self.load_nparray_from_bin(self.k2, result_path+'/k2.bin')
        self.urms = self.load_nparray_from_bin(self.urms, result_path+'/urms.bin')
        self.vrms = self.load_nparray_from_bin(self.vrms, result_path+'/vrms.bin')        
        self.invariant_eta = self.load_nparray_from_bin(self.invariant_eta, result_path+'/eta.bin')


def worker(args):
    case, filter, p = args
    rs = ReynoldsStress(case, filter, filter_id=p)
    return rs.calculate()

if __name__ == '__main__':
    from multiprocessing import Pool 

    from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
    from ZZZ_Result_Manager.A01_cases import cases_select, cases_select_f, cases_select_w, coeffs_to_eta
 
    print('Gaussian_lowpass')
    for coeff_id, coeff in enumerate(coeffs_to_eta):
        coeff_id += 1
        tasks = []
        with Pool() as pool:
            for case_id, case in enumerate(cases_select):
                tasks.append((cases_select_w[case_id], 'gaussian', coeff_id))
            results = pool.map(worker, tasks)   
