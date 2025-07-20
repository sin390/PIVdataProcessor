import numpy as np
from scipy.linalg import schur

A = np.array([[0, -1],
              [1,  0]])

T, Q = schur(A, output='real')

print("Q =\n", Q)
print("T =\n", T)
