''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/12  =
=========================
'''

import numpy as np
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as swc
from pivdataprocessor.A01_toolbox import central_stepping_indexs, least_squared_fitting
from scipy.integrate import quad
import ZZZ_Result_Manager.A01_cases as A01

from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT

from Z11_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD
from Z25_Autocorrelation.T02_find_crossing import find_threshold_crossings_quadratic_minimal

class AutoCorrelation(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None, avg_ylines_for_x = None, avg_xlines_for_y = None, center = 'Grid'):
        super().__init__(casename)
        assert filter in ('gaussian','gaussian_bp','wavelet')
        self.datasource = filter
        self.filter_id = filter_id
        self.td = TD(casename, filter, filter_id)
        self.frames_in_runs = self.td.vfh.frames_in_runs

        self.result_json = PT(self.result_path + self.td.vfh.middle_path()+"/result.json")

        self.X = self.td.vfh.X
        self.effctive_range = self.td.vfh.effctive_range

        self.td = TD(casename, filter, filter_id)
        self.td.load_avg()

        self.X_ac_range = self.effctive_range[0]
        self.Y_ac_range = self.effctive_range[1]

        ic,jc = self.td.vfh.central_pos_grid

        if avg_ylines_for_x == None:
            self.X_avg_Yrange = self.effctive_range[1]
        else:
            self.X_avg_Yrange = (jc - avg_ylines_for_x,
                                 jc + avg_ylines_for_x)
        if avg_xlines_for_y == None:
            self.Y_avg_Xrange = self.effctive_range[0]
        else:
            self.Y_avg_Xrange = (ic - avg_xlines_for_y,
                                 ic + avg_xlines_for_y)
        
        
        self.ac_length_xdir = self.X_ac_range[1]-self.X_ac_range[0]
        self.ac_length_ydir = self.Y_ac_range[1]-self.Y_ac_range[0]
        if center == 'Flow':
            self.stepping_indexs_x = central_stepping_indexs(self.ac_length_xdir) + ic
            self.stepping_indexs_y = central_stepping_indexs(self.ac_length_ydir) + jc
        elif center == 'Grid':
            self.stepping_indexs_x = central_stepping_indexs(self.ac_length_xdir) + ic
            self.stepping_indexs_y = central_stepping_indexs(self.ac_length_ydir) + jc          

        self.__cal_corr_xdir = swc((2,self.ac_length_xdir))
        self.__cal_corr_ydir = swc((2,self.ac_length_ydir))
        self.__tmp_xdir = np.zeros((2,self.ac_length_xdir))
        self.__tmp_ydir = np.zeros((2,self.ac_length_ydir))

        self.autocorr_xdir = np.zeros((2,self.ac_length_xdir))
        self.r_xdir = np.zeros((self.ac_length_xdir,))
        self.autocorr_ydir = np.zeros((2,self.ac_length_ydir))
        self.r_ydir = np.zeros((self.ac_length_ydir,))
        
        '[0]->L11-xdir, [1]->L22-ydir'
        self.Integral_length = np.zeros((2,))

        self.__fitting_point_number = 50    

        '[0]->R11-xdir-corr, [1]->R11-xdir-r, [2]->R22-ydir-corr, [3]->R22-ydir-r'
        self.fitting_part = np.zeros((4, self.__fitting_point_number))
        
    
    def calculate(self):
        result_path = self.result_path + self.td.vfh.middle_path()
        self.rm_and_create_directory(result_path)
        for run_ID in range(len(self.frames_in_runs)):
            for frame_ID in range(self.frames_in_runs[run_ID]):
                self.td.cal_frame(run_ID,frame_ID)
                fluc_intensity_shear = self.td.intensity_shear - self.td.avg_intensity_shear
                fluc_intensity_rotation = self.td.intensity_rotation - self.td.avg_intensity_rotation
                for y_line in range(self.X_avg_Yrange[0],self.X_avg_Yrange[1]+1):
                    for temp_r in range(self.ac_length_xdir):
                        stat, end = self.stepping_indexs_x[temp_r]
                        self.__tmp_xdir[0][temp_r] = fluc_intensity_shear[stat,y_line]*fluc_intensity_shear[end,y_line]
                        self.__tmp_xdir[1][temp_r] = fluc_intensity_rotation[stat,y_line]*fluc_intensity_rotation[end,y_line]
                    self.__cal_corr_xdir.add_point(self.__tmp_xdir)

                for x_line in range(self.Y_avg_Xrange[0],self.Y_avg_Xrange[1]+1):
                    for temp_r in range(self.ac_length_ydir):
                        stat, end = self.stepping_indexs_y[temp_r]
                        self.__tmp_ydir[0][temp_r] = fluc_intensity_shear[x_line,stat]*fluc_intensity_shear[x_line,end]
                        self.__tmp_ydir[1][temp_r] = fluc_intensity_rotation[x_line,stat]*fluc_intensity_rotation[x_line,end]
                    self.__cal_corr_ydir.add_point(self.__tmp_ydir)

        self.autocorr_xdir = self.__cal_corr_xdir.get_mean()
        self.autocorr_xdir[0] = self.autocorr_xdir[0] / self.autocorr_xdir[0][0]
        self.autocorr_xdir[1] = self.autocorr_xdir[1] / self.autocorr_xdir[1][0]
        self.r_xdir[:] = (np.array(list(range(self.ac_length_xdir)))*self.td.vfh.dX_in_mm[0])[:]
        self.autocorr_ydir = self.__cal_corr_ydir.get_mean()
        self.autocorr_ydir[0] = self.autocorr_ydir[0] / self.autocorr_ydir[0][0]
        self.autocorr_ydir[1] = self.autocorr_ydir[1] / self.autocorr_ydir[1][0]
        self.r_ydir[:] = (np.array(list(range(self.ac_length_ydir)))*self.td.vfh.dX_in_mm[1])[:]

        self.__save()


    def __save(self):
        result_path = self.result_path + self.td.vfh.middle_path()
        self.save_nparray_to_bin(self.autocorr_xdir, result_path+'/autocorr_xdir.bin')
        self.save_nparray_to_bin(self.r_xdir, result_path+'/r_xdir.bin')
        self.save_nparray_to_bin(self.autocorr_ydir, result_path+'/autocorr_ydir.bin')
        self.save_nparray_to_bin(self.r_ydir, result_path+'/r_ydir.bin')

    def cal_L_thr(self, thr=0.5):
        L_thr_Is_x = find_threshold_crossings_quadratic_minimal(self.r_xdir,self.autocorr_xdir[0],thr)
        L_thr_Ir_x = find_threshold_crossings_quadratic_minimal(self.r_xdir,self.autocorr_xdir[1],thr)
        L_thr_Is_y = find_threshold_crossings_quadratic_minimal(self.r_ydir,self.autocorr_ydir[0],thr)
        L_thr_Ir_y = find_threshold_crossings_quadratic_minimal(self.r_ydir,self.autocorr_ydir[1],thr)

        self.result_json.set(0, L_thr_Is_x=L_thr_Is_x, L_thr_Is_y=L_thr_Is_y)
        self.result_json.set(0, L_thr_Ir_x=L_thr_Ir_x, L_thr_Ir_y=L_thr_Ir_y)



    def load(self):
        result_path = self.result_path + self.td.vfh.middle_path()
        self.autocorr_xdir = self.load_nparray_from_bin(self.autocorr_xdir, result_path+'/autocorr_xdir.bin')
        self.r_xdir = self.load_nparray_from_bin(self.r_xdir, result_path+'/r_xdir.bin')
        self.autocorr_ydir = self.load_nparray_from_bin(self.autocorr_ydir, result_path+'/autocorr_ydir.bin')
        self.r_ydir = self.load_nparray_from_bin(self.r_ydir, result_path+'/r_ydir.bin')


def worker(args):
    case, filter, p = args
    ac = AutoCorrelation(case, filter, filter_id=p)
    return ac.calculate()

if __name__ == '__main__':
    from ZZZ_Result_Manager.A01_cases import gaussian_id, cases
    from multiprocessing import Pool 
    
    print('Gaussian_lowpass')
    for filter_param in gaussian_id:
        print(f'filter : {filter_param}')
        tasks = []
        with Pool() as pool:
            for case in cases:
                tasks.append((case, 'gaussian', filter_param))
            results = pool.map(worker, tasks)   