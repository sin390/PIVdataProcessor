import pandas as pd
import numpy as np

from pivdataprocessor.A01_toolbox import moving_average

class temp_sensor:
    def __init__(self, file:str, moving_avg_second=0.1, environment_temp=23.5):
        self.time = None
        self.temp = None

        df = pd.read_csv(file, sep=',', engine='python', skiprows=10, encoding='shift_jis', header=0)
        df_subset = df.iloc[:, :2]
        df_subset.columns = ['A', 'B']
        self.time = df_subset['A'].to_numpy()
        self.temp = df_subset['B'].to_numpy()
        self.d_time = self.time[1] - self.time[0]
        
        self.procession(moving_avg_second)
        self.check_zero()
        self.calibration(environment_temp)
    
    def procession(self,window_size_in_second):
        window_size = int(window_size_in_second/self.d_time)
        
        self.time = moving_average(self.time, window_size)
        self.temp = moving_average(self.temp, window_size)
        
    def check_zero(self):
        index = np.nanargmax(self.temp)
        zerotime = self.time[index]
        self.time = self.time - zerotime

    def calibration(self, environment_temp):
        index = np.where(~np.isnan(self.temp))[0][0]
        d_temp = self.temp[index] - environment_temp
        self.temp = self.temp - d_temp
        pass

