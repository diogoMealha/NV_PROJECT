import matplotlib.pyplot as plt
import numpy as np
from scipy.special import cbrt

# The general purpose of this script is to, GIVEN the observed splittings, infer the magnetic field
# Currently it just does the opposite: given mag field, calc's splittings
# possibly we'll need some sort of iterative method (gradient descent)


# x, y, z axes are wrt. gross shape of diamond
# theta is azimuthal angle, 0 on x axis, pi/2 on y axis, pi in -x direction

# B is unknown field; phi and theta are polar angles wrt. some fixed coord system
# Ba, phia, thetaa: parameters of the known field
# axis = 0, 1, 2, 3 depending on what NV axis is


# takes a list of fields in sph. coords
# outputs their sum, in sph. coords
def vector_sum(fields):
    Bx, By, Bz = [0]*3;
    for f in fields:
        B, phi, theta = f;
        Bx = Bx + B*np.sin(phi)*np.cos(theta);
        By = By + B*np.sin(phi)*np.sin(theta);
        Bz = Bz + B*np.cos(phi);
    
    
    B = np.sqrt(Bx**2 + By**2 + Bz**2);
    phi = arccos(Bx/np.sqrt(Bx**2 + By**2 + Bz**2));
    theta = By/abs(By)*np.arccos(Bx/np.sqrt(Bx**2 + By**2));
#     if Bx == 0:
#         theta = np.pi/2*By/abs(By);
#     else:
#         theta = np.arctan(By/Bx);
    return [B, phi, theta];

def level(field, applied, axis, spin):
    hbar = 1.054572e-34
    DG = 2.87e9;
    D = 2*np.pi*hbar * DG;
    ge = 2.003;
    mub = 9.274010e-24;
    tetr = np.arccos(-1/3);
    axes = {0: [0, 0], 1: [tetr, 0], 2: [tetr, 2*np.pi/3], 3: [tetr, 4*np.pi/3]}
    phinv, thetanv = axes[axis]
    vecnv = [np.sin(phinv)*np.cos(thetanv), np.sin(phinv)*np.sin(thetanv), np.cos(phinv)]
    B, phi, theta = field
    Ba, phia, thetaa = applied
    Bx = B*np.sin(phi)*np.cos(theta) + Ba*np.sin(phia)*np.cos(thetaa);
    By = B*np.sin(phi)*np.sin(theta) + Ba*np.sin(phia)*np.sin(thetaa);
    Bz = B*np.cos(phi) + Ba*np.cos(phia)
    Bmag = np.sqrt(Bx**2 + By**2 + Bz**2);
    
    angle = np.arccos(np.dot([Bx, By, Bz], vecnv)/Bmag);
    Bz = Bmag*np.cos(angle);
    Bx = Bmag*np.sin(angle);
    By = 0;
    X = ge*mub*Bx;
    Y = 0;
    Z = ge*mub*Bz;
    E = 0;
    X = X*1e25;
    Z = Z*1e25;
    D = D*1e25;
    match(spin):
        case 0:
            E = (-D**3 - 9*X**2*D + 9*D*Z**2 + 3*np.sqrt(-3*D**4*Z**2 - 3*D**2*X**4 - 30*D**2*X**2*Z**2 + 6*D**2*Z**4 - 24*X**6 - 36*X**4*Z**2 - 18*X**2*Z**4 - 3*Z**6))**(1/3)/3 + (D**2 + 6*X**2 + 3*Z**2)/(3*(-D**3 - 9*X**2*D + 9*D*Z**2 + 3*np.sqrt(-3*D**4*Z**2 - 3*D**2*X**4 - 30*D**2*X**2*Z**2 + 6*D**2*Z**4 - 24*X**6 - 36*X**4*Z**2 - 18*X**2*Z**4 - 3*Z**6))**(1/3)) + (2*D)/3
        case 1:
            E = -(-D**3 - 9*X**2*D + 9*D*Z**2 + 3*np.sqrt(-3*D**4*Z**2 - 3*D**2*X**4 - 30*D**2*X**2*Z**2 + 6*D**2*Z**4 - 24*X**6 - 36*X**4*Z**2 - 18*X**2*Z**4 - 3*Z**6))**(1/3)/6 + 3*(-D**2/9 - (2*X**2)/3 - Z**2/3)/(2*(-D**3 - 9*X**2*D + 9*D*Z**2 + 3*np.sqrt(-3*D**4*Z**2 - 3*D**2*X**4 - 30*D**2*X**2*Z**2 + 6*D**2*Z**4 - 24*X**6 - 36*X**4*Z**2 - 18*X**2*Z**4 - 3*Z**6))**(1/3)) + (2*D)/3 \
+ 0.5*1j*np.sqrt(3)*((-D**3 - 9*X**2*D + 9*D*Z**2 + 3*np.sqrt(-3*D**4*Z**2 - 3*D**2*X**4 - 30*D**2*X**2*Z**2 + 6*D**2*Z**4 - 24*X**6 - 36*X**4*Z**2 - 18*X**2*Z**4 - 3*Z**6))**(1/3)/3 + 3*(-D**2/9 - (2*X**2)/3 - Z**2/3)/(-D**3 - 9*X**2*D + 9*D*Z**2 + 3*np.sqrt(-3*D**4*Z**2 - 3*D**2*X**4 - 30*D**2*X**2*Z**2 + 6*D**2*Z**4 - 24*X**6 - 36*X**4*Z**2 - 18*X**2*Z**4 - 3*Z**6))**(1/3))
        case 2:
            E = 0;
            
    #return np.real(E[0]-E[2]);
    return E*1e25;


