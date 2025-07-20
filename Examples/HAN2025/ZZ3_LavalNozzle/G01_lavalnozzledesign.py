'''
=========================
= Author:   Z.X. Han    =
= Version:  1.2         =
= Date:     2024/07/01  =
=========================

Cite : 
[1] K. Foelsch. Journal of the Aeronautical Sciences. (1949)
[2] J. Conrad Crown. NACA TN No. 1651. (1948)
[3] E. Witoszynski. in book: Vorträge aus dem Gebiete der Hydro- und Aerodynamik. (1922)
[4] M. S. Kisenko. NACA TM No. 1066. (1944)
'''

import numpy as np
import math
from scipy.optimize import fsolve

import os
from datetime import datetime

'''
    AB  -> (adjust the total length)        -> Straight line
    BC  -> (convergent part)                -> by Witoszynski (introduced by Kisenko) if Witoszynski method applied
    CD  -> (divergent part: initial line)   -> by Crown
    DE  -> (divergent part: final line)     -> by Foelsch
'''

class DesignPars():
    # Overall parameters
    Gamma = 1.4
    Ma_e = 1.36
    D_e = 4.31          # mm
    D_i = 6.0           # mm
    TotalLength = 25    # mm

    method_semiangle = 'given'      # 'given', 'proportional' or 'shortest'
    SemiAngle = 1.1                 # degrees, for the 'given' method.       
    coef_semiangle = 2/4.5          # for the 'proportional' method.

    #====
    
    # BC parameters
    BC_method = 'cubic'             # 'cubic', 'quartic', or 'Witoszynski'
    
    # for 'Witoszynski' method
    Offset_Witoszynski = 10         # shape control introduced by Yi.
    Coef_Length_Witoszynski = 4.14  # emperical value introduced by Kisenko.
    
    # for 'cubic' method
    BC_Referencepoint = 'exit'      # 'exit' or 'throat'
    L_Cubic = 20                    # the length of 'BC' for 'throat', or the length of 'BE' for 'exit'
    #====
    
    # Boundary layer correction.
    BLcorr_method = 'constant'      # 'constant' or 'linear'
    BLcorr = 0.15                   # ''

    def __init__(cls) -> None:
        pass

class OptionPars():
    N_AB = 40
    N_BC = 40
    N_CD = 40
    N_DE = 40

    outputdir = os.getcwd() + "/CCA_Outputs"
    filename = datetime.now().strftime("%Y%m%d%H%M%S")

    def __init__(self) -> None:
        pass


