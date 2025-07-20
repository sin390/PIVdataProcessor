''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/07/08  =
=========================
'''

import numpy as np
from dataclasses import dataclass
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L01_base import GeneralDataHandler as GDH
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as swc


@dataclass
class DissipationRateInfo(GDH):
    Case_name:str = None
    Kinematic_viscosity:float_precsion = None
    DissipationRate:float_precsion = None
    urms:float_precsion = None
    vrms:float_precsion = None
    lambda_x:float_precsion = None
    lambda_y:float_precsion = None
    Re_lambda_x:float_precsion = None
    Re_lambda_y:float_precsion = None
    eta:float_precsion = None
    dx_over_eta:float_precsion = None

class DissipationRate(pTS):
    def __init__(self, casename, kinematic_viscosity=1.6e-5):
        super().__init__(casename)
        self.Result = DissipationRateInfo()
        self.kinematic_viscosity = kinematic_viscosity


    def calculate(self):
        pBase.rm_and_create_directory(self.result_path)
        self.Result.Case_name = self.CaseInfo.CaseName
        self.Result.Kinematic_viscosity = self.kinematic_viscosity
 
        left,right = self.CaseInfo.Uniform_Range[0]
        bottom,up = self.CaseInfo.Uniform_Range[1]
        shape = (right+1 - left, up+1 - bottom)
        DissipationRate_swc = swc(shape=shape)
        urms_swc = swc(shape=shape)
        vrms_swc = swc(shape=shape)
        dudx_rms_swc = swc(shape=shape)
        dvdy_rms_swc = swc(shape=shape)
 
        for run_ID in range(len(pBase.frame_numbers_in_runs)):
            for frame_ID in range(pBase.frame_numbers_in_runs[run_ID]):
                pBase.base_load_data_all(run_ID,frame_ID)
                fluc_U = pBase.fluc_U[:, left:right+1, bottom:up+1]
                fluc_dUdX = pBase.fluc_dUdX[:,:, left:right+1, bottom:up+1]
                urms_swc.add_point(fluc_U[0, :, :]*fluc_U[0, :, :])
                vrms_swc.add_point(fluc_U[1, :, :]*fluc_U[1, :, :])
                dudx_rms_swc.add_point(fluc_dUdX[0,0, :, :]*fluc_dUdX[0,0, :, :])
                dvdy_rms_swc.add_point(fluc_dUdX[1,1, :, :]*fluc_dUdX[1,1, :, :])

                tmp = 4*fluc_dUdX[0,0, :, :]*fluc_dUdX[0,0, :, :]
                tmp += 4*fluc_dUdX[1,1, :, :]*fluc_dUdX[1,1, :, :]
                tmp += 3*fluc_dUdX[0,1, :, :]*fluc_dUdX[0,1, :, :]
                tmp += 3*fluc_dUdX[1,0, :, :]*fluc_dUdX[1,0, :, :]
                tmp += 4*fluc_dUdX[0,0, :, :]*fluc_dUdX[1,1, :, :]
                tmp += 6*fluc_dUdX[0,1, :, :]*fluc_dUdX[1,0, :, :]
                DissipationRate_swc.add_point(self.kinematic_viscosity*tmp)
        
        self.Result.DissipationRate = float(np.mean(DissipationRate_swc.get_mean()))
        self.Result.urms = float(np.sqrt(np.mean(urms_swc.get_mean())))
        self.Result.vrms = float(np.sqrt(np.mean(vrms_swc.get_mean())))
        self.Result.lambda_x = float(self.Result.urms / np.sqrt(np.mean(dudx_rms_swc.get_mean())))
        self.Result.lambda_y = float(self.Result.vrms / np.sqrt(np.mean(dvdy_rms_swc.get_mean())))
        self.Result.Re_lambda_x = self.Result.urms * self.Result.lambda_x / self.kinematic_viscosity
        self.Result.Re_lambda_y = self.Result.vrms * self.Result.lambda_y / self.kinematic_viscosity
        self.Result.eta = (self.kinematic_viscosity**3/self.Result.DissipationRate)**(1/4)
        self.Result.dx_over_eta = float(self.dX[0]/1000 / self.Result.eta)
        self.Result.to_yaml(self.result_path +'/DissipationRate.yaml')

    def load(self):
        self.Result = self.Result.from_yaml(self.result_path +'/DissipationRate.yaml')

if __name__ == "__main__":
    cases = ['All100','Grad','AntiGrad','Shear']
    for case_id in range(len(cases)):
        DR = DissipationRate(cases[case_id])
        DR.calculate()

