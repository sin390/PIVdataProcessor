import numpy as np
cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

Temp = np.array([292, 289, 288, 288, 288, 290])
press = np.array([102000,102000,102000,102000,102000,102000])
Rho = press/287.05/Temp

Mu0 = 1.724e-5
T0 = 273
S = 110.4
Mu = Mu0* ((Temp/T0)**1.5)*(T0+S)/(Temp+S)
Upsilon = Mu/Rho


k2 = np.array([318.27, 322.84, 347.88, 715.24, 683.30, 758.82])
urms = (k2*2/3)**0.5
print(urms)
urms1 = [17.79, 18.37, 19.56, 28.11, 27.68, 29.55]
print(urms1)

L11 = np.array([24.9, 29.3, 34.1, 28.0, 32.2, 33.3])
L11 = L11 /1000

ReL = urms1*L11/Upsilon
print(f'---\nReL:\n{ReL}\n---')

TimeL = L11/urms1
print(f'---\nTimeL:\n{TimeL}\n---')

S11_avg = np.array([720, 640, 600, 830, 700, 730])
S11_center = np.array([850,830,750,1080,960,930])

SL = S11_avg*TimeL
print(f'---\nSL:{SL}\n---')

