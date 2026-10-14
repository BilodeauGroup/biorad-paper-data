"""Reproduce the numerical global-probe occupancy and free-energy panels."""
import numpy as np
import matplotlib.pyplot as plt
from _common import DATA, LIGANDS, COLORS, label, read_csv, values, style, output_dir, save, cli

DATASET = "global_water_occupancy_and_free_energy"
# Display settings from the manuscript's original plotting notebook.
MARKER_X = np.array([0, .4, .8, 1.2, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8,
                     3, 3.2, 3.4, 3.8, 4.2, 4.6, 5, 5.4, 5.8, 6.2, 6.6,
                     7, 7.4, 7.8, 8.2, 8.6, 8.8, 9.2, 9.6, 10, 10.4, 10.8,
                     11.2, 11.6, 12])


def main(supplied_output_dir=None):
    """Read saved plotted summaries and export both manuscript numerical panels."""
    style()
    plt.rcdefaults()
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    paths = []
    for kind, xkey, ykey, sdkey in (
        ("occupancy", "beta_phi", "normalized_water_count_mean", "normalized_water_count_sd"),
        ("free_energy", "normalized_water_count", "normalized_beta_free_energy_mean", "normalized_beta_free_energy_sd"),
    ):
        fig, ax = plt.subplots(figsize=(6, 5), dpi=200)
        fig.subplots_adjust(left=.24, right=.98, bottom=.22, top=.98)
        for spine in ax.spines.values():
            spine.set_linewidth(2.2)
        for ligand in LIGANDS:
            rows = read_csv(DATA / DATASET / ligand / f"{kind}_summary.csv")
            x, y, sd = (values(rows, key) for key in (xkey, ykey, sdkey))
            # Saved summaries already contain the original normalization,
            # smoothing and replica statistics; do not process them again.
            ax.plot(x, y, color=COLORS[ligand], label=label(ligand), linewidth=2.5)
            ax.fill_between(x, y - sd, y + sd, color=COLORS[ligand], alpha=.5, linewidth=0)
            if kind == "occupancy":
                mx = MARKER_X[(MARKER_X >= x[0]) & (MARKER_X <= x[-1])]
                my = np.interp(mx, x, y)
            else:
                idx = list(range(0, len(x), 2))
                if len(x) - 1 not in idx:
                    idx.append(len(x) - 1)
                mx, my = x[idx], y[idx]
            ax.plot(mx, my, linestyle="None", marker="o", markersize=4.5, color=COLORS[ligand])
        if kind == "occupancy":
            ax.set_xlabel(r"$\beta\phi$", fontsize=20)
            ax.set_ylabel(r"$\langle N\rangle/N_0$", fontsize=20)
        else:
            ax.set_xlabel(r"$\langle N\rangle/N_0$", fontsize=20)
            ax.set_ylabel(r"$\beta\,F(\langle N\rangle)/N_0$", fontsize=20)
            ax.set_xlim(-.03, 1.05)
        ax.tick_params(axis="both", which="major", labelsize=16)
        ax.legend(fontsize=17, frameon=False)
        paths.extend(save(fig, directory, kind, dpi=600, padding=.02))
    return paths


if __name__ == "__main__":
    cli(main)
