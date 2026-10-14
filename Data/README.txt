Source data

Characterizing the Hydrophobic Contribution to Adsorption on Ligand-functionalized
Surfaces

This folder contains the numerical data behind Figures 3–13 and Figures S2, S4–S9,
and S11–S13, together with available replicate results and selected supporting
files. It covers water occupancy, cavity-formation free energy, surface geometry,
hydration, protein adsorption, and protein elution.

Finding the data

Folder names combine the figure number with a short description of the data. For
example, Figure_07_inner_outer_water_occupancy contains the data for Figure 7.
The S prefix identifies figures in the Supplementary Information. file_index.csv
lists each data file and its figure; paths are relative to this Data folder.

Each figure folder has a README.txt describing its files and calculations.
metadata.json provides the column definitions and units. Figures 1, 2, S1, S3,
and S10 contain illustrations or molecular views rather than numerical plot tables.

Reading and using the files

CSV files have one header row and can be opened in a spreadsheet or read with an
analysis program. Units are given in column names or the figure documentation.
Nuvia_cPrime in a filename means Nuvia cPrime. Replicate numbers identify separate
simulation runs; location numbers identify different probe positions on a surface.

Summary and plotted files contain the values used to draw the figures, including
any documented normalization or smoothing. Individual replicate and analysis files
provide the underlying calculated results. Use the figure README to choose the
appropriate table and interpret uncertainty. SD means standard deviation, not
standard error. Blank or nonfinite entries are not zeros; their meaning is explained
in the relevant folder. Figure 13 uses a binding-status column to identify proteins
that did not bind.

Plotting scripts are included for Figures 7 and S9, with instructions in their
folders. Selected coordinate and probe-definition files are also supplied. Full
simulation trajectories are not part of this collection.

Contact

Camille Bilodeau
Department of Chemical Engineering, University of Virginia
cur5wz@virginia.edu
