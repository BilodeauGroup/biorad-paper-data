"""Reproduce cavity-formation free energy and SASA across probe locations."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from _common import DATA, LIGANDS, COLORS, label, read_csv, values, style, output_dir, save, cli

DATASET = "probe_location_dependence"
CATEGORIES = (("charged", "Charged", "#A63A34"),
              ("polar", "Polar", "#008C95"),
              ("hydrophobic", "Hydrophobic", "#C49A00"))


def main(supplied_output_dir=None):
    """Read deposited means and SD and reproduce the two numerical panels."""
    style()
    plt.rcdefaults()
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    paths = []
    x = np.arange(len(LIGANDS))
    summary = read_csv(DATA / DATASET / "free_energy_summary.csv")
    rows = [next(row for row in summary if row["ligand"] == label(ligand)) for ligand in LIGANDS]
    fig, ax = plt.subplots(figsize=(7, 5.5), dpi=220)
    fig.subplots_adjust(left=.15, right=.98, bottom=.20, top=.86)
    ax.bar(x, values(rows, "normalized_beta_free_energy_mean"), width=.62,
           yerr=values(rows, "normalized_beta_free_energy_sd"), capsize=5,
           color=[COLORS[ligand] for ligand in LIGANDS], edgecolor="black", linewidth=.8,
           error_kw={"ecolor": "black", "elinewidth": 2.5, "capthick": 2})
    for center, ligand in zip(x, LIGANDS):
        rows = read_csv(DATA / DATASET / ligand / "free_energy_by_location.csv")
        ax.scatter(np.full(len(rows), center), values(rows, "normalized_beta_free_energy"),
                   color="black", s=30, alpha=1, linewidths=0, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels([label(ligand) for ligand in LIGANDS], rotation=30, ha="center", rotation_mode="anchor")
    ax.set_ylabel(r"$\beta F(\langle N\rangle)/N_0$", fontsize=20)
    ax.tick_params(axis="both", which="major", labelsize=16, length=6, width=1.6)
    ax.tick_params(axis="x", pad=26)
    ax.set_ylim(2, 4.5)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(MultipleLocator(.5))
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    paths.extend(save(fig, directory, "free_energy", dpi=600, padding=.02))

    summary = read_csv(DATA / DATASET / "sasa_summary.csv")
    fig, ax = plt.subplots(figsize=(7, 5.5), dpi=200)
    fig.subplots_adjust(left=.15, right=.98, bottom=.20, top=.86)
    width = .24
    for i, (category, title, color) in enumerate(CATEGORIES):
        rows = [next(row for row in summary if row["ligand"] == label(ligand)
                     and row["chemical_category"] == category) for ligand in LIGANDS]
        centers = x + (i - 1) * width
        ax.bar(centers, values(rows, "mean_sasa_nm2"), width,
               yerr=values(rows, "sd_sasa_nm2"), capsize=4, color=color, edgecolor="none", linewidth=0,
               error_kw={"ecolor": "black", "elinewidth": 1.8, "capthick": 1.8}, label=title)
        for center, ligand in zip(centers, LIGANDS):
            rows = read_csv(DATA / DATASET / ligand / "sasa_by_location.csv")
            ax.scatter(np.full(len(rows), center), values(rows, f"{category}_sasa_nm2"),
                       color="black", s=16, alpha=.75, linewidths=0, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels([label(ligand) for ligand in LIGANDS], rotation=30, ha="center", rotation_mode="anchor")
    ax.set_ylabel(r"SASA ($\mathrm{nm^2}$)", fontsize=20)
    ax.tick_params(axis="both", which="major", labelsize=16)
    ax.tick_params(axis="x", pad=26)
    ax.set_ylim(bottom=0)
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(.5, 1.02), fontsize=14, borderaxespad=0)
    paths.extend(save(fig, directory, "sasa", dpi=600, padding=.02))
    return paths


if __name__ == "__main__":
    cli(main)
