import numpy as np
cases = ['Case01XY_Z0_Ethanol', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

Temp = np.array([299, 289, 288, 288, 288, 290])
press = np.array([102000,102000,102000,102000,102000,102000])
Rho = press/287.05/Temp

Mu0 = 1.724e-5
T0 = 273
S = 110.4
Mu = Mu0* ((Temp/T0)**1.5)*(T0+S)/(Temp+S)
Upsilon = Mu/Rho



k2 = np.array([268.59, 322.84, 347.88, 715.24, 683.30, 758.82])
urms = np.sqrt(k2*2/3)


urms1 = np.array([16.63, 18.36, 19.54, 28.11, 27.65, 29.53])
vrms1 = np.array([11.36, 12.32, 12.43, 17.84, 17.27, 17.88])
print(urms1/vrms1)

k2 = (urms1**2 + vrms1**2+ vrms1**2)/2
urms = np.sqrt(k2*2/3)

L11 = np.array([27.62, 30.33, 35.17, 28.87, 33.39, 34.86])/1000
L22 = np.array([22.27, 20.06, 19.65, 18.60, 17.80, 17.33])/1000
print(L11/L22)
L = (L11+L22+L22)/3

A=1
dissipationRate = A *urms**3/L
print(f'---\ndissipationRate:\n{dissipationRate}\n---')



TimeL = L/urms
print(f'---\nTimeL:\n{TimeL}\n---')

S11_avg = np.array([665, 640, 600, 830, 700, 730])

Lambda = np.sqrt(10*(Mu/Rho)*k2/dissipationRate)
print(f'---\nLambda:{Lambda}\n---')

eta = (Mu/Rho)**(3/4)*dissipationRate**(-1/4)
print(f'---\neta:{eta}\n---')

Re_lambda = Rho* urms * Lambda /Mu
print(f'---\nRe_lambda:{Re_lambda}\n---')

SL = S11_avg*TimeL
print(f'---\nSL:{SL}\n---')

