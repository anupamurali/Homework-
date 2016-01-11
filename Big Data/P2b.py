
from mpi4py import MPI
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import math

from P2serial import data_transformer

plt.ion()         # Allow interactive updates to the plots
SAMPLE_SIZE = 6144
IMAGE_SIZE = 2048

"""
Comm = communication object (process)
result = final result of computation
image_data = data for current process
data_trans = data_transformer object

Returns result of computation
"""

def parallel_transform(comm, data_trans, image_data, p_root=0):
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # Do work in current process 
    start = rank * int(IMAGE_SIZE / size)
    end = ((rank+1) * int(IMAGE_SIZE / size))

    data = np.zeros((IMAGE_SIZE, IMAGE_SIZE))
    print "about to transform for rank ",rank

    # Compute partial transformation
    for i in xrange(start, end):
    	print 'transforming for row ',i
    	print 'process = ',rank
        data += data_trans.transform(image_data[i-start], -np.pi/IMAGE_SIZE*i)

    # Reduce to root process
    result = comm.reduce(data, op=MPI.SUM, root=p_root)

    return result

    

if __name__ == '__main__':
    dt = np.dtype('d')
    data_trans = data_transformer(SAMPLE_SIZE, IMAGE_SIZE)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    im_data = []

    result = np.zeros((IMAGE_SIZE, IMAGE_SIZE))

    start_end = {}
    for i in xrange(size):
        start = i * int(IMAGE_SIZE / size)
        end = ((i+1) * int(IMAGE_SIZE / size))
        start_end[i] = (start, end)

    print start_end

    if rank == 0:
        print "loading data ..."
        all_im_data = np.fromfile('TomoData.bin', dtype=dt)
        print "got data!"
        all_im_data = np.reshape(all_im_data,(2048, SAMPLE_SIZE))
        print "RESHAPED"

        # Scatter data, send relevant data to each process
        im_data = [all_im_data[start_end[i][0]:start_end[i][1]] for i in xrange(size)]
        #im_data = comm.scatter(im_data, root=0)

    print "here"
    comm.barrier()
    p_start = MPI.Wtime()
    print "about to transform"
    im_data = comm.scatter(im_data, root=0)
    print "IMAGE DATA = ",im_data
    print len(im_data)

    result = parallel_transform(comm, data_trans, im_data)
    comm.barrier()
    p_stop = MPI.Wtime()

    print "TIME TAKEN = ", p_stop - p_start
    if rank == 0:
        print result.shape
        print result
        plt.imsave('result2b_1processes1024.png', result, cmap='bone')
