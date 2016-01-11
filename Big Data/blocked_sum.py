from __future__ import division
import pyopencl as cl
import numpy as np

platforms = cl.get_platforms()

devices = platforms[0].get_devices()
context = cl.Context(devices)

def blocked(N, W, Ng, hx):
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
    sum_vector(__global const int *kernN, __global const float *x, __global float *y) 
    {
      int thread_id = get_global_id(0);
      int n = get_global_size(0);
      int N = *kernN;
      int k = (int)N/n; 

      if (n <= N)
      {
        if (thread_id < n-1) 
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
      else
      { 
        if (thread_id <= N-1)
          y[thread_id] = y[thread_id] + x[thread_id];
      }
    }
    """


    x = cl.Buffer(context, cl.mem_flags.READ_ONLY, N*4)
    kernN = cl.Buffer(context, cl.mem_flags.READ_ONLY, np.int64(N).nbytes*4)
    
    num_threads = Ng*W
    if num_threads < N:
        y = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, N*4)
    else:
        y = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, num_threads*4)

    print 'here'
    program = cl.Program(context, src).build(options = '')
    print 'here2'
    #Transfers the data

    print hx.shape
    print W*Ng
    hy = np.zeros(N).astype(np.float32)

    cl.enqueue_copy(queue, x, hx, is_blocking=False)
    cl.enqueue_copy(queue, kernN, np.int64(N), is_blocking=False)
    print "Ng = ",Ng
    print "W = ",W
    event_execute = program.sum_vector(queue, (Ng*W,), (W,), kernN, x, y)
    # print "RESULT B4", hy[W*Ng]
    event_copy = cl.enqueue_copy(queue, hy, y, is_blocking=True)
    print "RESULT = ",hy[:W*Ng]
    print 'here'
    cl_sum = sum(hy[:W*Ng])
    print "SUM RESULT = ",cl_sum

    print 'Kernel submitted at time ', event_execute.profile.submit/1e9
    print 'Kernel started at time ', event_execute.profile.start/1e9
    print 'Kernel ended at time ', event_execute.profile.end/1e9

    print 'Time between enqueued and started:',  event_execute.profile.start -  event_execute.profile.submit, 'ns'
    print 'Time between started and finished:',  event_execute.profile.end -  event_execute.profile.start, 'ns'
    time = event_execute.profile.end -  event_execute.profile.start

    print '----------'
    print 'The effective device bandwidth is', 2*N*4/(event_execute.profile.end -  event_execute.profile.start), 'GB/s'
    bandwidth = 2*N*4/(event_execute.profile.end -  event_execute.profile.start)
    print 'The effective host-device transfer bandwidth is', N*4/(event_copy.profile.end -  event_copy.profile.start), 'GB/s'

    #At this point, the queue is not flush. Nothing has been sent for execution.
    queue.flush()
    #At this point, the queue is not finished. The completion of the operations is not guaranteed!
    queue.finish()

    return (bandwidth, time)

if __name__ == "__main__":
    hx = np.random.uniform(0, 1, 10000000).astype(np.float32)
    blocked(10000000, 64, 1024, hx)










    # """
    # #pragma OPENCL EXTENSION cl_intel_printf: enable
    # __kernel void 
    # sum_vector(__global const int *kernN, __global const float *x, __global float *y) 
    # {
    #   int thread_id = get_global_id(0);
    #   int n = get_global_size(0);
    #   int N = %s;
    #   int k = (int)N/n; 

    #   if (thread_id < n-1 && n <= N) 
    #   {
    #      for (int i = thread_id*k; i<(thread_id+1)*k; i++)
    #         y[thread_id] = y[thread_id] + x[i];
    #   }  
    #   else 
    #   {
    #     for (int i = thread_id*k; i < N; i++)
    #       y[thread_id] = y[thread_id] + x[i];
    #   }
    # }
    # """ % "HI"
