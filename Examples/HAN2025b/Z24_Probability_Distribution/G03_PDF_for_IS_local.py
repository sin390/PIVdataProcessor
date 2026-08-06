''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/17  =
=========================
'''

import numpy as np
from pivdataprocessor.A01_toolbox import ProbabilityDensity as PD
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from Z12_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD
from Z02_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH

class PDF_for_IS(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None):
        super().__init__(casename)
        assert filter in ('gaussian','gaussian_bp','wavelet')
        self.datasource = filter
        self.filter_id = filter_id
        self.td = TD(casename, filter, filter_id)
        self.td.load_avg()
        self.PDF_x = None
        self.PDF_y = None

    def calculate(self, bins=100, hist_range_coef_to_avg=None, coef_threshold = 2, location = [50,50], windowsize = 2):
        result_path = self.result_path + self.td.vfh.middle_path()
        result_path = result_path+ f'/Cth_{int(coef_threshold*1000)}'
        self.rm_and_create_directory(result_path)
        self.result_json = PT(result_path+"/result.json")
        left,right,bottom,up = [location[0]-windowsize, location[0]+windowsize, location[1]-windowsize, location[1]+windowsize]
        I_SH_avg = np.nanmean(self.td.avg_intensity_shear[left:right,bottom:up])

        PD_for_Ish = PD(bins=bins, hist_range=np.array(hist_range_coef_to_avg)*I_SH_avg)

        frames_in_runs = self.td.frames_in_runs
        for run_ID in range(len(frames_in_runs)):
            print(f'  run ID {run_ID}')
            for frame_ID in range(frames_in_runs[run_ID]):
                self.td.cal_frame(run_ID,frame_ID,if_adjust_direction=True)
                PD_for_Ish.add_point(self.td.intensity_shear[left:right,bottom:up])

        PD_for_Ish.process_hist()
        x = PD_for_Ish.KDE_x/I_SH_avg
        y = PD_for_Ish.KDE_y*I_SH_avg
        self.PDF_x = x
        self.PDF_y = y


def worker(args):
    case, filter, p, bins, hist_range = args
    pdf = PDF_for_IS(case, filter, filter_id=p)
    return pdf.calculate(bins=bins,hist_range_coef_to_avg = hist_range, coef_threshold = 1.5)

if __name__ == '__main__':
    from multiprocessing import Pool 
    from ZZZ_Result_Manager.A01_cases import cases_select,cases_select_w,cases_select_f,coeffs_to_eta
    from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM

    bins = 100
    range_to_Ish_avg = [0,5]

    print('Gaussian_lowpass')
    filter = 'gaussian'
    for filter_id, _ in enumerate(coeffs_to_eta): 
        filter_param = filter_id+1
        tasks = []
        with Pool() as pool:
            for case in cases_select_w:
                tasks.append((case, filter, filter_param, bins, range_to_Ish_avg))
            results = pool.map(worker, tasks)   