def splitrange(B):
    hbar = 1.054572e-34
    DG = 2.87e9;
    D = 2*np.pi*hbar * DG;
    ge = 2.003;
    mub = 9.274010e-24;
    tetr = np.arccos(-1/3);
    maxi = np.sqrt(D**2+4*(ge*mub*B)**2);
    mini = 2*ge*mub*B;
    print(f"D, mini, maxi: {D}, {mini}, {maxi}")
    
    return [mini, maxi]

def zeeman(B, phi, theta, Ba, phia, thetaa, axis, no):
    hbar = 1.054572e-34
    DG = 2.87e9;
    D = 2*np.pi*hbar * DG;
    ge = 2.003;
    mub = 9.274010e-24;
    tetr = np.arccos(-1/3);
#     maxi = np.sqrt(D**2+4*(ge*mub*hbar*B)**2);
#     mini = 2*ge*mub*hbar*B;
    
    
    axes = {0: [0, 0], 1: [tetr, 0], 2: [tetr, 2*np.pi/3], 3: [tetr, 4*np.pi/3]}
    phinv, thetanv = axes[axis]
    vecnv = [np.sin(phinv)*np.cos(thetanv), np.sin(phinv)*np.sin(thetanv), np.cos(phinv)]
    
    Bx = B*np.sin(phi)*np.cos(theta) + Ba*np.sin(phia)*np.cos(thetaa);
    By = B*np.sin(phi)*np.sin(theta) + Ba*np.sin(phia)*np.sin(thetaa);
    Bz = B*np.cos(phi) + Ba*np.cos(phia)
    Bmag = np.sqrt(Bx**2 + By**2 + Bz**2);
    
    angle = np.arccos(np.dot([Bx, By, Bz], vecnv)/Bmag);
    Bz = Bmag*np.cos(angle);
    Bx = Bmag*np.sin(angle);
    By = 0;
    X = ge*mub*Bx;
    Y = 0;
    Z = ge*mub*Bz;
    
    kappa = -3*D**4*Z**2 - 3*D**2*X**4 - 30*D**2*X**2*Z**2 + 6*D**2*Z**4 - 24*X**6 - 36*X**4*Z**2 - 18*X**2*Z**4 - 3*Z**6;
    if kappa >= 0:
        print("positive")
        rkappa = np.sqrt(kappa)+0*1j;
    else:
        print("negative")
        rkappa = 1j*np.sqrt(-kappa);
    xi = -D**3-9*X**2*D+9*D*Z**2+3*rkappa;
    split = 1j*np.sqrt(3)*(1/3*cbrt(xi)-(1/3*D**2-2*X**2-Z**2)/cbrt(xi));
#     H = [[D+Z, X - 1j*Y, 0], [X + 1j*Y, 0, X-1j*Y], [0, X+1j*Y, D-Z]];
#     E, v = np.linalg.eig(H)
    #return np.real(E[0]-E[2]);
    return split


# given an estimator of B, phi, theta, and the splittings, yields a loss value
def loss(estims, applied, zee):
    B, phi, theta = estims;
    Ba, phia, thetaa = applied;
    loss = 0;
    for j in range(4):
        g = zeeman(B, phi, theta, Ba, phia, thetaa, j);
        loss = loss + abs(g-zee[j]);
    return loss;

# given four observed zeeman splittings, ordered accordingly, this provides the best estimate
# for Bmag, phi and theta
def Bestim(zee):
    return 0




B = 5e-3
split = zeeman(5, 0, 0, 0, 0, 0, 0, 0)

print(f"split: {split}")
#E = zeeman(5, 1, 1)
#E = np.real(E) # due to numerical errors, output is complex


phis = np.arange(0, np.pi, 0.001);
thetas = np.arange(0, 2*np.pi, 0.1);
Nf = len(phis);
Nt = len(thetas);

Es = [[0]*Nt]*Nf

# for nf in range(Nf):
#     f = phis[nf];
#     #print(f)
#     #rint(zeeman(B , f, 0));
#     for nt in range(Nt):
#         t = thetas[nt];
#         Es[nf][nt] = zeeman(B, f, t, 0, 0, 0, 0);
        

extent = [0, np.pi, 0, 2*np.pi]


E0 = level([5, 0, 0], [0, 0, 0], 0, 0);
E1 = level([5, 0, 0], [0, 0, 0], 0, 1);
print("levels:")
print(E0)
print(E1)
#E0s = [zeeman(B, f, 0, 0, 0, 0, 0) for f in phis];

# for e in E0s:
#     print(e)

mini, maxi = splitrange(B)

# print(f"range: {mini, maxi}")
# 
# plt.figure(2)
# plt.plot(phis, E0s, '--', label = "splitting", lw = 5)
# plt.plot(phis, [mini]*Nf, 'r', phis, [-mini]*Nf, 'r', label = "minimum")
# plt.plot(phis, [maxi]*Nf, 'b', phis, [-maxi]*Nf, 'b', label = "maximum")
# 
# plt.xlabel("phi")
# plt.ylabel("Zeeman")
# plt.legend()
# plt.show()

# E0 = [zeeman(B, f, 0, 0, 0, 0, 0, 0) for f in phis];
# E1 = [zeeman(B, f, 0, 0, 0, 0, 0, 1) for f in phis];
# E2 = [zeeman(B, f, 0, 0, 0, 0, 0, 2) for f in phis];
# 
# plt.figure(3)
# plt.plot(phis, E0, 'r')
# plt.plot(phis, E1, 'b')
# plt.plot(phis, E2, 'g')
# plt.show()



