import numpy as np

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06', 'Mori_465']
# cases = [case + '_even' for case in cases]
# cases = [case + '_odd' for case in cases]
case_labels = ['Case S1', 'Case S2', 'Case S3', 'Case S4', 'Case S5', 'Case S6', 'Case U']

# a, b = 20.0, 60.0
# n = 8
# inv = np.linspace(1/a, 1/b, n)
# selected_k1L1 = 1.0 / inv
# k1L1_label = [rf'$k_1 L_{{u_1}} = {selected_k1L1[i]:.0f}$' for i in range(len(selected_k1L1))]
# gaussian_id = [i+1 for i in range(len(selected_k1L1))]

Lf_coeff = np.linspace(0.3,0.1,9)
Lf_label = [rf'$L_{{f}} = {Lf_coeff[i]:.3f}L_{{u_1}}$' for i in range(len(Lf_coeff))]
gaussian_id = [i+1 for i in range(len(Lf_coeff))]

deg_interval = 10
degs = [[(i,i+deg_interval),] for i in range(0,180,deg_interval)]
print(len(degs))