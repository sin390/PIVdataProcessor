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
from G01_fitted_slope import FittedSlope
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

# -------------------------------------------------------------------------
# region
class S22error(UET):
    def __init__(self, case_name):
        super().__init__(case_name)
    def load_target(self, casename: str):
        fs = FittedSlope(casename)
        fs.load_fitted()
        return fs.fit_avg_dUdX[1][1] * 1000  # convert to 1/s

# -------------------------------------------------------------------------
# endregion

import matplotlib.pyplot as plt
filter_range = 8
plt.figure(figsize=(6,4))

ws = WriteHandler(['x(mm)','S33/S22','error_(S33/S22)','interpolatedS22','error(itp_S22)','interpolatedS33','error(itp_S33)'])
ws_S33 = WriteHandler(['x(mm)','S33','error_S33'])
ws_S22 = WriteHandler(['x(mm)','S22','error_S22'])
point_num = 50
# y = 0, z = 0 line

lefts = []
rights = []

fs = FittedSlope('Case01')
fs.load_fitted()
central_x, central_y = pBase.CaseInfo.Central_Position_Grid
left,right = pBase.CaseInfo.Effective_Range[0]
right-=5
bottom,up = pBase.CaseInfo.Effective_Range[1]
x_xyplane = pBase.X[0][left:right,central_y].copy()
lefts.append(pBase.X[0][left,central_y])
rights.append(pBase.X[0][right-1,central_y])
S22_xyplane = fs.fit_avg_dUdX[1][1][left:right,central_y] * 1000

error_S22_xyplane = S22error('Case01')
eS22 = error_S22_xyplane.estimate_uncertainty(filter_range=filter_range)[left:right,central_y]
ws_S22.loaddata([x_xyplane,S22_xyplane,eS22/2])


fs = FittedSlope(f'Case01XZ_Y00')
fs.load_fitted()
central_x, central_y = pBase.CaseInfo.Central_Position_Grid
left,right = pBase.CaseInfo.Effective_Range[0]
right-=5
bottom,up = pBase.CaseInfo.Effective_Range[1]
x_xzplane = pBase.X[0][left:right,central_y].copy()
lefts.append(pBase.X[0][left,central_y])
rights.append(pBase.X[0][right-1,central_y])

S33_xzplane = fs.fit_avg_dUdX[1][1][left:right,central_y] * 1000
error_S33_xzplane = S22error(f'Case01XZ_Y00')
eS33 = error_S33_xzplane.estimate_uncertainty(filter_range=filter_range)[left:right,central_y]
ws_S33.loaddata([x_xzplane,S33_xzplane,eS33/2])


x_uniform = np.linspace(
    max(lefts),
    min(rights),
    point_num
)

f_S22 = interp1d(x_xyplane, S22_xyplane, kind='cubic', fill_value='extrapolate')
f_eS22 = interp1d(x_xyplane[1:-1], eS22[1:-1], kind='cubic', fill_value='extrapolate')
f_S33 = interp1d(x_xzplane, S33_xzplane, kind='cubic', fill_value='extrapolate')
f_eS33 = interp1d(x_xzplane[1:-1], eS33[1:-1], kind='cubic', fill_value='extrapolate')

S22_uniform = f_S22(x_uniform)
S33_uniform = f_S33(x_uniform)
eS22_uniform = f_eS22(x_uniform)
eS33_uniform = f_eS33(x_uniform)

error_ratio = np.abs(S33_uniform/S22_uniform) * np.sqrt( (eS22_uniform/S22_uniform)**2 + (eS33_uniform/S33_uniform)**2 )

ws.loaddata([x_uniform, S33_uniform/S22_uniform, error_ratio/2, S22_uniform, eS22_uniform/2, S33_uniform, eS33_uniform/2])

ws.write(fig_path+f'/S33_S22_y=0_z=0_line.txt')
ws_S22.write(fig_path+f'/(XY)S22_y=0_z=0_line.txt')
ws_S33.write(fig_path+f'/(XZ)S33_y=0_z=0_line.txt')