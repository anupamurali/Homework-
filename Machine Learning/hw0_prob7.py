import numpy as np 
import math

def buggy(x):
	return np.sin(x**2)/x

def linear_approximation_around_problematic_input(x):
	return float(x) - float(x)**5/6. + float(x)**9/120.0 - float(x)**13/5040.0 + float(x)**17/math.factorial(9) 

print buggy(0)
print linear_approximation_around_problematic_input(0)