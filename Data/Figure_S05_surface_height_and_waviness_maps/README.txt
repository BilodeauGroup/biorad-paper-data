Figure S5. Probe-volume boundary height and waviness

One CSV per ligand contains the x and y coordinates, upper-boundary height, and
waviness for grid points inside the circular probe. Points outside the probe are
omitted, not zero. Rows run through y for each successive x. The display grid
spacing is 0.05 angstrom. The circular region has radius 8 angstrom; the
union-of-spheres boundary uses spheres of radius 6 angstrom.

Waviness is calculated by subtracting a fitted plane from the boundary height and
applying a Gaussian low-pass filter with cutoff wavelength 5 angstrom (sigma =
0.936953125646388 angstrom). Heights and waviness are in angstroms. Use
surface_height_angstrom for the lower maps and waviness_angstrom for the upper maps.

Figure S6 reports the RMS waviness calculated independently on the original 0.15
angstrom analysis grid. It is not the RMS of these finer display maps. For the
shared colour scales in Figure S5, use -5.6255065959018005 to 5.6255065959018005
angstrom for waviness (RdBu_r) and 21.209300719444826 to 31.829958333188657 angstrom
for height (viridis).
