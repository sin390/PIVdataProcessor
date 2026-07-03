import numpy as np

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
# cases = [case + '_even' for case in cases]
# cases = [case + '_odd' for case in cases]

cases_appendix = ['Case01','Case01XZ']
# cases_appendix = [case + '_even' for case in cases_appendix]
# cases_appendix = [case + '_odd' for case in cases_appendix]
case_labels = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']
case_appendix_labels = [r'Case 1 ($x$-$y$ plane)', r'Case 1 ($x$-$z$ plane)']


Lf_coeff = np.linspace(0.3,0.1,9)
Lf_label = [rf'$L_{{F}} = {Lf_coeff[i]:.3f}L_{{u}}$' for i in range(len(Lf_coeff))]
gaussian_id = [i+1 for i in range(len(Lf_coeff))]

deg_interval = 10
degs = [[(i,i+deg_interval),] for i in range(0,180,deg_interval)]