import numpy as np

class RDT_integral_calculator():
    def __init__(self, resolution = 100000):
        self.t = np.linspace(-1,1,resolution)
        self.__coef_u11 = None
        self.__coef_u22 = None
        self.u11u22 = None
        self.L11L22 = None

    def __cal_coef_u11(self,c):
        t = self.t.copy()
        tmp_integral_1 = t**2-1
        tmp_integral_2 = ((c**(-3)-1)*t**2+1)**2
        tmp_integral = tmp_integral_1/tmp_integral_2/c**2
        self.__coef_u11 = np.trapz(tmp_integral, t)

    def __cal_coef_u22(self,c):
        t = self.t.copy()
        tmp_integral_1 = (2 - c**(3) - c**(-3))*t**4
        tmp_integral_1 += (2*c**(3) - c**(-3) - 2)*t**2 - c**(3)
        tmp_integral_2 = ((c**(-3)-1)*t**2+1)**2
        tmp_integral = tmp_integral_1/tmp_integral_2/2/c**2
        self.__coef_u22 = np.trapz(tmp_integral, t)

    def calculate(self, c):
        self.__cal_coef_u11(c)
        self.__cal_coef_u22(c)
        self.u11u22 = self.__coef_u11/self.__coef_u22
        self.L11L22 = self.__coef_u22/self.__coef_u11 * c**(-3/2)
