"""Plot the supplied upper-boundary height and waviness fields."""
import numpy as np
import matplotlib.pyplot as plt
from _common import DATA, LIGANDS, label, read_csv, values, style, output_dir, save, cli

DATASET = "surface_height_and_waviness"
# Shared colour limits of the manuscript maps, in angstroms.
WAVINESS_LIMITS = (-5.6255065959018005, 5.6255065959018005)
HEIGHT_LIMITS = (21.209300719444826, 31.829958333188657)

def map_grid(rows, column):
    """Place each supplied value on its original x/y grid; mask absent points."""
    x, y = values(rows, "x_angstrom"), values(rows, "y_angstrom")
    # The source display grid spans each radius-8 Å circle in steps of 0.05 Å.
    # Entirely masked edge rows/columns are absent from the CSV; retain them here.
    spacing, size = .05, 321
    ix = np.rint((x-x.min())/spacing).astype(int)
    iy = np.rint((y-y.min())/spacing).astype(int)
    if len(np.unique(iy*size+ix)) != len(rows):
        raise ValueError("Repeated coordinates in a surface map")
    field = np.full((size, size), np.nan)
    field[iy, ix] = values(rows, column)
    extent = (x.min()-spacing/2, x.min()+8*2+spacing/2,
              y.min()-spacing/2, y.min()+8*2+spacing/2)
    return field, extent

def main(supplied_output_dir=None):
    """Reproduce the height and waviness maps from their supplied grid values."""
    plt.rcdefaults()
    plt.rcParams.update({"pdf.fonttype": 42, "svg.fonttype": "path", "axes.grid": False})
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    directory = output_dir(DATASET, supplied_output_dir)
    fig, axes = plt.subplots(2, 6, figsize=(22, 11.4), constrained_layout=True)
    settings = (("waviness_angstrom", "RdBu_r", WAVINESS_LIMITS, "Waviness (Å)"),
                ("surface_height_angstrom", "viridis", HEIGHT_LIMITS, "Surface height (Å)"))
    for j, ligand in enumerate(LIGANDS):
        rows = read_csv(DATA / DATASET / f"{ligand}.csv")
        for i, (column, cmap, limits, title) in enumerate(settings):
            field, extent = map_grid(rows, column)
            im = axes[i, j].imshow(np.ma.masked_invalid(field), origin="lower", extent=extent,
                                  interpolation="bicubic", cmap=cmap, vmin=limits[0], vmax=limits[1])
            axes[i, j].set_aspect("equal")
            axes[i, j].set_axis_off()
            if i == 0:
                axes[i, j].set_title(label(ligand), color="black", fontsize=18)
            if j == len(LIGANDS)-1:
                cb = fig.colorbar(im, ax=axes[i, :].tolist(), fraction=.025, pad=.02, label=title)
                cb.outline.set_visible(False)
    return save(fig, directory, "surface_height_and_waviness", dpi=600, padding=0)

if __name__ == "__main__":
    cli(main)
