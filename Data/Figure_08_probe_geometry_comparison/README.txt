Figure 8. Probe geometry and water removal

The numerical panels compare cylindrical and cylindrical union-of-spheres probe
volumes. CB433 is panel c; CB434 is panel d. The complete six-ligand comparison is supplied in Figure_S04_probe_geometry_water_occupancy.

Each ligand folder is divided into cylindrical and cylindrical_union_of_spheres.
Each geometry has replicate_01 through replicate_03 folders and an
occupancy_summary.csv. The replicate files contain one mean water count at each
dimensionless bias beta*phi for each of three simulation replicas. These are
analysis results, not trajectory frames. The plotted curves use a Savitzky–Golay
filter (9 points, polynomial order 2), then divide each replica by its smoothed
zero-bias water count. The plotted mean and sample standard deviation (ddof=1) are
calculated across the three replicas. All normalized water counts and beta*phi
values are dimensionless. Panels a and b are molecular visualizations; they have no
plotted numerical axes.
