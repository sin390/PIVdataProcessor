''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2024/04/04  =
=========================
'''

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase 

cases = ['Case01','Case02','Case03','Case04','Case05','Case06']
for case in cases:
    pBase.preprocess_data(case)