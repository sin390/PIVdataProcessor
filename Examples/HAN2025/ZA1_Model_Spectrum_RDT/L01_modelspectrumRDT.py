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
from dataclasses import dataclass

@dataclass
class k_range():
    def __init__(self, kmin=0, kmax=0, point_number=0):
        self.kmin = kmin
        self.kmax = kmax
        self.points = point_number
        self.dk = (kmax-kmin)/(point_number-1)
    
    def recommend_value(self, L, Re_lamda):
        domain = 10*L
        self.kmin = 2 * np.pi / domain
        eta = 15**(3/4) * Re_lamda**(-3/2) * L
        self.kmax = 2 * np.pi / eta
        self.points = int(domain/eta)
        self.dk = (self.kmax-self.kmin)/(self.points-1)

class RDT_Axis_Symmetric_Strain(GT):
    def __init__(self, k_range_long:k_range, k_range_trans:k_range):

        super().__init__()
        self.k_range_long= k_range_long
        self.k_range_trans = k_range_trans

        self.k_long = np.linspace(self.k_range_long.kmin, self.k_range_long.kmax, self.k_range_long.points)

        self.E11k1_origin = np.zeros(shape=(k_range_long.points,),dtype=float_precsion)
        self.E11k1 = np.zeros(shape=(k_range_long.points,),dtype=float_precsion)
        self.E22k2 = np.zeros(shape=(k_range_long.points,),dtype=float_precsion)
        self.E33k3 = np.zeros(shape=(k_range_long.points,),dtype=float_precsion)    

    def model_spectrum(self, k):
        pass 
    
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
            squared_kmag = np.zeros(shape=k2.shape)
            squared_kmag = k1[i]**2+ k2**2 + k3**2
            tmp = self.model_spectrum(np.sqrt(squared_kmag))
            tmp *= (k2**2 + k3**2) / (np.pi* squared_kmag**2) 
            tmp *= self.k_range_trans.dk**2
            self.E11k1_origin[i] = tmp.sum()


    def cal_RDT_E11k1(self, c):
        k1 = self.k_long
        tmp_k2 = np.linspace(self.k_range_trans.kmin, self.k_range_trans.kmax, self.k_range_trans.points)
        tmp_k3 = tmp_k2
        
        k2, k3 = np.meshgrid(tmp_k2,tmp_k3,indexing='ij')
        img_k1 = k1* c
        img_k2 = k2/ c**0.5
        img_k3 = k3/ c**0.5

        for i in range(self.k_range_long.points):
            squared_kmag = np.zeros(shape=k2.shape)
            squared_kmag = k1[i]**2 + k2**2 + k3**2
            img_squared_kmag = np.zeros(shape=k2.shape)
            img_squared_kmag = img_k1[i]**2 + img_k2**2 + img_k3**2
            tmp = self.model_spectrum(np.sqrt(img_squared_kmag))
            tmp *= (img_k2**2+img_k3**2) / (np.pi* squared_kmag**2)
            tmp *= self.k_range_trans.dk**2
            self.E11k1[i] = tmp.sum()

    def cal_RDT_E22k2(self,c):
        k2 = self.k_long
        tmp_k1 = np.linspace(self.k_range_trans.kmin, self.k_range_trans.kmax, self.k_range_trans.points)
        tmp_k3 = tmp_k1
        k1, k3 = np.meshgrid(tmp_k1,tmp_k3,indexing='ij')

        img_k1 = k1* c
        img_k2 = k2/ c**0.5
        img_k3 = k3/ c**0.5

        for i in range(self.k_range_long.points):
            squared_kmag = np.zeros(shape=k2.shape)
            squared_kmag = k1**2 + k2[i]**2 + k3**2
            img_squared_kmag = np.zeros(shape=k1.shape)
            img_squared_kmag = img_k1**2 + img_k2[i]**2 + img_k3**2
            tmp = self.model_spectrum(np.sqrt(img_squared_kmag))
            tmp /= np.pi* squared_kmag**2 *img_squared_kmag
            tmp *= c**(-3)*img_k1**2*(img_k1**2+img_k2[i]**2) + c**3*img_k3**2*(img_k2[i]**2+img_k3**2)+ 2*img_k1**2*img_k3**2
            tmp *= self.k_range_trans.dk**2
            self.E22k2[i] = tmp.sum()        

    def cal_RDT_E33k3(self,c):
        k3 = self.k_long
        tmp_k1 = np.linspace(self.k_range_trans.kmin, self.k_range_trans.kmax, self.k_range_trans.points)
        tmp_k2 = tmp_k1
        k1, k2 = np.meshgrid(tmp_k1,tmp_k2,indexing='ij')

        img_k1 = k1* c
        img_k2 = k2/ c**0.5
        img_k3 = k3/ c**0.5

        for i in range(self.k_range_long.points):
            squared_kmag = np.zeros(shape=k1.shape)
            squared_kmag = k1**2 + k2**2 + k3[i]**2
            img_squared_kmag = np.zeros(shape=k1.shape)
            img_squared_kmag = img_k1**2 + img_k2**2 + img_k3[i]**2
            tmp = self.model_spectrum(np.sqrt(img_squared_kmag))
            tmp /= np.pi* squared_kmag**2 *img_squared_kmag
            tmp *= c**(-3)*img_k1**2*(img_k1**2+img_k3[i]**2) + c**3*img_k2**2*(img_k2**2+img_k3[i]**2)+ 2*img_k1**2*img_k2**2
            tmp *= self.k_range_trans.dk**2
            self.E33k3[i] = tmp.sum()  




class Pope_AX(RDT_Axis_Symmetric_Strain):
    def __init__(self, k_range_long:k_range, k_range_trans:k_range, L, Re_lamda, epsilon, C = 1.5, CL = 6.78, p0 = 2, Ceta = 0.4, beta = 5.2):
        super().__init__(k_range_long, k_range_trans)
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
    def __init__(self, k_range_long:k_range, k_range_trans:k_range, L, Re_lamda, epsilon, m = 11/2, alpha = 1.52):
        super().__init__(k_range_long, k_range_trans)
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
    pass
