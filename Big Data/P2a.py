
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

def parallel_transform(comm, image_data):
    rank = comm.Get_rank()
    size = comm.Get_size()
    print "transforming for rank i = ", rank

    # We assume number of processes is a power of 2
    # start and end are row indices
    start = rank * int(IMAGE_SIZE / size)
    end = ((rank+1) * int(IMAGE_SIZE / size))

    # Load partial data
    b = data_transformer(SAMPLE_SIZE, IMAGE_SIZE)
    data = np.zeros((IMAGE_SIZE, IMAGE_SIZE))
    print "about to transform for rank ",rank
    for i in xrange(start, end):
        print "working on row = ",i
        data += b.transform(image_data[i-start], -np.pi/2048*i)
    print "transformed image for rank ",rank
    
    if not (rank == 0):
        print "sending transformed data for rank ",rank
        comm.Send([data, MPI.FLOAT], dest=0)
        print "sent transformed data for rank ",rank
    
    return data

    

if __name__ == '__main__':
    dt = np.dtype('d')

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    start_end = {}
    for i in xrange(size):
        start = i * int(IMAGE_SIZE / size)
        end = ((i+1) * int(IMAGE_SIZE / size))
        start_end[i] = (start, end)
    # Load data in process 0 
    print "rank = ",rank
    data = np.zeros((IMAGE_SIZE, IMAGE_SIZE))
    im_data = np.zeros((int(IMAGE_SIZE/size), SAMPLE_SIZE))

    if rank == 0:
        print "loading data ..."
        all_im_data = np.fromfile('TomoData.bin', dtype=dt)
        print "got data!"
        all_im_data = np.reshape(all_im_data,(2048, 6144))
        print "RESHAPED"
        result = np.zeros((IMAGE_SIZE, IMAGE_SIZE))
        for i in xrange(1,size):
            start, end = start_end[i]
            im_data = all_im_data[start:end]
            print "sending im_data to rank ",i
            comm.Send([im_data, MPI.FLOAT], dest=i)
            print "sent to rank ",i

        im_data = all_im_data[:int(IMAGE_SIZE/size)]
        print "RESULT = ", result
   # comm.barrier()
    print "RANK = ",rank

    if not (rank == 0):
        comm.Recv([im_data, MPI.FLOAT], source=0)
    print "RECEIVED IM DATA BY RANK ",rank
    data = parallel_transform(comm, im_data)
    #comm.barrier()

    if rank == 0:
        result += data
        for i in xrange(1,size):
            comm.Recv([data, MPI.FLOAT], source=i)
            print "RECEIVED BY RANK ",i
            result += data
            print "RESULT = ", data
      
        plt.imsave('result2a_new.png', result, cmap='bone')
