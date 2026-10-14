Figure 10. Dependence on cylindrical probe radius

The four radius folders correspond to radii of 6, 8, 12, and 20 Å. Each ligand
folder contains replicate_01 through replicate_03, with occupancy.csv and
free_energy.csv analysis tables. occupancy_summary.csv and free_energy_summary.csv
contain the displayed mean curves and their sample standard deviations (ddof=1).
These tables reproduce the current manuscript curves; no values were read from an
image. Molecular water counts, beta*phi, beta*F and all normalized coordinates are
dimensionless.

For radii 8, 12 and 20 Å, each occupancy curve is divided by its zero-bias count and
smoothed with a 9-point, order-2 Savitzky–Golay filter. Free-energy axes are divided
by the largest water count in each replica's free-energy table. Replica curves are
linearly interpolated onto replica 1's grid within their common range.

For radius 6 Å, both occupancy and free energy use the water count at zero bias as
N0. Each replica is linearly interpolated onto a regular grid, smoothed with an
order-2 Savitzky–Golay filter and evaluated with a shape-preserving cubic
interpolator. The smoothing width/grid step are 1.8/0.05 in beta*phi for occupancy
and 0.06/0.0025 in normalized occupancy for free energy. Plotted curves contain 1001
points within the common support of all three replicas.

Two radius 6 Å input free energies are nonfinite. Their values are blank and
estimate_status records positive_infinity_in_source. The source figure uses local
interpolation for display. display_interpolation marks the affected smoothed
intervals; SD is blank there. Blank cells are never zero measurements.

The complete calculated SD is retained where available. The source plot may omit the
final shaded interval for CB441 for presentation purposes.

The shared supporting_files folder retains one GROMACS coordinate structure per
ligand. The radius-specific supporting_files folders retain INDUS input templates
for radii 8 and 20 Å. Coordinates and input geometry are in nm. The templates
contain phi=xxx, which is replaced for each biasing window. These files are geometry
support; this folder is a figure-data package, not a complete simulation archive.

Plotting

From the repository root, run:
  python scripts/plot_probe_radius_dependence.py

PDF, SVG, and PNG files are saved in plots/probe_radius_dependence/.
