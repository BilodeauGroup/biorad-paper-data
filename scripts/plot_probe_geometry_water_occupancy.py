"""Reproduce manuscript water-occupancy panels for both probe geometries."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.lines import Line2D
from _common import DATA, LIGANDS, label, read_csv, values, style, output_dir, save, cli

DATASET = "probe_geometry_water_occupancy"
GEOMETRIES = (("cylindrical", "Cylindrical", "#2B79B1"),
              ("cylindrical_union_of_spheres", "Cylindrical union of spheres", "#D25A0E"))
MARKER_X = np.array([0, .4, .8, 1.2, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8,
                     3, 3.2, 3.4, 3.8, 4.2, 4.6, 5, 5.4, 5.8, 6.2, 6.6,
                     7, 7.4, 7.8, 8.2, 8.6, 8.8, 9.2, 9.6, 10, 10.4, 10.8,
                     11.2, 11.6, 12])


def main(supplied_output_dir=None):
    """Use saved mean curves and sample SD without resmoothing."""
    style()
    plt.rcdefaults()
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    paths = []
    for ligand in LIGANDS:
        fig, ax = plt.subplots(figsize=(5, 4.3), dpi=200)
        fig.subplots_adjust(left=.24, right=.98, bottom=.22, top=.98)
        for spine in ax.spines.values():
            spine.set_linewidth(2.2)
        for geometry, title, color in GEOMETRIES:
            rows = read_csv(DATA / DATASET / ligand / geometry / "occupancy_summary.csv")
            x, y, sd = (values(rows, key) for key in
                        ("beta_phi", "normalized_water_count_mean", "normalized_water_count_sd"))
            ax.plot(x, y, color=color, linewidth=2.5, label=title)
            ax.fill_between(x, y - sd, y + sd, color=color, alpha=.5, linewidth=0)
            mx = MARKER_X[(MARKER_X >= x[0]) & (MARKER_X <= x[-1])]
            ax.plot(mx, np.interp(mx, x, y), linestyle="None", marker="o", markersize=4.5, color=color)
        ax.set_xlabel(r"$\beta\phi$", fontsize=22)
        ax.set_ylabel(r"$\langle N\rangle/N_0$", fontsize=22)
        ax.tick_params(axis="both", which="major", labelsize=18)
        ax.xaxis.set_major_locator(MultipleLocator(2))
        if False:
            ax.legend(fontsize=12.6, frameon=False)
        paths.extend(save(fig, directory, f"{ligand}_occupancy", dpi=600, padding=.02))
    if not False:
        handles = [Line2D([0], [0], color=color, linewidth=3.5, marker="o", markersize=8,
                          label=title) for geometry, title, color in GEOMETRIES]
        fig = plt.figure(figsize=(10, 1.4))
        fig.legend(handles=handles, loc="center", ncol=2, frameon=False, fontsize=18)
        paths.extend(save(fig, directory, "probe_geometry_legend", dpi=600, padding=.02))
    return paths


if __name__ == "__main__":
    cli(main)
