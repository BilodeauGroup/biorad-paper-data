"""Reproduce the manuscript comparison of cavity-formation free energies."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator
from _common import DATA, LIGANDS, COLORS, label, read_csv, values, style, output_dir, save, cli

DATASET = "cavity_formation_free_energy"
GEOMETRIES = ("cylindrical", "cylindrical_union_of_spheres")


def main(supplied_output_dir=None):
    """Draw the deposited bars, sample SD, and centered replica dots."""
    style()
    plt.rcdefaults()
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    summary = read_csv(DATA / DATASET / "free_energy_summary.csv")
    replicas = read_csv(DATA / DATASET / "free_energy_by_replicate.csv")
    fig, ax = plt.subplots(figsize=(7, 5.5), dpi=220)
    fig.subplots_adjust(left=.15, right=.98, bottom=.20, top=.86)
    x = np.arange(len(LIGANDS))
    width = .32
    for i, geometry in enumerate(GEOMETRIES):
        rows = [next(row for row in summary if row["ligand"] == label(ligand)
                     and row["probe_geometry"] == geometry) for ligand in LIGANDS]
        centers = x + (i - .5) * width
        heights = values(rows, "normalized_beta_free_energy_mean")
        ax.bar(centers, heights, width, yerr=values(rows, "normalized_beta_free_energy_sd"),
               color=[COLORS[ligand] for ligand in LIGANDS], edgecolor="none", linewidth=0,
               capsize=5, error_kw={"ecolor": "black", "elinewidth": 2.5, "capthick": 2})
        if geometry == "cylindrical_union_of_spheres":
            ax.bar(centers, heights, width, facecolor="none", edgecolor="black", linewidth=0, hatch="xx")
        for center, ligand in zip(centers, LIGANDS):
            points = [row for row in replicas if row["ligand"] == label(ligand)
                      and row["probe_geometry"] == geometry]
            ax.scatter(np.full(len(points), center), values(points, "normalized_beta_free_energy"),
                       color="black", s=30, alpha=1, linewidths=0, zorder=4)
    ax.set_xticks(x)
    ax.set_xticklabels([label(ligand) for ligand in LIGANDS], rotation=30, ha="center", rotation_mode="anchor")
    ax.tick_params(axis="both", which="major", labelsize=16, length=6, width=1.6)
    ax.tick_params(axis="x", pad=26)
    ax.set_ylabel(r"$\beta F(\langle N\rangle)/N_0$", fontsize=20)
    ax.set_ylim(2, 4.5)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(MultipleLocator(.5))
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    handles = [Patch(facecolor="white", edgecolor="black", label="Cylindrical"),
               Patch(facecolor="white", edgecolor="black", hatch="xx", label="Cylindrical union of spheres")]
    ax.legend(handles=handles, fontsize=14, frameon=False, loc="center", bbox_to_anchor=(.5, .95), ncol=2)
    return save(fig, directory, DATASET, dpi=600, padding=.02)


if __name__ == "__main__":
    cli(main)
