''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/12/26  =
=========================
'''

import numpy as np
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as swc
from pivdataprocessor.A01_toolbox import np_fft

class EnergySpectrum(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None, avg_ylines_for_x = None, avg_xlines_for_y = None):
        super().__init__(casename)
        self.datasource = filter
        self.filter_id = filter_id
        self.vfh = VFH(casename, filter, filter_id)
        self.vfh.load_X()
        self.vfh.load_field(0,0)
        self.frames_in_runs = self.vfh.frames_in_runs
        self.result_json = PT(self.result_path + self.vfh.middle_path()+"/result.json")
        self.X = self.vfh.X

        self.X_fft_range = self.vfh.effctive_range[0]
        self.Y_fft_range = self.vfh.effctive_range[1]
        if avg_ylines_for_x == None:
            self.X_avg_Yrange = self.vfh.effctive_range[1]
        else:
            self.X_avg_Yrange = (self.vfh.central_pos_grid[1] - avg_ylines_for_x,
                                 self.vfh.central_pos_grid[1] + avg_ylines_for_x)
        if avg_xlines_for_y == None:
            self.Y_avg_Xrange = self.vfh.effctive_range[0]
        else:
            self.Y_avg_Xrange = (self.vfh.central_pos_grid[0] - avg_xlines_for_y,
                                 self.vfh.central_pos_grid[0] + avg_xlines_for_y)
        
        spec_length_xdir = (self.X_fft_range[1]-self.X_fft_range[0])//2 -1
        spec_length_ydir = (self.Y_fft_range[1]-self.Y_fft_range[0])//2 -1

        self.__cal_spec_xdir = swc((2,spec_length_xdir))
        self.__cal_spec_ydir = swc((2,spec_length_ydir))
        self.__tmp_xdir = np.zeros((2,spec_length_xdir))
        self.__tmp_ydir = np.zeros((2,spec_length_ydir))

        self.spec_xdir = np.zeros((2,spec_length_xdir))
        self.wavenumber_xdir = np.zeros((spec_length_xdir,))
        self.spec_ydir = np.zeros((2,spec_length_ydir))
        self.wavenumber_ydir = np.zeros((spec_length_ydir,))
        
    
    def calculate(self):
        for run_ID in range(len(self.frames_in_runs)):
            for frame_ID in range(self.frames_in_runs[run_ID]):
                self.vfh.load_field(run_ID,frame_ID)
                left, right = self.X_fft_range
                bottom, up = self.Y_fft_range
                
                for y_line in range(self.X_avg_Yrange[0],self.X_avg_Yrange[1]+1):
                    fluc_u = self.vfh.u[0][left:right,y_line]
                    fluc_v = self.vfh.u[1][left:right,y_line]
                    fft_u = np_fft(fluc_u, dx_in_mm=self.vfh.dX_in_mm[0])
                    fft_v = np_fft(fluc_v, dx_in_mm=self.vfh.dX_in_mm[0])
                    fft_u.fft()
                    fft_v.fft()
                    self.__tmp_xdir[0], self.wavenumber_xdir = fft_u.get_result()
                    self.__tmp_xdir[1], self.wavenumber_xdir = fft_v.get_result()
                    self.__cal_spec_xdir.add_point(self.__tmp_xdir)

                for x_line in range(self.Y_avg_Xrange[0],self.Y_avg_Xrange[1]+1):
                    fluc_u = self.vfh.u[0][x_line,bottom:up]
                    fluc_v = self.vfh.u[1][x_line,bottom:up]
                    fft_u = np_fft(fluc_u, dx_in_mm=self.vfh.dX_in_mm[1])
                    fft_v = np_fft(fluc_v, dx_in_mm=self.vfh.dX_in_mm[1])
                    fft_u.fft()
                    fft_v.fft()
                    self.__tmp_ydir[0], self.wavenumber_ydir = fft_u.get_result()
                    self.__tmp_ydir[1], self.wavenumber_ydir = fft_v.get_result()
                    self.__cal_spec_ydir.add_point(self.__tmp_ydir)      
        
        self.spec_xdir[0] = self.__cal_spec_xdir.get_mean()[0][:]
        self.spec_xdir[1] = self.__cal_spec_xdir.get_mean()[1][:]      
        self.spec_ydir[0] = self.__cal_spec_ydir.get_mean()[0][:]
        self.spec_ydir[1] = self.__cal_spec_ydir.get_mean()[1][:]
        self.__save()

    def __save(self):
        result_path = self.result_path + self.vfh.middle_path()
        self.make_sure_directory(result_path)
        self.save_nparray_to_bin(self.spec_xdir, result_path+'/spec_xdir.bin')
        self.save_nparray_to_bin(self.wavenumber_xdir, result_path+'/wavenumber_xdir.bin')
        self.save_nparray_to_bin(self.spec_ydir, result_path+'/spec_ydir.bin')
        self.save_nparray_to_bin(self.wavenumber_ydir, result_path+'/wavenumber_ydir.bin')
    def load(self):
        result_path = self.result_path + self.vfh.middle_path()
        self.spec_xdir = self.load_nparray_from_bin(self.spec_xdir, result_path+'/spec_xdir.bin')
        self.wavenumber_xdir = self.load_nparray_from_bin(self.wavenumber_xdir, result_path+'/wavenumber_xdir.bin')
        self.spec_ydir = self.load_nparray_from_bin(self.spec_ydir, result_path+'/spec_ydir.bin')
        self.wavenumber_ydir = self.load_nparray_from_bin(self.wavenumber_ydir, result_path+'/wavenumber_ydir.bin')

if __name__ == "__main__":
    cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06', 'Mori_465']
    filter = 'gaussian'
    filter_id = -1
    ESs = [() for _ in range(len(cases))]
    for case_id in range(len(cases)):
        vfh = VFH(cases[case_id], filter=filter, filter_id=filter_id)
        vfh.load_X()
        d_array_nozzle = 12  # mm
        x_lines = int(2*d_array_nozzle/vfh.dX_in_mm[0])
        y_lines = int(d_array_nozzle/vfh.dX_in_mm[1])
        # ESs[case_id] = EnergySpectrum(cases[case_id], filter= filter, filter_id=filter_id, avg_ylines_for_x = y_lines, avg_xlines_for_y = x_lines)
        ESs[case_id] = EnergySpectrum(cases[case_id], filter= filter, filter_id=filter_id)
        ESs[case_id].calculate()