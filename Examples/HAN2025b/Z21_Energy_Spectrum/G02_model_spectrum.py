import numpy as np

class Pope_Spectrum():
    def __init__(self, L, Re_lamda, epsilon, C = 1.5, CL = 6.78, p0 = 2, Ceta = 0.4, beta = 5.2):
        self.L = L
        self.eta = 15**(3/4) * Re_lamda**(-3/2) * self.L #Taylor-Kolmogorov scaling
        self.nu = (epsilon * self.eta**4)**(1/3)
        self.epsilon = epsilon
        self.C = C
        self.CL = CL
        self.p0 = p0
        self.Ceta = Ceta
        self.beta = beta

    def model_spectrum(self, k):
        fL = ((k * self.L) / np.sqrt((k * self.L)**2 + self.CL))**(5/3 + self.p0)
        feta = np.exp(-self.beta * ((k * self.eta)**4 + self.Ceta**4)**0.25 - self.Ceta)
        return self.C * self.epsilon**(2/3) * k**(-5/3) * fL * feta         
    
def k53_line(a, b, y_ref=1.0, x_ref=None):
    """
    Return two points (x, y) forming a -5/3 slope line in log-log space.

    Parameters
    ----------
    a, b : float
        Left and right x-coordinates (a < b)
    y_ref : float, optional
        Reference y-value at x_ref
    x_ref : float, optional
        Reference x-position. Default is a.

    Returns
    -------
    x : ndarray, shape (2,)
    y : ndarray, shape (2,)
    """
    if x_ref is None:
        x_ref = a

    x = np.array([a, b])
    y = y_ref * (x / x_ref)**(-5/3)
    return x, y   