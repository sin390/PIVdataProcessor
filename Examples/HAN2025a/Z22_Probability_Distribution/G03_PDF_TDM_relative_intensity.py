''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2026/01/16  =
=========================
'''

import numpy as np
from pivdataprocessor.A01_toolbox import ProbabilityDensity as PD
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from Z11_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH

class PDF_TDM_relative_intensity(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None):
        super().__init__(casename)
        assert filter in ('gaussian','gaussian_bp','wavelet')
        self.datasource = filter
        self.filter_id = filter_id
        self.td = TD(casename, filter, filter_id)
        self.result_json = PT(self.result_path + self.td.vfh.middle_path()+"/result.json")
        self.PDF_S_omega_x = None
        self.PDF_S_omega_y = None
        self.PDF_R_omega_x = None
        self.PDF_R_omega_y = None

    def calculate(self, bins=100, hist_range=None):
        result_path = self.result_path + self.td.vfh.middle_path()
        self.rm_and_create_directory(result_path)
        left,right,bottom,up = VFH.unpackrange(self.td.effctive_range)
        frames_in_runs = self.td.frames_in_runs
        PD_S_omega = PD(bins=bins, hist_range=hist_range)
        PD_R_omega = PD(bins=bins, hist_range=hist_range)
        ref_mag_omega= self.td.result_json.get(0)['avg_intensity_Mag_Omega']
        for run_ID in range(len(frames_in_runs)):
            print(f'  run ID {run_ID}')
            for frame_ID in range(frames_in_runs[run_ID]):
                self.td.cal_frame(run_ID, frame_ID)
                S_omega = (self.td.intensity_shear/ref_mag_omega)[left:right,bottom:up]
                R_omega = (self.td.intensity_rotation/ref_mag_omega)[left:right,bottom:up]
                PD_S_omega.add_point(S_omega)
                PD_R_omega.add_point(R_omega)
        PD_S_omega.process_hist()
        PD_R_omega.process_hist()
        self.PDF_S_omega_x = PD_S_omega.KDE_x
        self.PDF_S_omega_y = PD_S_omega.KDE_y
        self.PDF_R_omega_x = PD_R_omega.KDE_x
        self.PDF_R_omega_y = PD_R_omega.KDE_y
        np.save(result_path + "/PDF_S_omega_x.npy", self.PDF_S_omega_x)
        np.save(result_path + "/PDF_S_omega_y.npy", self.PDF_S_omega_y)
        np.save(result_path + "/PDF_R_omega_x.npy", self.PDF_R_omega_x)
        np.save(result_path + "/PDF_R_omega_y.npy", self.PDF_R_omega_y)        
 
    def load_result(self):
        result_path = self.result_path + self.td.vfh.middle_path()
        self.PDF_S_omega_x = np.load(result_path + "/PDF_S_omega_x.npy")
        self.PDF_S_omega_y = np.load(result_path + "/PDF_S_omega_y.npy")
        self.PDF_R_omega_x = np.load(result_path + "/PDF_R_omega_x.npy")
        self.PDF_R_omega_y = np.load(result_path + "/PDF_R_omega_y.npy")

def worker(args):
    case, filter, p, bins, hist_range = args
    pdf = PDF_TDM_relative_intensity(case, filter, filter_id=p)
    return pdf.calculate(bins=bins,hist_range=hist_range)
if __name__ == '__main__':
    from Z01_Filtered_Velocity_Field.H01_gaussian_params import selected_k1L1, k1L1_label, gaussian_id, gaussian_bp_id, L11_cases, cases
    from multiprocessing import Pool 
    print('Gaussian_bandpass')
    for filter_param in gaussian_bp_id:
        print(f'filter : {filter_param}')
        tasks = []
        with Pool() as pool:
            for case in cases:
                tasks.append((case, 'gaussian_bp', filter_param, 500, (0,4)))
            results = pool.map(worker, tasks)    

    print('Gaussian_lowpass')
    for filter_param in gaussian_id:
        print(f'filter : {filter_param}')
        tasks = []
        with Pool() as pool:
            for case in cases:
                tasks.append((case, 'gaussian', filter_param, 500, (0,4)))
            results = pool.map(worker, tasks)   