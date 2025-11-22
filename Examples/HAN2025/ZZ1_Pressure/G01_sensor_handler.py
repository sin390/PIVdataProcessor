import pandas as pd
import numpy as np

from pivdataprocessor.A01_toolbox import moving_average

class press_sensor_PSE540:
    def __init__(self, file:str, col=1, samplerate = 5000, moving_avg_seconds=0.1, avg_zero_seconds=0.5):
        '''
        moving_avg_seconds < 0 : no smoothing
        '''
        self.samplerate = samplerate
        self.time = None
        self.press = None
        self.zero = None
        
        df = pd.read_csv(file, sep=',\s*', engine='python', skiprows=16)   
        df_subset = df.iloc[:, [col]]
        df_subset.columns = ['A']
        self.time = np.array([1.0/samplerate*i for i in range(len(df_subset['A'].to_numpy()))])       
        self.convertandsmooth(df_subset['A'].to_numpy(), moving_avg_seconds, avg_zero_seconds)
        self.check_zero()

    def convertandsmooth(self, data, moving_avg_seconds = 0.1, avg_zero_seconds=0.5):
        def __moving_average(data, window_size):
            return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

        zero_size = int(avg_zero_seconds*self.samplerate)
        data = (data-1.0)*250.0
        zero = np.nanmean(data[0:zero_size])
        if moving_avg_seconds < 0:
            self.press = data-zero
        else:
            window_size = int(moving_avg_seconds*self.samplerate)

            self.time = __moving_average(self.time, window_size)
            self.press = __moving_average(data, window_size) - zero
        return
    
    def check_zero(self):
        level = np.abs(self.press[:int(len(self.press)/2)] - 100)
        max_index = np.argmin(level)
        self.time = self.time - self.time[max_index]

class press_sensor_PSE543:
    def __init__(self, file:str, col=1, samplerate = 5000, zero_pos = 0):
        self.samplerate = samplerate
        self.time = None
        self.press = None
        self.zero = None
        
        df = pd.read_csv(file, sep=',\s*', engine='python', skiprows=16)   
        df_subset = df.iloc[:, [col]]
        df_subset.columns = ['A']
        self.time = np.array([1.0/samplerate*i for i in range(len(df_subset['A'].to_numpy()))])       
        self.convertandsmooth(df_subset['A'].to_numpy())
        self.check_zero(zero_pos)

    def convertandsmooth(self, data, moving_avg_seconds = 0.1, avg_zero_seconds=0.5):
        def __moving_average(data, window_size):
            return np.convolve(data, np.ones(window_size) / window_size, mode='valid')
        window_size = int(moving_avg_seconds*self.samplerate)
        zero_size = int(avg_zero_seconds*self.samplerate)

        data = (data-3.0)*50.0
        zero = np.nanmean(data[0:zero_size])
        self.time = __moving_average(self.time, window_size)
        self.press = __moving_average(data, window_size) - zero
        return
    
    def check_zero(self,zero_pos):
        self.time = self.time - zero_pos



        
    
