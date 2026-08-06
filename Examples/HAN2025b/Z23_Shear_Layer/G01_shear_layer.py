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
from Z23_Shear_Layer.T01_local_toolbox import compute_mask_lagrange, lagrange_interpolate_with_mask

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

    def calculate_general(self, deg_ranges=((0,30),), Cth = 1.5):
        if deg_ranges == None:
            result_path = self.result_path + self.td.vfh.middle_path() + '/general'
        else:
            deg_folder = '/deg'
            for deg_range in deg_ranges:
                deg_folder = deg_folder + f'_{deg_range[0]:.1f}to{deg_range[1]:.1f}'
            result_path = self.result_path + self.td.vfh.middle_path() + deg_folder
        result_path = result_path+ f'/Cth_{int(Cth*1000)}'
        self.rm_and_create_directory(result_path)

        self.result_json = PT(result_path+"/result.json")
        identified_LSL_number = 0
        LSL_count_pos = np.zeros_like(self.X_BRF[0], dtype=np.int32)
        avg_u_BRF = np.zeros_like(self.X_BRF, dtype=float_precsion)
        avg_Is_BRF = np.zeros_like(self.X_BRF[0], dtype=float_precsion)
        avg_omega_s_BRF = np.zeros_like(self.X_BRF[0], dtype=float_precsion)
        avg_omega_r_BRF = np.zeros_like(self.X_BRF[0], dtype=float_precsion)
        ','
        
        left, right, bottom, up = self.td.vfh.unpackrange(self.td.effctive_range)
        for run_id in range(len(self.td.frames_in_runs)):
            for frame_id in range(self.td.frames_in_runs[run_id]):
                self.td.cal_and_identify_SH_layer_frame(run_id, frame_id, coef_threshold=Cth)
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
                omega_s_LAB = self.td.LAB_dUdX_shear[1,0,:,:] - self.td.LAB_dUdX_shear[0,1,:,:]
                omega_r_LAB = self.td.LAB_dUdX_rotation[1,0,:,:] - self.td.LAB_dUdX_rotation[0,1,:,:]
                for SL_id in range(len(ixs)):
                    ix = ixs[SL_id]
                    iy = iys[SL_id]
                    
                    tmp_u = np.zeros_like(self.X_BRF, dtype= float_precsion)
                    tmp_Is = np.zeros_like(self.X_BRF[0], dtype= float_precsion)
                    tmp_omega_s = np.zeros_like(self.X_BRF[0], dtype= float_precsion)
                    tmp_omega_r = np.zeros_like(self.X_BRF[0], dtype= float_precsion)
                    ','

                    Q_from_BRF_to_LAB = self.td.Q[:,:,ix,iy]
                    detQ = np.linalg.det(Q_from_BRF_to_LAB)
                    sign = 1.0 if detQ > 0 else -1.0
                    X_BRF_in_LAB = np.einsum('ij,jkl->ikl', Q_from_BRF_to_LAB, self.X_BRF)
                    X0 = self.td.X[:, ix, iy].astype(float_precsion)
                    X_BRF_in_LAB += X0[:, None, None]   
                    mask_inside = compute_mask_lagrange(self.td.X, X_BRF_in_LAB, left, right, bottom, up)
                    LSL_count_pos[mask_inside] += 1
                    ','

                    for k in range(2):
                        relative_U = self.td.vfh.u[k] - self.td.vfh.u[k, ix, iy]
                        tmp_u[k][mask_inside] = lagrange_interpolate_with_mask(self.td.X, X_BRF_in_LAB, relative_U, mask_inside)[mask_inside]  
                    tmp_Is[mask_inside] = lagrange_interpolate_with_mask(self.td.X, X_BRF_in_LAB, self.td.intensity_shear, mask_inside)[mask_inside]          
                    tmp_omega_s[mask_inside] = sign*lagrange_interpolate_with_mask(self.td.X, X_BRF_in_LAB, omega_s_LAB, mask_inside)[mask_inside]
                    tmp_omega_r[mask_inside] = sign*lagrange_interpolate_with_mask(self.td.X, X_BRF_in_LAB, omega_r_LAB, mask_inside)[mask_inside]                    
                    ','

                    avg_u_BRF[:,mask_inside] += np.einsum('ij,jm->im', Q_from_BRF_to_LAB.T, tmp_u[:, mask_inside])
                    avg_Is_BRF[mask_inside] += tmp_Is[mask_inside]
                    avg_omega_s_BRF[mask_inside] += tmp_omega_s[mask_inside]
                    avg_omega_r_BRF[mask_inside] += tmp_omega_r[mask_inside]

        mask_nonzero = LSL_count_pos > 0
        avg_u_BRF[:,mask_nonzero] = avg_u_BRF[:,mask_nonzero]/LSL_count_pos[mask_nonzero]
        avg_Is_BRF[mask_nonzero] = avg_Is_BRF[mask_nonzero]/LSL_count_pos[mask_nonzero]
        avg_omega_s_BRF[mask_nonzero] = avg_omega_s_BRF[mask_nonzero]/LSL_count_pos[mask_nonzero]
        avg_omega_r_BRF[mask_nonzero] = avg_omega_r_BRF[mask_nonzero]/LSL_count_pos[mask_nonzero]
        ','
        np.save(result_path+'/avg_u_BRF.npy',avg_u_BRF)
        np.save(result_path+'/avg_Is_BRF.npy',avg_Is_BRF)
        np.save(result_path+'/avg_omega_s_BRF.npy',avg_omega_s_BRF)
        np.save(result_path+'/avg_omega_r_BRF.npy',avg_omega_r_BRF)
        '.'
        self.result_json.set(0,identified_LSL_number = identified_LSL_number)
        self.load_result(deg_ranges)

    def load_result(self, deg_ranges=None, Cth = 1.5):
        self.X_BRF = np.load(self.result_path + self.td.vfh.middle_path() + '/X_LSL.npy')
        if deg_ranges == None:
            result_path = self.result_path + self.td.vfh.middle_path() + '/general'
        else :
            deg_folder = '/deg'
            for deg_range in deg_ranges:
                deg_folder = deg_folder + f'_{deg_range[0]:.1f}to{deg_range[1]:.1f}'
            result_path = self.result_path + self.td.vfh.middle_path() + deg_folder
        result_path = result_path+ f'/Cth_{int(Cth*1000)}'
        self.result_json = PT(result_path+"/result.json")

        self.avg_u_BRF = np.load(result_path+'/avg_u_BRF.npy')
        self.avg_Is_BRF = np.load(result_path+'/avg_Is_BRF.npy')
        self.avg_omega_s_BRF = np.load(result_path+'/avg_omega_s_BRF.npy')
        self.avg_omega_r_BRF = np.load(result_path+'/avg_omega_r_BRF.npy')




