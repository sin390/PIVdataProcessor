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
from pivdataprocessor.A01_toolbox import central_stepping_indexs

class StructureFunction(pTS):
    def __init__(self, casename, avg_ylines_for_x = None, avg_xlines_for_y = None):
        super().__init__(casename)
        self.X_sf_range = self.CaseInfo.Uniform_Range[0]
        self.Y_sf_range = self.CaseInfo.Uniform_Range[1]

        center_x,center_y = self.CaseInfo.Central_Position_Grid
        if avg_ylines_for_x == None:
            self.X_avg_Yrange = self.CaseInfo.Uniform_Range[1]
        else:
            self.X_avg_Yrange = (center_y - avg_ylines_for_x,
                                 center_y + avg_ylines_for_x)
        if avg_xlines_for_y == None:
            self.Y_avg_Xrange = self.CaseInfo.Uniform_Range[0]
        else:
            self.Y_avg_Xrange = (center_x - avg_xlines_for_y,
                                 center_x + avg_xlines_for_y)      
        r_sf_x = min(self.X_sf_range[1]-center_x,center_x-self.X_sf_range[0])
        r_sf_y = min(self.Y_sf_range[1]-center_y,center_y-self.Y_sf_range[0])
        self.sf_length_xdir = 2 * r_sf_x 
        self.sf_length_ydir = 2 * r_sf_y 
        self.stepping_indexs_x = central_stepping_indexs(self.sf_length_xdir+1)[1:] + center_x
        self.stepping_indexs_y = central_stepping_indexs(self.sf_length_ydir+1)[1:] + center_y

        self.__cal_corr_xdir = swc((2,self.sf_length_xdir))
        self.__cal_corr_ydir = swc((2,self.sf_length_ydir))
        self.__tmp_xdir = np.zeros((2,self.sf_length_xdir))
        self.__tmp_ydir = np.zeros((2,self.sf_length_ydir))

        self.sf_xdir = np.zeros((2,self.sf_length_xdir))
        self.sf_ydir = np.zeros((2,self.sf_length_ydir))
        self.r_xdir = np.zeros((self.sf_length_xdir,))
        self.r_ydir = np.zeros((self.sf_length_ydir,))
    
    def calculate(self):
        pBase.rm_and_create_directory(self.result_path)
        for run_ID in range(len(pBase.frame_numbers_in_runs)):
            for frame_ID in range(pBase.frame_numbers_in_runs[run_ID]):
                pBase.base_load_data_all(run_ID,frame_ID)

                for y_line in range(self.X_avg_Yrange[0],self.X_avg_Yrange[1]+1):
                    for temp_r in range(self.sf_length_xdir):
                        stat, end = self.stepping_indexs_x[temp_r]
                        self.__tmp_xdir[0][temp_r] = (np.abs(pBase.fluc_U[0][stat,y_line]-pBase.fluc_U[0][end,y_line]))**2
                        self.__tmp_xdir[1][temp_r] = (np.abs(pBase.fluc_U[1][stat,y_line]-pBase.fluc_U[1][end,y_line]))**2
                    self.__cal_corr_xdir.add_point(self.__tmp_xdir)

                for x_line in range(self.Y_avg_Xrange[0],self.Y_avg_Xrange[1]+1):
                    for temp_r in range(self.sf_length_ydir):
                        stat, end = self.stepping_indexs_y[temp_r]
                        self.__tmp_ydir[0][temp_r] = (np.abs(pBase.fluc_U[0][x_line,stat]-pBase.fluc_U[0][x_line,end]))**2
                        self.__tmp_ydir[1][temp_r] = (np.abs(pBase.fluc_U[1][x_line,stat]-pBase.fluc_U[1][x_line,end]))**2
                    self.__cal_corr_ydir.add_point(self.__tmp_ydir)
        self.sf_xdir = self.__cal_corr_xdir.get_mean()
        self.sf_ydir = self.__cal_corr_ydir.get_mean()
        self.r_xdir[:] = (np.array(list(range(1,self.sf_length_xdir+1)))*self.dX[0])[:]
        self.r_ydir[:] = (np.array(list(range(1,self.sf_length_ydir+1)))*self.dX[1])[:]
 
        # center_x,center_y = self.CaseInfo.Central_Position_Grid
        # for temp_r in range(self.sf_length_xdir):
        #     stat, end = self.stepping_indexs_x[temp_r]
        #     self.r_xdir[temp_r] = abs(pBase.X[0][stat,center_y] - pBase.X[0][end,center_y])
        # for temp_r in range(self.sf_length_ydir):
        #     stat, end = self.stepping_indexs_y[temp_r]
        #     self.r_ydir[temp_r] = abs(pBase.X[1][center_x,stat] - pBase.X[1][center_x,end])
        self.__save()

    def __save(self):
        self.save_nparray_to_bin(self.sf_xdir, self.result_path+'/sf_xdir.bin')
        self.save_nparray_to_bin(self.r_xdir, self.result_path+'/r_xdir.bin')
        self.save_nparray_to_bin(self.sf_ydir, self.result_path+'/sf_ydir.bin')
        self.save_nparray_to_bin(self.r_ydir, self.result_path+'/r_ydir.bin')
    def load(self):
        self.sf_xdir = self.load_nparray_from_bin(self.sf_xdir, self.result_path+'/sf_xdir.bin')
        self.r_xdir = self.load_nparray_from_bin(self.r_xdir, self.result_path+'/r_xdir.bin')
        self.sf_ydir = self.load_nparray_from_bin(self.sf_ydir, self.result_path+'/sf_ydir.bin')
        self.r_ydir = self.load_nparray_from_bin(self.r_ydir, self.result_path+'/r_ydir.bin')

if __name__ == "__main__":
    cases =  ['Case01', 'Case01F_x0', 'Case01F_x15', 'Case01F_x30']
    cases = cases + ['Case04', 'Case04F_x0', 'Case04F_x15','Case04F_x30']
    cases = ['Case04', 'Case04F_x0', 'Case04F_x15','Case04F_x30']
    SFs = [() for _ in range(len(cases))]
    for case_id in range(len(cases)):
        SFs[case_id] = StructureFunction(cases[case_id])
        SFs[case_id].calculate()