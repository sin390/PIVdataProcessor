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
        return np.sqrt(rs.uu)

import matplotlib.pyplot as plt
plt.figure(figsize=(6,4))

# -------------------------------------------------------------------------
# endregion

# -------------------------------------------------------------------------
# region
case_a = 'Case01XZ_Y0_Ethanol'
case_b = 'Case01XZ_Y0_Ethanol'
case_c = 'Case01XZ_Y0_Ethanol'


comment_a = ['XZ-plane Y = 0, u_rms(x, y=0, z=12)']
ws_a = WriteHandler(['x(mm)','u_rms','err(u_rms)','-err(u_rms)'], comment_a)
ws_a_filename = '\\XZ-Y0, u_rms(x,y=0,z=12).txt'

comment_b = ['XZ-plane Y = 0, u_rms(x, y=0, z=13)']
ws_b = WriteHandler(['x(mm)','u_rms','err(u_rms)','-err(u_rms)'],comment_b)
ws_b_filename = '\\XZ-Y0, u_rms(x,y=0,z=13).txt'

comment_c = ['XZ-plane Y = 0, u_rms(x, y=0, z=17)']
ws_c = WriteHandler(['x(mm)','u_rms','err(u_rms)','-err(u_rms)'],comment_c)
ws_c_filename = '\\XZ-Y0, u_rms(x,y=0,z=17).txt'

point_num = 100
err_filter_range = 8
# -------------------------------------------------------------------------
# endregion



# -------------------------------------------------------------------------
# region
# calculate for a
rs = RS(case_a)
rs.load()
central_x, central_y = pBase.CaseInfo.Central_Position_Grid
plot_x, plot_y = pBase.pos_mm_to_index_list([0],[12])
line_y = plot_y[0]

left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]

# rms_a = np.sqrt(rs.vv[left:right,line_y])
rms_a = nanmean_filter2d(np.sqrt(rs.uu), err_filter_range)[left:right,line_y]
x_a = pBase.X[0][left:right,line_y].copy()

err_a = rms_error(case_a)
e_a = err_a.estimate_uncertainty(filter_range=err_filter_range)[left:right,line_y]

ws_a.loaddata([x_a, rms_a, e_a/2, -e_a/2])
ws_a.write(fig_path + ws_a_filename)


# -------------------------------------------------------------------------
# endregion

# -------------------------------------------------------------------------
# region
# calculate for b
rs = RS(case_b)
rs.load()

central_x, central_y = pBase.CaseInfo.Central_Position_Grid
plot_x,plot_y = pBase.pos_mm_to_index_list([0],[13])
line_y = plot_y[0]

left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]

x_b = pBase.X[0][left:right,line_y].copy()
# rms_b = np.sqrt(rs.vv[left:right,line_y])
rms_b = nanmean_filter2d(np.sqrt(rs.uu),err_filter_range)[left:right,line_y]
err_b = rms_error(case_b)
e_b = err_b.estimate_uncertainty(filter_range=err_filter_range)[left:right,line_y]
ws_b.loaddata([x_b, rms_b, e_b/2, -e_b/2])
ws_b.write(fig_path + ws_b_filename)


# -------------------------------------------------------------------------
# endregion


# -------------------------------------------------------------------------
# region
# calculate for c
rs = RS(case_c)
rs.load()

central_x, central_y = pBase.CaseInfo.Central_Position_Grid
plot_x,plot_y = pBase.pos_mm_to_index_list([0],[17])
line_y = plot_y[0]

left,right = pBase.CaseInfo.Effective_Range[0]
bottom,up = pBase.CaseInfo.Effective_Range[1]

x_c = pBase.X[0][left:right,line_y].copy()
# rms_c = np.sqrt(rs.vv[left:right,line_y])
rms_c = nanmean_filter2d(np.sqrt(rs.uu),err_filter_range)[left:right,line_y]
err_c = rms_error(case_c)
e_c = err_c.estimate_uncertainty(filter_range=err_filter_range)[left:right,line_y]
ws_c.loaddata([x_c, rms_c, e_c/2, -e_c/2])
ws_c.write(fig_path + ws_c_filename)


# -------------------------------------------------------------------------
# endregion



plt.plot(x_a, rms_a, 'o', label='z=12')
# plt.plot(x_uniform, a_uniform, '-', label='interpolated v_rms')
plt.plot(x_b, rms_b, 'o', label='z=13')
plt.plot(x_c, rms_c, 'o', label='z=17')
# plt.plot(x_uniform, b_uniform, '-', label='interpolated w_rms')

plt.xlabel('x')
plt.ylabel('u_rms')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()