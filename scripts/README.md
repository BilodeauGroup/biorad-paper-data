# Plotting the numerical data

Each dataset has a matching script. From the repository root, run `python plot_all.py` to generate every numerical panel, or run an individual script with:

```bash
python scripts/plot_<dataset>.py
```

Replace `<dataset>` with a folder name from the table below. Every script accepts `--output-dir`. By default, PDF, SVG, and PNG files are saved under `plots/<dataset>/`.

| Dataset | Manuscript figure | Script |
| --- | --- | --- |
| [`global_water_occupancy_and_free_energy`](../Data/global_water_occupancy_and_free_energy/) | 3 | [plot_global_water_occupancy_and_free_energy.py](plot_global_water_occupancy_and_free_energy.py) |
| [`ligand_log_p_and_surface_sasa`](../Data/ligand_log_p_and_surface_sasa/) | 4 | [plot_ligand_log_p_and_surface_sasa.py](plot_ligand_log_p_and_surface_sasa.py) |
| [`chemical_group_hydration`](../Data/chemical_group_hydration/) | 5 | [plot_chemical_group_hydration.py](plot_chemical_group_hydration.py) |
| [`local_water_occupancy_and_free_energy`](../Data/local_water_occupancy_and_free_energy/) | 6 | [plot_local_water_occupancy_and_free_energy.py](plot_local_water_occupancy_and_free_energy.py) |
| [`inner_outer_water_occupancy`](../Data/inner_outer_water_occupancy/) | 7 | [plot_inner_outer_water_occupancy.py](plot_inner_outer_water_occupancy.py) |
| [`probe_geometry_comparison`](../Data/probe_geometry_comparison/) | 8 | [plot_probe_geometry_comparison.py](plot_probe_geometry_comparison.py) |
| [`cavity_formation_free_energy`](../Data/cavity_formation_free_energy/) | 9 | [plot_cavity_formation_free_energy.py](plot_cavity_formation_free_energy.py) |
| [`probe_radius_dependence`](../Data/probe_radius_dependence/) | 10 | [plot_probe_radius_dependence.py](plot_probe_radius_dependence.py) |
| [`water_removal_by_region`](../Data/water_removal_by_region/) | 11 | [plot_water_removal_by_region.py](plot_water_removal_by_region.py) |
| [`probe_location_dependence`](../Data/probe_location_dependence/) | 12 | [plot_probe_location_dependence.py](plot_probe_location_dependence.py) |
| [`protein_elution_salt_concentrations`](../Data/protein_elution_salt_concentrations/) | 13 | [plot_protein_elution_salt_concentrations.py](plot_protein_elution_salt_concentrations.py) |
| [`chemical_group_sasa`](../Data/chemical_group_sasa/) | S2 | [plot_chemical_group_sasa.py](plot_chemical_group_sasa.py) |
| [`probe_geometry_water_occupancy`](../Data/probe_geometry_water_occupancy/) | S4 | [plot_probe_geometry_water_occupancy.py](plot_probe_geometry_water_occupancy.py) |
| [`surface_height_and_waviness`](../Data/surface_height_and_waviness/) | S5 | [plot_surface_height_and_waviness.py](plot_surface_height_and_waviness.py) |
| [`rms_surface_waviness`](../Data/rms_surface_waviness/) | S6 | [plot_rms_surface_waviness.py](plot_rms_surface_waviness.py) |
| [`ligand_free_probe_volume`](../Data/ligand_free_probe_volume/) | S7 | [plot_ligand_free_probe_volume.py](plot_ligand_free_probe_volume.py) |
| [`bound_protein_footprints`](../Data/bound_protein_footprints/) | S8 | [plot_bound_protein_footprints.py](plot_bound_protein_footprints.py) |
| [`additional_probe_locations`](../Data/additional_probe_locations/) | S9 | [plot_additional_probe_locations.py](plot_additional_probe_locations.py) |
| [`surface_and_protein_density_profiles`](../Data/surface_and_protein_density_profiles/) | S11 | [plot_surface_and_protein_density_profiles.py](plot_surface_and_protein_density_profiles.py) |
| [`protein_adsorption_pmf`](../Data/protein_adsorption_pmf/) | S12 | [plot_protein_adsorption_pmf.py](plot_protein_adsorption_pmf.py) |
| [`hydration_vs_protein_surface_distance`](../Data/hydration_vs_protein_surface_distance/) | S13 | [plot_hydration_vs_protein_surface_distance.py](plot_hydration_vs_protein_surface_distance.py) |

The scripts reproduce the numerical panels from the deposited tables. Dataset READMEs explain which columns contain plotted values and how normalization, smoothing, and uncertainty were calculated. Illustrations and molecular views are prepared separately.

The plotting scripts were checked with Python 3.12, NumPy 1.26.4, SciPy 1.12.0, and Matplotlib 3.8.3. These dependency versions are recorded in requirements.txt.

Arial is used for the surface-waviness chart; Aptos is used for map scale bars and density-profile annotations added during figure assembly. These fonts must be installed to reproduce their original appearance. Other panel fonts are supplied with Matplotlib.
