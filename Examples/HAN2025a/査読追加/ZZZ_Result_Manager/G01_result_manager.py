''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/12/03  =
=========================
'''

from pivdataprocessor.L02_extension_tmpl import ParamTable as PT
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT

import os

class ResultManager(GT):
    def __init__(self, case_name='unnamed', ifdelete = False):
        self.case_name = case_name
        super().__init__(case_name)
        self.result_table = PT(self.result_path + "/" + case_name + ".json", ifdelete=ifdelete)
    
    def clean(self):
        self.result_table.data = {}
        self.result_table.save()
    