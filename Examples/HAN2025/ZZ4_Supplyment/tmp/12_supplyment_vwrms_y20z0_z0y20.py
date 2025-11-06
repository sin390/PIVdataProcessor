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

ws = WriteHandler(['x(mm)','v_rms/w_rms','err(v_rms/w_rms)','interpolated_vrms','err(itp_vrms)','interpolated_wrms','err(itp_wrms)'])
ws_vrms = WriteHandler(['x(mm)','v_rms','err(v_rms)'])
ws_wrms = WriteHandler(['x(mm)','w_rms','err(w_rms)'])
point_num = 100
err_filter_range = 8

# y = 0, z = 0 line

lefts = []
rights = []
rs = RS('Case01')
rs.load()
central_x, central_y = pBase.CaseInfo.Central_Position_Grid
plot_x,plot_y = pBase.pos_mm_to_index_list([0],[20])
central_y = plot_y[0]
left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]
x_xyplane = pBase.X[0][left:right,central_y].copy()
vrms_xyplane = np.sqrt(rs.vv[left:right,central_y])
err_vrms = vrms_error('Case01')
e_vrms = err_vrms.estimate_uncertainty(filter_range=err_filter_range)[left:right,central_y]
ws_vrms.loaddata([x_xyplane,vrms_xyplane,e_vrms/2])
lefts.append(pBase.X[0][left,central_y])
rights.append(pBase.X[0][right-1,central_y])

rs = RS(f'Case01XZ_Y00')
rs.load()
central_x, central_y = pBase.CaseInfo.Central_Position_Grid
plot_x,plot_y = pBase.pos_mm_to_index_list([0],[-20])
central_y = plot_y[0]
left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]
x_xzplane = pBase.X[0][left:right,central_y].copy()

wrms_xzplane = np.sqrt(rs.vv[left:right,central_y])
err_wrms = vrms_error(f'Case01XZ_Y00')
e_wrms = err_wrms.estimate_uncertainty(filter_range=err_filter_range)[left:right,central_y]
ws_wrms.loaddata([x_xzplane,wrms_xzplane,e_wrms/2])
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
ws.loaddata([x_uniform, v_uniform/w_uniform,error_ratio/2, v_uniform, e_v_uni/2, w_uniform, e_w_uni/2])
ws.write(fig_path+f'/vrms(y=20,z=0)--wrms(y=0,z=-20).txt')
ws_vrms.write(fig_path+f'/(XY)vrms(y=20,z=0).txt')
ws_wrms.write(fig_path+f'/(XZ)wrms(y=0,z=-20).txt')



plt.plot(x_uniform, v_uniform/w_uniform, '-', label=f'v_rms/w_rms_y=0')
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