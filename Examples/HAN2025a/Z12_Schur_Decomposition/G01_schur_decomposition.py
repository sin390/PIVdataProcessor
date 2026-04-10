''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/12/14  =
=========================
'''

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GH
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as SWC
from pivdataprocessor.A01_toolbox import scalar_field_5points_stencil
from collections import deque
from scipy.spatial import cKDTree

class SchurDecomposition(GH):
    def __init__(self, casename, filter = 'gaussian', filter_id = None):
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
        left,right,bottom,up = self.vfh.unpackrange(self.effctive_range)
        self.e_range_slice = (slice(left,right),slice(bottom,up))
        self.lsq_B = self.lsq_kernel_2nd(self.vfh.dX_in_m[0], self.vfh.dX_in_m[1])

    @staticmethod
    def lsq_kernel_2nd(dx, dy):
        xs = np.arange(-2, 3) * dx
        ys = np.arange(-2, 3) * dy
        X, Y = np.meshgrid(xs, ys, indexing="ij")

        x = X.ravel()
        y = Y.ravel()

        A = np.column_stack([
            np.ones_like(x),   # a
            x,                 # Ix
            y,                 # Iy
            0.5*x**2,          # Ixx
            x*y,               # Ixy
            0.5*y**2           # Iyy
        ])

        # B @ Z_flat = [a, Ix, Iy, Ixx, Ixy, Iyy]
        B = np.linalg.solve(A.T @ A, A.T)   # (6,25)

        return B.reshape(6,5,5)

    @staticmethod
    def hessian_lsq_simple(I, B):
        # I: (H,W)
        # B: (6,5,5)

        patches = sliding_window_view(I, (5,5))      # (H-4, W-4, 5,5)
        coef = np.einsum("kij,xyij->kxy", B, patches)

        _, Ix, Iy, Ixx, Ixy, Iyy = coef

        pad = ((2,2),(2,2))
        return (
            np.pad(Ix,  pad, constant_values=np.nan),
            np.pad(Iy,  pad, constant_values=np.nan),
            np.pad(Ixx, pad, constant_values=np.nan),
            np.pad(Ixy, pad, constant_values=np.nan),
            np.pad(Iyy, pad, constant_values=np.nan),
        )

    @staticmethod
    def get_intensity(T):
        assert T.shape[:2] == (2,2)
        # Frobenius norm: sqrt(tr(T T^H)) = sqrt(sum_ij |T_ij|^2)
        return np.sqrt(2*np.einsum("ij...,ij...->...", T, np.conj(T)).real)

    @staticmethod
    def S_Omega_Split(T):
        assert T.shape[:2] == (2, 2)
        T_star = T.conj().swapaxes(0, 1)   # 共轭转置 A*
        S = 0.5 * (T + T_star)            # Hermitian
        Omega = 0.5 * (T - T_star)        # skew-Hermitian
        return S, Omega

    @staticmethod
    def Keylock2018(A, eps=1e-14):
        A = np.asarray(A, dtype=np.complex128)
        assert A.shape[0:2] == (2, 2)

        a = A[0, 0]
        b = A[0, 1]
        c = A[1, 0]
        d = A[1, 1]

        tr = a + d
        det = a * d - b * c
        disc = np.sqrt(tr * tr - 4.0 * det)

        lam2 = 0.5 * (tr - disc)

        m11 = a - lam2
        m12 = b
        m21 = c
        m22 = d - lam2

        n1 = np.abs(m12) + np.abs(m11)
        n2 = np.abs(m22) + np.abs(m21)
        use1 = (n1 >= n2)

        u1x = np.where(use1, m12, m22)
        u1y = np.where(use1, -m11, -m21)

        u1n = np.sqrt(np.abs(u1x)**2 + np.abs(u1y)**2)
        deg = (u1n < eps)
        u1x = np.where(deg, 1.0 + 0j, u1x)
        u1y = np.where(deg, 0.0 + 0j, u1y)

        u1n = np.sqrt(np.abs(u1x)**2 + np.abs(u1y)**2)
        u1x /= u1n
        u1y /= u1n

        u2x = -np.conj(u1y)
        u2y =  np.conj(u1x)

        U = np.empty_like(A, dtype=np.complex128)
        U[0, 0] = u1x
        U[1, 0] = u1y
        U[0, 1] = u2x
        U[1, 1] = u2y

        Uh = np.conj(U).transpose(1, 0, 2, 3)

        # Schur form
        T = np.einsum("ijxy,jkxy,klxy->ilxy", Uh, A, U)

        B_T = np.zeros_like(T,dtype=np.complex128)
        B_T[0, 0] = T[0, 0]
        B_T[1, 1] = T[1, 1]
        C_T = T - B_T

        B_phys = np.einsum("ijxy,jkxy,klxy->ilxy", U, B_T, Uh)
        C_phys = np.einsum("ijxy,jkxy,klxy->ilxy", U, C_T, Uh)

        return B_phys, C_phys

    
    def cal_frame(self, run_id, frame_id):
        self.vfh.load_field(run_id, frame_id)
        dudx = self.vfh.dudx
        B, C = self.Keylock2018(dudx)
        self.i_B = self.get_intensity(B)
        self.i_C = self.get_intensity(C)
        B_strain, B_omega = self.S_Omega_Split(B)
        self.i_B_s = self.get_intensity(B_strain)
        self.i_B_o = self.get_intensity(B_omega)
 

    def cal_avg(self):
        swc_i_B = SWC(self.X[0].shape)
        swc_i_B_s = SWC(self.X[0].shape)
        swc_i_B_o = SWC(self.X[0].shape)
        swc_i_C = SWC(self.X[0].shape)
        for run_id in range(len(self.frames_in_runs)):
            for frame_id in range(self.frames_in_runs[run_id]):
                self.cal_frame(run_id, frame_id)
                swc_i_B.add_point(self.i_B)
                swc_i_B_o.add_point(self.i_B_o)
                swc_i_B_s.add_point(self.i_B_s)
                swc_i_C.add_point(self.i_C)
        self.i_B = swc_i_B.get_mean()
        self.i_C = swc_i_C.get_mean()
        self.i_B_o = swc_i_B_o.get_mean()
        self.i_B_s = swc_i_B_s.get_mean()
        save_path = self.result_path + self.vfh.middle_path()
        self.make_sure_directory(save_path)
        np.save(save_path+'/avg_I_B.npy', self.i_B)
        np.save(save_path+'/avg_I_C.npy', self.i_C)
        np.save(save_path+'/avg_I_B_o.npy', self.i_B_o)
        np.save(save_path+'/avg_I_B_s.npy', self.i_B_s)

        self.result_json.set(0, avg_I_B = np.nanmean(self.i_B[self.e_range_slice]))
        self.result_json.set(0, avg_I_C = np.nanmean(self.i_C[self.e_range_slice]))
        self.result_json.set(0, avg_I_B_s = np.nanmean(self.i_B_s[self.e_range_slice]))
        self.result_json.set(0, avg_I_B_o = np.nanmean(self.i_B_o[self.e_range_slice]))

    def load_avg(self):
        save_path = self.result_path + self.vfh.middle_path()
        self.avg_i_B = np.load(save_path+'/avg_I_B.npy')
        self.avg_i_C = np.load(save_path+'/avg_I_C.npy')
        self.avg_i_B_o =np.load(save_path+'/avg_I_B_o.npy')
        self.avg_i_B_s = np.load(save_path+'/avg_I_B_s.npy')
      

from ZZZ_Result_Manager.A01_cases import cases, gaussian_id
if __name__ == "__main__":
    for case in cases:
        for _, i in enumerate(gaussian_id):
            sd = SchurDecomposition(case, 'gaussian', i)
            sd.cal_avg()