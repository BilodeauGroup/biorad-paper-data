Figure S2. Local surface composition

sasa_by_category.csv contains the mean SASA for each chemical category and ligand.
mean_sasa_angstrom2 retains the original analysis values in square angstroms.
mean_sasa_nm2 contains the values divided by 100, matching the square-nanometre
units used on the figure axis. No error bars are shown in this figure.

Plotting

From the repository root, run:
  python scripts/plot_chemical_group_sasa.py

PDF, SVG, and PNG files are saved in plots/chemical_group_sasa/.
