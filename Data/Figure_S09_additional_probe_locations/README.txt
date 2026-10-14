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

To plot the CSVs, run python plot_figure_s9.py from this folder. Python, NumPy, and
Matplotlib are required. Add --show for an interactive window. PNG, SVG, and PDF
files are written to a plots subfolder. figure_s09.pdf shows the curves with the same
ligand and colour mapping.
