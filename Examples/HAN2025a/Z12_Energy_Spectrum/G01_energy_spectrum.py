''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/12  =
=========================
'''

import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as swc
from pivdataprocessor.A01_toolbox import np_fft

class EnergySpectrum(pTS):
    def __init__(self, casename, avg_ylines_for_x = None, avg_xlines_for_y = None):
        super().__init__(casename)

        self.X_fft_range = self.CaseInfo.Uniform_Range[0]
        self.Y_fft_range = self.CaseInfo.Uniform_Range[1]
        if avg_ylines_for_x == None:
            self.X_avg_Yrange = self.CaseInfo.Uniform_Range[1]
        else:
            self.X_avg_Yrange = (self.CaseInfo.Central_Position_Flow[1] - avg_ylines_for_x,
                                 self.CaseInfo.Central_Position_Flow[1] + avg_ylines_for_x)
        if avg_xlines_for_y == None:
            self.Y_avg_Xrange = self.CaseInfo.Uniform_Range[0]
        else:
            self.Y_avg_Xrange = (self.CaseInfo.Central_Position_Flow[0] - avg_xlines_for_y,
                                 self.CaseInfo.Central_Position_Flow[0] + avg_xlines_for_y)
        
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
        pBase.rm_and_create_directory(self.result_path)
        for run_ID in range(len(pBase.frame_numbers_in_runs)):
            for frame_ID in range(pBase.frame_numbers_in_runs[run_ID]):
                pBase.base_load_data_all(run_ID,frame_ID)
                left, right = self.X_fft_range
                bottom, up = self.Y_fft_range
                
                for y_line in range(self.X_avg_Yrange[0],self.X_avg_Yrange[1]+1):
                    fluc_u = pBase.fluc_U[0][left:right,y_line]
                    fluc_v = pBase.fluc_U[1][left:right,y_line]
                    fft_u = np_fft(fluc_u,pBase.dX[0])
                    fft_v = np_fft(fluc_v,pBase.dX[0])
                    fft_u.fft()
                    fft_v.fft()
                    self.__tmp_xdir[0], self.wavenumber_xdir = fft_u.get_result()
                    self.__tmp_xdir[1], self.wavenumber_xdir = fft_v.get_result()
                    self.__cal_spec_xdir.add_point(self.__tmp_xdir)

                for x_line in range(self.Y_avg_Xrange[0],self.Y_avg_Xrange[1]+1):
                    fluc_u = pBase.fluc_U[0][x_line,bottom:up]
                    fluc_v = pBase.fluc_U[1][x_line,bottom:up]
                    fft_u = np_fft(fluc_u,pBase.dX[1])
                    fft_v = np_fft(fluc_v,pBase.dX[1])
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
        self.save_nparray_to_bin(self.spec_xdir, self.result_path+'/spec_xdir.bin')
        self.save_nparray_to_bin(self.wavenumber_xdir, self.result_path+'/wavenumber_xdir.bin')
        self.save_nparray_to_bin(self.spec_ydir, self.result_path+'/spec_ydir.bin')
        self.save_nparray_to_bin(self.wavenumber_ydir, self.result_path+'/wavenumber_ydir.bin')
    def load(self):
        self.spec_xdir = self.load_nparray_from_bin(self.spec_xdir, self.result_path+'/spec_xdir.bin')
        self.wavenumber_xdir = self.load_nparray_from_bin(self.wavenumber_xdir, self.result_path+'/wavenumber_xdir.bin')
        self.spec_ydir = self.load_nparray_from_bin(self.spec_ydir, self.result_path+'/spec_ydir.bin')
        self.wavenumber_ydir = self.load_nparray_from_bin(self.wavenumber_ydir, self.result_path+'/wavenumber_ydir.bin')

if __name__ == "__main__":
    cases = ['All100','Grad','AntiGrad','Shear']
    ESs = [() for _ in range(len(cases))]
    for case_id in range(len(cases)):
        ESs[case_id] = EnergySpectrum(cases[case_id])
        ESs[case_id].calculate()