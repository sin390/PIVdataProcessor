''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.1         =
= Date:     2025/12/12  =
=========================
'''

import numpy as np
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GH
from pivdataprocessor.A01_toolbox import float_precsion
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT


class PODHandler(GH):
    def __init__(self, casename, filter='gaussian', filter_id=None):
        super().__init__(casename)   # <<< MOD 1: remove duplicate super() >>>

        self.datasource = filter
        self.filter_id = filter_id

        self.vfh = VFH(casename, filter, filter_id)
        self.vfh.load_X()
        self.vfh.load_field(0, 0)

        self.frames_in_runs = self.vfh.frames_in_runs
        self.Nsnapshot = sum(self.frames_in_runs)

        self.result_json = PT(self.result_path + self.vfh.middle_path() + "/result.json")

        self.X = self.vfh.X
        self.effctive_range = self.vfh.effctive_range
        self.e_Nx = self.effctive_range[0][1] - self.effctive_range[0][0]
        self.e_Ny = self.effctive_range[1][1] - self.effctive_range[1][0]

        self.Nassemble = 2 * self.e_Nx * self.e_Ny
        self.max_rank = min(self.Nassemble, self.Nsnapshot)

        # Assemble matrix (space × snapshot)
        self.assemble = np.zeros((self.Nassemble, self.Nsnapshot), dtype=float_precsion)

        # POD results (allocated after SVD)
        self.Umatrix = None
        self.sigma = None
        self.VmatrixT = None

        self.POD_X = self.X[:,self.effctive_range[0][0]:self.effctive_range[0][1],self.effctive_range[1][0]:self.effctive_range[1][1]]

        self.pod_result_path = self.result_path + self.vfh.middle_path()

    # ==========================================================
    # POD calculation
    # ==========================================================
    def PODcalculate(self):
        self.rm_and_create_directory(self.pod_result_path)

        # ------------------------------
        # Assemble snapshot matrix
        # ------------------------------
        current_snapshot = -1
        for run_ID in range(len(self.frames_in_runs)):
            for frame_ID in range(self.frames_in_runs[run_ID]):
                current_snapshot += 1
                self.vfh.load_field(run_ID, frame_ID)

                fluc_U = self.vfh.u[
                    :,
                    self.effctive_range[0][0]:self.effctive_range[0][1],
                    self.effctive_range[1][0]:self.effctive_range[1][1]
                ]

                self.assemble[:, current_snapshot] = fluc_U.reshape(self.Nassemble)

        # ------------------------------
        # NaN check (warning only)
        # ------------------------------
        if np.isnan(self.assemble).any():        # <<< MOD 4 >>>
            print("[WARNING] NaNs detected in POD assemble matrix, replaced by zeros.")
            self.assemble = np.nan_to_num(self.assemble)

        # ------------------------------
        # SVD (economy mode)
        # ------------------------------
        # <<< MOD 2: full_matrices=False >>>
        U, s, VT = np.linalg.svd(self.assemble, full_matrices=False)

        self.Umatrix = U.astype(float_precsion)
        self.sigma = s.astype(float_precsion)
        self.VmatrixT = VT.astype(float_precsion)

        self.__PODsave()

    # ==========================================================
    # POD modes
    # ==========================================================
    def spatial_mode(self, rank: int):
        """
        Pure spatial POD mode (unit-norm)
        """
        return self.Umatrix[:, rank].reshape(2, self.e_Nx, self.e_Ny)

    def energy_mode(self, rank: int):
        """
        Energy-weighted POD mode (σ_k * φ_k)
        """
        return (self.Umatrix[:, rank] * self.sigma[rank]).reshape(
            2, self.e_Nx, self.e_Ny
        )

    # ==========================================================
    # Reconstruction
    # ==========================================================
    def reconstruct(self, rank_Number, rank_start=0):
        if rank_Number == -1:
            rank_end = self.max_rank
        else:
            rank_end = rank_Number

        U = self.Umatrix[:, rank_start:rank_end]
        S = self.sigma[rank_start:rank_end]
        V = self.VmatrixT[rank_start:rank_end, :]

        # <<< MOD 8: clearer formulation >>>
        uv_fluc = (U * S[np.newaxis, :]) @ V

        return uv_fluc.reshape(2, self.e_Nx, self.e_Ny, self.Nsnapshot)

    # ==========================================================
    # I/O
    # ==========================================================
    def __PODsave(self):
        np.save(self.pod_result_path + '/Umatrix.npy', self.Umatrix)
        np.save(self.pod_result_path + '/sigma.npy', self.sigma)
        np.save(self.pod_result_path + '/VmatrixT.npy', self.VmatrixT)
        np.save(self.pod_result_path + '/POD_X.npy', self.POD_X)

    def PODload(self):
        self.Umatrix = np.load(self.pod_result_path + '/Umatrix.npy')
        self.sigma = np.load(self.pod_result_path + '/sigma.npy')
        self.VmatrixT = np.load(self.pod_result_path + '/VmatrixT.npy')
        self.POD_X = np.load(self.pod_result_path + '/POD_X.npy') 

from Z03_Velocity_Field_Handler.G01_velocity_field_handler import params, params_mori
if __name__ == "__main__":
    # case = 'Case03'
    # filters = ['gaussian', 'gaussian_bp','wavelet']
    # for f_id, filter in enumerate(filters):
    #     for p in params[f_id]:
    #         pod = PODHandler(case, filter, p)
    #         print(f"{case}: Calculating POD for filter: {filter}, param: {p}")
    #         pod.PODcalculate()

    case = 'Mori_465'
    filters = ['gaussian', 'gaussian_bp','wavelet']
    for f_id, filter in enumerate(filters):
        for p in params_mori[f_id]:
            pod = PODHandler(case, filter, p)
            print(f"{case}: Calculating POD for filter: {filter}, param: {p}")
            pod.PODcalculate()