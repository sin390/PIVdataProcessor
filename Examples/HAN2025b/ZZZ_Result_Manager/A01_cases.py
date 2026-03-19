cases_w = ['W-all100','W-asymgrad','W-symgrad','W-strain','W-shear']
cases_f = ['N-all100','N-asymgrad','N-symgrad','N-strain','N-shear']
cases = ['all100', 'asymgrad','symgrad', 'strain', 'shear']

cases_select = ['all100', 'asymgrad', 'shear']
cases_select_w = ['W-all100','W-asymgrad','W-shear']
cases_select_f = ['N-all100','N-asymgrad','N-shear']
cases_select_labels = ['Case 1', 'Case 2', 'Case 3']

coeffs_to_eta = [80,70,60,50,40,30,20]

Lf_labels = [rf'$L_f={i}\eta$' for i in coeffs_to_eta]

deg_interval = 20
degs = [[(i,i+deg_interval),] for i in range(0,180,deg_interval)]