from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = {'a': 7, 'b': 3.14}
    time.sleep(3)
    comm.send(data, dest=1, tag=11)
elif rank == 1:
    msg = False
    status = MPI.Status()
    while not msg:
        msg = comm.Iprobe(source=MPI.ANY_SOURCE, tag=11, status=status)
        print msg, status.Get_source()
        print 'rank 1 Doing some work...'
        time.sleep(1)
    rdata = comm.recv(source=0, tag=11)
    print 'rank 1: got ', rdata