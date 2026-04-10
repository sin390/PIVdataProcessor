''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

from turtle import st
import matplotlib.pyplot as plt
import numpy as np

from Q01_Plot.L02_cloud_plot import CloudFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Z15_POD.G01_POD_Handler import PODHandler as POD


quickset()
nrows = 2
ncols = 3
CF = CloudFigure(nrows=2, ncols=3,figsize=(16,10),cmap="turbo")
''

xlables = [r'$x$ (mm)']
ylables = [r'$y$ (mm)']
axtitles = ['Mode 1', 'Mode 2', 'Mode 3', 'Mode 4', 'Mode 5', 'Mode 6']



global_min = 0
global_max = 60
first_quiv = None

width=0.004

from Z03_Velocity_Field_Handler.G01_velocity_field_handler import params,params_mori
case = 'Case03'
filter = 'gaussian_bp'
param = params[1][0]

# case = 'Mori_465'
# filter = 'gaussian_bp'
# param = params_mori[1][1]

pod = POD(case,filter,param)
pod.PODload()

X = pod.POD_X[0]
Y = pod.POD_X[1]

magmax = 0
magmin = 0
Label = ['']*6
''

for mode_id in range(nrows*ncols):
    pod_uv = pod.energy_mode(mode_id)
    pod_u = pod_uv[0]
    pod_v = pod_uv[1]
    magnitude = np.sqrt(pod_u**2 + pod_v**2)
    if mode_id == 0:
        magmax = magnitude.max()
        magmin = 0
    CF.add_cloud(mode_id, X, Y, magnitude, vmin=magmin, vmax=magmax)
    CF.add_quiver(mode_id, X, Y, pod_u, pod_v, stride=1, color='k', scale=2000, width=width)

plt.show()