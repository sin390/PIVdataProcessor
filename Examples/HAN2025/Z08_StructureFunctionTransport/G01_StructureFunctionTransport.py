''' 
=========================
= Author:   Claude      =
= Supervisor: HAN Zexu  =
= Version:  1.0         =
= Date:     2026/07/22  =
=========================

Implements the pre-derivative (i.e. before taking d/dr) quantities inside
Eqs. (3.5)-(3.8) of Valente & Vassilicos (2015):

    Pi_u'(x,y,r)     = -d/dr < [u'(x+,y) - u'(x-,y)]^3 >
    Pi_v'(x,y,r)     = -d/dr < [v'(x,y+) - v'(x,y-)]^3 >
    Pi_<u>(x,y,r)    = -d/dr { [<u>(x+,y) - <u>(x-,y)] * <[u'(x+,y) - u'(x-,y)]^2> }
    Pi_<v>(x,y,r)    = -d/dr { [<v>(x,y+) - <v>(x,y-)] * <[v'(x,y+) - v'(x,y-)]^2> }

with x+ = x + r/2, x- = x - r/2, y+ = y + r/2, y- = y - r/2.

This module only computes the bracketed quantities (the arguments of d/dr),
i.e. it stops one step before the derivative in r is taken, as requested.
The r-derivative itself (and the minus sign) is left to a downstream step.

NOTE: this assumes pBase exposes a mean-velocity field `pBase.U` with the
same [component][x_idx, y_idx] indexing convention as `pBase.fluc_U`
(i.e. U[0] -> <u>, U[1] -> <v>). If the actual attribute name in
L01_base differs, adjust `pBase.U` below accordingly.
'''

import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as swc
from pivdataprocessor.A01_toolbox import central_stepping_indexs


