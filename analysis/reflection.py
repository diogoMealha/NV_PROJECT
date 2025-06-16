import matplotlib.pyplot as plt
import numpy as np

# given a signal, this attempts to find the symmetry point
# the "norm" will be low near points of symmetry. it will also be low near the edges
# (because a sufficiently short segment is flat), so that will have to be "stripped away"

dx = 0.1;
x = np.arange(-4, 6, dx);
N = len(x);

A = [-15*xi**2 + 3 + xi**4+ 0.1*np.random.rand(1) for xi in x];
norm = [0]*N;

for j in range(N):
    w = min(j, N-j-1);
    Aw = A[j-w:j+w+1];
    #print(f"j: {j}, w: {w}, l = {len(Aw)}");
    n = len(Aw);
    diff = [(Aw[k] - Aw[n-k-1])**2 for k in range(n)];
    norm[j] = sum(diff)/n;
    
    
norm = [n*max(A)/max(norm) for n in norm];
    
plt.figure(1)
plt.plot(x, A, 'r', label = "signal");
plt.plot(x, norm, 'b', label = "norm");
plt.legend()
plt.ylim(-1, 50)
plt.show()