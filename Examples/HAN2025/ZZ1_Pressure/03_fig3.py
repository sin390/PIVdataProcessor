import matplotlib.pyplot as plt
import numpy as np
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from ZZ1_Pressure.G01_sensor_handler import press_sensor_PSE540 as ps
from pivdataprocessor.A02_pltcfg import getplotpath
from pivdataprocessor.A01_toolbox import WriteHandler as WH

data_folder = './ZZ1_Pressure/01/'
cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
files = ['20241221_125452_973.CSV',
         '20250215_203716_752.CSV',
         '20250227_181320_623.CSV',
         '20250325_203741_250.CSV',
         '20250319_174844_261.CSV',
         '20250316_152845_627.CSV']

# -------------------------------------------------------------------------
# region
# single column, single plot
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)

data_folder = './ZZ1_Pressure/01/'
cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
files = ['20241221_125452_973.CSV',
         '20250215_203716_752.CSV',
         '20250227_181320_623.CSV',
         '20250325_203741_250.CSV',
         '20250319_174844_261.CSV',
         '20250316_152845_627.CSV']


env_press = 102
case_number = 4
left = ps(data_folder+cases[case_number]+'/'+ files[case_number],col = 2) 
right = ps(data_folder+cases[case_number]+'/'+ files[case_number],col = 1)

start_left = np.abs(left.time - 0).argmin()
end_left = np.abs(left.time - 6).argmin()
start_right = np.abs(right.time - 0).argmin()   
end_right = np.abs(right.time - 6).argmin() 

avg_both = (np.mean(left.press[start_left:end_left]) + np.mean(right.press[start_right:end_right]))/2
press_left = left.press[start_left:end_left] - avg_both
press_right = right.press[start_right:end_right] - avg_both

rms = np.sqrt(np.mean(np.concatenate([press_left, press_right]) ** 2))
print(f'RMS Pressure Fluctuation: {rms:.2f} kPa')

wh = WH(['time','press(kPa)'])
wh.loaddata([left.time, left.press+ env_press])
wh.write(fig_path+'/left.txt')
wh.loaddata([right.time, right.press+ env_press])
wh.write(fig_path+'/right.txt')

print
    