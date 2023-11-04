import numpy as np
import matplotlib.pyplot as plt

pathToFolder = "/home/frusso/hep/out/track_densities/"
nVtcs = 5
nTracksPerVtx = 4
nTracks = nTracksPerVtx * nVtcs

compsWithTime = np.loadtxt(pathToFolder + "compatibilitiesWithTime.txt")
compsWithTime = np.reshape(compsWithTime, (-1, nTracks))
plt.figure()
plt.imshow(compsWithTime)
plt.colorbar()
plt.savefig(pathToFolder+"compatibilitiesWithTime.pdf")

comps = np.loadtxt(pathToFolder + "compatibilities.txt")
comps = np.reshape(comps, (-1, nTracks))
plt.figure()
plt.imshow(comps)
plt.colorbar()
plt.savefig(pathToFolder+"compatibilities.pdf")

vtxInd = 1
trkInds = np.arange(nTracks)
if (vtxInd == 0):
    correctTrkInds = np.array([1, 5, 12, 13])
elif (vtxInd == 1):
    correctTrkInds = np.array([0, 10, 17, 18])
fig, ax = plt.subplots()
ax.plot(trkInds, compsWithTime[vtxInd]/np.max(compsWithTime[vtxInd]), label="with time")
ax.plot(trkInds, comps[vtxInd]/(np.max(comps[vtxInd])), label = "without time")
ax.legend()
ax.set_xticks(trkInds)
for correctTrkInd in correctTrkInds:
    ax.axvline(x=correctTrkInd, color='red', linestyle='--')
plt.savefig(pathToFolder+"compatibilityComparison.pdf")


