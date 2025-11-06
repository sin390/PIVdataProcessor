''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/10/16  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from G01_reynolds_stress import ReynoldsStress as RS
from pivdataprocessor.A02_pltcfg import  getplotpath
from pivdataprocessor.A01_toolbox import nanmean_filter2d, WriteHandler
from pivdataprocessor.L02_extension_tmpl import UncertaintyEstimationTemplate as UET
from scipy.interpolate import interp1d

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
# -------------------------------------------------------------------------
# endregion

class vrms_error(UET):
    def __init__(self, case_name):
        super().__init__(case_name)
    def load_target(self, casename: str):
        rs = RS(casename)
        rs.load()
        return np.sqrt(rs.vv)

import matplotlib.pyplot as plt
plt.figure(figsize=(6,4))

ws = WriteHandler(['x(mm)','v_rms/w_rms','err_v_rms/w_rms'])
point_num = 100
err_filter_range = 8

# y = 0, z = 0 line
plotted_y = [0,20]
for y in plotted_y:
    lefts = []
    rights = []
    rs = RS('Case01')
    rs.load()
    _,index_y = pBase.pos_mm_to_index_list([0], [y])
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    x_xyplane = pBase.X[0][left:right,index_y[0]].copy()
    vrms_xyplane = np.sqrt(rs.vv[left:right,index_y[0]])
    err_vrms = vrms_error('Case01')
    e_vrms = err_vrms.estimate_uncertainty(filter_range=err_filter_range)[left:right,index_y[0]]
    lefts.append(pBase.X[0][left,index_y[0]])
    rights.append(pBase.X[0][right-1,index_y[0]])

    rs = RS(f'Case01XZ_Y{y:02d}')
    rs.load()
    central_x, central_y = pBase.CaseInfo.Central_Position_Grid
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]
    x_xzplane = pBase.X[0][left:right,central_y].copy()

    wrms_xzplane = np.sqrt(rs.vv[left:right,central_y])
    err_wrms = vrms_error(f'Case01XZ_Y{y:02d}')
    e_wrms = err_wrms.estimate_uncertainty(filter_range=err_filter_range)[left:right,central_y]
    lefts.append(pBase.X[0][left,central_y])
    rights.append(pBase.X[0][right-1,central_y])

    x_uniform = np.linspace(
        max(lefts),
        min(rights),
        point_num
    )
    f_v = interp1d(x_xyplane, vrms_xyplane, kind='cubic', fill_value='extrapolate')
    f_ev = interp1d(x_xyplane[1:-1], e_vrms[1:-1], kind='cubic', fill_value='extrapolate')
    f_w = interp1d(x_xzplane, wrms_xzplane, kind='cubic', fill_value='extrapolate')
    f_ew = interp1d(x_xzplane[1:-1], e_wrms[1:-1], kind='cubic', fill_value='extrapolate')


    v_uniform = f_v(x_uniform)
    e_v_uni = f_ev(x_uniform)
    w_uniform = f_w(x_uniform)
    e_w_uni = f_ew(x_uniform)

    error_ratio = np.abs(v_uniform/w_uniform) * np.sqrt( (e_v_uni/v_uniform)**2 + (e_w_uni/w_uniform)**2 )
    ws.loaddata([x_uniform, v_uniform/w_uniform,error_ratio])
    ws.write(fig_path+f'/vrms_wrms_y{y:02d}z0_line.txt')
    plt.plot(x_uniform, v_uniform/w_uniform, '-', label=f'v_rms/w_rms_y={y}')



# plt.plot(x_xyplane, vrms_xyplane, 'o', label='original v_rms')
# plt.plot(x_uniform, v_uniform, '-', label='interpolated v_rms')
# plt.plot(x_xzplane, wrms_xzplane, 'o', label='original w_rms')
# plt.plot(x_uniform, w_uniform, '-', label='interpolated w_rms')

plt.xlabel('x')
plt.ylabel('v_rms/w_rms')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()