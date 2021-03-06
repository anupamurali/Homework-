from __future__ import division
import pyopencl as cl
import numpy as np

platforms = cl.get_platforms()

devices = platforms[0].get_devices()
context = cl.Context(devices)

W = 64
Ng = 1024

N = 10000000
x = cl.Buffer(context, cl.mem_flags.READ_ONLY, N*4)
y = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, N*4)

#Let's create a queue for our transfers and our operations
queue = cl.CommandQueue(context, context.devices[1], properties=cl.command_queue_properties.PROFILING_ENABLE)
print 'The queue is using the device:', queue.device.name
# y[thread_id] = y[thread_id] + x[thread_id*n+i];
#for (int i = 1; i < n; i++)
#      printf("hi");
src = \
"""
#pragma OPENCL EXTENSION cl_intel_printf: enable
__kernel void 
add_vectors(__global const float *x, __global float *y) 
{
  int thread_id = get_global_id(0);
  int N = 10000000;
  int W = 64;
  int Ng = 1024;
  int k = (int)N/(W*Ng); 

  if (thread_id < W*Ng-1) 
  {
     for (int i = thread_id*k; i<(thread_id+1)*k; i++)
        y[thread_id] = y[thread_id] + x[i];
  } 
  else 
  {
  	for (int i = thread_id*k; i < N; i++)
  	  y[thread_id] = y[thread_id] + x[i];
  }
}
"""

program = cl.Program(context, src).build(options = '')

#Transfers the data
#hx = np.random.uniform(0, 1, N).astype(np.float32)
hx = np.ones(N).astype(np.float32)
print hx.shape
print W*Ng
hy = np.zeros(N).astype(np.float32)

cl.enqueue_copy(queue, x, hx, is_blocking=False)
event_execute = program.add_vectors(queue, (Ng*W,), (W,), x, y)
# print "RESULT B4", hy[W*Ng]
event_copy = cl.enqueue_copy(queue, hy, y, is_blocking=True)
print "RESULT = ",hy[:W*Ng], hx[9999999]
print 'here'
print "SUM RESULT = ",sum(hy[:W*Ng])

print "NUMPY RESULT = ",sum(hx)
#At this point, the queue is not flush. Nothing has been sent for execution.
queue.flush()
#At this point, the queue is not finished. The completion of the operations is not guaranteed!
queue.finish()