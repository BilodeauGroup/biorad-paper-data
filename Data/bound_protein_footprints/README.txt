Figure S8. Protein footprints in the bound state

Each ligand CSV contains a 180 by 180 density map, flattened with y varying fastest.
Water density is in water oxygen atoms per cubic angstrom. dewetted_mask is 1 below
the original threshold of 0.002 atoms/angstrom^3 and 0 elsewhere. The map was
recentered using periodic shifts.

display_x and display_y reproduce the coordinates used to draw the original figure,
which stretched the maps to x = -10 to 100 and y = -20 to 90. These display
coordinates must not be used to measure physical distances or areas.
source_x_angstrom and source_y_angstrom retain the physical bin centres; their
periodic wrapping is expected after recentering. Use those coordinates for physical
measurements. The density values have not been rescaled.

Plotting

From the repository root, run:
  python scripts/plot_bound_protein_footprints.py

PDF, SVG, and PNG files are saved in plots/bound_protein_footprints/.
