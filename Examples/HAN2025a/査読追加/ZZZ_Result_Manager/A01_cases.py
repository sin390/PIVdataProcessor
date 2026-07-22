import numpy as np

cases = ['Case_FanW_All100']
case_labels = cases
coeffs_to_eta = [60.0,]

gaussian_id = [i+1 for i in range(len(coeffs_to_eta))]

deg_interval = 10
degs = [[(i,i+deg_interval),] for i in range(0,180,deg_interval)]