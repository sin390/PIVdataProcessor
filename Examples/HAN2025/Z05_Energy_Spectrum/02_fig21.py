''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from G01_energy_spectrum import EnergySpectrum as ES

from pivdataprocessor.A02_pltcfg import getplotpath
from pivdataprocessor.A01_toolbox import WriteHandler

cases = ['Case01XY_Z0_Ethanol', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
# -------------------------------------------------------------------------
# endregion
wh = WriteHandler(['k(m-1)','Eu/Ev'])
inter_kind = 'linear'
for case_number in range(len(cases)):
    es = ES(cases[case_number])
    es.load()
    k1 = es.wavenumber_xdir
    E11 = es.spec_xdir[0]
    f1 = interp1d(np.log(k1), np.log(E11), kind=inter_kind, fill_value="extrapolate")

    k2 = es.wavenumber_ydir
    E22 = es.spec_ydir[1]
    f2 = interp1d(np.log(k2), np.log(E22), kind=inter_kind, fill_value="extrapolate")

    left = np.max([k1[0], k2[0]])
    right = np.min([k1[-1], k2[-1]])
    k = np.logspace(np.log10(left), np.log10(right), 100)

    E11_uni = np.exp(f1(np.log(k)))
    E22_uni = np.exp(f2(np.log(k)))
    wh.loaddata([k,E11_uni/E22_uni])
    wh.write(fig_path+f'/{cases[case_number]}.txt')



f_Eu = './Z05_Energy_Spectrum/Mori605/Eu_kx_x605mm.txt'
f_Ev = './Z05_Energy_Spectrum/Mori605/Ev_ky_x605mm.txt' 
k1, E11 = np.loadtxt(f_Eu, unpack=True,skiprows=1)
k2, E22 = np.loadtxt(f_Ev, unpack=True,skiprows=1)
f1 = interp1d(np.log(k1), np.log(E11), kind=inter_kind, fill_value="extrapolate")
f2 = interp1d(np.log(k2), np.log(E22), kind=inter_kind, fill_value="extrapolate")
left = np.max([k1[0], k2[0]])
right = np.min([k1[-1], k2[-1]])
k = np.logspace(np.log10(left), np.log10(right), 100)
E11_uni = np.exp(f1(np.log(k)))
E22_uni = np.exp(f2(np.log(k)))
wh.loaddata([k,E11_uni/E22_uni])
wh.write(fig_path+f'/Mori.txt')

