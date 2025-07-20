''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/26  =
=========================
'''
import numpy as np

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L02_extension_tmpl import PIVDataProcessorExtensionTemplate as pTS
from pivdataprocessor.A01_toolbox import float_precsion

class POD(pTS):
    def __init__(self, casename):
        super().__init__(casename)

        self.Nsnapshot = sum(pBase.frame_numbers_in_runs)
        self.range = ((self.CaseInfo.Central_Position_Grid[0],self.CaseInfo.Uniform_Range[0][1])\
                      ,(self.CaseInfo.Central_Position_Grid[1],self.CaseInfo.Uniform_Range[1][1]))
        self.Nx = self.CaseInfo.Uniform_Range[0][1]-self.CaseInfo.Central_Position_Grid[0]
        self.Ny = self.CaseInfo.Uniform_Range[1][1]-self.CaseInfo.Central_Position_Grid[1]

        Nassemble = 2*self.Nx*self.Ny
        self.assemble = np.zeros((Nassemble,self.Nsnapshot), dtype=float_precsion)
        
        self.max_rank = min(Nassemble,self.Nsnapshot)
        
        self.Umatrix = np.zeros((Nassemble,Nassemble),dtype=float_precsion)
        self.sigma = np.zeros((self.max_rank,),dtype=float_precsion)
        self.VmatrixT = np.zeros((self.Nsnapshot,self.Nsnapshot),dtype=float_precsion)
        self.POD_X = self.X[:, self.range[0][0]:self.range[0][1], self.range[1][0]:self.range[1][1]]


    def PODcalculate(self):
        pBase.rm_and_create_directory(self.result_path)   
        
        ''' assemble '''
        current_snapshot:int = -1
        for run_ID in range(len(pBase.frame_numbers_in_runs)):
            for frame_ID in range(pBase.frame_numbers_in_runs[run_ID]):
                current_snapshot += 1
                pBase.base_load_data_all(run_ID,frame_ID)
                fluc_U = pBase.fluc_U[:, self.range[0][0]:self.range[0][1], self.range[1][0]:self.range[1][1]]
                self.assemble[:,current_snapshot] = fluc_U.reshape(2*self.Nx*self.Ny)
        self.assemble = np.nan_to_num(self.assemble)
        self.Umatrix, self.sigma, self.VmatrixT = np.linalg.svd(self.assemble)
        self.__PODsave()
                
    def singlePODmode(self,rank:int):
        return (self.Umatrix[:,rank]*self.sigma[rank]).reshape(2,self.Nx,self.Ny)
    
    def reconstruct(self, rank_Number, rank_start = 0):
        if rank_Number == -1:
            rank = self.max_rank  
        else:
            rank = rank_Number
        scaled_U = self.Umatrix[:,rank_start:rank] * self.sigma[rank_start:rank][np.newaxis, :]
        uv_fluc = scaled_U @ self.VmatrixT[rank_start:rank, :]
        return uv_fluc.reshape(2, self.Nx, self.Ny, self.Nsnapshot)

    def removemodes(self, rank_number, rank_start = 0):
        r = self.max_rank
        rank = rank_number
        uv_pod = (self.Umatrix[:, :r] * self.sigma[:r][np.newaxis, :]) @ self.VmatrixT[:r, :]
        uv_fluc = (self.Umatrix[:, rank_start:rank] * self.sigma[rank_start:rank][np.newaxis, :]) @ self.VmatrixT[rank_start:rank, :]
        residual = uv_pod - uv_fluc
        return residual.reshape(2, self.Nx, self.Ny, self.Nsnapshot)

    def PODload(self):
        self.Umatrix = self.load_nparray_from_bin(self.Umatrix, self.result_path+'/Umatrix.bin')
        self.sigma = self.load_nparray_from_bin(self.sigma, self.result_path+'/sigma.bin')
        self.VmatrixT = self.load_nparray_from_bin(self.VmatrixT, self.result_path+'/VmatrixT.bin')
        self.POD_X = self.load_nparray_from_bin(self.POD_X, self.result_path+'/POD_X.bin')

    def __PODsave(self):
        self.save_nparray_to_bin(self.Umatrix, self.result_path+'/Umatrix.bin')
        self.save_nparray_to_bin(self.sigma, self.result_path+'/sigma.bin')
        self.save_nparray_to_bin(self.VmatrixT, self.result_path+'/VmatrixT.bin')
        self.save_nparray_to_bin(self.POD_X, self.result_path+'/POD_X.bin')
 
    def cal_assemble_frame_ID(self,run_ID,frame_ID):
        assemble_frame_ID = 0
        for i in range(run_ID):
            assemble_frame_ID += pBase.frame_numbers_in_runs[i]
        assemble_frame_ID += frame_ID       
        return assemble_frame_ID



if __name__ == "__main__":
    cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06','Mori465']
    for case_id in range(len(cases)):
        pod = POD(cases[case_id])
        pod.PODcalculate()
        print(f"{cases[case_id]} completed")