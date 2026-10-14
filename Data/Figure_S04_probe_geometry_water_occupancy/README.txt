Figure S4. Water removal for two probe-volume definitions

Each ligand folder is divided into cylindrical and cylindrical_union_of_spheres.
Each geometry has replicate_01 through replicate_03 folders, each containing
occupancy.csv, and an occupancy_summary.csv. Replicate files retain the original
bias strengths and mean water counts. Summary files contain the normalized mean
curves and the sample SD used for the shaded bands.

For each replicate, water counts were smoothed with a Savitzky-Golay filter (9-point
window, polynomial order 2, interpolation at the ends), then divided by the smoothed
count at beta_phi = 0. Replicates were interpolated onto the first replicate's grid
over their common range, then averaged. The SD uses ddof = 1. Use the summary files
directly; do not smooth them again.

Panels a-f: CB431, Nuvia cPrime, CB433, CB441, CB434, and CB442.
