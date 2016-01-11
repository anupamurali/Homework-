import csv
import numpy as np
import pylab as pl
import math

csv_filename = 'motorcycle.csv'

times  = []
forces = []
with open(csv_filename, 'rU') as csv_fh:

    # Parse as a CSV file.
    reader = csv.reader(csv_fh, dialect='excel')

    # Skip the header line.
    next(reader, None)

    # Loop over the file.
    for row in reader:

        # Store the data.
        times.append(float(row[0]))
        forces.append(float(row[1]))

# Turn the data into numpy arrays.
times  = np.array(times)
forces = np.array(forces)

# Plot the data.
# pl.plot(times, forces, 'o')
# pl.show()

# Create the simplest basis, with just the time and an offset.
X = np.vstack((np.ones(times.shape), times)).T

# Nothing fancy for outputs.
Y = forces

# Find the regression weights using the Moore-Penrose pseudoinverse.
w = np.linalg.solve(np.dot(X.T, X) , np.dot(X.T, Y))

# Compute the regression line on a grid of inputs.
grid_times = np.linspace(0, 60, 200)
grid_X     = np.vstack((np.ones(grid_times.shape), grid_times))
grid_Yhat  = np.dot(grid_X.T, w)

# Plot the data and the regression line.
pl.plot(times, forces, 'o',
        grid_times, grid_Yhat, '-')
pl.show()

"""
Solution to Part a
"""
X = np.vstack([[-1*(math.exp(-((time-10*j)/5)**2)) for time in times] for j in xrange(0,7)]).T


# Nothing fancy for outputs.
Y = forces

# Find the regression weights using the Moore-Penrose pseudoinverse.
w = np.linalg.solve(np.dot(X.T, X) , np.dot(X.T, Y))

# Compute the regression line on a grid of inputs.
grid_times = np.linspace(0, 60, 200)
grid_X     = np.vstack([[-1*(math.exp(-((grid_time-10*j)/5)**2)) for grid_time in grid_times] for j in xrange(0,7)])
grid_Yhat  = np.dot(grid_X.T, w)

# Plot the data and the regression line.
pl.plot(times, forces, 'o',
        grid_times, grid_Yhat, '-')
pl.show()

"""
Solution to Part b
"""
X = np.vstack([[-1*(math.exp(-((time-10*j)/10)**2)) for time in times] for j in xrange(0,7)]).T

# Nothing fancy for outputs.
Y = forces

# Find the regression weights using the Moore-Penrose pseudoinverse.
w = np.linalg.solve(np.dot(X.T, X) , np.dot(X.T, Y))

# Compute the regression line on a grid of inputs.
grid_times = np.linspace(0, 60, 200)
grid_X     = np.vstack([[-1*(math.exp(-((grid_time-10*j)/10)**2)) for grid_time in grid_times] for j in xrange(0,7)])
grid_Yhat  = np.dot(grid_X.T, w)

# Plot the data and the regression line.
pl.plot(times, forces, 'o',
        grid_times, grid_Yhat, '-')
pl.show()

"""
Solution to Part c
"""
X = np.vstack([[-1*(math.exp(-((time-10*j)/25)**2)) for time in times] for j in xrange(0,7)]).T

# Nothing fancy for outputs.
Y = forces

# Find the regression weights using the Moore-Penrose pseudoinverse.
w = np.linalg.solve(np.dot(X.T, X) , np.dot(X.T, Y))

# Compute the regression line on a grid of inputs.
grid_times = np.linspace(0, 60, 200)
grid_X     = np.vstack([[-1*(math.exp(-((grid_time-10*j)/25)**2)) for grid_time in grid_times] for j in xrange(0,7)])
grid_Yhat  = np.dot(grid_X.T, w)

# Plot the data and the regression line.
pl.plot(times, forces, 'o',
        grid_times, grid_Yhat, '-')
pl.show()

"""
Solution to Part d
"""
X = np.vstack([[time**j for time in times] for j in xrange(0,11)]).T
print X.shape

# Nothing fancy for outputs.
Y = forces

# Find the regression weights using the Moore-Penrose pseudoinverse.
w = np.linalg.solve(np.dot(X.T, X) , np.dot(X.T, Y))

# Compute the regression line on a grid of inputs.
grid_times = np.linspace(0, 60, 200)
grid_X     = np.vstack([[grid_time**j for grid_time in grid_times] for j in xrange(0,11)])
grid_Yhat  = np.dot(grid_X.T, w)

# Plot the data and the regression line.
pl.plot(times, forces, 'o',
        grid_times, grid_Yhat, '-')
pl.show()

"""
Solution to Part e
"""
X = np.vstack([[math.sin(time/j) for time in times] for j in xrange(1,21)]).T

# Nothing fancy for outputs.
Y = forces

# Find the regression weights using the Moore-Penrose pseudoinverse.
w = np.linalg.solve(np.dot(X.T, X) , np.dot(X.T, Y))

# Compute the regression line on a grid of inputs.
grid_times = np.linspace(0, 60, 200)
grid_X     = np.vstack([[math.sin(grid_time/j)  for grid_time in grid_times] for j in xrange(1,21)])
grid_Yhat  = np.dot(grid_X.T, w)

# Plot the data and the regression line.
pl.plot(times, forces, 'o',
        grid_times, grid_Yhat, '-')
pl.show()


