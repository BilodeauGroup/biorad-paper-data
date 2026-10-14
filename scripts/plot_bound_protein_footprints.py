"""Plot bound-state water-density maps with the original dewetted-mask contour."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager, FontProperties
from pathlib import Path
from _common import DATA, label, read_csv, values, style, output_dir, save, cli

DATASET = "bound_protein_footprints"
LIGANDS = ("Nuvia_cPrime", "CB434", "CB442")
# Numerical-panel graphic geometry recovered from the original assembled SVGs.
# Each entry records panel left/top/width/height, bar endpoints/y, cap y limits,
# text left/baseline, and original frame width, all in the SVG coordinate system.
GRAPHICS = {
    "Nuvia_cPrime": (-227.99226735, 460.3354, 1436.59553435, 1434.1016,
                     -176.5, 176.6, 177.5, 625.5, 593.5, 655.796, -124.72, 570, 6.86455),
    "CB434": (1333.8897, 462.02946743, 1431.7603, 1432.63037177,
              1385.5, 1738.6, 1739.5, 628.5, 597.5, 659.796, 1437, 573, 6.92912),
    "CB442": (2957.513365, 475.112, 1420.9635566, 1420.578,
              3008.5, 3361.6, 3362.5, 634.5, 603.5, 665.796, 3060.74, 580, 6.875),
}

def footprint_grid(rows, column):
    """Use original display coordinates without interpreting them as distances."""
    x, y = values(rows, "display_x"), values(rows, "display_y")
    xs, ys = np.unique(x), np.unique(y)
    ix, iy = np.searchsorted(xs, x), np.searchsorted(ys, y)
    if len(np.unique(iy*len(xs)+ix)) != len(rows):
        raise ValueError("Repeated coordinates in a footprint map")
    field = np.full((len(ys), len(xs)), np.nan)
    field[iy, ix] = values(rows, column)
    dx, dy = np.median(np.diff(xs)), np.median(np.diff(ys))
    return field, (xs[0]-dx/2, xs[-1]+dx/2, ys[0]-dy/2, ys[-1]+dy/2)

def main(supplied_output_dir=None):
    """Draw density and dewetted maps with the original display-coordinate extent."""
    plt.rcdefaults()
    plt.rcParams.update({"pdf.fonttype": 42, "svg.fonttype": "path", "axes.grid": False})
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    directory = output_dir(DATASET, supplied_output_dir)
    paths = []
    regular_aptos = [f.fname for f in fontManager.ttflist if f.name == "Aptos" and "display" not in Path(f.fname).stem.casefold() and f.style == "normal" and f.weight in (400, "normal")]
    if not regular_aptos:
        raise RuntimeError("Install regular Aptos to reproduce the manuscript footprint scale labels, then rebuild the Matplotlib font cache.")
    scale_font = FontProperties(fname=regular_aptos[0])
    for ligand in LIGANDS:
        rows = read_csv(DATA / DATASET / f"{ligand}.csv")
        density, extent = footprint_grid(rows, "water_density_atoms_per_angstrom3")
        dewetted, _ = footprint_grid(rows, "dewetted_mask")
        if not np.array_equal(dewetted.astype(bool), density < .002):
            raise ValueError(f"Supplied dewetted mask is inconsistent for {ligand}")
        # The manuscript cropped the source colorbar and retained the square density panel.
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(density, origin="lower", extent=extent, aspect="equal", cmap="viridis", vmin=0, vmax=.04)
        ax.set_box_aspect(1)
        panel_left, panel_top, panel_width, panel_height, bar_left, bar_right, cap_right, bar_y, cap_top, cap_bottom, text_left, text_baseline, frame_width = GRAPHICS[ligand]
        # Express the original fixed graphics in axis fractions, retaining their placement.
        sx = lambda pixel: (pixel-panel_left)/panel_width
        sy = lambda pixel: 1-(pixel-panel_top)/panel_height
        fig.canvas.draw()
        panel_width_pt = ax.get_window_extent().width/fig.dpi*72
        scale = panel_width_pt/panel_width
        for spine in ax.spines.values():
            spine.set_linewidth(frame_width*scale)
        ax.set_xticks([])
        ax.set_yticks([])
        # Retain the original density-threshold contour using the supplied mask.
        xs = np.unique(values(rows, "display_x"))
        ys = np.unique(values(rows, "display_y"))
        if np.any(dewetted):
            ax.contour(xs, ys, dewetted, levels=[.5], linewidths=frame_width*scale)
        ax.plot([sx(bar_left), sx(bar_right)], [sy(bar_y), sy(bar_y)], transform=ax.transAxes,
                color="black", linewidth=20.625*scale, solid_capstyle="butt")
        for location in (bar_left, cap_right):
            ax.plot([sx(location), sx(location)], [sy(cap_top), sy(cap_bottom)], transform=ax.transAxes,
                    color="black", linewidth=9.16667*scale, solid_capstyle="butt")
        ax.text(sx(text_left), sy(text_baseline), "2 nm", transform=ax.transAxes,
                ha="left", va="baseline", fontsize=110*scale, fontproperties=scale_font)
        paths += save(fig, directory, f"{ligand}_water_density", dpi=600, padding=0)
    return paths

if __name__ == "__main__":
    cli(main)
