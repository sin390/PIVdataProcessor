''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.1         =
= Date:     2026/01/21  =
=========================
'''

import numpy as np
from pivdataprocessor.A01_toolbox import ProbabilityDensity as PD
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from Z11_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD

class PDF_for_e2x(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None):
        super().__init__(casename)
        assert filter in ('gaussian','gaussian_bp','wavelet')
        self.datasource = filter
        self.filter_id = filter_id
        self.td = TD(casename, filter, filter_id)
        self.td.load_avg()
        self.result_json = PT(self.result_path + self.td.vfh.middle_path()+"/result.json")
        self.PDF_x = None
        self.PDF_y = None


    def calculate(self,bins=100, hist_range=None):
        result_path = self.result_path + self.td.vfh.middle_path()
        self.rm_and_create_directory(result_path)
        total_SH_layer = 0
        PD_for_e2x = PD(bins=bins, hist_range=hist_range)
        frames_in_runs = self.td.frames_in_runs
        for run_ID in range(len(frames_in_runs)):
            print(f'  run ID {run_ID}')
            for frame_ID in range(frames_in_runs[run_ID]):
                self.td.cal_and_identify_SH_layer_frame(run_ID,frame_ID,coef_threshold=1.5)
                X, Y = np.where(self.td.identified_pos)
                if len(X) == 0:
                    continue

                dir_e2x = self.td.Q[0,1][X, Y]
                dir_e2y = self.td.Q[1,1][X, Y]

                valid = np.isfinite(dir_e2x) & np.isfinite(dir_e2y)
                dir_e2x = dir_e2x[valid]
                dir_e2y = dir_e2y[valid]

                angle = np.degrees(np.arctan2(dir_e2y, dir_e2x))
                # angle = np.mod(angle, 180.0)

                PD_for_e2x.add_point(angle)
                total_SH_layer += len(angle)
        PD_for_e2x.process_hist()
        x = PD_for_e2x.KDE_x
        y = PD_for_e2x.KDE_y
        self.PDF_x = x
        self.PDF_y = y
        np.save(result_path + "/PDF_for_e2x_x.npy", x)
        np.save(result_path + "/PDF_for_e2x_y.npy", y)
        self.result_json.set(0, total_SH_layer=total_SH_layer)
 
    def load_result(self):
        result_path = self.result_path + self.td.vfh.middle_path()
        self.PDF_x = np.load(result_path + "/PDF_for_e2x_x.npy")
        self.PDF_y = np.load(result_path + "/PDF_for_e2x_y.npy")


def worker(args):
    case, filter, p, bins, hist_range = args
    pdf = PDF_for_e2x(case, filter, filter_id=p)
    return pdf.calculate(bins=bins,hist_range=hist_range)

if __name__ == '__main__':
    from ZZZ_Result_Manager.A01_cases import cases, degs, gaussian_id
    from multiprocessing import Pool 

    d_deg = 10
    deg_range = (0, 180)
    bins = int((deg_range[1]-deg_range[0])/d_deg)+1

    print('Gaussian_lowpass')
    for filter_param in gaussian_id:
        print(f'filter : {filter_param}')
        tasks = []
        with Pool() as pool:
            for case in cases:
                tasks.append((case, 'gaussian', filter_param, bins, deg_range))
            results = pool.map(worker, tasks)   