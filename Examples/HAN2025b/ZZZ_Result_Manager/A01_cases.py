cases_w = ['W-all100','W-asymgrad','W-symgrad','W-strain','W-shear']
cases_f = ['N-all100','N-asymgrad','N-symgrad','N-strain','N-shear']
cases = ['all100', 'asymgrad','symgrad', 'strain', 'shear']
cases_select = ['W-all100','W-asymgrad','W-symgrad','N-strain','N-shear']

case_labels = ['Case 1L', 'Case 2L', 'Case 3L', 'Case 4S', 'Case 5S']

coeffs_to_eta = [20,30,40,50]

deg_interval = 10
degs = [[(i,i+deg_interval),] for i in range(0,180,deg_interval)]