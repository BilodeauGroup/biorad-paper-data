Figure 9. Cavity free energy for two probe geometries

free_energy_by_replicate.csv contains the individual points. The three indices
identify simulation replicas of the same probe location. free_energy_summary.csv
contains the bar heights and sample standard deviations across three replicas.

The reported quantity is beta*F/N0 evaluated at the occupancy corresponding to
beta*phi=11. Occupancy was divided by its zero-bias value and smoothed with a
9-point, order-2 Savitzky–Golay filter. The normalized free-energy curve was
linearly interpolated at that occupancy. beta_phi and normalized_beta_free_energy
are dimensionless.

Plotting

From the repository root, run:
  python scripts/plot_cavity_formation_free_energy.py

PDF, SVG, and PNG files are saved in plots/cavity_formation_free_energy/.
