Figure 5. Hydration of ligand chemical groups

The umbrella_sampling folders correspond to panels (a–c), and indus to panels (d–f),
in the order Nuvia cPrime, CB434, and CB442. Each ligand has an unsmoothed
hydration_analysis.csv and a hydration_plotted.csv containing the line coordinates
shown in the figure. Chemical-group names identify separate curves. CB434 phenyl_1
and phenyl_2 retain the figure's 1st phenyl and 2nd phenyl labels, respectively. The
first is the common scaffold ring; the second is the additional phenyl group. CB442
butyl retains the figure's label for its branched alkyl group.

For umbrella sampling, rows are sorted by protein–surface center-of-mass distance in
nm and divided into 10 equal-count bins. The mean distance and median water count
are calculated in each bin. Binned water counts are smoothed with a Gaussian kernel
(sigma 1.2 bins, radius 5 bins, edge padding), then divided by the last smoothed
value, representing the unbound state.

For INDUS, the water counts are smoothed with a Gaussian kernel (sigma 1.5 points,
radius 6 points, edge padding), then divided by the first smoothed value at zero
bias. beta_phi is dimensionless. Plotted marker positions are sampled from these
curves.

The analysis files preserve the supplied hydration values before plotting
transformations. These are mean counts for the chemical-group hydration selections,
rather than individual-water trajectories. metadata.json defines every column.

Plotting

From the repository root, run:
  python scripts/plot_chemical_group_hydration.py

PDF, SVG, and PNG files are saved in plots/chemical_group_hydration/.
