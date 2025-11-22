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
from Z02_Reynolds_Stress.G01_reynolds_stress import ReynoldsStress as RS
from pivdataprocessor.A02_pltcfg import  getplotpath
from pivdataprocessor.A01_toolbox import nanmean_filter2d, WriteHandler
from pivdataprocessor.L02_extension_tmpl import UncertaintyEstimationTemplate as UET
from scipy.interpolate import interp1d

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)

'''
    Here, calculate for urms
'''
class rms_error(UET):
    def __init__(self, case_name):
        super().__init__(case_name)
    def load_target(self, casename: str):
        rs = RS(casename)
        rs.load()
        return np.sqrt(rs.vv)

import matplotlib.pyplot as plt
plt.figure(figsize=(6,4))

# -------------------------------------------------------------------------
# endregion

# -------------------------------------------------------------------------
# region
case_a = 'Case01XY_Z12_Ethanol'
case_b = 'Case01XZ_Y0_Ethanol'

comment_ratio = ['Note: these are interpolated values used for calculating the ratio.',
           'The original values are provided in other files',
           '-- a: XY-plane Z = 12, v_rms(x, y=0, z=12)',
           '-- b: XZ-plane Y = 0, w_rms(x, y=0, z=12)']
ws = WriteHandler(['x(mm)','a/b','err(a/b)','-err(a/b)','a','err(a)','-err(a)','b','err(b)','-err(b)'],comment_ratio)
ws_filename = '\\ratio.txt'

comment_a = ['XY-plane Z = 12, v_rms(x, y=0, z=12)']
ws_a = WriteHandler(['x(mm)','v_rms','err(v_rms)','-err(v_rms)'], comment_a)
ws_a_filename = '\\XY-Z12, v_rms(x,y=0,z=12).txt'

comment_b = ['XZ-plane Y = 0, w_rms(x, y=0, z=12)']
ws_b = WriteHandler(['x(mm)','w_rms','err(w_rms)','-err(w_rms)'],comment_b)
ws_b_filename = '\\XZ-Y0, w_rms(x,y=0,z=12).txt'

point_num = 100
err_filter_range = 8
# -------------------------------------------------------------------------
# endregion


lefts = []
rights = []

# -------------------------------------------------------------------------
# region
# calculate for a
rs = RS(case_a)
rs.load()
central_x, central_y = pBase.CaseInfo.Central_Position_Grid
plot_x, plot_y = pBase.pos_mm_to_index_list([0],[0])
line_y = plot_y[0]

left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]

# rms_a = np.sqrt(rs.vv[left:right,line_y])
rms_a = nanmean_filter2d(np.sqrt(rs.vv), err_filter_range)[left:right,line_y]
x_a = pBase.X[0][left:right,line_y].copy()

err_a = rms_error(case_a)
e_a = err_a.estimate_uncertainty(filter_range=err_filter_range)[left:right,line_y]

ws_a.loaddata([x_a, rms_a, e_a/2, -e_a/2])
ws_a.write(fig_path + ws_a_filename)

lefts.append(pBase.X[0][left,line_y])
rights.append(pBase.X[0][right-1,line_y])
# -------------------------------------------------------------------------
# endregion

# -------------------------------------------------------------------------
# region
# calculate for b
rs = RS(case_b)
rs.load()

central_x, central_y = pBase.CaseInfo.Central_Position_Grid
plot_x,plot_y = pBase.pos_mm_to_index_list([0],[12])
line_y = plot_y[0]

left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]

x_b = pBase.X[0][left:right,line_y].copy()
# rms_b = np.sqrt(rs.vv[left:right,line_y])
rms_b = nanmean_filter2d(np.sqrt(rs.vv),err_filter_range)[left:right,line_y]
err_b = rms_error(case_b)
e_b = err_b.estimate_uncertainty(filter_range=err_filter_range)[left:right,line_y]
ws_b.loaddata([x_b, rms_b, e_b/2, -e_b/2])
ws_b.write(fig_path + ws_b_filename)

lefts.append(pBase.X[0][left,line_y])
rights.append(pBase.X[0][right-1,line_y])
# -------------------------------------------------------------------------
# endregion

x_uniform = np.linspace(
    max(lefts),
    min(rights),
    point_num
)

fit_slice = slice(1,-1)
f_v = interp1d(x_a[fit_slice], rms_a[fit_slice], kind='cubic', fill_value='extrapolate')
f_ev = interp1d(x_a[fit_slice], e_a[fit_slice], kind='cubic', fill_value='extrapolate')
f_w = interp1d(x_b[fit_slice], rms_b[fit_slice], kind='cubic', fill_value='extrapolate')
f_ew = interp1d(x_b[fit_slice], e_b[fit_slice], kind='cubic', fill_value='extrapolate')

a_uniform = f_v(x_uniform)
e_a_uni = f_ev(x_uniform)
b_uniform = f_w(x_uniform)
e_b_uni = f_ew(x_uniform)

error_ratio = np.abs(a_uniform/b_uniform) * np.sqrt( (e_a_uni/a_uniform)**2 + (e_b_uni/b_uniform)**2 )
ws.loaddata([x_uniform, a_uniform/b_uniform, error_ratio/2, -error_ratio/2, a_uniform, e_a_uni/2, -e_a_uni/2, b_uniform, e_b_uni/2, -e_b_uni/2])
ws.write(fig_path + ws_filename)




plt.plot(x_uniform, a_uniform/b_uniform, '-', label=f'v_rms/w_rms_y=0')
# plt.plot(x_a, rms_a, 'o', label='original v_rms')
# plt.plot(x_uniform, a_uniform, '-', label='interpolated v_rms')
# plt.plot(x_b, rms_b, 'o', label='original w_rms')
# plt.plot(x_uniform, b_uniform, '-', label='interpolated w_rms')

plt.xlabel('x')
plt.ylabel('v_rms/w_rms')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()