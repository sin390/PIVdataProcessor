''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2024/04/04  =
=========================
'''

import numpy as np

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase 
from pivdataprocessor.A01_toolbox import float_precsion

edge_cut = 3


# Type 1: Define the flow field center as the location where the mean velocity approaches zero.
cases1 = ['Case01','Case02','Case03','Case04','Case05','Case06']
for case in cases1:
    pBase.load_case(case)
    Nx = pBase.CaseInfo.Nx
    Ny = pBase.CaseInfo.Ny
    
    cutted_range = ((edge_cut,Nx-1-edge_cut),(edge_cut,Ny-1-edge_cut))
    pBase.CaseInfo.Effective_Range = cutted_range
    
    sum_nine_points = np.zeros((Nx-2,Ny-2), dtype=float_precsion)

    for i in range(-1,2):
        for j in range(-1,2):
            tmp_U = pBase.avg_U[0][1+i : Nx-1+i, 1+j : Ny-1+j]
            tmp_V = pBase.avg_U[1][1+i : Nx-1+i, 1+j : Ny-1+j]
            sum_nine_points += tmp_U*tmp_U + tmp_V*tmp_V

    sum_nine_points = sum_nine_points/9

    sum_nine_points = np.where(np.isnan(sum_nine_points), np.inf, sum_nine_points)
    min_index_flat = np.argmin(sum_nine_points)
    min_index = np.unravel_index(min_index_flat, sum_nine_points.shape)
    min_index_tuple = (int(min_index[0])+1,int(min_index[1])+1)
    pBase.CaseInfo.Central_Position_Flow = min_index_tuple
    pBase.save_case()


#Type 2: Specify the center of the measurement region as the center of the flow field.
cases2 = ['Mori465']
for case in cases2:
    pBase.load_case(case)
    Nx = pBase.CaseInfo.Nx
    Ny = pBase.CaseInfo.Ny
    
    cutted_range = ((edge_cut,Nx-1-edge_cut),(edge_cut,Ny-1-edge_cut))
    pBase.CaseInfo.Effective_Range = cutted_range
    pBase.CaseInfo.Central_Position_Flow = (int(Nx/2),int(Ny/2))
    pBase.CaseInfo.Central_Position_Flow = pBase.CaseInfo.Central_Position_Grid
    pBase.save_case()