def worker(args):
    case, filter, p, Lf, cth, deg_ranges  = args
    sl = ShearLayer(case, filter, filter_id=p)
    if filter == 'gaussian':
        coef = 7.5
    elif filter == 'gaussian_bp':
        coef = 4.5
    sl.prepare_BRF_coordinate(coef*Lf, N=100)
    print (f'Started:{args}')
    sl.calculate_general(deg_ranges, Cth=cth)
    return print (f'Finished:{args}')


if __name__ == '__main__':
    from multiprocessing import Pool  
    from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
    from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS
    from ZZZ_Result_Manager.A01_cases import cases_select, cases_select_f,cases_select_w, coeffs_to_eta
    cth = 1.5

    filter = 'gaussian'
    for coeff_id, coeff in enumerate(coeffs_to_eta):
        coeff_id += 1
        filter_params = coeff_id
        with Pool() as pool:
            tasks = []
            for case_id, case in enumerate(cases_select):
                    ds = DS(cases_select_f[case_id], 'gaussian',-1)
                    eta = ds.result_json.get(0)['eta']*1000
                    Lf = eta * coeff
                    tasks.append((cases_select_w[case_id], filter, coeff_id, Lf, cth, None))
            results = pool.map(worker, tasks)  

        
        from ZZZ_Result_Manager.A01_cases import degs
        for deg in degs:
            with Pool() as pool:
                tasks = []
                for case_id, case in enumerate(cases_select):
                        ds = DS(cases_select_f[case_id], 'gaussian',-1)
                        eta = ds.result_json.get(0)['eta']*1000
                        Lf = eta * coeff
                        tasks.append((cases_select_w[case_id], filter, coeff_id, Lf, cth, deg))
                results = pool.map(worker, tasks)  

