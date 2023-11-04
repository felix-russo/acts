import numpy as np
import matplotlib.pyplot as plt

def calcNBinsFromArray(arr, binExtent):
    min = np.min(arr)
    max = np.max(arr)
    nBins = calcNBins(min, max, binExtent)
    return nBins

def calcNBins(min, max, binExtent):
    nBins = int(np.round((max-min)/binExtent)) + 1 
    return nBins

def getBin(value, binExtent):
  return int(np.floor(value / binExtent - 0.5) + 1)

pathToFolder = "/home/frusso/hep/out/track_densities/"
data = np.loadtxt(pathToFolder + "densities1D.txt")
print(np.shape(data))

spatialBinExtent = 0.025
#nBinsZ = calcNBinsFromArray(data[:, 0], spatialBinExtent)
#print(nBinsZ)

temporalBinExtent = 0.1
#nBinsT = calcNBinsFromArray(data[:, 1], temporalBinExtent)
#print(nBinsT)


maxZ = 4
maxZBin = getBin(maxZ, spatialBinExtent)
minZ = 3
minZBin = getBin(minZ, spatialBinExtent)
nBinsZShown = calcNBins(minZ, maxZ, spatialBinExtent)
print(nBinsZShown)

maxT = 0
maxTBin = getBin(maxT, temporalBinExtent)
minT = 0
minTBin = getBin(minT, temporalBinExtent)
nBinsTShown = calcNBins(minT, maxT, temporalBinExtent)
print(nBinsTShown)
density = np.zeros((nBinsZShown, nBinsTShown))
print(maxZBin, minZBin, maxTBin, minTBin)
#Fill density
for i in range(len(data)):
    zBin = data[i, 0]
    tBin = data[i, 1]
    if not minZBin < zBin < maxZBin:
        continue
    if not minTBin < tBin < maxTBin:
        continue
    zBinShifted = int(zBin - minZBin)
    tBinShifted = int(tBin - minTBin)
    density[zBinShifted, tBinShifted] = data[i, 2]


#renormalize z and t
data[:, 0] = (data[:, 0]-np.min(data[:, 0]))/(np.max(data[:, 0])-np.min(data[:, 0]))
data[:, 1] = (data[:, 1]-np.min(data[:, 1]))/(np.max(data[:, 1])-np.min(data[:, 1]))

plt.figure()
#plt.imshow(density, cmap="OrRd")
plt.scatter(data[:, 0], data[:, 1], c=data[:, 2], cmap='viridis', s=0.1)
ax = plt.gca()
#ax.set_xlim([-2, 4])

#ax.set_ylim([-100, 100])
#ax.set_aspect('equal')
#plt.autoscale(enable=True, axis='y')
plt.colorbar()
plt.savefig(pathToFolder + "densities1D.pdf")