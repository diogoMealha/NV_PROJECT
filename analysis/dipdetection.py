import matplotlib.pyplot as plt
import numpy as np
#import numpy.random.rand as rand

# this tries to detect dips

dx = 0.01;
x = np.arange(0, 30, dx);
N = len(x);

A = [np.cos(xi) + np.cos(3*xi) + np.random.rand(1) for xi in x];

# smoothing parameter; the longer, the greater integration area for running mean
s = 200;
# minimum length of dip
minlen = 6;

mean = [0]*N;
dip = [];
dips = [];
for j in range(N):
    start = max(0, j-s);
    end = min(N-1, j+s);
    r = A[start:end+1];
    mean[j] = sum(r)/len(r);
    if A[j] < mean[j]:
        dip.append(j);
    else:
        if len(dip) > minlen:
            dips.append(dip);
        dip = [];
            


plt.figure(1)
plt.plot(x, A, 'r', x, mean, 'b');
for d in dips:
    xd = x[d[0]:d[-1]+1];
    Ad = A[d[0]:d[-1]+1];
    plt.plot(xd, Ad, 'g')
plt.show()
