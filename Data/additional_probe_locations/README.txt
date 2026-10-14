Figure S9. Water removal at probe locations 2 and 3

Each location and ligand folder contains occupancy.csv and free_energy.csv. Both
source values and the values used to draw the figure are retained. The occupancy
curve is normalized by its mean water count at zero bias, then smoothed using a
9-point, order-2 Savitzky-Golay filter with interpolated ends. The free-energy
coordinates are both divided by the largest water count in that free-energy table.
No smoothing is applied to free energy. Use the columns ending in _plotted directly
to reproduce the curves.

Ligand IDs follow the simulation source files. The colour mapping is: CB431, dark
green; Nuvia cPrime, green; CB433, blue; CB441, purple; CB434, magenta; CB442,
orange.

Plotting

From the repository root, run:
  python scripts/plot_additional_probe_locations.py

PDF, SVG, and PNG files are saved in plots/additional_probe_locations/.
