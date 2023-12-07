import numpy as np
import matplotlib.pyplot as plt

# Impact parameter covariance
covs = np.loadtxt("/home/frusso/hep/out/gaussian_plot/cov.txt")
covs = covs.reshape((-1, 3, 3))
# Impact parameters
ips = np.loadtxt("/home/frusso/hep/out/gaussian_plot/ip.txt")
ips = ips.reshape((-1, 3))

# Indices of maximum (co)variance
max_inds = np.argmax(covs, axis=0)

# Print covariance matrix and impact parameters corresponding to the highest
# var(T)
print(covs[max_inds[2, 2]])
print(ips[max_inds[2, 2]])

# choose a covariance matrix and impact parameters to plot
plotIndex = 30
ip = ips[plotIndex]
cov = covs[plotIndex]

# Algorithm parameters
zBinExtent = 0.05
tBinExtent = 19
nZVals = 41  # 9
nTVals = 5


def f(vals):
    diff = vals - ip
    res = (
        1
        / np.sqrt(np.linalg.det(cov))
        * np.exp(-0.5 * diff.transpose().dot(np.linalg.inv(cov) @ diff))
    )
    return res


def zValFromBin(bin):
    return ip[1] + zBinExtent * (bin - nZVals / 2)


def tValFromBin(bin):
    return ip[2] + tBinExtent * (bin - nTVals / 2)


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
