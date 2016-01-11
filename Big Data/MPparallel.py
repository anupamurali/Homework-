import numpy as np
import graphlab
from graphlab import SGraph, Vertex, Edge 

def MP_graph(D, x):
    N, M = D.shape
    z = np.zeros((M,1))
    z_temp = np.zeros(M)
    r = np.copy(x)
    num_iter = 30
    # Create bipartite graph
    G = SGraph()
    x_vertices = [Vertex(i) for i in xrange(N)]
    z_vertices = [Vertex(j+N) for j in xrange(M)]
    D_edges = [Edge(i, j) for i in xrange(N) for j in xrange(N, N+M)]
    G.add_vertices(x_vertices, z_vertices)
    G.add_edges(D_edges)
    
    for i in xrange(N):
        x_vertices[i]["value"] = x[i]
    for j in xrange(M):
        z_vertices[j]["value"] = 0.0
        z_vertices[j]["dummy"] = 0.0
        z_vertices[j]["max"] = 0.0
    for i in xrange(N):
        for j in xrange(M):
            Edge(x_vertices[i], z_vertices[j])["value"] = D[i][j]
            
    def inner_prod(s, e, t):
        t["dummy"] += e["value"]*s["value"]
    
    def update_z(s, e, t):
        if not t["max"] == 0.0:
            t["value"] += e["value"]*s["value"]
            
    def compute_residual(s, e, t):
        if not t["max"] == 0.0:
            s["value"] -= t["value"]*e["value"]
    
    for itr in xrange(num_iter):
        # Compute inner products with r
        print "NUM ITR = ",itr
        G = G.triple_apply(inner_prod, mutated_fields=["value", "dummy"])
        for i in xrange(M):
            z_vertices[i]["max"] = 0.0
            z_temp[i] = z_vertices[i]["dummy"]
        max_pos = np.argmax(z_temp)
        z_vertices[max_pos]["max"] = z_temp[max_pos]
        G = G.triple_apply(update_z, mutated_fields=["max", "value"])
        
    for i in xrange(M):
        z[i] = z_vertices[i]["value"]
        
    return z

N_VAL = 100
M_VAL = 100000
D = np.random.rand(N_VAL, M_VAL)
D_norm = np.zeros((N_VAL,M_VAL))
for i in xrange(M_VAL):
    D_norm[:,i] = D[:,i]/np.linalg.norm(D[:,i])
z_actual = np.random.rand(M_VAL,1)
x = np.dot(D,z_actual)

z = MP_graph(D_norm, x)
print z 
print z.shape

x_mp = np.dot(D, z)
print 'ACTUAL X = ',x
print "X FROM MP = ",x_mp
print "Z=", z
print "NORM D=", np.linalg.norm(D[:,4])
