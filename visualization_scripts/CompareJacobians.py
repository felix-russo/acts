import numpy as np
import matplotlib.pyplot as plt

threshold = 1e-4

# Analytical A
anaPosJac = np.loadtxt("/home/frusso/hep/out/JacobianComparison/A_analytical.txt")
anaPosJac = anaPosJac.reshape((-1, 6, 4))
# Impact parameters
numPosJac = np.loadtxt("/home/frusso/hep/out/JacobianComparison/A_numerical.txt")
numPosJac = numPosJac.reshape((-1, 6, 4))

smallValueMask = (np.abs(anaPosJac) < threshold) & (np.abs(numPosJac) < threshold)
anaPosJac[smallValueMask] = np.nan
numPosJac[smallValueMask] = np.nan

relativeDiff = np.abs(numPosJac - anaPosJac) / np.abs(numPosJac)
meanRelativeDiff = np.nanmean(relativeDiff, axis=0)
stdRelativeDiff = np.nanstd(relativeDiff, axis=0)

# Plotting
fig, axs = plt.subplots(1, 3, gridspec_kw={"width_ratios": [4, 4, 0.5]}, figsize=(8, 5))

max = np.nanmax(np.maximum(meanRelativeDiff, stdRelativeDiff))

im1 = axs[0].imshow(meanRelativeDiff, cmap="viridis", vmin=0, vmax=max)
axs[0].set_xticks(np.arange(4), np.arange(1, 5))
axs[0].set_yticks(np.arange(6), np.arange(1, 7))

im2 = axs[1].imshow(stdRelativeDiff, cmap="viridis", vmin=0, vmax=max)
axs[1].set_xticks(np.arange(4), np.arange(1, 5))
axs[1].set_yticks(np.arange(6), np.arange(1, 7))

# cbar = fig.colorbar(im2, ax=axs, orientation='vertical')#, fraction=0.046, pad=0.04)

# fig.subplots_adjust(right=0.8)
fig.colorbar(im1, cax=axs[2], shrink=0.1)

for i, label in enumerate(["a)", "b)"]):
    axs[i].text(-0.1, 1.05, label, transform=axs[i].transAxes, fontsize=12, va="top")

plt.tight_layout()
plt.savefig("/home/frusso/hep/out/JacobianComparison/jacobian_comparison.pdf")
