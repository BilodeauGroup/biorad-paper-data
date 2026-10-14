"""Plot chemical-group hydration against protein-surface COM distance."""
import numpy as np
import matplotlib.pyplot as plt
from _common import DATA, read_csv, values, output_dir, save, cli

DATASET = "hydration_vs_protein_surface_distance"
SURFACES = ("Nuvia_cPrime", "CB434", "CB442")
GROUP_COLORS = {"carboxylate": "red", "amide": "green", "phenyl": "mediumorchid",
                "phenyl_1": "mediumorchid", "phenyl_2": "black",
                "butyl": "black", "hydroxyl": "orange"}


GROUP_ORDERS = {
    "Nuvia_cPrime": ("carboxylate", "amide", "phenyl", "hydroxyl"),
    "CB434": ("phenyl_2", "carboxylate", "amide", "phenyl_1", "hydroxyl"),
    "CB442": ("butyl", "carboxylate", "amide", "phenyl", "hydroxyl"),
}
LEGEND_SIZES = {"Nuvia_cPrime": (3.0, 2.6), "CB434": (3.2, 3.0), "CB442": (3.0, 3.0)}
GROUP_LABELS = {"phenyl_1": "1st Phenyl", "phenyl_2": "2nd Phenyl"}


def make_panel(ligand):
    from matplotlib.ticker import MultipleLocator
    rows = read_csv(DATA / DATASET / f"{ligand}.csv")
    x = values(rows, "com_distance_nm")
    order = np.argsort(x)
    fig, ax = plt.subplots(figsize=(6.5, 5.0))
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    ax.tick_params(axis="both", which="major", labelsize=18, length=6, width=1.6)
    ax.tick_params(axis="both", which="minor", labelsize=18, length=3.6, width=1.6)
    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    for group in GROUP_ORDERS[ligand]:
        y = values(rows, f"{group}_mean_water_count")
        ax.plot(x[order], y[order], color=GROUP_COLORS[group], linewidth=3,
                label=GROUP_LABELS.get(group, group.capitalize()))
    ax.set_xlabel("COM distance (nm)", fontsize=22)
    ax.set_ylabel(r"$\langle N\rangle$", fontsize=22)
    fig.tight_layout()
    return fig, ax


def make_legend(ligand):
    from matplotlib.lines import Line2D
    fig, ax = plt.subplots(figsize=LEGEND_SIZES[ligand])
    ax.axis("off")
    groups = GROUP_ORDERS[ligand]
    handles = [Line2D([], [], color=GROUP_COLORS[group], linewidth=3) for group in groups]
    legend = ax.legend(handles, [GROUP_LABELS.get(group, group.capitalize()) for group in groups],
                       loc="center", ncol=1, frameon=True, fancybox=False, framealpha=1,
                       facecolor="white", edgecolor="black", fontsize=16, handlelength=2.2,
                       handletextpad=0.6, labelspacing=0.6, borderpad=0.7, borderaxespad=0)
    legend.get_frame().set_linewidth(1.5)
    return fig


def main(supplied_output_dir=None):
    """Draw the original unsmoothed hydration panels and separate boxed legends."""
    plt.rcdefaults()
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    paths = []
    for ligand in SURFACES:
        fig, _ = make_panel(ligand)
        paths.extend(save(fig, directory, ligand, dpi=600, padding=0.02))
        paths.extend(save(make_legend(ligand), directory, f"{ligand}_legend", dpi=600, padding=0.02))
    return paths


if __name__ == "__main__":
    cli(main)
