Figure 4. Surface chemistry and ligand logP

surface_sasa.csv contains the supplied mean solvent-accessible surface areas for
charged, polar, and hydrophobic groups. The means use five trajectory frames
(4996–5000); sample standard deviations (ddof=1) and the frame count are retained
from the original analysis summary. The original values are in angstrom^2; the nm^2
columns use 1 nm^2 = 100 angstrom^2. The plot displays means without error bars.
surface_sasa_by_frame.csv retains the per-frame category values.

The SASA analysis used VMD with a 1.4 angstrom probe and periodic-boundary
corrections. Charged groups comprise carboxylate groups; polar groups comprise amide
and linker groups; hydrophobic groups comprise the phenyl and added nonpolar groups.
Values are retained at their saved precision, so recomputing summaries from the
rounded per-frame table may differ in the final reported decimal place.

ligand_log_p.csv contains the six calculated logP values displayed in the figure.
These values were transcribed from the editable figure source and checked against
the manuscript. They are reported descriptors; the underlying chemical-property
calculation files are not part of this dataset.

metadata.json defines the columns.
