import matplotlib.pyplot as plt
from scipy.special import gamma
from scipy.integrate import quad as integrate
import numpy as np

def pdfY(D) :
    def pdf(y) :
        factor = gamma(D/2.0) * (2 **(D/2.0 - 1))
        return (y  (D - 1)) * np.exp((-1) * (y ** 2)/2.0 ) / factor
    return pdf


