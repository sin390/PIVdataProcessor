''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''
import numpy as np
from numpy.polynomial.polynomial import polyvander2d, polyval2d
from numpy.linalg import lstsq

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from Z02_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT

class FittedSlope(pTS):  
    def __init__(self, casename):
        super().__init__(casename)
        self.casename = pBase.CaseInfo.CaseName
        self.effctive_range = pBase.CaseInfo.Effective_Range
        self.fit_avg_dUdX = pBase.get_a_container(2)
        self.fit_avg_U = pBase.get_a_container(1)
        self.result_json = PT(self.result_path + "/result.json")

    def calculate(self, order = 3):
        pBase.rm_and_create_directory(self.result_path)
        left,right = self.effctive_range[0]
        bottom,up = self.effctive_range[1]

        x_ravel = pBase.X[0][left:right,bottom:up].flatten() 
        y_ravel = pBase.X[1][left:right,bottom:up].flatten()
        X = polyvander2d(x_ravel, y_ravel, [order, order])
        order1= order+1

        'U'
        coeffs, *_ = lstsq(X, pBase.avg_U[0][left:right,bottom:up].flatten(), rcond=None)
        a_U = coeffs.reshape((order+1, order+1))

        self.fit_avg_U[0][left:right,bottom:up] = sum(a_U[i, j] * x_ravel**i * y_ravel**j for i in range(order1) for j in range(order1)).reshape(right-left,up-bottom)
        self.fit_avg_dUdX[0][0][left:right,bottom:up] = sum(i * a_U[i, j] * x_ravel**(i - 1) * y_ravel**j for i in range(1, order1) for j in range(order1)).reshape(right-left,up-bottom)
        self.fit_avg_dUdX[0][1][left:right,bottom:up] = sum(j * a_U[i, j] * x_ravel**i * y_ravel**(j - 1) for i in range(order1) for j in range(1,order1)).reshape(right-left,up-bottom)

        'V'
        coeffs, *_ = lstsq(X, pBase.avg_U[1][left:right,bottom:up].flatten(), rcond=None)
        a_V = coeffs.reshape((order+1, order+1))
        self.fit_avg_U[1][left:right,bottom:up] = sum(a_V[i, j] * x_ravel**i * y_ravel**j for i in range(order1) for j in range(order1)).reshape(right-left,up-bottom)
        self.fit_avg_dUdX[1][0][left:right,bottom:up] = sum(i * a_V[i, j] * x_ravel**(i - 1) * y_ravel**j for i in range(1, order1) for j in range(order1)).reshape(right-left,up-bottom)
        self.fit_avg_dUdX[1][1][left:right,bottom:up] = sum(j * a_V[i, j] * x_ravel**i * y_ravel**(j - 1) for i in range(order1) for j in range(1,order1)).reshape(right-left,up-bottom)

        self.__save()                  

    def __save(self):
        left,right = self.effctive_range[0]
        bottom,up = self.effctive_range[1]
        self.save_nparray_to_bin(self.fit_avg_U, self.result_path+'/fit_avg_U.bin')
        self.save_nparray_to_bin(self.fit_avg_dUdX, self.result_path+'/fit_slope.bin')
        A11_avg = np.mean(self.fit_avg_dUdX[0,0][left:right,bottom:up])*1000
        A12_avg = np.mean(self.fit_avg_dUdX[0,1][left:right,bottom:up])*1000
        A21_avg = np.mean(self.fit_avg_dUdX[1,0][left:right,bottom:up])*1000
        A22_avg = np.mean(self.fit_avg_dUdX[1,1][left:right,bottom:up])*1000
        S= np.sqrt((self.fit_avg_dUdX[0,0]**2 + self.fit_avg_dUdX[0,1]**2 + self.fit_avg_dUdX[1,0]**2 + self.fit_avg_dUdX[1,1]**2)/1)
        S_avg = np.mean(S[left:right,bottom:up])*1000
        self.result_json.set(0,A11_avg = A11_avg)
        self.result_json.set(0,A12_avg = A12_avg)
        self.result_json.set(0,A21_avg = A21_avg)
        self.result_json.set(0,A22_avg = A22_avg)
        self.result_json.set(0,S_avg = S_avg)
        self.result_json.set(0,A11_nor = A11_avg/S_avg)
        self.result_json.set(0,A12_nor = A12_avg/S_avg)
        self.result_json.set(0,A21_nor = A21_avg/S_avg)
        self.result_json.set(0,A22_nor = A22_avg/S_avg)
        self.result_json.set(0,A11_A22 = A11_avg/A22_avg)

    def load_fitted(self):
        self.fit_avg_U = self.load_nparray_from_bin(self.fit_avg_U, self.result_path+'/fit_avg_U.bin')
        self.fit_avg_dUdX = self.load_nparray_from_bin(self.fit_avg_dUdX, self.result_path+'/fit_slope.bin')
        

if __name__ == "__main__":
    from ZZZ_Result_Manager.A01_cases import cases_w, case_labels, cases_f
    for case_id in range(len(cases_f)):
        fitted_cases = FittedSlope(cases_f[case_id])
        fitted_cases.calculate(order=2)
        xc,yc = pBase.CaseInfo.Central_Position_Grid
        fitted_cases.report(f'Case : {cases_w[case_id]}')
        fitted_cases.report(f'S11@xc,yc : {fitted_cases.fit_avg_dUdX[0][0][xc,yc]*1000} (s^-1)')
        left,right = pBase.CaseInfo.Effective_Range[0]
        bottom, up = pBase.CaseInfo.Effective_Range[1]
        fitted_cases.report(f'S11_max : {np.nanmin(fitted_cases.fit_avg_dUdX[0][0][left:right,bottom:up])*1000} (s^-1)')
        fitted_cases.report(f'S11_avg : {np.nanmean(fitted_cases.fit_avg_dUdX[0][0][left:right,bottom:up])*1000} (s^-1)')
        fitted_cases.report(f'S22_max : {np.nanmax(fitted_cases.fit_avg_dUdX[1][1][left:right,bottom:up])*1000} (s^-1)')
        fitted_cases.report(f'S22_avg : {np.nanmean(fitted_cases.fit_avg_dUdX[1][1][left:right,bottom:up])*1000} (s^-1)')