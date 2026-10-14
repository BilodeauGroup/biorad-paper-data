#!/usr/bin/env python3
"""Draw the numerical plots from the deposited simulation and experimental data."""
from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
DATASETS = (
    "global_water_occupancy_and_free_energy",
    "ligand_log_p_and_surface_sasa",
    "chemical_group_hydration",
    "local_water_occupancy_and_free_energy",
    "inner_outer_water_occupancy",
    "probe_geometry_comparison",
    "cavity_formation_free_energy",
    "probe_radius_dependence",
    "water_removal_by_region",
    "probe_location_dependence",
    "protein_elution_salt_concentrations",
    "chemical_group_sasa",
    "probe_geometry_water_occupancy",
    "surface_height_and_waviness",
    "rms_surface_waviness",
    "ligand_free_probe_volume",
    "bound_protein_footprints",
    "additional_probe_locations",
    "surface_and_protein_density_profiles",
    "protein_adsorption_pmf",
    "hydration_vs_protein_surface_distance",
)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=DATASETS, nargs="+", help="Plot only the selected datasets")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "plots", help="Parent folder for all generated plots")
    parser.add_argument("--list", action="store_true", help="List the available datasets")
    args = parser.parse_args()
    if args.list:
        print("\n".join(DATASETS))
        return
    selected = args.dataset or DATASETS
    output = args.output_dir.resolve()
    for dataset in selected:
        script = ROOT / "scripts" / f"plot_{dataset}.py"
        if not script.is_file():
            raise FileNotFoundError(f"Missing plotting script: {script}")
        print(f"Plotting {dataset}...", flush=True)
        subprocess.run([sys.executable, str(script), "--output-dir", str(output / dataset)], check=True)
    print(f"Completed {len(selected)} datasets. Plots are in {output}")

if __name__ == "__main__":
    main()
