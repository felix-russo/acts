import numpy as np
import matplotlib.pyplot as plt

def calcDensity(coords, ip, cov):
    diff = coords - ip
    coef = 1. / np.sqrt(np.linalg.det(cov))
    exp = -0.5 * np.transpose(diff) @ np.linalg.inv(cov) @ diff
    return coef * np.exp(exp)

nTs = 1
ts = np.linspace(-200, 600, nTs)

if nTs == 1:
    nZs = 101
else: 
    nZs = nTs
zs = np.linspace(-0.2, 0.2, nZs)

density = np.zeros((nZs, nTs))

if nTs == 1:
    nDim = 2
else:
    nDim = 3

pathToFolder = "/home/frusso/hep/out/track_densities/"

ips = np.loadtxt(pathToFolder + "trackParams.txt")
ips = np.reshape(ips, (-1, 3))
nTracks = len(ips)

covs = np.loadtxt(pathToFolder + "trackCovs.txt")
covs = np.reshape(covs, (-1, 3, 3))

vtcs = np.loadtxt(pathToFolder + "truthVertices.txt")
vtcs = np.reshape(vtcs, (-1, 4))
nVtcs = len(vtcs)
vtxPosInds = np.zeros((nVtcs, 2))
print(vtcs[:,3])

print(nTracks) 
coords = np.array([0.0, 0.0, 0.0])

# Fill track density
for trkInd in range(nTracks):
    ip = ips[trkInd]
    cov = covs[trkInd]
    for zInd in range(nZs):
        coords[1] = zs[zInd]
        for tInd in range(nTs):
            coords[2] = ts[tInd] 
            density[zInd, tInd] += calcDensity(coords[:nDim], ip[:nDim], cov[:nDim, :nDim])

# Calculate indices of truth vertices
for vtxInd in range(nVtcs):
    z = vtcs[vtxInd, 2]
    t = vtcs[vtxInd, 3]
    zInd = np.argmin(np.abs(zs-z))
    tInd = np.argmin(np.abs(ts-t))
    vtxPosInds[vtxInd, 0] = zInd
    vtxPosInds[vtxInd, 1] = tInd

if nTs == 1:
    plt.figure()
    plt.xlabel("z [mm]")    
    plt.ylabel("Track Density []")    
    plt.plot(zs, density[:, 0])
    plt.yticks([0, np.max(density)], [0, "max"])
    plt.scatter(vtcs[:, 2], np.zeros(nVtcs), color = "r")
    plt.savefig(pathToFolder+"trackDensity1D.pdf")

plt.figure()
if nTs == 1:
    density = np.repeat(density[:, 0, np.newaxis], 10, axis=1)
    offset = 4
else:
    offset = 0
plt.imshow(np.transpose(density), origin="lower")
plt.scatter(vtxPosInds[:, 0], vtxPosInds[:, 1]+4, color = "r")
# style settings
plt.xlabel("z [mm]")
plt.xticks([0, nZs-1], [zs[0], zs[-1]])
if nTs == 1:
    plt.yticks([])
else:
    plt.yticks([0, nTs-1], [ts[0], ts[-1]])
    plt.ylabel("t [mm]")
#colorbar
cbar = plt.colorbar(ax=[plt.gca()], ticks=[np.min(density), np.max(density)])
cbar.ax.set_yticklabels(['min', 'max'])      
cbar.set_label("Track Density []")
if nTs == 1:
    plt.savefig(pathToFolder+"trackDensity2D.pdf")
else:
    plt.savefig(pathToFolder+"trackDensityWithTime2D.pdf")
        
    