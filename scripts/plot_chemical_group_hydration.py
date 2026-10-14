"""Plot chemical-group hydration during umbrella sampling and INDUS sampling."""
import numpy as np
import matplotlib.pyplot as plt
from _common import DATA, read_csv, values, output_dir, save, cli

DATASET = "chemical_group_hydration"
SURFACES = ("Nuvia_cPrime", "CB434", "CB442")
GROUP_COLORS = {"carboxylate": "red", "amide": "green", "phenyl": "mediumorchid",
                "phenyl_1": "mediumorchid", "phenyl_2": "black",
                "butyl": "black", "hydroxyl": "orange"}
GROUP_LABELS = {"phenyl_1": "1st phenyl", "phenyl_2": "2nd phenyl"}


GROUP_ORDERS = {
    "Nuvia_cPrime": ("carboxylate", "amide", "phenyl", "hydroxyl"),
    "CB434": ("phenyl_2", "carboxylate", "amide", "phenyl_1", "hydroxyl"),
    "CB442": ("butyl", "carboxylate", "amide", "phenyl", "hydroxyl"),
}
INDUS_DRAW_ORDERS = {
    "Nuvia_cPrime": ("hydroxyl", "amide", "carboxylate", "phenyl"),
    "CB434": ("hydroxyl", "amide", "carboxylate", "phenyl_1", "phenyl_2"),
    "CB442": ("hydroxyl", "amide", "butyl", "carboxylate", "phenyl"),
}
BOUND_DISTANCES = {"Nuvia_cPrime": 3.39, "CB434": 3.1, "CB442": 3.07}
MARKER_X = np.array([0, 0.4, 0.8, 1.2, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6,
                     2.8, 3.0, 3.2, 3.4, 3.8, 4.2, 4.6, 5.0, 5.4, 5.8,
                     6.2, 6.6, 7.0, 7.4, 7.8, 8.2, 8.6, 8.8, 9.2, 9.6,
                     10.0, 10.4, 10.8, 11.2, 11.6, 12.0])


def make_panel(method, ligand):
    rows = read_csv(DATA / DATASET / method / ligand / "hydration_plotted.csv")
    umbrella = method == "umbrella_sampling"
    x_key = "com_distance_nm" if umbrella else "beta_phi"
    fig, ax = plt.subplots(figsize=(6.5, 5.0), dpi=100 if umbrella else 200)
    if not umbrella:
        fig.subplots_adjust(left=0.14, right=0.98, bottom=0.14, top=0.98)
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    group_order = GROUP_ORDERS[ligand] if umbrella else INDUS_DRAW_ORDERS[ligand]
    for group in group_order:
        selected = [r for r in rows if r["chemical_group"] == group]
        x = values(selected, x_key)
        y = values(selected, "normalized_water_count_plotted")
        order = np.argsort(x)
        x, y = x[order], y[order]
        # These are the source plot's processed coordinates. Do not smooth again.
        ax.plot(x, y, linewidth=3.0 if umbrella else 2.5,
                color=GROUP_COLORS[group],
                label=GROUP_LABELS.get(group, group.capitalize()))
        if not umbrella:
            marker_x = MARKER_X[(MARKER_X >= x[0]) & (MARKER_X <= x[-1])]
            ax.plot(marker_x, np.interp(marker_x, x, y), linestyle="None", marker="o",
                    markersize=4.5, color=GROUP_COLORS[group])
    ax.tick_params(axis="both", which="major", labelsize=18)
    if umbrella:
        from matplotlib.ticker import MultipleLocator
        ax.tick_params(axis="both", which="major", length=6, width=1.6)
        ax.xaxis.set_major_locator(MultipleLocator(1.0))
        ax.set_xlabel("COM distance (nm)", fontsize=22)
        ax.set_ylabel(r"$\langle N\rangle / \langle N\rangle_{\mathrm{unbound}}$", fontsize=22)
        ax.set_ylim(0.7, 1.05)
        x_bound = BOUND_DISTANCES[ligand]
        ax.plot([x_bound, x_bound], [0.75, 1.015], color="black", linestyle="--", linewidth=2.2)
        ax.text(0.11 if ligand == "Nuvia_cPrime" else 0.02, 0.945,
                "Favorable bound state", transform=ax.transAxes, ha="left", va="center", fontsize=18)
        ax.legend(frameon=False, fontsize=16, loc="lower right",
                  handlelength=2.2, handletextpad=0.6, borderaxespad=0.4)
        fig.tight_layout()
    else:
        ax.set_xlabel(r"$\beta\phi$", fontsize=22)
        ax.set_ylabel(r"$\langle N\rangle/N_0$", fontsize=22)
        handles, names = ax.get_legend_handles_labels()
        by_name = dict(zip(names, handles))
        names = [GROUP_LABELS.get(group, group.capitalize()) for group in GROUP_ORDERS[ligand]]
        ax.legend([by_name[name] for name in names], names, frameon=False,
                  fontsize=16, loc="best")
    return fig


def main(supplied_output_dir=None):
    """Draw the six numerical panels with the manuscript's fonts, colors and markers."""
    plt.rcdefaults()
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    paths = []
    for method in ("umbrella_sampling", "indus"):
        for ligand in SURFACES:
            fig = make_panel(method, ligand)
            paths.extend(save(fig, directory, f"{method}_{ligand}", dpi=600,
                              padding=0.1 if method == "umbrella_sampling" else 0.02))
    return paths


if __name__ == "__main__":
    cli(main)
