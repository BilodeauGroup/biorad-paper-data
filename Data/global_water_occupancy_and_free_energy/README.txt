Figure 3. Global union of spheres

Panels (b) and (c) show the occupancy and water-removal free-energy curves. Each
ligand folder contains three simulation replicas and the plotted mean and sample
standard deviation (ddof=1).

The occupancy analysis gives the mean water count at each dimensionless INDUS bias,
beta_phi. Each replica is normalized by its own water count at zero bias, then
smoothed with a Savitzky–Golay filter (9 points, polynomial order 2, mode='interp').
The mean and sample standard deviation are calculated after linear interpolation
onto the first replica's grid within the shared range.

The free-energy analysis gives mean water count and beta F. Both are divided by the
largest water-count value in that replica's free-energy table, as in the figure's
plotting code. No smoothing is applied to free energy. Replica curves are
interpolated onto the first replica's normalized grid within the shared range before
averaging. The normalization values for occupancy and free energy therefore come
from their respective analysis files.

Per-replica files preserve the analysis values and include the derived values used
to prepare the plots. These are analysis results, rather than trajectory time
series. Summary files contain all line coordinates; the figure displays markers at
selected positions along these lines. metadata.json defines every column.

Plotting

From the repository root, run:
  python scripts/plot_global_water_occupancy_and_free_energy.py

PDF, SVG, and PNG files are saved in plots/global_water_occupancy_and_free_energy/.
