Figure 11. Regional hydration of Nuvia cPrime

Each CSV contains one region from panel b. beta_phi is the dimensionless INDUS bias.
mean_water_count is the unscaled average number of water molecules.
normalized_water_count_plotted is the curve in the figure.

The displayed curves use Gaussian smoothing with a standard deviation of 1.5 points,
a 13-point kernel and edge padding. Each smoothed curve is divided by its smoothed
value at zero bias. The source hydration analysis uses a 20 Å radius cylinder with
z=17.93–29.93 Å and a 4 Å distance cutoff around the surface heavy atoms. The
ligand-free region is farther than 4 Å from those atoms. Each bias value averages
2001 frames, beginning at frame 3000 with stride 1. The region definitions can
overlap; their counts must not be added to infer the total number of water
molecules. Panel a contains molecular snapshots.

Plotting

From the repository root, run:
  python scripts/plot_water_removal_by_region.py

PDF, SVG, and PNG files are saved in plots/water_removal_by_region/.
