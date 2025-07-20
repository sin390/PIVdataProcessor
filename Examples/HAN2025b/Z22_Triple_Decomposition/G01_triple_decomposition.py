''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/07/17  =
=========================
'''

import numpy as np
import os
from scipy.linalg import schur
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L01_base import GeneralDataHandler as GDH
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import float_precsion as float_precsion
from pivdataprocessor.A01_toolbox import ShortWelfordStatisticsCalculator as swc


from Z21_Filtered_Velocity_Field.G01_filtered_velocity_field import FilteredVelocityField as FVF

@dataclass
class TripleDecompositionInfo(GDH):
    Effective_Range: tuple[tuple[int, int], tuple[int, int]] = ((0, 0), (0, 0))

class TripleDecomposition(pTS):
    def __init__(self, casename, filter_option = None, ifinit = False, ifcleanfolder = False):
        super().__init__(casename)

        self.info = TripleDecompositionInfo()
        self.filter_option = filter_option
        self.casename = casename

        if ifcleanfolder == True:
            self.rm_and_create_directory(self.result_path)

        if filter_option is not None:
            self.result_path = self.result_path + f'/_{int(filter_option[0]*1000)}_{int(filter_option[1]*1000)}'
            self.fvf = FVF(casename, filter_option)
            self.info.Effective_Range = self.fvf.info.Effective_Range
        else:
            self.result_path = self.result_path + '/_original'
            self.info.Effective_Range = self.CaseInfo.Effective_Range        
 
        if ifinit == True:
            self.rm_and_create_directory(self.result_path)
            self.info.to_yaml(self.result_path + '/info.yaml')

        self.info.from_yaml(self.result_path + '/info.yaml')

        left,right = self.info.Effective_Range[0]
        bottom,up = self.info.Effective_Range[1]
        self.effctive_region = (slice(left,right+1),slice(bottom,up+1))

        self.input_dUdX = self.get_a_container(2)
        self.schur_dUdX_total = self.get_a_container(2)
        self.schur_Q = self.get_a_container(2)
        self.schur_dUdX_shear = self.get_a_container(2)
        self.schur_dUdX_rotation = self.get_a_container(2)
        self.schur_dUdX_elongation = self.get_a_container(2)
        self.intensity_shear = self.get_a_container(0)
        self.intensity_rotation = self.get_a_container(0)
        self.intensity_elongation = self.get_a_container(0)

    def __save_path(self, run_id, frame_id):
        return f'{self.result_path}/Run{run_id}', f'{self.result_path}/Run{run_id}/Frame_{frame_id}'

    def __prepare_dUdX(self, run_id, frame_id):
        if self.filter_option is None:
            pBase.base_load_data_all(run_id, frame_id)
            self.input_dUdX = pBase.fluc_dUdX
        else:
            self.fvf.load(run_id, frame_id)
            self.input_dUdX = self.fvf.filtered_fluc_dUdX

    def __parallel_schur(self):
        def __schur_one_point(dUdX):
            pass
    def __loop_schur(self):
        pass

    def __decomposition(self):
        pass

    def __cal_intensity(self):
        pass

    def calculate(self, ifparallel = True):
        for run_id in range(len(self.frame_numbers_in_runs)):
            run_dir, = self.__save_path(run_id,0)
            os.mkdir(run_dir)
            for frame_id in range(self.frame_numbers_in_runs[run_id]):
                _,frame_dir = self.__save_path(run_id,frame_id)
                os.mkdir(frame_dir)
                self.__prepare_dUdX(run_id,frame_id)
                if ifparallel == True:
                    self.__parallel_schur()
                else:
                    self.__loop_schur()
                self.__decomposition()
                self.__cal_intensity()
                self.__save(run_id,frame_id)



    def __save(self, run_id, frame_id):
        _,frame_dir = self.__save_path(run_id,frame_id)

    def load(self, run_id, frame_id):
        _,frame_dir = self.__save_path(run_id,frame_id)