class LavalNozzle():
    Pars = DesignPars()
    Options = OptionPars()

    def __init__(self) -> None:

        '''
            Gamma           -> specific heat ratio
            Ma_e            -> Mach number at the exit section
            D_e             -> diameter of the exit section         (mm)
            D_i             -> diameter of the inlet section        (mm)
            SemiAngle       -> semicone angle at the point D        (degree)
            TotalLength     -> total length of the nozzle           (mm)
            Offset_BC       -> adjust the shape of BC curve         (mm)
            Coef_LengthBC   -> adjust the length of BC curve. Here, 4.14 is a empirical value.
            BLcorr          -> the tangent value of boundary layer correction angle.
                             'BL thickness' = 'distance along the axis (from the throat section)' multipled by 'BLcorr'
        '''            
        
        self.y_throat = 0
        self.semiangle_rads = math.radians(self.Pars.SemiAngle)

        self.ifavailable = {'available': False}
        self.ifavailable = False

        self.rgamma = (self.Pars.Gamma + 1)/(self.Pars.Gamma - 1)

        self.Result_x = {'AB':np.zeros(self.Options.N_AB, dtype=float),
                         'BC':np.zeros(self.Options.N_BC, dtype=float),
                         'CD':np.zeros(self.Options.N_CD, dtype=float),
                         'DE':np.zeros(self.Options.N_DE, dtype=float)}
        self.Result_y = {'AB':np.zeros(self.Options.N_AB, dtype=float),
                         'BC':np.zeros(self.Options.N_BC, dtype=float),
                         'CD':np.zeros(self.Options.N_CD, dtype=float),
                         'DE':np.zeros(self.Options.N_DE, dtype=float)}
        print("Initialization finished")

    # Functions for convenience
    def __atan(self, x:float)->float:
        return math.degrees( math.atan(x) ) 

    def cot_Ma_angle(self, Ma:float)->float:
        if math.pow(Ma,2) > 1:
            return math.sqrt( math.pow(Ma,2) - 1 )
        else:
            return -100
    #====

    # Foelsch1949. Eq. (25), expension angle(in degrees) vs. Mach number
    def __psi(self, Ma:float) -> float:
        rgamma = self.rgamma
        psi_value = 0.5 * ( 
            math.sqrt(rgamma) * self.__atan( math.sqrt(1/rgamma* self.cot_Ma_angle(Ma)* self.cot_Ma_angle(Ma)) )
            - self.__atan(self.cot_Ma_angle(Ma)) 
            )
        return psi_value        

    # Foelsch1949. Eq. (13a)
    def __tau(self, Ma:float) -> float:
        rgamma = self.rgamma
        gamma = self.Pars.Gamma
        squared_tau = math.pow( (2/(gamma+1) + 1/rgamma*math.pow(Ma,2)), rgamma/2) / Ma
        return math.sqrt(squared_tau)
    # Functions for convenience -- END --

    def __stepDE(self)->None:
        assert self.Pars.method_semiangle in ('shortest','proportional','given')
        psi_e = self.__psi(self.Pars.Ma_e)
        tau_e = self.__tau(self.Pars.Ma_e)
        if self.Pars.method_semiangle == 'shortest':
            print("!!! Designated semi-angle value has been overwritten by 0.5*Ma_e for the shortest design")
            self.Pars.SemiAngle = 0.5*psi_e
        elif self.Pars.method_semiangle == 'proportional':
            print("!!! Designated semi-angle value has been overwritten by proportion method")
            self.Pars.SemiAngle = self.Pars.coef_semiangle*psi_e
        
        psi_a = psi_e - self.Pars.SemiAngle
        semiangle_rads = self.semiangle_rads
        assert 0.5*psi_e <= psi_a < psi_e

        def fpsi_a(x):
            Ma=x[0]
            return self.__psi(Ma)-psi_a
        Ma_a= fsolve(fpsi_a, x0=[2])[0]         # Attention here to selection of the initial value.
        tau_a = self.__tau(Ma_a)

        # Step3
        Ma_p_seq = np.linspace(Ma_a, self.Pars.Ma_e, self.Options.N_DE)
        psi_vector = np.vectorize(self.__psi)
        tau_vector = np.vectorize(self.__tau)
        cot_Ma_angle_vector = np.vectorize(self.cot_Ma_angle)

        psi_p_seq = psi_vector(Ma_p_seq)
        tau_p_seq = tau_vector(Ma_p_seq)
        cot_Ma_angle_p_seq = cot_Ma_angle_vector(Ma_p_seq)
        theta_p_seq = psi_e-psi_p_seq

        united_par_p_seq = np.array(list(zip(tau_p_seq, cot_Ma_angle_p_seq, theta_p_seq)))
        def cal_DEcoordinate(united_par_p):
            tau_p=united_par_p[0]
            cot_Ma_angle_p=united_par_p[1]
            theta_p=united_par_p[2]
            theta_p_rads = math.radians(theta_p)

            # Eq. (16a)
            F = math.sqrt(
                math.pow(math.sin(theta_p_rads),2)
                +2*(math.cos(theta_p_rads)-math.cos(semiangle_rads)) * (cot_Ma_angle_p*math.sin(theta_p_rads)+math.cos(theta_p_rads))
                )   # Eq.(16a)
            
            # Eq. (20)
            y = self.Pars.D_e/4/math.sin(semiangle_rads/2)*tau_p/tau_e*F        
            
            # Eq.(21)
            x = (self.Pars.D_e/4/math.sin(semiangle_rads/2)*tau_p/tau_e
                *(1+(math.cos(semiangle_rads/2)*cot_Ma_angle_p-math.sin(theta_p_rads))*F)
                /(math.sin(theta_p_rads)*cot_Ma_angle_p+math.cos(theta_p_rads))
                )                                   
            return np.array([x,y])

        DE_coordinates = np.apply_along_axis(cal_DEcoordinate, axis=1, arr=united_par_p_seq)
        DE_coordinates = DE_coordinates.swapaxes(0,1)
        np.copyto(self.Result_x['DE'], DE_coordinates[0])
        np.copyto(self.Result_y['DE'], DE_coordinates[1])

        # Eq. (28)
        self.y_throat = self.Pars.D_e/2/tau_e  

    def __stepCD(self)->None:
        y_a = self.Result_y['DE'][0]
        x_a = 3.0 * (y_a - self.y_throat) /2 /math.tan(self.semiangle_rads)
        CD_coordinates_x = np.linspace(0,x_a, self.Options.N_CD)
        def cal_CD_y(x):
            y = self.y_throat + math.tan(self.semiangle_rads)/x_a *x*x *(1 - x/3/x_a)
            return y
        cal_CD_y_vector = np.vectorize(cal_CD_y)
        CD_coordinates_y = cal_CD_y_vector(CD_coordinates_x)
        np.copyto(self.Result_x['CD'], CD_coordinates_x)
        np.copyto(self.Result_y['CD'], CD_coordinates_y)
        
        delta = self.Result_x['DE'][0] - x_a     
        self.Result_x['DE'] = self.Result_x['DE'] - delta

    def __stepBC(self)->None:
        assert self.Pars.BC_method in ('cubic','quartic','Witoszynski')

        if self.Pars.BC_method == 'Witoszynski':
            offset_BC = self.Pars.Offset_Witoszynski
            y_throat_offset = self.y_throat + offset_BC
            y_inlet_offset = self.Pars.D_i/2 + offset_BC
            LengthBC = self.Pars.Coef_Length_Witoszynski * self.y_throat
            BC_coordinates_x = np.linspace(0, LengthBC, self.Options.N_BC)
            BC_ratio_of_height = y_throat_offset / y_inlet_offset
            
            def cal_WitoszynskiCurve(x:float):
                normalized_x = x/LengthBC
                tmp_a = math.pow(1 - math.pow(normalized_x,2) , 2)
                tmp_b = math.pow(1 + 3 * math.pow(normalized_x,2) ,3)
                tmp_c = 1 - math.pow(BC_ratio_of_height,2)
                return y_throat_offset / math.sqrt(1 - tmp_c * tmp_a / tmp_b)
            cal_WitoszynskiCurve_vector = np.vectorize(cal_WitoszynskiCurve)

            BC_coordinates_y = cal_WitoszynskiCurve_vector(BC_coordinates_x)
            BC_coordinates_x = BC_coordinates_x - LengthBC
            BC_coordinates_y = BC_coordinates_y - offset_BC
        
        elif self.Pars.BC_method == 'cubic':
            if self.Pars.BC_Referencepoint == 'exit':
                LengthBC = self.Pars.L_Cubic - (self.Result_x['DE'][-1] - self.Result_x['CD'][0])
            else:
                LengthBC = self.Pars.L_Cubic
            BC_coordinates_x = np.linspace(-LengthBC, 0, self.Options.N_BC)
            y_in = self.Pars.D_i / 2.0
            y_throat = self.y_throat
            relative_x = BC_coordinates_x/(-LengthBC)
            BC_coordinates_y = (y_in - y_throat)*(3*(relative_x)**2 - 2*(relative_x)**3) + y_throat
         
        elif self.Pars.BC_method == 'quartic':
            if self.Pars.BC_Referencepoint == 'exit':
                LengthBC = self.Pars.L_Cubic - (self.Result_x['DE'][-1] - self.Result_x['CD'][0])
            else:
                LengthBC = self.Pars.L_Cubic
            BC_coordinates_x = np.linspace(-LengthBC, 0, self.Options.N_BC)
            y_in = self.Pars.D_i / 2.0
            y_throat = self.y_throat
            relative_x = BC_coordinates_x/(-LengthBC)
            theta_1 = math.radians(self.Pars.SemiAngle)
            def Area(M):
                gamma = self.Pars.Gamma
                return (((gamma-1)*M**2+2)/(gamma+1))**((gamma+1)/(2*(gamma-1)))/M
            r1=y_throat *np.sqrt(Area(self.Pars.Ma_e)/(2*(1-np.cos(theta_1))))
            y1=r1*np.sin(theta_1)
            x1=3*(y1 - y_throat)/(2*np.tan(theta_1))
            BC_coordinates_y = ( (y_throat - y_in)*(3*(relative_x)**4 - 4*(relative_x)**3) 
                                + ((-LengthBC)**2*np.tan(theta_1)/x1)*(relative_x**4-2*relative_x**3+relative_x**2) + y_throat)

        np.copyto(self.Result_x['BC'], BC_coordinates_x)
        np.copyto(self.Result_y['BC'], BC_coordinates_y)
        
    def __stepAB(self)->None:
        x_A = self.Result_x['DE'][-1] - self.Pars.TotalLength
        x_B = self.Result_x['BC'][0]
        y = self.Result_y['BC'][0]
        AB_coordinates_x = np.linspace(x_A, x_B, self.Options.N_AB)
        AB_coordinates_y = np.linspace(y, y, self.Options.N_AB)
        np.copyto(self.Result_x['AB'], AB_coordinates_x)
        np.copyto(self.Result_y['AB'], AB_coordinates_y)

    def generate(self)->None:
        self.__stepDE()
        self.__stepCD()
        self.__stepBC()
        self.__stepAB()
        self.ifavailable = True

    def BLcorrection(self, method = 'constant')->None:
        assert method in ('constant','linear')
        assert self.ifavailable == True
        def BLcorrection_constant():
            self.Result_y['AB'] = self.Result_y['AB'] + self.Pars.BLcorr
            self.Result_y['BC'] = self.Result_y['BC'] + self.Pars.BLcorr
            self.Result_y['CD'] = self.Result_y['CD'] + self.Pars.BLcorr
            self.Result_y['DE'] = self.Result_y['DE'] + self.Pars.BLcorr
        if method == 'constant':
            BLcorrection_constant()

    def export_csv(self, filename = 'output.csv', zeroPosition = 'throat', offset:float = 0.0) -> None:
        '''
            A positive [offset] shift the curve to the left.
        '''
        assert zeroPosition in ('throat','inlet','outlet')
        assert self.ifavailable == True
        x,y = self.getResult(zeroPosition = zeroPosition, offset= offset)
        z = np.zeros_like(x)
        xyz = np.vstack((x, y, z)).T
        np.savetxt(filename, xyz, delimiter=',', header='', comments='')
    
    def getResult(self, zeroPosition = 'throat', offset:float = 0.0):
        assert zeroPosition in ('throat','inlet','outlet')
        assert self.ifavailable == True

        x,y = self.Result_x, self.Result_y
        def concatenate_arrays(*arrays):
            return np.concatenate(arrays, axis=0)
        concatenated_x = concatenate_arrays(x['AB'][0:-1], x['BC'][0:-1], x['CD'][0:-1], x['DE'])
        concatenated_y = concatenate_arrays(y['AB'][0:-1], y['BC'][0:-1], y['CD'][0:-1], y['DE'])

        if zeroPosition == 'throat':
            pass
        elif zeroPosition == 'inlet':
            concatenated_x = concatenated_x - x['AB'][0]
        elif zeroPosition == 'outlet':
            concatenated_x = concatenated_x - x['DE'][-1]

        concatenated_x = concatenated_x - offset
        return concatenated_x, concatenated_y

    def getRawResult(self, zeroPosition = 'throat', offset:float = 0.0):
        assert self.ifavailable == True
        return self.Result_x, self.Result_y





