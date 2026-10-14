Figure S12. Protein adsorption PMFs

Each ligand CSV contains 200 distances, the plotted PMF, bootstrap SD, and the lower
and upper edges of the one-SD uncertainty band. Distances are in nanometres and
energies are in kJ/mol. WHAM used the final 50 ns of each umbrella window and 100
bootstrap trials.

The original plotting code shifted each PMF separately so that its minimum is -41.3
kJ/mol: plotted PMF = source PMF - min(source PMF) - 41.3. This additive reference
changes neither the profile shape nor its SD. It does not establish a common zero
for comparing adsorption free energies across ligands. The exported PMFs retain this
original plotting reference.
