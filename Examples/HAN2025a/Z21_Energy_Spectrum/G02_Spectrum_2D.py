''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/12/26  =
=========================
'''
import numpy as np
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from Z03_Velocity_Field_Handler.G01_velocity_field_handler import VelocityFieldHandler as VFH
from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as SWC
from scipy.signal.windows import tukey

class Spectrum2D(GT):
    def __init__(self, casename, filter = 'gaussian', filter_id = None, cal_range = None):
        '''
        Docstring for __init__
        :param cal_range: None, calculate all the point; (Nx,Ny), central_pos +- Nx or Ny
        
        E2D definition:
        E2D[0] = < |FFT(u)|^2 > * (dx dy) / (pi^2 Nx Ny)
        E2D[1] = < |FFT(u)|^2 > * (dx dy) / (pi^2 Nx Ny)
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

        if cal_range == None:
            self.e_range = self.vfh.effctive_range
        else:
            c_X,c_Y = self.vfh.central_pos_grid
            left = c_X - cal_range[0]
            right = c_X + cal_range[0]
            bottom = c_Y - cal_range[1]
            up = c_Y + cal_range[1]
            self.e_range = ((left,right),(bottom,up))
        left,right,bottom,up = self.vfh.unpackrange(self.e_range)
        self.E2D = np.zeros((2,right-left,up-bottom))
        self.k2D = np.zeros((2,right-left,up-bottom))

    def cal_2D_FFT(self):
        left,right,bottom,up = self.vfh.unpackrange(self.e_range)
        Nx = right-left
        Ny = up-bottom
        cal_swc = SWC((2,Nx,Ny))
        tmp_E2D_fft = np.zeros((2,Nx,Ny))
        for run_id in range(len(self.frames_in_runs)):
            for frame_id in range(self.frames_in_runs[run_id]):
                self.vfh.load_field(run_id,frame_id)
                fluc_u = self.vfh.u[0][left:right,bottom:up]
                fluc_v = self.vfh.u[1][left:right,bottom:up]
                tmp_fft_u = np.fft.fft2(fluc_u)
                tmp_fft_v = np.fft.fft2(fluc_v)
                tmp_fft_u = np.fft.fftshift(tmp_fft_u)
                tmp_fft_v = np.fft.fftshift(tmp_fft_v)
                tmp_E2D_fft[0]=np.abs(tmp_fft_u)**2 
                tmp_E2D_fft[1]= np.abs(tmp_fft_v)**2
                cal_swc.add_point(tmp_E2D_fft)
        self.E2D = cal_swc.get_mean()
        dx = self.vfh.dX_in_m
        self.E2D *= (dx[0] * dx[1]) / (np.pi**2 * Nx * Ny)
        dx = self.vfh.dX_in_m
        kx = np.fft.fftfreq(Nx, d=dx[0]) * 2*np.pi
        ky = np.fft.fftfreq(Ny, d=dx[1]) * 2*np.pi
        kx = np.fft.fftshift(kx)
        ky = np.fft.fftshift(ky)
        KX, KY = np.meshgrid(kx, ky, indexing='ij')
        self.k2D[0] = KX
        self.k2D[1] = KY
        self.saveE2D()

    def cal_2D_FFT_hanning(self):
        left, right, bottom, up = self.vfh.unpackrange(self.e_range)
        Nx = right - left
        Ny = up - bottom

        cal_swc = SWC((2, Nx, Ny))
        tmp_E2D_fft = np.zeros((2, Nx, Ny))

        # ==================================================
        # 1. Build 2D Hann window (separable)
        # ==================================================
        wx = np.hanning(Nx)
        wy = np.hanning(Ny)
        W2 = wx[:, None] * wy[None, :]

        # Energy correction factor for 2D Hann window
        window_energy_factor = (3.0 / 8.0) ** 2  # = 9/64

        # ==================================================
        # 2. Loop over realizations
        # ==================================================
        for run_id in range(len(self.frames_in_runs)):
            for frame_id in range(self.frames_in_runs[run_id]):
                self.vfh.load_field(run_id, frame_id)

                fluc_u = self.vfh.u[0][left:right, bottom:up]
                fluc_v = self.vfh.u[1][left:right, bottom:up]

                # ----------------------------------------------
                # Apply window
                # ----------------------------------------------
                fluc_u_w = fluc_u * W2
                fluc_v_w = fluc_v * W2

                # ----------------------------------------------
                # FFT
                # ----------------------------------------------
                tmp_fft_u = np.fft.fftshift(np.fft.fft2(fluc_u_w))
                tmp_fft_v = np.fft.fftshift(np.fft.fft2(fluc_v_w))

                tmp_E2D_fft[0] = np.abs(tmp_fft_u) ** 2
                tmp_E2D_fft[1] = np.abs(tmp_fft_v) ** 2

                cal_swc.add_point(tmp_E2D_fft)

        # ==================================================
        # 3. Ensemble average
        # ==================================================
        self.E2D = cal_swc.get_mean()

        # ==================================================
        # 4. Window energy compensation
        # ==================================================
        self.E2D /= window_energy_factor

        # ==================================================
        # 5. Physical normalization (unchanged from your code)
        # ==================================================
        dx = self.vfh.dX_in_m
        self.E2D *= (dx[0] * dx[1]) / (np.pi**2 * Nx * Ny)

        # ==================================================
        # 6. Wavenumber grids
        # ==================================================
        kx = np.fft.fftfreq(Nx, d=dx[0]) * 2 * np.pi
        ky = np.fft.fftfreq(Ny, d=dx[1]) * 2 * np.pi
        kx = np.fft.fftshift(kx)
        ky = np.fft.fftshift(ky)

        KX, KY = np.meshgrid(kx, ky, indexing='ij')
        self.k2D[0] = KX
        self.k2D[1] = KY

        self.saveE2D()


    def cal_2D_FFT_tukey(self):
        left, right, bottom, up = self.vfh.unpackrange(self.e_range)
        Nx = right - left
        Ny = up - bottom

        cal_swc = SWC((2, Nx, Ny))
        tmp_E2D_fft = np.zeros((2, Nx, Ny))

        # ==================================================
        # 1. Build 2D Tukey window
        # ==================================================
        alpha = 0.25   # recommended
        wx = tukey(Nx, alpha=alpha)
        wy = tukey(Ny, alpha=alpha)
        W2 = wx[:, None] * wy[None, :]

        # --------------------------------------------------
        # Energy correction factor (robust numerical form)
        # <w^2> over the 2D domain
        # --------------------------------------------------
        window_energy_factor = np.mean(W2**2)

        # ==================================================
        # 2. Loop over realizations
        # ==================================================
        for run_id in range(len(self.frames_in_runs)):
            for frame_id in range(self.frames_in_runs[run_id]):
                self.vfh.load_field(run_id, frame_id)

                fluc_u = self.vfh.u[0][left:right, bottom:up]
                fluc_v = self.vfh.u[1][left:right, bottom:up]

                # ----------------------------------------------
                # Apply window
                # ----------------------------------------------
                fluc_u_w = fluc_u * W2
                fluc_v_w = fluc_v * W2

                # ----------------------------------------------
                # FFT
                # ----------------------------------------------
                Fu = np.fft.fftshift(np.fft.fft2(fluc_u_w))
                Fv = np.fft.fftshift(np.fft.fft2(fluc_v_w))

                tmp_E2D_fft[0] = np.abs(Fu)**2
                tmp_E2D_fft[1] = np.abs(Fv)**2

                cal_swc.add_point(tmp_E2D_fft)

        # ==================================================
        # 3. Ensemble average
        # ==================================================
        self.E2D = cal_swc.get_mean()

        # ==================================================
        # 4. Window energy compensation (CRITICAL)
        # ==================================================
        self.E2D /= window_energy_factor

        # ==================================================
        # 5. Physical normalization (unchanged)
        # ==================================================
        dx = self.vfh.dX_in_m
        self.E2D *= (dx[0] * dx[1]) / (np.pi**2 * Nx * Ny)

        # ==================================================
        # 6. Wavenumber grids
        # ==================================================
        kx = np.fft.fftfreq(Nx, d=dx[0]) * 2 * np.pi
        ky = np.fft.fftfreq(Ny, d=dx[1]) * 2 * np.pi
        kx = np.fft.fftshift(kx)
        ky = np.fft.fftshift(ky)

        KX, KY = np.meshgrid(kx, ky, indexing='ij')
        self.k2D[0] = KX
        self.k2D[1] = KY

        self.saveE2D()

    def saveE2D(self):
        save_path = self.result_path + self.vfh.middle_path()
        self.make_sure_directory(save_path)
        np.save(save_path+'/E2D.npy', self.E2D)
        np.save(save_path+'/k2D.npy', self.k2D)
    def loadE2D(self):
        save_path = self.result_path + self.vfh.middle_path()
        self.E2D = np.load(save_path+'/E2D.npy')
        self.k2D = np.load(save_path+'/k2D.npy')

if __name__ == "__main__":
    case = 'Case03'
    filter = 'gaussian'
    filter_id = -1
    s2d = Spectrum2D(case,filter,filter_id)
    s2d.cal_2D_FFT_tukey()   
    # s2d.cal_2D_FFT()     
