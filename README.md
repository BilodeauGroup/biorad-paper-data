# Bio-Rad manuscript data

Data supporting **Characterizing the Hydrophobic Contribution to Adsorption on Ligand-functionalized Surfaces**.

This repository contains simulation and experimental data on the hydrophobic contribution to protein adsorption on ligand-functionalized surfaces. The data include water occupancy, free energy of cavity formation, solvent-accessible surface area (SASA), chemical-group hydration, probe volume geometry, protein adsorption, and protein elution salt concentrations.

## Repository contents

- [Data/](Data/) contains the numerical data, organized by subject. Each dataset has a short README and column definitions in `metadata.json`.
- [Data/file_index.csv](Data/file_index.csv) maps each data file to its manuscript or Supplementary Information figure.
- [scripts/](scripts/) contains a plotting script for every numerical dataset. The [script guide](scripts/README.md) lists the matching datasets and figures.
- [plot_all.py](plot_all.py) runs all plotting scripts. Generated files are saved in `plots/`, organized by dataset.

CSV files can be opened in a spreadsheet or read with an analysis program. Individual replicate results and plotted summaries are supplied where available. The [data guide](Data/README.txt) explains file conventions; each dataset's documentation gives units, uncertainty, and any normalization or smoothing. Selected coordinate and probe-definition files are included; full simulation trajectories are not.

## Generating the plots

Use Python 3.10–3.12, with Arial and Aptos available for the panels that use those fonts. From the repository root, install the plotting dependencies and generate all numerical plots:

```bash
python -m pip install -r requirements.txt
python plot_all.py
```

Every dataset is exported as PDF, SVG, and PNG. The scripts reproduce the numerical panels using the deposited plot values and documented calculations. Molecular illustrations, chemical structures, and final composite layouts are assembled separately.

To list the datasets or plot a selected dataset:

```bash
python plot_all.py --list
python plot_all.py --dataset protein_adsorption_pmf
```

Individual scripts can also be run directly. Use `--output-dir` to choose where the generated plots are saved. Reading the CSV files does not require these plotting dependencies.

## Contact

Camille Bilodeau  
Department of Chemical Engineering, University of Virginia  
[cur5wz@virginia.edu](mailto:cur5wz@virginia.edu)
