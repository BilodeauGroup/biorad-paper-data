Figure 12. Location-dependent cavity free energy and SASA

Each ligand folder contains free_energy_by_location.csv for panel a and
sasa_by_location.csv for panel b. The three rows are the three selected probe
locations on the same surface. The two summary CSVs contain plotted means and sample
standard deviations across those locations (ddof=1).

Free energy is dimensionless beta*F/N0, evaluated at the occupancy corresponding to
beta*phi=11. SASA is in nm^2 in the plotted and location-mean tables. The
location_01 through location_03 folders contain sasa_by_frame.csv, retaining the
original Å^2 values and XTC frame indices; 1 Å^2=0.01 nm^2. Each location is
averaged over ten frames (4991–5000). Polar SASA includes the linker. SASA uses a
1.4 Å solvent probe and periodic images, counting exposed sample points inside each
cylindrical probe volume. Per-frame values, individual location means and summary
values are separate because they represent different levels of analysis. The
supplied summary and location-mean values retain their original four decimal places.
