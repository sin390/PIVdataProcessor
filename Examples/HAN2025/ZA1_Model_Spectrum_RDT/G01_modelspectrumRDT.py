''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.1         =
= Date:     2025/06/02  =
=========================
'''

import numpy as np
from pivdataprocessor.L02_extension_tmpl import GeneralTemplate as GT
from pivdataprocessor.A01_toolbox import float_precsion
from pivdataprocessor.L01_base import GeneralDataHandler
from dataclasses import dataclass

@dataclass
class k_range(GeneralDataHandler):
    kmin: float = 0.0
    kmax: float = 0.0
    points: int = 0
    dk: float = 0.0
    L: float = 0.0
    Re_lamda: float = 0.0    
    def recommend_value(self, L, Re_lamda):
        self.L = L
        self.Re_lamda = Re_lamda

        domain = 10*L
        self.kmin = 2 * np.pi / domain
        eta = 15**(3/4) * Re_lamda**(-3/2) * L
        self.kmax = 2 * np.pi / eta
        self.points = int(domain/eta)
        self.dk = (self.kmax-self.kmin)/(self.points-1)

class RDT_Axis_Symmetric_Strain(GT):
    def __init__(self, k_range_long:k_range = None, k_range_trans:k_range = None, casename:str = 'RDT_Axis_Symmetric_Strain',ifinit = False):
        super().__init__(casename)
        if ifinit == True:
            self.k_range_long= k_range_long
            self.k_range_trans = k_range_trans
            self.k_long = np.linspace(self.k_range_long.kmin, self.k_range_long.kmax, self.k_range_long.points)
            self.rm_and_create_directory(self.result_path)
            self.k_range_long.to_yaml(self.result_path + '/k_range_long.yaml')
            self.k_range_trans.to_yaml(self.result_path + '/k_range_trans.yaml')
            self.GTreport('====',ifinit=True)
        else:
            self.k_range_long = k_range.from_yaml(self.result_path + '/k_range_long.yaml')
            self.k_long = np.linspace(self.k_range_long.kmin, self.k_range_long.kmax, self.k_range_long.points)
            self.k_range_trans = k_range.from_yaml(self.result_path + '/k_range_trans.yaml')
        
        self.E11k1_origin = np.zeros(shape=(self.k_range_long.points,),dtype=float_precsion)
        self.E11k1 = np.zeros(shape=(self.k_range_long.points,),dtype=float_precsion)
        self.E22k2 = np.zeros(shape=(self.k_range_long.points,),dtype=float_precsion)
    def model_spectrum(self, k):
        pass 


    def load_origin(self):
        self.k_range_long = k_range.from_yaml(self.result_path + '/k_range_long.yaml')
        self.k_long = np.linspace(self.k_range_long.kmin, self.k_range_long.kmax, self.k_range_long.points)
        self.k_range_trans = k_range.from_yaml(self.result_path + '/k_range_trans.yaml')
        self.E11k1_origin = self.load_nparray_from_bin(np.zeros((self.k_range_long.points,)), self.result_path + '/E11k1_origin.bin')
    
    def load_E11k1(self, c):
        self.E11k1 = self.load_nparray_from_bin(np.zeros((self.k_range_long.points,)), self.result_path + f'/E11k1_{int(c*100)}.bin')
    def load_E22k2(self, c):
        self.E22k2 = self.load_nparray_from_bin(np.zeros((self.k_range_long.points,)), self.result_path + f'/E22k2_{int(c*100)}.bin')

    
    def cal_integral_scale(self, k_long, E):
        dk = k_long[1]-k_long[0]
        tmp = E/k_long*dk
        integral_scale = np.pi/2*tmp.sum()/self.cal_energy(k_long,E)
        return integral_scale
    
    def cal_energy(self, k_long, E):
        dk = k_long[1]-k_long[0]
        tmp = E*dk
        energy = tmp.sum()
        return energy

    def cal_origin(self):
        k1 = self.k_long
        tmp_k2 = np.linspace(self.k_range_trans.kmin, self.k_range_trans.kmax, self.k_range_trans.points)
        tmp_k3 = tmp_k2

        k2, k3 = np.meshgrid(tmp_k2,tmp_k3,indexing='ij')
        for i in range(self.k_range_long.points):
            print(f'cal_origin: {i} of {self.k_range_long.points}')
            squared_kmag = np.zeros(shape=k2.shape)
            squared_kmag = k1[i]**2+ k2**2 + k3**2
            tmp = self.model_spectrum(np.sqrt(squared_kmag))
            tmp *= (k2**2 + k3**2) / (np.pi* squared_kmag**2) 
            tmp *= self.k_range_trans.dk**2
            self.E11k1_origin[i] = tmp.sum()*2
        self.save_nparray_to_bin(self.E11k1_origin, self.result_path + '/E11k1_origin.bin')        

    def cal_RDT_E11k1(self, c):
        self.GTreport(f'cal_RDT_E11k1: c = {c}')
        k1 = self.k_long
        tmp_k2 = np.linspace(self.k_range_trans.kmin, self.k_range_trans.kmax, self.k_range_trans.points)
        tmp_k3 = tmp_k2
        
        k2, k3 = np.meshgrid(tmp_k2,tmp_k3,indexing='ij')
        img_k1 = k1* c
        img_k2 = k2/ c**0.5
        img_k3 = k3/ c**0.5
        for i in range(self.k_range_long.points):
            print(f'cal_RDT_E11k1: {i} of {self.k_range_long.points}')
            squared_kmag = np.zeros(shape=k2.shape)
            squared_kmag = k1[i]**2 + k2**2 + k3**2
            img_squared_kmag = np.zeros(shape=k2.shape)
            img_squared_kmag = img_k1[i]**2 + img_k2**2 + img_k3**2
            tmp = self.model_spectrum(np.sqrt(img_squared_kmag))
            tmp *= (img_k2**2+img_k3**2) / (np.pi* squared_kmag**2)
            tmp *= self.k_range_trans.dk**2
            self.E11k1[i] = tmp.sum()*2
        self.save_nparray_to_bin(self.E11k1, self.result_path + f'/E11k1_{int(c*100)}.bin') 

    def cal_RDT_E22k2(self,c):
        k2 = self.k_long
        tmp_k1 = np.linspace(self.k_range_trans.kmin, self.k_range_trans.kmax, self.k_range_trans.points)
        tmp_k3 = tmp_k1
        k1, k3 = np.meshgrid(tmp_k1,tmp_k3,indexing='ij')

        img_k1 = k1* c
        img_k2 = k2/ c**0.5
        img_k3 = k3/ c**0.5

        for i in range(self.k_range_long.points):
            print(f'cal_RDT_E22k2: {i} of {self.k_range_long.points}')
            squared_kmag = np.zeros(shape=k2.shape)
            squared_kmag = k1**2 + k2[i]**2 + k3**2
            img_squared_kmag = np.zeros(shape=k1.shape)
            img_squared_kmag = img_k1**2 + img_k2[i]**2 + img_k3**2
            tmp = self.model_spectrum(np.sqrt(img_squared_kmag))
            tmp /= np.pi* squared_kmag**2 *img_squared_kmag
            tmp *= c**(-3)*img_k1**2*(img_k1**2+img_k2[i]**2) + c**3*img_k3**2*(img_k2[i]**2+img_k3**2)+ 2*img_k1**2*img_k3**2
            tmp *= self.k_range_trans.dk**2
            self.E22k2[i] = tmp.sum()*2
        self.save_nparray_to_bin(self.E22k2, self.result_path + f'/E22k2_{int(c*100)}.bin')      


class Pope_AX(RDT_Axis_Symmetric_Strain):
    def __init__(self, k_range_long:k_range, k_range_trans:k_range, L, Re_lamda, epsilon, C = 1.5, CL = 6.78, p0 = 2, Ceta = 0.4, beta = 5.2
                 ,casename:str = 'Pope_AX',ifinit = False):
        super().__init__(k_range_long, k_range_trans, casename=casename, ifinit=ifinit)
        self.L = L
        self.eta = 15**(3/4) * Re_lamda**(-3/2) * self.L #Taylor-Kolmogorov scaling
        self.epsilon = epsilon
        self.C = C
        self.CL = CL
        self.p0 = p0
        self.Ceta = Ceta
        self.beta = beta

    def model_spectrum(self, k):
        fL = ((k * self.L) / np.sqrt((k * self.L)**2 + self.CL))**(5/3 + self.p0)
        feta = np.exp(-self.beta * ((k * self.eta)**4 + self.Ceta**4)**0.25 - self.Ceta)
        return self.C * self.epsilon**(2/3) * k**(-5/3) * fL * feta         

class Pao_AX(RDT_Axis_Symmetric_Strain):
    def __init__(self, k_range_long:k_range, k_range_trans:k_range, L, Re_lamda, epsilon, m = 11/2, alpha = 1.52, casename:str = 'unamed'):
        super().__init__(k_range_long, k_range_trans,casename=casename)
        self.L = L
        self.eta = 15**(3/4) * Re_lamda**(-3/2) * self.L
        self.epsilon = epsilon
        self.m = m
        self.alpha = alpha
    
    def model_spectrum(self,k):
        fL = (1 + (3*self.alpha/2)*(k*self.L)**(-2/3))**self.m
        feta = np.exp(-(3*self.alpha/2)*(self.eta*k)**(4/3))
        return self.alpha * self.epsilon**(2/3) * k **(-5/3) / fL * feta

if __name__ == "__main__":
    integral_L = 2e-2
    Re_lamda = 300
    epsilon = 4.5e4
    casename = f'Re_{Re_lamda}'

    k_range_long = k_range()
    k_range_long.recommend_value(integral_L,Re_lamda)
    k_range_trans = k_range()
    k_range_trans.recommend_value(integral_L,Re_lamda)

    # Pope = Pope_AX(k_range_long, k_range_trans, L=integral_L, Re_lamda=Re_lamda, epsilon=epsilon, casename=casename,ifinit=True)
    Pope = Pope_AX(k_range_long, k_range_trans, L=integral_L, Re_lamda=Re_lamda, epsilon=epsilon, casename=casename,ifinit=False)
    # Pope.cal_origin()
    # Pope.cal_RDT_E11k1(c=0.25)
    Pope.cal_RDT_E22k2(c=0.25)