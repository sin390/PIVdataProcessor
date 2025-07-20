''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/07/08  =
=========================
'''

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase

cases = ['All100','Grad','AntiGrad','Shear']

for case_id in range(len(cases)):
    pBase.load_case(casename=cases[case_id])
    left,right = pBase.CaseInfo.Uniform_Range[0]
    bottom,up = pBase.CaseInfo.Uniform_Range[1]
    print(f'X range: {pBase.X[0, left,bottom]:.2f} to {pBase.X[0, right,up]:.2f}')
    print(f'Y range: {pBase.X[0, left,bottom]:.2f} to {pBase.X[0, right,up]:.2f}')