''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.1         =
= Date:     2025/07/24  =
=========================
'''

import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as swc
from pivdataprocessor.A01_toolbox import central_stepping_indexs, least_squared_fitting
from scipy.integrate import quad


class AutoCorrelation(pTS):
    def __init__(self, casename, avg_ylines_for_x = None, avg_xlines_for_y = None):
        super().__init__(casename)

        self.X_ac_range = self.CaseInfo.Uniform_Range[0]
        self.Y_ac_range = self.CaseInfo.Uniform_Range[1]

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
        r_ac_x = min(self.X_ac_range[1]-center_x,center_x-self.X_ac_range[0])
        r_ac_y = min(self.Y_ac_range[1]-center_y,center_y-self.Y_ac_range[0])
        self.ac_length_xdir = 2 * r_ac_x + 1
        self.ac_length_ydir = 2 * r_ac_y + 1
        self.stepping_indexs_x = central_stepping_indexs(self.ac_length_xdir) + center_x
        self.stepping_indexs_y = central_stepping_indexs(self.ac_length_ydir) + center_y        

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
        
    
    def calculate(self, fitting_start_x = 0.5, fitting_start_y = 0.5):
        pBase.rm_and_create_directory(self.result_path)
        for run_ID in range(len(pBase.frame_numbers_in_runs)):
            for frame_ID in range(pBase.frame_numbers_in_runs[run_ID]):
                pBase.base_load_data_all(run_ID,frame_ID)

                for y_line in range(self.X_avg_Yrange[0],self.X_avg_Yrange[1]+1):
                    for temp_r in range(self.ac_length_xdir):
                        stat, end = self.stepping_indexs_x[temp_r]
                        self.__tmp_xdir[0][temp_r] = pBase.fluc_U[0][stat,y_line]*pBase.fluc_U[0][end,y_line]
                        self.__tmp_xdir[1][temp_r] = pBase.fluc_U[1][stat,y_line]*pBase.fluc_U[1][end,y_line]
                    self.__cal_corr_xdir.add_point(self.__tmp_xdir)

                for x_line in range(self.Y_avg_Xrange[0],self.Y_avg_Xrange[1]+1):
                    for temp_r in range(self.ac_length_ydir):
                        stat, end = self.stepping_indexs_y[temp_r]
                        self.__tmp_ydir[0][temp_r] = pBase.fluc_U[0][x_line,stat]*pBase.fluc_U[0][x_line,end]
                        self.__tmp_ydir[1][temp_r] = pBase.fluc_U[1][x_line,stat]*pBase.fluc_U[1][x_line,end]
                    self.__cal_corr_ydir.add_point(self.__tmp_ydir)

        self.autocorr_xdir = self.__cal_corr_xdir.get_mean()
        self.autocorr_xdir[0] = self.autocorr_xdir[0] / self.autocorr_xdir[0][0]
        self.autocorr_xdir[1] = self.autocorr_xdir[1] / self.autocorr_xdir[1][0]
        self.r_xdir[:] = (np.array(list(range(self.ac_length_xdir)))*self.dX[0])[:]
        self.autocorr_ydir = self.__cal_corr_ydir.get_mean()
        self.autocorr_ydir[0] = self.autocorr_ydir[0] / self.autocorr_ydir[0][0]
        self.autocorr_ydir[1] = self.autocorr_ydir[1] / self.autocorr_ydir[1][0]
        self.r_ydir[:] = (np.array(list(range(self.ac_length_ydir)))*self.dX[1])[:]

        self.__fitting(start_value_x=fitting_start_x,start_value_y=fitting_start_y) 
        self.__save()

    def __fitting(self, start_value_x = 0.5, start_value_y = 0.5,  end_value = 0.00001):
        def fittingpart(f,r):
            log_f = np.log(f)
            fitting = least_squared_fitting(r,log_f)
            fitting.calculate()
            a = np.exp(fitting.result_b)
            b = fitting.result_a

            x1 = (np.log(f[0]/a))/b
            x2 = (np.log(end_value/a))/b
            def myfunc(x):
                return a*np.exp(b*x)
            L_fitting, error = quad(myfunc, x1, x2)

            r_extend = np.linspace(x1, x2, self.__fitting_point_number)
            f_fit = a*np.exp(b*r_extend)

            return f_fit, r_extend, L_fitting
        
        if (self.autocorr_xdir[0][-1] > end_value):
            half_pos_x = np.abs(self.autocorr_xdir[0] - start_value_x).argmin()
            corr_R11_x_ready = self.autocorr_xdir[0][0:half_pos_x]
            r_R11_x_ready = self.r_xdir[0:half_pos_x]
            self.fitting_part[0], self.fitting_part[1], L11_x_fitting = fittingpart(self.autocorr_xdir[0][half_pos_x+1:],
                                                                                self.r_xdir[half_pos_x+1:])
            L11_x_measure = np.trapezoid(corr_R11_x_ready,r_R11_x_ready)
            L11_x = L11_x_measure + L11_x_fitting
            self.report(f'L11_x: {L11_x:.2f} mm, measured part: {L11_x_measure:.2f} mm, fitted part: {L11_x_fitting:.2f} mm')
            self.Integral_length[0] = L11_x
        else:
            index = np.argmin(np.abs(self.autocorr_xdir[0]))
            if index+1 < len(self.r_xdir):
                index+=1
            L11_x_measure = np.trapezoid(self.autocorr_xdir[0][:index],self.r_xdir[:index])
            self.Integral_length[0] = L11_x_measure
            self.report(f'L11_x: {L11_x_measure:.2f} mm, measured part: {L11_x_measure:.2f} mm')

        if (self.autocorr_ydir[1][-1] > end_value):
            half_pos_y = np.abs(self.autocorr_ydir[1] - start_value_y).argmin()
            corr_R22_y_ready = self.autocorr_ydir[1][0:half_pos_y]
            r_R22_y_ready = self.r_ydir[0:half_pos_y]
            self.fitting_part[2], self.fitting_part[3], L22_y_fitting = fittingpart(self.autocorr_ydir[1][half_pos_y+1:],
                                                                                self.r_ydir[half_pos_y+1:])
            L22_y_measure = np.trapezoid(corr_R22_y_ready,r_R22_y_ready)
            L22_y = L22_y_measure + L22_y_fitting
            self.report(f'L22_y: {L22_y:.2f} mm, measured part: {L22_y_measure:.2f} mm, fitted part: {L22_y_fitting:.2f} mm')
            self.Integral_length[1] = L22_y
        else:
            index = np.argmin(np.abs(self.autocorr_ydir[1]))
            if index+1 < len(self.r_ydir):
                index+=1
            L22_y_measure = np.trapezoid(self.autocorr_ydir[1][:index],self.r_ydir[:index])
            self.Integral_length[1] = L22_y_measure
            self.report(f'L22_y: {L22_y_measure:.2f} mm, measured part: {L22_y_measure:.2f} mm')


    def __save(self):
        self.save_nparray_to_bin(self.autocorr_xdir, self.result_path+'/autocorr_xdir.bin')
        self.save_nparray_to_bin(self.r_xdir, self.result_path+'/r_xdir.bin')
        self.save_nparray_to_bin(self.autocorr_ydir, self.result_path+'/autocorr_ydir.bin')
        self.save_nparray_to_bin(self.r_ydir, self.result_path+'/r_ydir.bin')
        self.save_nparray_to_bin(self.fitting_part, self.result_path+'/fitting_part.bin')
        self.save_nparray_to_bin(self.Integral_length, self.result_path+'/Integral_length.bin')
    def load(self):
        self.autocorr_xdir = self.load_nparray_from_bin(self.autocorr_xdir, self.result_path+'/autocorr_xdir.bin')
        self.r_xdir = self.load_nparray_from_bin(self.r_xdir, self.result_path+'/r_xdir.bin')
        self.autocorr_ydir = self.load_nparray_from_bin(self.autocorr_ydir, self.result_path+'/autocorr_ydir.bin')
        self.r_ydir = self.load_nparray_from_bin(self.r_ydir, self.result_path+'/r_ydir.bin')
        self.fitting_part = self.load_nparray_from_bin(self.fitting_part, self.result_path+'/fitting_part.bin')
        self.Integral_length = self.load_nparray_from_bin(self.Integral_length, self.result_path+'/Integral_length.bin')

if __name__ == "__main__":
    cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06', 'Mori465']
    for case_id in range(len(cases)):
        AC = AutoCorrelation(cases[case_id])
        AC.calculate(fitting_start_x=0.3, fitting_start_y = 0.3)