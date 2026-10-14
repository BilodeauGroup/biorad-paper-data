# Bio-Rad manuscript data

Data supporting **Characterizing the Hydrophobic Contribution to Adsorption on Ligand-functionalized Surfaces**.

This repository contains the numerical data for Figures 3–13 and Figures S2, S4–S9, and S11–S13. The collection includes water occupancy and cavity-formation free energies, surface properties, hydration, protein adsorption, and protein elution data.

## Finding the data

The [Data folder](Data/) is organized by figure number and subject. Start with the [data guide](Data/README.txt) or the [file index](Data/file_index.csv). Each figure folder includes a short README and column definitions in `metadata.json`.

CSV files can be opened in a spreadsheet or read with an analysis program. Individual replicate results and plotted summaries are supplied where available. The figure documentation explains units, uncertainty, and any normalization or smoothing. Selected coordinate and probe-definition files are included; full simulation trajectories are not.

## Plotting scripts

Scripts are provided for the numerical panels of Figure 7 and for Figure S9. From the repository root, install the optional plotting dependencies and run:

```bash
python -m pip install -r requirements.txt
python Data/Figure_07_inner_outer_water_occupancy/plot_figure7.py
python Data/Figure_S09_additional_probe_locations/plot_figure_s9.py
```

Each script saves PDF, SVG, and PNG files in a `plots` subfolder. The Figure 7 script checks the saved summaries against all three replicas before plotting; molecular illustrations and chemical structures are not redrawn.

## Contact

Camille Bilodeau  
Department of Chemical Engineering, University of Virginia  
[cur5wz@virginia.edu](mailto:cur5wz@virginia.edu)
