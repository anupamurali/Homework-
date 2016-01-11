import numpy as np
import scipy 
import math
import matplotlib.pyplot as plt
def compute_design_vector(x):
    design_vector = []
    for i in range(10):
        datum = x[i]
        design_vector.append([1, x[i], x[i]**2])
    return np.array(design_vector)


x = np.array([-1.87, -1.76, -1.67, -1.22, -0.07, 0.11, 0.67, 1.60, 2.22, 2.51])
y = np.array([0.06, 1.67, 0.54, -1.45, -0.18, -0.67, 0.92, 2.95, 5.13, 5.18])
Phi = compute_design_vector(x)

plt.plot(x, y, 'ro',label='data')

w_0 = np.zeros(3)
V_0 = np.identity(3)
sigma_sq = 0.01

posterior_variance = np.linalg.inv(np.linalg.inv(V_0) + (1 / sigma_sq) * Phi.T.dot(Phi))
posterior_mean = posterior_variance.dot(np.linalg.inv(V_0).dot(w_0) + (1 / sigma_sq) * Phi.T.dot(y))

start = -4.0
end = 4.0
steps = 200

prev_upper = None
prev_lower = None

for i in range(steps):
    X = start + i * ((end - start) / float(steps))
    phi_x = np.array([1, X, X**2])
        #print X
    pred_mean = posterior_mean.T.dot(phi_x)
    pred_variance = sigma_sq + phi_x.T.dot(posterior_variance).dot(phi_x)
    Y_upper = pred_mean + 1.96 * math.sqrt(pred_variance)
    Y_lower = pred_mean - 1.96 * math.sqrt(pred_variance)

    if prev_upper is not None:
        plt.plot((prev_upper[0], X), (prev_upper[1], Y_upper), 'r')
    plt.draw()
    if prev_lower is not None:
        plt.plot((prev_lower[0], X), (prev_lower[1], Y_lower), 'r')
    plt.draw()

    prev_upper = (X, Y_upper)
    prev_lower = (X, Y_lower)

plt.show()


if __name__ == "__main__":
    main()