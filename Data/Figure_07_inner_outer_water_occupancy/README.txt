Figure 7. Water occupancy in the inner and outer probe regions

Ligand folders correspond to panels (b–g), in the order CB431, Nuvia cPrime, CB433,
CB441, CB434, and CB442. The inner and outer regions partition the local union of
spheres; the geometry is illustrated in panel (a) and defined in the manuscript.

Each replica contains unsmoothed mean water counts for the inner region, outer
region, and their total. These columns retain the values originally labeled
N_inside_circle, N_outside_circle, and N_total_union.

The summary files contain the line and shaded-band values used in the figure. Each
replica is smoothed with a Savitzky–Golay filter (9 points, polynomial order 2,
mode='interp'), then interpolated onto the first replica's grid within the shared
bias range. The reported mean and sample standard deviation (ddof=1) are calculated
across three simulation replicas for every ligand. The n_replicates column
records this count. beta_phi is
dimensionless; water counts are numbers of molecules.

metadata.json defines every column.

figure07.pdf is the assembled figure. plot_figure7.py redraws the numerical
panels from the CSV files in this folder; it does not draw the molecular
configuration or chemical structures. Run python plot_figure7.py from this
folder. NumPy, SciPy, and Matplotlib are required.
