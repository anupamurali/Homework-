import numpy as np
import mpi4py.MPI as MPI
from Plotter3DCS205 import MeshPlotter3D, MeshPlotter3DParallel
from P3serial import initial_conditions, apply_stencil, set_ghost_points

if __name__ == '__main__':
    # Global constants

  xMin, xMax = 0.0, 1.0     # Domain boundaries
  yMin, yMax = 0.0, 1.0     # Domain boundaries
  Nx = 64                   # Number of total grid points in x
  Ny = Nx                   # Number of total grid points in y
  dx = (xMax-xMin)/(Nx-1)   # Grid spacing, Delta x
  dy = (yMax-yMin)/(Ny-1)   # Grid spacing, Delta y
  dt = 0.4 * dx             # Time step (Magic factor of 0.4)
  T = 5                     # Time end
  DTDX = (dt*dt) / (dx*dx)  # Precomputed CFL scalar

  # The global indices: I[i,j] and J[i,j] are indices of u[i,j]
  [I,J] = np.mgrid[-1:Nx+1, -1:Ny+1]
  # Convenience so u[1:Ix,1:Iy] are all interior points
  Ix, Iy = Nx+1, Ny+1

  # Set the initial conditions
  up, u, um = initial_conditions(DTDX, I*dx-0.5, J*dy)

  # Setup the serial plotter -- one plot per process
  plotter = MeshPlotter3D()
  # Setup the parallel plotter -- one plot gathered from all processes
  #plotter = MeshPlotter3DParallel()

  for k,t in enumerate(np.arange(0,T,dt)):
    # Compute u^{n+1} with the computational stencil
    apply_stencil(DTDX, up, u, um)

    # Set the ghost points on u^{n+1}
    set_ghost_points(up)

    # Swap references for the next step
    # u^{n-1} <- u^{n}
    # u^{n}   <- u^{n+1}
    # u^{n+1} <- u^{n-1} to be overwritten in next step
    um, u, up = u, up, um

    # Output and draw Occasionally
    print "Step: %d  Time: %f" % (k,t)
    if k % 5 == 0:
      plotter.draw_now(I[1:Ix,1:Iy], J[1:Ix,1:Iy], u[1:Ix,1:Iy])

  plotter.save_now(I[1:Ix,1:Iy], J[1:Ix,1:Iy], u[1:Ix,1:Iy], "FinalWave.png")