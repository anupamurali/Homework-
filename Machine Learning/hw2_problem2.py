import numpy as np
import scipy 
import math
import matplotlib.pyplot as plt

data = np.loadtxt('CASP.csv', delimiter = ',', skiprows = 1)

x = np.array([-1.87, -1.76, -1.67, -1.22, -0.07, 0.11, 0.67, 1.60, 2.22, 2.51])
y = np.array([0.06, 1.67, 0.54, -1.45, -0.18, -0.67, 0.92, 2.95, 5.13, 5.18])

# sinusoidal

D = x.shape[0]
print D
def basis_func_sin(x):
   return np.array([math.sin(x/float(j+1)) for j in range(7)])

def basis_func_poly(x):
   return np.array([x**j for j in range(3)])


def get_transformed_X(x, basis_func):
    x_transformed = np.empty((D,3))
    for i in range(D):      
        x_transformed[i] = basis_func(x[i])
    return x_transformed

def compute_design_vector(x):
    design_vector = []
    for i in range(10):
        datum = x[i]
        design_vector.append([1, x[i], x[i]**2])
    return np.array(design_vector)

def compute_design_vector_3(x):
    design_vector = []
    for i in range(10):
        datum = x[i]
        design_vector.append([math.sin(x[i]/float(j+1)) for j in range(7)])
    return np.array(design_vector)

def compute_design_vector_2(x):
    design_vector = []
    for i in range(10):
        datum = x[i]
        design_vector.append([1, x[i], x[i]**2, x[i]**3])
    return np.array(design_vector)

def compute_design_vector_n(x, order):
    design_vector = []
    for i in range(10):
        datum = x[i]
        design_vector.append([x[i]**j for j in range(order)])
    return np.array(design_vector)

def marginal_likelihood(Phi, V_0, w_0, sigma_sq):
    V_n = Phi.T.dot(Phi) + V_0
    w_n = np.linalg.inv(V_n).dot(V_0.dot(w_0) + Phi.T.dot(y))
    likelihood = (1.0 / 2.0 * math.pi)**(10.0/2.0) * (1.0 / sigma_sq)**(10.0/2.0) * math.e**((-1.0/(2.0*sigma_sq)) * (y.T.dot(y) - w_n.T.dot(V_n).dot(w_n) + w_0.T.dot(V_0).dot(w_0)) ) * (np.linalg.det(V_0)**0.5 / np.linalg.det(V_n)**0.5)
    return likelihood

x_transformed_old = get_transformed_X(x, basis_func_poly)
x_transformed = compute_design_vector(x)

w0 = np.zeros(3)
V0 = np.identity(3)
sigma = 0.1

w_new = np.random.multivariate_normal(w0, V0, D) + np.random.normal(0, sigma)
values = np.linspace(-3, 3, num=200)
# for i in xrange(10):
#     y_val = [w_new[i][0] + w_new[i][1]*x + w_new[i][2]*x**2 for x in values]
#     plt.plot(values, y_val, label='$i = {i}$'.format(i=i))

# plt.legend()
# plt.title('Functions for each data point')
# plt.xlabel('Data points')
# plt.ylabel('Functions')
# plt.savefig('hw2problem2_plot1_sin.png')
# plt.show()


Vn_inv = np.linalg.inv(V0) + 1/sigma**2*x_transformed.T.dot(x_transformed)
Vn = np.linalg.inv(Vn_inv)
wN = (Vn.dot(np.linalg.inv(V0))).dot(w0) + 1/sigma**2 * Vn.dot(x_transformed.T.dot(y))

Vn_inv = np.linalg.inv(V0) + 1/sigma**2*np.dot(x_transformed.T,x_transformed)
Vn = sigma**2*(sigma**2*np.linalg.inv(V0) + np.dot(x_transformed.T,x_transformed))
wN = np.dot(Vn*np.linalg.inv(V0),w0) + 1/sigma**2 * np.dot(Vn,np.dot(x_transformed.T,y))
#print wN

w_conditional = np.random.multivariate_normal(wN, Vn, D)
print w_conditional
for i in xrange(10):
    y_val = [w_conditional[i][0] + w_conditional[i][1]*x + w_conditional[i][2]*x**2 for x in values]
    plt.plot(values, y_val, label='$i = {i}$'.format(i=i))
x = np.array([-1.87, -1.76, -1.67, -1.22, -0.07, 0.11, 0.67, 1.60, 2.22, 2.51])
y = np.array([0.06, 1.67, 0.54, -1.45, -0.18, -0.67, 0.92, 2.95, 5.13, 5.18])

plt.plot(x, y, 'ro',label='data')

plt.legend()
plt.title('Functions for each data point')
plt.xlabel('Data pionts')
plt.ylabel('Functions')
plt.savefig('hw2problem2_plot2.png')
plt.show()
# #print wN

# w_conditional = np.random.multivariate_normal(wN, Vn, D)
# print w_conditional
# for i in xrange(10):
#     y_val = [w_conditional[i][0] + w_conditional[i][1]*x + w_conditional[i][2]*x**2 for x in values]
#     plt.plot(values, y_val)
x = np.array([-1.87, -1.76, -1.67, -1.22, -0.07, 0.11, 0.67, 1.60, 2.22, 2.51])
y = np.array([0.06, 1.67, 0.54, -1.45, -0.18, -0.67, 0.92, 2.95, 5.13, 5.18])

# plt.plot(x, y, 'ro')

# plt.legend()
# plt.title('Functions for each data point')
# plt.xlabel('Data pionts')
# plt.ylabel('Functions')
# plt.savefig('hw2problem2_plot2_sin.png')
# plt.show()

# Get marginal likelihoods
likelihoods = []
for i in range(2,18):
    w0 = np.zeros(i)
    V0 = np.identity(i)
    sigma = 0.01
    phi = compute_design_vector_n(x, i)
    likelihood = marginal_likelihood(phi, V0, w0, sigma)
    print "this likelihood = ",likelihood
    likelihoods.append(likelihood)
objects = ('1','2', '3', '4', '5', '6', '7','8','9','10','11','12','13','14','15','16')
y_pos = np.arange(len(objects))
# for i in range(len(likelihoods)):
#     print "likelihoods = ",likelihoods[i]
plt.bar(y_pos, likelihoods, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.xlabel('Degrees')
plt.ylabel('Marginal Likelihoods')
plt.title('Marginal Likelihoods for Degrees')
 
plt.show()
