''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/06/02  =
=========================
'''
import numpy as np
import matplotlib.pyplot as plt

from ZA1_Model_Spectrum_RDT.G01_modelspectrumRDT import Pope_AX, Pao_AX, k_range
from pivdataprocessor.A01_toolbox import float_precsion
from pivdataprocessor.A02_pltcfg import getplotpath
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT

class LargeScaleAnisotropy(GT):
    def __init__(self, casename:str, c_points = 10):
        super().__init__()
        self.result_path = self.result_path+ '/' + casename
        self.c = np.zeros((c_points,), dtype= float_precsion)
        self.L11_L22 = np.zeros((c_points,), dtype= float_precsion)
        self.uu_vv = np.zeros((c_points,), dtype= float_precsion)

    def LSA_save(self):
        self.save_nparray_to_bin(self.c, self.result_path+'/c.bin')
        self.save_nparray_to_bin(self.L11_L22, self.result_path+'/L11_L22.bin')
        self.save_nparray_to_bin(self.uu_vv, self.result_path+'/uu_vv.bin')

    def LSA_load(self):
        self.c = self.load_nparray_from_bin(self.c, self.result_path+'/c.bin')
        self.L11_L22 = self.load_nparray_from_bin(self.L11_L22, self.result_path+'/L11_L22.bin')
        self.uu_vv = self.load_nparray_from_bin(self.uu_vv, self.result_path+'/uu_vv.bin')

def log_c_with_one(min, max, N_left, N_right):
    left = np.geomspace(min, 1, N_left, endpoint=False)
    right = np.geomspace(1, max, N_right+1, endpoint=True)
    return np.concatenate((left,right))

if __name__ == "__main__":

    c = log_c_with_one(1e-1, 10, 50, 50)
    lsa = LargeScaleAnisotropy('Pope_LowRe', c_points=len(c))
    lsa.c = c
    
    lsa.rm_and_create_directory(lsa.result_path)
    integral_L = 2e-2
    Re_lamda = 50
    epsilon = 4.5e4
    lsa.GTreport(f'c_points: {len(c)}')
    lsa.GTreport(f'Model spectrum parameters:')
    lsa.GTreport(f'integral_L: {integral_L}')
    lsa.GTreport(f'Re_lamda: {Re_lamda}')
    lsa.GTreport(f'epsilon: {epsilon}')

    k_range_long = k_range()
    k_range_long.recommend_value(integral_L,Re_lamda)
    k_range_trans = k_range()
    k_range_trans.recommend_value(integral_L,Re_lamda)

    Pope = Pope_AX(k_range_long, k_range_trans, L=integral_L, Re_lamda=Re_lamda, epsilon=epsilon)

    for c_id in range(len(c)):
        print(f'{c_id} of {len(c)}')
        Pope.cal_RDT_E11k1(c=c[c_id])
        uu = Pope.cal_energy(Pope.k_long,Pope.E11k1)
        L11 = Pope.cal_integral_scale(Pope.k_long,Pope.E11k1)
        Pope.cal_RDT_E22k2(c=c[c_id])
        vv = Pope.cal_energy(Pope.k_long,Pope.E22k2)
        L22 = Pope.cal_integral_scale(Pope.k_long,Pope.E22k2)
        lsa.uu_vv[c_id] = uu/vv
        lsa.L11_L22[c_id] = L11/L22
    
    lsa.LSA_save()

