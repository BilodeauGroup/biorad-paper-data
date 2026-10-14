Source data

Characterizing the Hydrophobic Contribution to Adsorption on Ligand-functionalized
Surfaces

This collection contains simulation and experimental data on water occupancy, free
energy of cavity formation, solvent-accessible surface area (SASA), chemical-group
hydration, probe volume geometry, protein adsorption, and protein elution salt
concentrations.

Finding the data

Folders are named by the quantities or comparisons they contain. file_index.csv
lists each data file and its corresponding manuscript or Supplementary Information
figure. File paths in the index are relative to this Data folder.

Each dataset has a README.txt describing its files and calculations, and a
metadata.json defining columns and units. The collection contains the numerical
plot data, available replicate results, and selected coordinate and probe-definition
files. Full simulation trajectories are not included.

Reading the files

CSV files have one header row. Units appear in the column names or metadata.
Nuvia_cPrime means Nuvia cPrime. Replicate numbers identify separate simulation
runs; location numbers identify probe positions on a surface.

Summary and plotted tables contain the values used to draw the plots, including
documented normalization or smoothing. Individual replicate and analysis tables
retain the underlying calculated results. SD means standard deviation. Consult the
dataset README for the relevant uncertainty definition. Blank or nonfinite entries
are not zeros. In the protein-elution data, binding_status identifies proteins that
did not bind, with a blank elution concentration.

Plotting

Every numerical dataset has a matching script in the repository's scripts folder.
From the repository root, install requirements.txt and run python plot_all.py to
generate all plots. Each dataset README gives its individual plotting command.
PDF, SVG, and PNG outputs are organized by dataset in the plots folder. See the
repository README and scripts/README.md for instructions and the figure mapping.

Contact

Camille Bilodeau
Department of Chemical Engineering, University of Virginia
cur5wz@virginia.edu
