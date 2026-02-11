''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2024/04/04  =
=========================
'''

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
import ZZZ_Result_Manager.A01_cases as A01


for case in A01.cases_w:
    pBase.preprocess_data(case)