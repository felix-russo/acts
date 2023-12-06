import numpy as np
import matplotlib.pyplot as plt

covs = np.loadtxt("/home/frusso/hep/out/gaussian_plot/cov.txt")
covs = covs.reshape((-1, 3, 3))
ips = np.loadtxt("/home/frusso/hep/out/gaussian_plot/ip.txt")
ips = ips.reshape((-1, 3))

#print(np.mean(covs, axis=0))
max_inds = np.argmax(covs, axis=0)
print(covs[max_inds[2, 2]])
print(ips[max_inds[2, 2]])

ipParams = np.array([0.008389, -43.8941, -346.304])
cov = np.array( [[0.011,         -1.4928e-06,  -1.95788e-05],
                 [-1.4928e-06,   0.5,         -3.18842e-05],#0.5, 3.0
                 [-1.95788e-05, -3.18842e-05, 208.]])

zBinExtent = 0.05
tBinExtent = 19
nZVals = 41#9
nTVals = 5

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def f(vals):
    diff = vals - ipParams
    res = 1/np.sqrt(np.linalg.det(cov)) * np.exp(-0.5 * diff.transpose().dot(np.linalg.inv(cov) @ diff))
    return res

def zValFromBin(bin):
    return ipParams[1] + zBinExtent * (bin - nZVals / 2)

def tValFromBin(bin):
    return ipParams[2] + tBinExtent * (bin - nTVals / 2)

densities = np.zeros((nZVals, nTVals))
for zBin in range(nZVals):
    z = zValFromBin(zBin)
    for tBin in range(nTVals):
        t = tValFromBin(tBin)
        vec = np.array([0, z, t])
        densities[zBin, tBin] = f(vec)

plt.imshow(densities)
plt.colorbar()
plt.savefig("/home/frusso/hep/out/gaussian_plot/gaussian.pdf")