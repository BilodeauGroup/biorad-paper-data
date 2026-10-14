Figure 13. Protein elution salt concentrations

One CSV is provided for each protein. Rows follow the ligand order in the figure.
Concentrations are mM NaCl, estimated from Kp experiments at pH 6.0. The full-range
and expanded panels show the same values; stars in the expanded panel mark bars
that continue above its axis limit.

The binding_status column distinguishes concentrations from nonbinding.
Nonbinding is recorded as did_not_bind with a blank concentration. The source
value 0 for myoglobin on CB441 denotes nonbinding and is encoded the same way.
A blank concentration is not a zero measurement.

The input table contains estimates used for plotting; it does not contain
individual experimental replicates or uncertainty estimates.

Plotting

From the repository root, run:
  python scripts/plot_protein_elution_salt_concentrations.py

PDF, SVG, and PNG files are saved in plots/protein_elution_salt_concentrations/.
