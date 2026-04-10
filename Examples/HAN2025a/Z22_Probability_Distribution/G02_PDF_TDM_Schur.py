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
from Z12_Schur_Decomposition.G01_schur_decomposition import SchurDecomposition as SD
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH

class PDF_TDM_Schur(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None):
        super().__init__(casename)
        assert filter in ('gaussian','gaussian_bp','wavelet')
        self.datasource = filter
        self.filter_id = filter_id
        self.td = TD(casename, filter, filter_id)
        self.sd = SD(casename, filter, filter_id)
        self.result_json = PT(self.result_path + self.td.vfh.middle_path()+"/result.json")
        self.PDF_E_NS_x = None
        self.PDF_E_NS_y = None
        self.PDF_R_NO_x = None
        self.PDF_R_NO_y = None
        self.PDF_S_NN_x = None
        self.PDF_S_NN_y = None

    def calculate(self, bins=100, hist_range=None):
        result_path = self.result_path + self.td.vfh.middle_path()
        self.rm_and_create_directory(result_path)
        left,right,bottom,up = VFH.unpackrange(self.td.effctive_range)
        frames_in_runs = self.td.frames_in_runs
        PD_E_NS = PD(bins=bins, hist_range=hist_range)
        PD_R_NO = PD(bins=bins, hist_range=hist_range)
        PD_S_NN = PD(bins=bins, hist_range=hist_range)
        for run_ID in range(len(frames_in_runs)):
            print(f'  run ID {run_ID}')
            for frame_ID in range(frames_in_runs[run_ID]):
                self.td.cal_frame(run_ID, frame_ID)
                self.sd.cal_frame(run_ID, frame_ID)
                E_NS = (self.td.intensity_elongation/self.sd.i_B_s)[left:right,bottom:up]
                R_NO = (self.td.intensity_rotation/self.sd.i_B_o)[left:right,bottom:up]
                S_NN = (self.td.intensity_shear/self.sd.i_C)[left:right,bottom:up]
                PD_E_NS.add_point(E_NS)
                PD_R_NO.add_point(R_NO)
                PD_S_NN.add_point(S_NN)
        PD_E_NS.process_hist()
        PD_R_NO.process_hist()
        PD_S_NN.process_hist()
        self.PDF_E_NS_x = PD_E_NS.KDE_x
        self.PDF_E_NS_y = PD_E_NS.KDE_y
        self.PDF_R_NO_x = PD_R_NO.KDE_x
        self.PDF_R_NO_y = PD_R_NO.KDE_y
        self.PDF_S_NN_x = PD_S_NN.KDE_x
        self.PDF_S_NN_y = PD_S_NN.KDE_y
        np.save(result_path + "/PDF_E_NS_x.npy", self.PDF_E_NS_x)
        np.save(result_path + "/PDF_E_NS_y.npy", self.PDF_E_NS_y)
        np.save(result_path + "/PDF_R_NO_x.npy", self.PDF_R_NO_x)
        np.save(result_path + "/PDF_R_NO_y.npy", self.PDF_R_NO_y)        
        np.save(result_path + "/PDF_S_NN_x.npy", self.PDF_S_NN_x)
        np.save(result_path + "/PDF_S_NN_y.npy", self.PDF_S_NN_y)
 
    def load_result(self):
        result_path = self.result_path + self.td.vfh.middle_path()
        self.PDF_E_NS_x = np.load(result_path + "/PDF_E_NS_x.npy")
        self.PDF_E_NS_y = np.load(result_path + "/PDF_E_NS_y.npy")
        self.PDF_R_NO_x = np.load(result_path + "/PDF_R_NO_x.npy")
        self.PDF_R_NO_y = np.load(result_path + "/PDF_R_NO_y.npy")
        self.PDF_S_NN_x = np.load(result_path + "/PDF_S_NN_x.npy")
        self.PDF_S_NN_y = np.load(result_path + "/PDF_S_NN_y.npy")


def worker(args):
    case, filter, p, bins, hist_range = args
    pdf = PDF_TDM_Schur(case, filter, filter_id=p)
    return pdf.calculate(bins=bins,hist_range=hist_range)
if __name__ == '__main__':
    filter_id = 5
    from ZZZ_Result_Manager.A01_cases import cases, gaussian_id
    from multiprocessing import Pool  
    with Pool() as pool:
        tasks = []
        for case in cases:
            tasks.append((case, 'gaussian', filter_id, 500, (0,3)))
        results = pool.map(worker, tasks)    

