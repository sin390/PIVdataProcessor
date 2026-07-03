''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/12/05  =
=========================
'''

import numpy as np
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GH
from Z02_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as SWC

class TripleDecomposition(GH):
    R45 = np.array([
        [np.cos(np.pi / 4), -np.sin(np.pi / 4)],
        [np.sin(np.pi / 4),  np.cos(np.pi / 4)]])
    R_90 = np.array([
        [0, -1],
        [1,  0]])  
    R_180 = R_90@R_90  
    Q_reflect = np.array([
        [-1,  0],
        [0, 1]])    
    def __init__(self, casename, filter = 'gaussian', filter_id = -1):
        '''
        Q[0,0] e1x; Q[1,0] e1y; Q[0,1] e2x; Q[1,1] e2y
        '''
        super().__init__(casename)
        self.datasource = filter
        self.filter_id = filter_id
        self.vfh = VFH(casename, filter, filter_id)
        self.vfh.load_X()
        self.vfh.load_field(0,0)
        self.frames_in_runs = self.vfh.frames_in_runs

        self.result_json = PT(self.result_path + self.vfh.middle_path()+"/result.json")
        self.X = self.vfh.X
        self.effctive_range = self.vfh.effctive_range

        self.T = np.zeros_like(self.vfh.dudx)
        'Q[0,0] e1x; Q[1,0] e1y; Q[0,1] e2x; Q[1,1] e2y'
        self.Q = np.zeros_like(self.vfh.dudx)
        self.BRF_dUdX_shear = np.zeros_like(self.vfh.dudx)
        self.BRF_dUdX_rotation = np.zeros_like(self.vfh.dudx)
        self.BRF_dUdX_elongation = np.zeros_like(self.vfh.dudx)
        self.LAB_dUdX_shear = np.zeros_like(self.vfh.dudx)
        self.LAB_dUdX_rotation = np.zeros_like(self.vfh.dudx)
        self.LAB_dUdX_elongation = np.zeros_like(self.vfh.dudx)

        self.intensity_shear = np.zeros_like(self.vfh.u[0])
        self.intensity_rotation = np.zeros_like(self.vfh.u[0])
        self.intensity_elongation = np.zeros_like(self.vfh.u[0])
        self.intensity_omega = np.zeros_like(self.vfh.u[0])
        self.intensity_mag_omega = np.zeros_like(self.vfh.u[0])

    def cal_frame(self, run_id, frame_id, if_adjust_direction = True):
        self.vfh.load_field(run_id, frame_id)
        dudx = self.vfh.dudx
        self.omega = dudx[1,0]-dudx[0,1]
        self.intensity_omega = np.sqrt(2 * np.sum(self.omega**2, axis=(0,1)))

        'Step1: find BRF'
        A = dudx.copy()
        A_T = A.transpose(1, 0, 2, 3)  
        S = 0.5 * (A + A_T)
        eigvals, V = self.eig_decompostition_2x2(S)

        Q = np.einsum('ij,jkxy', TripleDecomposition.R45, V)
        self.Q = Q


        'Step2: conduct TDM'
        if if_adjust_direction == True:
            self.TDM_with_adjusted_direction()
            self.intensity_shear = np.sqrt(2 * np.sum(self.LAB_dUdX_shear**2, axis=(0,1)))
            self.intensity_elongation = np.sqrt(2 * np.sum(self.LAB_dUdX_elongation**2, axis=(0,1)))
            self.intensity_rotation = np.sqrt(2 * np.sum(self.LAB_dUdX_rotation**2, axis=(0,1)))
        else:
            self.conduct_TDM()
            self.intensity_shear = np.sqrt(2 * np.sum(self.BRF_dUdX_shear**2, axis=(0,1)))
            self.intensity_elongation = np.sqrt(2 * np.sum(self.BRF_dUdX_elongation**2, axis=(0,1)))
            self.intensity_rotation = np.sqrt(2 * np.sum(self.BRF_dUdX_rotation**2, axis=(0,1)))




    def conduct_TDM(self):
        '''dUdX = Q @ T @ Q^t'''
        Q = self.Q
        Qt = Q.transpose(1, 0, 2, 3)
        dudx = self.vfh.dudx.copy()
        self.T = np.einsum("ijxy,jkxy,klxy->ilxy", Qt, dudx, Q)
        res = np.zeros_like(dudx)
        for i in [0,1]:
            for j in [0,1]:
                res[i,j] = np.sign(self.T[i,j]) * np.minimum(np.abs(self.T[i,j]),np.abs(self.T[j,i]))
        for i in [0,1]:
            for j in [0,1]:
                self.BRF_dUdX_shear[i,j] = self.T[i,j]-res[i,j]
                self.BRF_dUdX_rotation[i,j] = (res[i,j]-res[j,i])/2
                self.BRF_dUdX_elongation[i,j] = (res[i,j]+res[j,i])/2
    
    def TDM_with_adjusted_direction(self):

        self.BRF_dUdX_shear[:] = np.nan
        self.BRF_dUdX_rotation[:] = np.nan
        self.BRF_dUdX_elongation[:] = np.nan

        # always work with updated SH
        self.conduct_TDM()
        # --- Step 1: rotate 90° where |SH01| < |SH10| ---
        SH = self.BRF_dUdX_shear
        mask_rot =  (np.abs(SH[0,1]) < np.abs(SH[1,0]))
        if mask_rot.any():        
            # rotate Q only on masked points
            Q = self.Q
            Q_new = np.einsum("ab,bixy->aixy", self.R_90, Q)
            Q[:,:,mask_rot] = Q_new[:,:,mask_rot]
            self.Q = Q
            # re-evaluate LSL/TDM decomposition
            self.conduct_TDM()
            SH = self.BRF_dUdX_shear   # refresh SH

        # --- Step 2: reflect where SH01 > 0 ---
        mask_ref =  (SH[0,1] > 0)
        if mask_ref.any():
            Q = self.Q
            Q[:, 0, mask_ref] *= -1
            self.Q = Q

        # --- Step 3: align towards y>0
        mask_align = (self.Q[1,1] < 0)
        if mask_align.any():
            Q = self.Q
            Q_new = np.einsum("ab,bixy->aixy", self.R_180, Q)
            Q[:,:,mask_align] = Q_new[:,:,mask_align]
            self.Q = Q
        self.conduct_TDM()
        Q = self.Q
        Qt = Q.transpose(1, 0, 2, 3)
        self.LAB_dUdX_elongation = np.einsum("ijxy,jkxy,klxy->ilxy", Q, self.BRF_dUdX_elongation, Qt)
        self.LAB_dUdX_rotation = np.einsum("ijxy,jkxy,klxy->ilxy", Q, self.BRF_dUdX_rotation, Qt)
        self.LAB_dUdX_shear = np.einsum("ijxy,jkxy,klxy->ilxy", Q, self.BRF_dUdX_shear, Qt)

    def cal_avg(self):
        swc_shear = SWC(self.intensity_shear.shape)
        swc_rotation = SWC(self.intensity_rotation.shape)
        swc_elongation = SWC(self.intensity_elongation.shape)
        swc_mag_omega = SWC(self.intensity_omega.shape)

        for run_id in range(len(self.frames_in_runs)):
            for frame_id in range(self.frames_in_runs[run_id]):
                self.cal_frame(run_id, frame_id)
                swc_shear.add_point(self.intensity_shear)
                swc_rotation.add_point(self.intensity_rotation)
                swc_elongation.add_point(self.intensity_elongation)
                swc_mag_omega.add_point(np.abs(self.omega))
        self.intensity_elongation = swc_elongation.get_mean()
        self.intensity_rotation = swc_rotation.get_mean()
        self.intensity_shear = swc_shear.get_mean()
        self.intensity_mag_omega = swc_mag_omega.get_mean()
        save_path = self.result_path + self.vfh.middle_path()
        self.make_sure_directory(save_path)
        self.save_nparray_to_bin(self.intensity_elongation, save_path+'/avg_intensity_el.bin')
        self.save_nparray_to_bin(self.intensity_rotation, save_path+'/avg_intensity_rr.bin')
        self.save_nparray_to_bin(self.intensity_shear, save_path+'/avg_intensity_sh.bin')
        self.save_nparray_to_bin(self.intensity_mag_omega, save_path+'/avg_intensity_mag_omega.bin')
        left,right,bottom,up = VFH.unpackrange(self.effctive_range)
        self.result_json.set(0, avg_intensity_EL = np.nanmean(self.intensity_elongation[left:right,bottom:up]))
        self.result_json.set(0, avg_intensity_RR = np.nanmean(self.intensity_rotation[left:right,bottom:up]))
        self.result_json.set(0, avg_intensity_SH = np.nanmean(self.intensity_shear[left:right,bottom:up]))
        self.result_json.set(0, avg_intensity_Mag_Omega = np.nanmean(self.intensity_mag_omega[left:right,bottom:up]))
    
    def load_avg(self):
        load_path = self.result_path + self.vfh.middle_path()
        self.avg_intensity_elongation = self.load_nparray_from_bin(self.intensity_elongation, load_path+'/avg_intensity_el.bin')
        self.avg_intensity_rotation = self.load_nparray_from_bin(self.intensity_rotation, load_path+'/avg_intensity_rr.bin')
        self.avg_intensity_shear = self.load_nparray_from_bin(self.intensity_shear, load_path+'/avg_intensity_sh.bin')
        self.avg_intensity_mag_omega = self.load_nparray_from_bin(self.intensity_mag_omega, load_path+'/avg_intensity_mag_omega.bin')


    def cal_and_identify_SH_layer_frame(self, run_id, frame_id, coef_threshold = 2, maximum_window = 3):
        '''load_avg() must be called before this function'''
        self.cal_frame(run_id, frame_id)
        self.identified_pos = np.zeros_like(self.intensity_shear, dtype=bool)
        left,right,bottom,up = VFH.unpackrange(self.effctive_range)

        '1. Effective Range'
        self.identified_pos[left:right,bottom:up] = True
        
        '2b. intensity'
        gt_than_avg = self.intensity_shear > coef_threshold * self.avg_intensity_shear
        self.identified_pos = self.identified_pos & gt_than_avg

        '3b. Discrete local maximum (NMS only)'
        local_max = self.discrete_local_maximum(
            self.intensity_shear,
            mask=self.identified_pos,
            window=3
        )
        self.identified_pos &= local_max




    @staticmethod
    def eig_decompostition_2x2(A):
        """
        Robust 2x2 eigen-decomposition for symmetric matrices.
        - No directional bias
        - Continuous eigen-directions
        - Safe for orientation statistics

        Parameters
        ----------
        A : ndarray, shape (2,2,Nx,Ny)
            Symmetric 2x2 tensor field.
        eps : float
            Degeneracy threshold.

        Returns
        -------
        eigvals : ndarray, shape (2,2,Nx,Ny)
            Diagonal matrix of eigenvalues.
        eigvecs : ndarray, shape (2,2,Nx,Ny)
            Eigenvector matrix Q = [e1, e2].
        """

        assert A.shape[0:2] == (2, 2)

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 1]

        # -------------------------------------------------
        # Eigenvalues (analytic, safe)
        # -------------------------------------------------
        trace = a + c
        delta = np.sqrt((a - c)**2 + 4.0 * b**2)

        lam1 = 0.5 * (trace + delta)
        lam2 = 0.5 * (trace - delta)

        eigvals = np.zeros((2, 2) + a.shape)
        eigvals[0, 0] = lam1
        eigvals[1, 1] = lam2

        # -------------------------------------------------
        # Eigenvectors via analytic angle
        # tan(2θ) = 2b / (a-c)
        # -------------------------------------------------
        theta = 0.5 * np.arctan2(2.0 * b, a - c)

        e1 = np.zeros((2,) + a.shape)
        e2 = np.zeros((2,) + a.shape)

        e1[0] = np.cos(theta)
        e1[1] = np.sin(theta)

        e2[0] = -np.sin(theta)
        e2[1] =  np.cos(theta)
        # -------------------------------------------------
        # Assemble eigenvector matrix Q = [e1, e2]
        # -------------------------------------------------
        eigvecs = np.zeros((2, 2) + a.shape)
        eigvecs[:, 0] = e1
        eigvecs[:, 1] = e2
        return eigvals, eigvecs 
        

    @staticmethod
    def discrete_local_maximum(intensity, mask=None, window=3):
        """
        Discrete local maximum (NMS only).

        A pixel is kept if its value is the maximum in a local window.

        Parameters
        ----------
        intensity : (H, W) ndarray
            Scalar field (e.g. intensity_shear)

        mask : (H, W) bool array or None
            Valid candidate mask.

        window : int (odd)
            Neighborhood size (3 or 5)

        Returns
        -------
        local_max : (H, W) bool array
            Discrete local maxima mask.
        """
        assert window % 2 == 1, "window must be odd"

        H, W = intensity.shape
        r = window // 2

        if mask is None:
            mask = np.ones_like(intensity, dtype=bool)

        local_max = np.zeros_like(mask, dtype=bool)

        for i in range(r, H - r):
            for j in range(r, W - r):
                if not mask[i, j]:
                    continue

                patch = intensity[i-r:i+r+1, j-r:j+r+1]
                I0 = intensity[i, j]

                # Strict NMS: keep only if it is the maximum
                if I0 >= np.max(patch):
                    local_max[i, j] = True

        return local_max



if __name__ == "__main__":
    from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
    from ZZZ_Result_Manager.A01_cases import cases, coeffs_to_eta

    # for case in cases_w:
    #     td = TripleDecomposition(case, 'gaussian', 3)
    #     td.cal_avg()
    for coeff_id, coeff in enumerate(coeffs_to_eta):
        coeff_id += 1
        for case_id, case in enumerate(cases):
            td = TripleDecomposition(case, 'gaussian', coeff_id)
            td.cal_avg()