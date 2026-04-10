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
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH

class DissipationRate(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None):
        super().__init__(casename)
        assert filter in ('gaussian','gaussian_bp','wavelet')
        self.datasource = filter
        self.filter_id = filter_id
        self.vfh = VFH(casename, filter, filter_id)
        self.vfh.load_X()
        self.vfh.load_field(0,0)
        self.result_json = PT(self.result_path + self.vfh.middle_path()+"/result.json")


    def calculate(self, kinematic_viscosity=1.6e-5):
        result_path = self.result_path + self.vfh.middle_path()
        self.rm_and_create_directory(result_path)

        self.result_json.set(0, kinematic_viscosity=kinematic_viscosity)
        left, right, bottom, up = VFH.unpackrange(self.vfh.effctive_range)

        shape = self.vfh.u[0].shape
        DissipationRate_swc = swc(shape=shape)
        urms_swc = swc(shape=shape)
        vrms_swc = swc(shape=shape)
        dudx_rms_swc = swc(shape=shape)
        dvdy_rms_swc = swc(shape=shape)
        dudy_rms_swc = swc(shape=shape)
        dvdx_rms_swc = swc(shape=shape)
        
        frames_in_runs = self.vfh.frames_in_runs
        for run_ID in range(len(frames_in_runs)):
            for frame_ID in range(frames_in_runs[run_ID]):
                self.vfh.load_field(run_ID,frame_ID)
                fluc_U = self.vfh.u
                fluc_dUdX = self.vfh.dudx
                urms_swc.add_point(fluc_U[0, :, :]*fluc_U[0, :, :])
                vrms_swc.add_point(fluc_U[1, :, :]*fluc_U[1, :, :])
                dudx_rms_swc.add_point(fluc_dUdX[0,0, :, :]*fluc_dUdX[0,0, :, :])
                dvdy_rms_swc.add_point(fluc_dUdX[1,1, :, :]*fluc_dUdX[1,1, :, :])
                dudy_rms_swc.add_point(fluc_dUdX[0,1, :, :]*fluc_dUdX[0,1, :, :])
                dvdx_rms_swc.add_point(fluc_dUdX[1,0, :, :]*fluc_dUdX[1,0, :, :])

                tmp = 4*fluc_dUdX[0,0, :, :]*fluc_dUdX[0,0, :, :]
                tmp += 4*fluc_dUdX[1,1, :, :]*fluc_dUdX[1,1, :, :]
                tmp += 3*fluc_dUdX[0,1, :, :]*fluc_dUdX[0,1, :, :]
                tmp += 3*fluc_dUdX[1,0, :, :]*fluc_dUdX[1,0, :, :]
                tmp += 4*fluc_dUdX[0,0, :, :]*fluc_dUdX[1,1, :, :]
                tmp += 6*fluc_dUdX[0,1, :, :]*fluc_dUdX[1,0, :, :]
                DissipationRate_swc.add_point(kinematic_viscosity*tmp)
        
        e_range = (slice(left, right), slice(bottom, up))
        DissipationRate = np.mean(DissipationRate_swc.get_mean()[e_range])
        urms = np.sqrt(np.mean(urms_swc.get_mean()[e_range]))
        vrms = np.sqrt(np.mean(vrms_swc.get_mean()[e_range]))

        dudx_rms = np.sqrt(np.mean(dudx_rms_swc.get_mean()[e_range]))
        dvdy_rms = np.sqrt(np.mean(dvdy_rms_swc.get_mean()[e_range]))
        dudy_rms = np.sqrt(np.mean(dudy_rms_swc.get_mean()[e_range]))
        dvdx_rms = np.sqrt(np.mean(dvdx_rms_swc.get_mean()[e_range]))

        lambda_x = urms / dudx_rms
        lambda_y = vrms / dvdy_rms
        Re_lambda_x = urms * lambda_x / kinematic_viscosity
        Re_lambda_y = vrms * lambda_y / kinematic_viscosity
        eta = (kinematic_viscosity**3/DissipationRate)**(1/4)
        dx = float(self.vfh.X[0,1,1]-self.vfh.X[0,0,0])
        val = self.vfh.scale_in_grid
        if isinstance(val, (list, tuple, np.ndarray)):
            scale_in_grid = float(np.max(val))
        else:
            scale_in_grid = float(val)
        dx_over_eta = scale_in_grid * dx / 1000 / eta
        self.result_json.set(0, scale_in_grid = self.vfh.scale_in_grid)
        self.result_json.set(0, urms = urms) 
        self.result_json.set(0, vrms = vrms) 
        self.result_json.set(0, dudx_rms = dudx_rms)
        self.result_json.set(0, dvdy_rms = dvdy_rms)
        self.result_json.set(0, dudy_rms = dudy_rms)
        self.result_json.set(0, dvdx_rms = dvdx_rms)
        self.result_json.set(0, ratio_dudx_dvdy_rms = dudx_rms/dvdy_rms)
        self.result_json.set(0, ratio_dudy_dvdx_rms = dudy_rms/dvdx_rms)

        self.result_json.set(0, Re_lambda_x = Re_lambda_x)       
        self.result_json.set(0, Re_lambda_y = Re_lambda_y)
        self.result_json.set(0, dx_over_eta = dx_over_eta)
        self.result_json.set(0, DissipationRate = DissipationRate)



def worker(args):
    case, filter, p = args
    ds = DissipationRate(case, filter, filter_id=p)
    return ds.calculate()
if __name__ == '__main__':
    from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
    from ZZZ_Result_Manager.A01_cases import cases, gaussian_id
    from multiprocessing import Pool  

    print('Gaussian_lowpass')
    for filter_param in gaussian_id:
        print(f'filter : {filter_param}')
        tasks = []
        with Pool() as pool:
            for case in cases[:-1]:
                tasks.append((case, 'gaussian', filter_param))
            results = pool.map(worker, tasks)   