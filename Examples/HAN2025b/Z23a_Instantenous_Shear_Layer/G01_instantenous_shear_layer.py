''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.1         =
= Date:     2026/01/21  =
=========================
'''

import numpy as np
from pivdataprocessor.A01_toolbox import ProbabilityDensity as PD
from pivdataprocessor.A01_toolbox import float_precsion
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from Z12_Triple_Decomposition.G01_triple_decomposition import TripleDecomposition as TD
from Z23a_Instantenous_Shear_Layer.T01_local_toolbox import compute_mask_lagrange, lagrange_interpolate_with_mask
from Z23a_Instantenous_Shear_Layer.T02_find_crossing import find_threshold_crossings_quadratic_minimal
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as SWC


class ShearLayer(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None):
        super().__init__(casename)
        assert filter in ('gaussian','gaussian_bp','wavelet')
        self.datasource = filter
        self.filter_id = filter_id
        self.td = TD(casename, filter, filter_id)
        self.td.load_avg()

    def prepare_BRF_coordinate(self, zeta_max, N = 60, alpha = 2.5):
        X_BRF = np.zeros((2,2*N+1,2*N+1))
        n = np.arange(-N, N+1)
        zeta = - (zeta_max / alpha) * np.arctanh(np.tanh(alpha) * (1 - (n + N) / N))
        x, y = np.meshgrid(zeta, zeta, indexing="ij")
        X_BRF[0] = x
        X_BRF[1] = y
        self.X_BRF = X_BRF
        self.make_sure_directory(self.result_path + self.td.vfh.middle_path())
        np.save(self.result_path + self.td.vfh.middle_path() + '/X_LSL.npy', X_BRF)

    def calculate_general(self, n_list:list, deg_ranges=((0,30),)):
        X = self.X_BRF[0]
        ic, jc = len(X[:,0])//2, len(X[0,:])//2
        if deg_ranges is None:
            result_path = self.result_path + self.td.vfh.middle_path() + '/general'
            self.rm_and_create_directory(result_path)
        else:
            deg_folder = '/deg'
            for deg_range in deg_ranges:
                deg_folder = deg_folder + f'_{deg_range[0]:.1f}to{deg_range[1]:.1f}'
            result_path = self.result_path + self.td.vfh.middle_path() + deg_folder
            self.rm_and_create_directory(result_path)

        self.result_json = PT(result_path+"/result.json")
        self.result_json.set(1, n_list = n_list)

        v_jump_array = np.zeros_like(n_list,dtype=float_precsion)

        identified_LSL_number = 0
        effective_instan_LSL = 0
        ','
        
        left, right, bottom, up = self.td.vfh.unpackrange(self.td.effctive_range)
        swc = SWC(v_jump_array.shape)
        for run_id in range(len(self.td.frames_in_runs)):
            for frame_id in range(self.td.frames_in_runs[run_id]):
                self.td.cal_and_identify_SH_layer_frame(run_id, frame_id, coef_threshold=1.5)
                identified_pos = self.td.identified_pos.copy()
                if deg_ranges is not None:
                    dir_e2x = self.td.Q[0,1]
                    dir_e2y = self.td.Q[1,1]
                    angle = np.degrees(np.arctan2(dir_e2y, dir_e2x))
                    condition_angle = np.zeros_like(angle, dtype = bool)
                    for deg_range in deg_ranges:
                        range_tmp = (angle > deg_range[0]) & (angle < deg_range[1])
                        condition_angle[range_tmp] = True
                    range_not_finite = ~(np.isfinite(dir_e2x) & np.isfinite(dir_e2y))
                    condition_angle[range_not_finite] = False
                    identified_pos = identified_pos & condition_angle

                ixs, iys = np.where(identified_pos)
                identified_LSL_number += len(ixs)
                for SL_id in range(len(ixs)):
                    ix = ixs[SL_id]
                    iy = iys[SL_id]
                    
                    tmp_Is = np.full_like(self.X_BRF[0], np.nan, dtype=float_precsion)
                    ','

                    Q_from_BRF_to_LAB = self.td.Q[:,:,ix,iy]
                    dudy_S = self.td.BRF_dUdX_shear[0,1,ix,iy]

                    X_BRF_in_LAB = np.einsum('ij,jkl->ikl', Q_from_BRF_to_LAB, self.X_BRF)
                    X0 = self.td.X[:, ix, iy].astype(float_precsion)
                    X_BRF_in_LAB += X0[:, None, None]   
                    mask_inside = compute_mask_lagrange(self.td.X, X_BRF_in_LAB, left, right, bottom, up)
                    mask_row = np.zeros_like(mask_inside, dtype=bool)
                    mask_row[ic, :] = mask_inside[ic, :]
                    tmp_Is[mask_row] = lagrange_interpolate_with_mask(self.td.X, X_BRF_in_LAB, self.td.intensity_shear, mask_row)[mask_row]          
                    
                    ','
                    norm_Is = tmp_Is / tmp_Is[ic,jc]
                    thickness = find_threshold_crossings_quadratic_minimal(self.X_BRF[1,ic,:],norm_Is[ic,:],ic=jc,thr=0.5)
                    if thickness is None:
                        continue 

                    effective_instan_LSL+=1
                    velocity_jump = -dudy_S*thickness/1000.0
                    for i,_ in enumerate(v_jump_array):
                        # v_jump_array[i] += velocity_jump**n_list[i]
                        v_jump_array[i] = velocity_jump**n_list[i]
                    swc.add_point(v_jump_array)
        v_jump_array = swc.get_mean()
        # v_jump_array = v_jump_array/effective_instan_LSL
        v_jump_array = list(v_jump_array)
        self.result_json.set(1, v_jump_array = v_jump_array)
        self.load_result(deg_ranges)

    def load_result(self, deg_ranges=None):
        self.X_BRF = np.load(self.result_path + self.td.vfh.middle_path() + '/X_LSL.npy')
        if deg_ranges == None:
            result_path = self.result_path + self.td.vfh.middle_path() + '/general'
        else :
            deg_folder = '/deg'
            for deg_range in deg_ranges:
                deg_folder = deg_folder + f'_{deg_range[0]:.1f}to{deg_range[1]:.1f}'
            result_path = self.result_path + self.td.vfh.middle_path() + deg_folder
        self.result_json = PT(result_path+"/result.json")




def worker(args):
    case, filter, p, Lf, deg_ranges, n_list  = args
    sl = ShearLayer(case, filter, filter_id=p)
    if filter == 'gaussian':
        coef = 7.5

    sl.prepare_BRF_coordinate(coef*Lf, N=100)
    print (f'Started:{args}')
    sl.calculate_general(n_list, deg_ranges)
    return print (f'Finished:{args}')

if __name__ == '__main__':
    from ZZZ_Result_Manager.A01_cases import cases_select, cases_select_f,cases_select_w, coeffs_to_eta
    from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
    from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
    from multiprocessing import Pool  

    filter = 'gaussian'
    n_list = [i for i in range(1,10)]
    deg_ranges = None
    with Pool() as pool:
        tasks = []
        for case_id, case in enumerate(cases_select):
            for coeff_id, coeff in enumerate(coeffs_to_eta):
                coeff_id += 1
                filter_params = coeff_id
                ds = DS(cases_select_f[case_id], 'gaussian',-1)
                eta = ds.result_json.get(0)['eta']*1000
                Lf = eta * coeff
                tasks.append((cases_select_w[case_id], filter, coeff_id, Lf, deg_ranges, n_list))
        results = pool.map(worker, tasks)  

    # for deg in degs:
    #     with Pool() as pool:
    #         tasks = []
    #         for case_id, case in enumerate(cases):
    #             for filter_id, filter_param in enumerate(filter_params):
    #                 rm = RM(case)
    #                 Lf = rm.result_table.get(2)['Lfs'][filter_id]
    #                 tasks.append((case, filter, filter_param, Lf, deg, n_list))
    #         results = pool.map(worker, tasks)  
