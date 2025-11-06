''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from G01_energy_spectrum import EnergySpectrum as ES

from pivdataprocessor.A02_pltcfg import getplotpath
from pivdataprocessor.A01_toolbox import WriteHandler, nanmean_filter1d

cases = ['Case01XY_Z0_Ethanol', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
# -------------------------------------------------------------------------
# endregion

wh_x = WriteHandler(['k_x(m-1)','Eu(m3/s2)','k5.3*Eu(m4.3/s2)','err_Eu','-err_Eu'])
wh_y = WriteHandler(['k_y(m-1)','Ev(m3/s2)','k5.3*Ev(m4.3/s2)','err_Ev','-err_Ev'])

pBase.rm_and_create_directory(fig_path+'/Eu')
pBase.rm_and_create_directory(fig_path+'/Ev')

target = 5/3
for case_number in range(len(cases)):
    es = ES(cases[case_number]+'_sub1')
    es.load()
    sub1_wavenumber_xdir = es.wavenumber_xdir.copy()
    sub1_wavenumber_ydir = es.wavenumber_ydir.copy()
    sub1_spec_xdir = es.spec_xdir[0].copy()
    sub1_spec_ydir = es.spec_ydir[1].copy()

    es = ES(cases[case_number]+'_sub2')
    es.load()
    sub2_wavenumber_xdir = es.wavenumber_xdir.copy()
    sub2_wavenumber_ydir = es.wavenumber_ydir.copy()
    sub2_spec_xdir = es.spec_xdir[0].copy()
    sub2_spec_ydir = es.spec_ydir[1].copy()
    F_u_len = min(len(sub1_spec_xdir),len(sub2_spec_xdir))
    F_v_len = min(len(sub1_spec_ydir),len(sub2_spec_ydir))
 
    spec_xdir_for_uncertainty = (sub1_spec_xdir[:F_u_len] - sub2_spec_xdir[:F_u_len])**2
    spec_ydir_for_uncertainty = (sub1_spec_ydir[:F_v_len] - sub2_spec_ydir[:F_v_len])**2
    spec_xdir_uncertainty = np.sqrt(nanmean_filter1d(spec_xdir_for_uncertainty,8))/2
    spec_ydir_uncertainty = np.sqrt(nanmean_filter1d(spec_ydir_for_uncertainty,8))/2

    es = ES(cases[case_number])
    es.load()
    
    target_len = len(es.wavenumber_xdir)
    current_len = len(spec_xdir_uncertainty)
    if current_len < target_len:
        pad_len = target_len - current_len
        spec_xdir_uncertainty = np.concatenate([spec_xdir_uncertainty, np.full(pad_len, np.nan)])
    target_len = len(es.wavenumber_ydir)
    current_len = len(spec_ydir_uncertainty)
    if current_len < target_len:
        pad_len = target_len - current_len
        spec_ydir_uncertainty = np.concatenate([spec_ydir_uncertainty, np.full(pad_len, np.nan)])
    wh_x.loaddata([es.wavenumber_xdir,es.spec_xdir[0],es.spec_xdir[0]*(es.wavenumber_xdir**target), spec_xdir_uncertainty,-spec_xdir_uncertainty])
    wh_x.write(fig_path+'/Eu'+f'/{cases[case_number]}_Eu.txt')
    wh_y.loaddata([es.wavenumber_ydir,es.spec_ydir[1],es.spec_ydir[1]*(es.wavenumber_ydir**target), spec_ydir_uncertainty,-spec_ydir_uncertainty])
    wh_y.write(fig_path+'/Ev'+f'/{cases[case_number]}_Ev.txt')

f_Eu = './Z05_Energy_Spectrum/Mori605/Eu_kx_x605mm.txt'
f_Ev = './Z05_Energy_Spectrum/Mori605/Ev_ky_x605mm.txt' 
k_x, Eu = np.loadtxt(f_Eu, unpack=True,skiprows=1)
k_y, Ev = np.loadtxt(f_Ev, unpack=True,skiprows=1)

wh_x.loaddata([k_x,Eu,Eu*(k_x**target),np.full_like(k_x, np.nan, dtype=float), np.full_like(k_x, np.nan, dtype=float)])
wh_x.write(fig_path+'/Eu'+f'/Mori_Eu.txt')
wh_y.loaddata([k_y,Ev,Ev*(k_y**target),np.full_like(k_y, np.nan, dtype=float), np.full_like(k_y, np.nan, dtype=float)])
wh_y.write(fig_path+'/Ev'+f'/Mori_Ev.txt')