class StructureFunctionTransport(pTS):
    def __init__(self, casename, avg_ylines_for_x = None, avg_xlines_for_y = None):
        super().__init__(casename)

        self.X_ac_range = self.CaseInfo.Uniform_Range[0]
        self.Y_ac_range = self.CaseInfo.Uniform_Range[1]

        if avg_ylines_for_x == None:
            self.X_avg_Yrange = self.CaseInfo.Uniform_Range[1]
        else:
            self.X_avg_Yrange = (self.CaseInfo.Central_Position_Grid[1] - avg_ylines_for_x,
                                 self.CaseInfo.Central_Position_Grid[1] + avg_ylines_for_x)
        if avg_xlines_for_y == None:
            self.Y_avg_Xrange = self.CaseInfo.Uniform_Range[0]
        else:
            self.Y_avg_Xrange = (self.CaseInfo.Central_Position_Grid[0] - avg_xlines_for_y,
                                 self.CaseInfo.Central_Position_Grid[0] + avg_xlines_for_y)

        center_x,center_y = self.CaseInfo.Central_Position_Grid
        r_ac_x = min(self.X_ac_range[1]-center_x,center_x-self.X_ac_range[0])
        r_ac_y = min(self.Y_ac_range[1]-center_y,center_y-self.Y_ac_range[0])
        self.ac_length_xdir = 2 * r_ac_x + 1
        self.ac_length_ydir = 2 * r_ac_y + 1
        self.stepping_indexs_x = central_stepping_indexs(self.ac_length_xdir) + center_x
        self.stepping_indexs_y = central_stepping_indexs(self.ac_length_ydir) + center_y

        '''
        Accumulators (Welford running statistics), one component each:
        B3_xdir  -> <[u'(x+,y)-u'(x-,y)]^3>      (Eq. 3.5, pre-derivative part)
        B2_xdir  -> <[u'(x+,y)-u'(x-,y)]^2>      (needed for Eq. 3.7)
        MD_xdir  -> <u>(x+,y) - <u>(x-,y)        (needed for Eq. 3.7)
        B3_ydir  -> <[v'(x,y+)-v'(x,y-)]^3>      (Eq. 3.6, pre-derivative part)
        B2_ydir  -> <[v'(x,y+)-v'(x,y-)]^2>      (needed for Eq. 3.8)
        MD_ydir  -> <v>(x,y+) - <v>(x,y-)        (needed for Eq. 3.8)
        '''
        self.__cal_B3_xdir = swc((1,self.ac_length_xdir))
        self.__cal_B2_xdir = swc((1,self.ac_length_xdir))
        self.__cal_MD_xdir = swc((1,self.ac_length_xdir))
        self.__cal_B3_ydir = swc((1,self.ac_length_ydir))
        self.__cal_B2_ydir = swc((1,self.ac_length_ydir))
        self.__cal_MD_ydir = swc((1,self.ac_length_ydir))

        self.__tmp_B3_xdir = np.zeros((1,self.ac_length_xdir))
        self.__tmp_B2_xdir = np.zeros((1,self.ac_length_xdir))
        self.__tmp_MD_xdir = np.zeros((1,self.ac_length_xdir))
        self.__tmp_B3_ydir = np.zeros((1,self.ac_length_ydir))
        self.__tmp_B2_ydir = np.zeros((1,self.ac_length_ydir))
        self.__tmp_MD_ydir = np.zeros((1,self.ac_length_ydir))

        self.r_xdir = np.zeros((self.ac_length_xdir,))
        self.r_ydir = np.zeros((self.ac_length_ydir,))

        self.B3_xdir = np.zeros((self.ac_length_xdir,))
        self.B2_xdir = np.zeros((self.ac_length_xdir,))
        self.meandiff_xdir = np.zeros((self.ac_length_xdir,))
        self.B3_ydir = np.zeros((self.ac_length_ydir,))
        self.B2_ydir = np.zeros((self.ac_length_ydir,))
        self.meandiff_ydir = np.zeros((self.ac_length_ydir,))

        '''
        Pre-derivative quantities, i.e. the arguments of d/dr in Eqs. (3.5)-(3.8):
        [0] -> Pi_u'  pre-derivative term  (Eq. 3.5)
        [1] -> Pi_v'  pre-derivative term  (Eq. 3.6)
        [2] -> Pi_<u> pre-derivative term  (Eq. 3.7)
        [3] -> Pi_<v> pre-derivative term  (Eq. 3.8)
        '''
        self.Pi_uprime_pre = np.zeros((self.ac_length_xdir,))
        self.Pi_vprime_pre = np.zeros((self.ac_length_ydir,))
        self.Pi_meanu_pre = np.zeros((self.ac_length_xdir,))
        self.Pi_meanv_pre = np.zeros((self.ac_length_ydir,))

        self.Pi_uprime_pre = np.zeros((self.ac_length_xdir,))
        self.Pi_vprime_pre = np.zeros((self.ac_length_ydir,))
        self.Pi_meanu_pre = np.zeros((self.ac_length_xdir,))
        self.Pi_meanv_pre = np.zeros((self.ac_length_ydir,))

        self.Pi_uprime = np.zeros((self.ac_length_xdir,))
        self.Pi_vprime = np.zeros((self.ac_length_ydir,))
        self.Pi_meanu = np.zeros((self.ac_length_xdir,))
        self.Pi_meanv = np.zeros((self.ac_length_ydir,))


    def calculate(self):
        pBase.rm_and_create_directory(self.result_path)
        for run_ID in range(len(pBase.frame_numbers_in_runs)):
            for frame_ID in range(pBase.frame_numbers_in_runs[run_ID]):
                pBase.base_load_data_all(run_ID,frame_ID)

                for y_line in range(self.X_avg_Yrange[0],self.X_avg_Yrange[1]+1):
                    for temp_r in range(self.ac_length_xdir):
                        stat, end = self.stepping_indexs_x[temp_r]
                        du = pBase.fluc_U[0][end,y_line] - pBase.fluc_U[0][stat,y_line]
                        dU = pBase.U[0][end,y_line] - pBase.U[0][stat,y_line]
                        self.__tmp_B3_xdir[0][temp_r] = du**3
                        self.__tmp_B2_xdir[0][temp_r] = du**2
                        self.__tmp_MD_xdir[0][temp_r] = dU
                    self.__cal_B3_xdir.add_point(self.__tmp_B3_xdir)
                    self.__cal_B2_xdir.add_point(self.__tmp_B2_xdir)
                    self.__cal_MD_xdir.add_point(self.__tmp_MD_xdir)

                for x_line in range(self.Y_avg_Xrange[0],self.Y_avg_Xrange[1]+1):
                    for temp_r in range(self.ac_length_ydir):
                        stat, end = self.stepping_indexs_y[temp_r]
                        dv = pBase.fluc_U[1][x_line,end] - pBase.fluc_U[1][x_line,stat]
                        dV = pBase.U[1][x_line,end] - pBase.U[1][x_line,stat]
                        self.__tmp_B3_ydir[0][temp_r] = dv**3
                        self.__tmp_B2_ydir[0][temp_r] = dv**2
                        self.__tmp_MD_ydir[0][temp_r] = dV
                    self.__cal_B3_ydir.add_point(self.__tmp_B3_ydir)
                    self.__cal_B2_ydir.add_point(self.__tmp_B2_ydir)
                    self.__cal_MD_ydir.add_point(self.__tmp_MD_ydir)

        self.B3_xdir[:] = self.__cal_B3_xdir.get_mean()[0]
        self.B2_xdir[:] = self.__cal_B2_xdir.get_mean()[0]
        self.meandiff_xdir[:] = self.__cal_MD_xdir.get_mean()[0]
        self.r_xdir[:] = (np.array(list(range(self.ac_length_xdir)))*self.dX[0])[:]

        self.B3_ydir[:] = self.__cal_B3_ydir.get_mean()[0]
        self.B2_ydir[:] = self.__cal_B2_ydir.get_mean()[0]
        self.meandiff_ydir[:] = self.__cal_MD_ydir.get_mean()[0]
        self.r_ydir[:] = (np.array(list(range(self.ac_length_ydir)))*self.dX[1])[:]

        # Eqs. (3.5)-(3.8), stopped before d/dr is applied
        self.Pi_uprime_pre[:] = self.B3_xdir
        self.Pi_vprime_pre[:] = self.B3_ydir
        self.Pi_meanu_pre[:] = self.meandiff_xdir * self.B2_xdir
        self.Pi_meanv_pre[:] = self.meandiff_ydir * self.B2_ydir

        self.report(f'Pi_uprime_pre[r=0]: {self.Pi_uprime_pre[0]:.6g}')
        self.report(f'Pi_vprime_pre[r=0]: {self.Pi_vprime_pre[0]:.6g}')
        self.report(f'Pi_meanu_pre[r=0]: {self.Pi_meanu_pre[0]:.6g}')
        self.report(f'Pi_meanv_pre[r=0]: {self.Pi_meanv_pre[0]:.6g}')

        self.__save()

    def __save(self):
        self.save_nparray_to_bin(self.r_xdir, self.result_path+'/r_xdir.bin')
        self.save_nparray_to_bin(self.r_ydir, self.result_path+'/r_ydir.bin')
        self.save_nparray_to_bin(self.B3_xdir, self.result_path+'/B3_xdir.bin')
        self.save_nparray_to_bin(self.B2_xdir, self.result_path+'/B2_xdir.bin')
        self.save_nparray_to_bin(self.meandiff_xdir, self.result_path+'/meandiff_xdir.bin')
        self.save_nparray_to_bin(self.B3_ydir, self.result_path+'/B3_ydir.bin')
        self.save_nparray_to_bin(self.B2_ydir, self.result_path+'/B2_ydir.bin')
        self.save_nparray_to_bin(self.meandiff_ydir, self.result_path+'/meandiff_ydir.bin')
        self.save_nparray_to_bin(self.Pi_uprime_pre, self.result_path+'/Pi_uprime_pre.bin')
        self.save_nparray_to_bin(self.Pi_vprime_pre, self.result_path+'/Pi_vprime_pre.bin')
        self.save_nparray_to_bin(self.Pi_meanu_pre, self.result_path+'/Pi_meanu_pre.bin')
        self.save_nparray_to_bin(self.Pi_meanv_pre, self.result_path+'/Pi_meanv_pre.bin')

    def load(self):
        self.r_xdir = self.load_nparray_from_bin(self.r_xdir, self.result_path+'/r_xdir.bin')
        self.r_ydir = self.load_nparray_from_bin(self.r_ydir, self.result_path+'/r_ydir.bin')
        self.B3_xdir = self.load_nparray_from_bin(self.B3_xdir, self.result_path+'/B3_xdir.bin')
        self.B2_xdir = self.load_nparray_from_bin(self.B2_xdir, self.result_path+'/B2_xdir.bin')
        self.meandiff_xdir = self.load_nparray_from_bin(self.meandiff_xdir, self.result_path+'/meandiff_xdir.bin')
        self.B3_ydir = self.load_nparray_from_bin(self.B3_ydir, self.result_path+'/B3_ydir.bin')
        self.B2_ydir = self.load_nparray_from_bin(self.B2_ydir, self.result_path+'/B2_ydir.bin')
        self.meandiff_ydir = self.load_nparray_from_bin(self.meandiff_ydir, self.result_path+'/meandiff_ydir.bin')
        self.Pi_uprime_pre = self.load_nparray_from_bin(self.Pi_uprime_pre, self.result_path+'/Pi_uprime_pre.bin')
        self.Pi_vprime_pre = self.load_nparray_from_bin(self.Pi_vprime_pre, self.result_path+'/Pi_vprime_pre.bin')
        self.Pi_meanu_pre = self.load_nparray_from_bin(self.Pi_meanu_pre, self.result_path+'/Pi_meanu_pre.bin')
        self.Pi_meanv_pre = self.load_nparray_from_bin(self.Pi_meanv_pre, self.result_path+'/Pi_meanv_pre.bin')

    # def differentiate(self):
    #     '''
    #     Applies the -d/dr operator to the pre-derivative quantities computed
    #     by calculate() (or restored by load()), giving the actual Pi terms of
    #     Eqs. (3.5)-(3.8). Not called automatically -- call this manually after
    #     calculate()/load() once Pi_*_pre and r_xdir/r_ydir are populated.
    #     '''
    #     self.Pi_uprime[:] = -np.gradient(self.Pi_uprime_pre, self.r_xdir)
    #     self.Pi_vprime[:] = -np.gradient(self.Pi_vprime_pre, self.r_ydir)
    #     self.Pi_meanu[:] = -np.gradient(self.Pi_meanu_pre, self.r_xdir)
    #     self.Pi_meanv[:] = -np.gradient(self.Pi_meanv_pre, self.r_ydir)
 
    #     self.report(f'Pi_uprime[r=0]: {self.Pi_uprime[0]:.6g}')
    #     self.report(f'Pi_vprime[r=0]: {self.Pi_vprime[0]:.6g}')
    #     self.report(f'Pi_meanu[r=0]: {self.Pi_meanu[0]:.6g}')
    #     self.report(f'Pi_meanv[r=0]: {self.Pi_meanv[0]:.6g}')

    def differentiate(self, window_length=9, polyorder=2):
        from scipy.signal import savgol_filter
        '''

        Noise-robust alternative to differentiate(): instead of a plain

        3-point central difference (np.gradient), this fits a local

        polynomial of order `polyorder` (default 2, i.e. a centered

        quadratic -- the classic Savitzky-Golay derivative) inside a sliding

        window of `window_length` points around each r, and evaluates its

        derivative analytically at the center. Because it uses more points

        per estimate and least-squares-fits away high-frequency noise before

        differentiating, it is much less sensitive to scatter in the raw

        Pi_*_pre statistics than differentiate(), at the cost of some

        smoothing/bias near sharp features.



        `window_length` must be odd and <= the number of r points; increase

        it for more smoothing, decrease it (down to polyorder+2, then odd)

        for less. Not called automatically -- call manually, same as

        differentiate().

        '''

        self.Pi_uprime[:] = -savgol_filter(self.Pi_uprime_pre, window_length, polyorder,

                                            deriv=1, delta=self.dX[0], mode='interp')

        self.Pi_vprime[:] = -savgol_filter(self.Pi_vprime_pre, window_length, polyorder,

                                            deriv=1, delta=self.dX[1], mode='interp')

        self.Pi_meanu[:] = -savgol_filter(self.Pi_meanu_pre, window_length, polyorder,

                                           deriv=1, delta=self.dX[0], mode='interp')

        self.Pi_meanv[:] = -savgol_filter(self.Pi_meanv_pre, window_length, polyorder,

                                           deriv=1, delta=self.dX[1], mode='interp')



        self.report(f'[savgol] Pi_uprime[r=0]: {self.Pi_uprime[0]:.6g}')

        self.report(f'[savgol] Pi_vprime[r=0]: {self.Pi_vprime[0]:.6g}')

        self.report(f'[savgol] Pi_meanu[r=0]: {self.Pi_meanu[0]:.6g}')

        self.report(f'[savgol] Pi_meanv[r=0]: {self.Pi_meanv[0]:.6g}')




if __name__ == "__main__":
    cases = ['Case04']
    # cases = [case + '_even' for case in cases]
    SFTs = [() for _ in range(len(cases))]
    for case_id in range(len(cases)):
        pBase.load_case(cases[case_id])
        d_array_nozzle = 12  # mm
        x_lines = int(2*d_array_nozzle/pBase.dX[0])
        y_lines = int(d_array_nozzle/pBase.dX[1])
        print(x_lines,y_lines)
        # x_lines = 1
        # y_lines = 1
        SFTs[case_id] = StructureFunctionTransport(cases[case_id], avg_ylines_for_x = y_lines, avg_xlines_for_y = x_lines)
        SFTs[case_id].calculate()