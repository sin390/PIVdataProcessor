''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/07/17  =
=========================
'''

import numpy as np
from dataclasses import dataclass
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L01_base import GeneralDataHandler as GDH
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion


@dataclass
class FilterOptionShape(GDH):
    total_options: int = 0

class FilterOptionInfo(pTS):
    def __init__(self, casename:str, option_list:np.ndarray = None, ifcleandir:bool = False):
        '''
        option_list: np.ndarray
            shape: (2, N), N is the number of options
            option_list[0] is Lf_in_mm, option_list[1] is truncate_coef
        '''
        super().__init__(casename)
        self.casename = casename
        self.result_path = self.result_path + f'/{self.casename}'
        if ifcleandir:
            self.rm_and_create_directory(self.result_path)
        self.option_list = option_list
        self.option_list_shape = FilterOptionShape()

    def save(self):
        self.option_list_shape = FilterOptionShape(self.option_list.shape[-1])
        self.option_list_shape.to_yaml(self.result_path + f'/shape.yaml')
        self.save_nparray_to_bin(self.option_list, self.result_path + f'/{self.casename}.bin')
    def load(self):
        self.option_list_shape = FilterOptionShape.from_yaml(self.result_path + f'/shape.yaml')
        self.option_list = np.zeros((2, self.option_list_shape.total_options), dtype=float_precsion)
        self.option_list = self.load_nparray_from_bin(self.option_list, self.result_path + f'/{self.casename}.bin')

if __name__ == "__main__":
    cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06', 'Mori465']
    cf_lists = np.array([5.0, 6.0, 7.0, 8.0, 9.0])
    truncate_lists = np.zeros_like(cf_lists) + 2.0
    for case_id in range(len(cases)):
        pBase.load_case(cases[case_id])
        Lf_lists = cf_lists * pBase.dX[0]
        option_list = np.array([Lf_lists, truncate_lists])
        FO = FilterOptionInfo(cases[case_id], option_list=option_list, ifcleandir=True)
        FO.save()