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


#Type 1: Select a region (in mm) where two-point statistics can be applied.
cases1 = []
distances_x = []
distances_y = [] 

for case_id in range(len(cases1)):
    pBase.load_case(cases1[case_id])
    center_index = pBase.CaseInfo.Central_Position_Flow
    Xc = pBase.X[0][center_index[0],center_index[1]]
    Yc = pBase.X[1][center_index[0],center_index[1]]
    
    distance_x = distances_x[case_id]
    distance_y = distances_y[case_id]
    X_left, X_right = Xc-distance_x, Xc+distance_x
    Y_bottom, Y_up = Yc-distance_y, Yc+distance_y

    x_list, y_list = pBase.pos_mm_to_index_list([X_left,X_right],[Y_bottom,Y_up])
    left_index, right_index = x_list[0], x_list[1]
    bottom_index, up_index = y_list[0], y_list[1]

    pBase.CaseInfo.Uniform_Range = ((left_index,right_index),(bottom_index,up_index))
    pBase.save_case()


#Type 2: Two-point statistics can be applied across the measurement region.
cases2 = ['Case01','Case02','Case03','Case04','Case05','Case06','Mori465']
for case in cases2:
    pBase.load_case(case)   
    pBase.CaseInfo.Uniform_Range = pBase.CaseInfo.Effective_Range
    pBase.save_case()
