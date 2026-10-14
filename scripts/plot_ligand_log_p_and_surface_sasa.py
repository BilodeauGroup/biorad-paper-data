"""Reproduce the manuscript's chemical-group SASA plot from deposited values."""
import numpy as np
import matplotlib.pyplot as plt
from _common import DATA, LIGANDS, label, read_csv, output_dir, save, cli

DATASET = "ligand_log_p_and_surface_sasa"
CATEGORIES = ("charged", "polar", "hydrophobic")
CATEGORY_COLORS = ("#A63A34", "#008C95", "#C49A00")


def main(supplied_output_dir=None):
    """Draw the deposited SASA bars using the manuscript's plotting settings."""
    plt.rcdefaults()
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    sasa = {(r["ligand"].replace(" ", "_"), r["chemical_category"]):
            float(r["mean_sasa_nm2"])
            for r in read_csv(DATA / DATASET / "surface_sasa.csv")}
    x = np.arange(len(LIGANDS))
    width = 0.24
    fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
    fig.subplots_adjust(left=0.15, right=0.98, bottom=0.20, top=0.86)
    for index, (category, color) in enumerate(zip(CATEGORIES, CATEGORY_COLORS)):
        ax.bar(x + (index - 1) * width,
               [sasa[lig, category] for lig in LIGANDS], width=width,
               color=color, label=category.capitalize(), edgecolor="none", linewidth=0)
    ax.set_xticks(x)
    ax.set_xticklabels([label(lig) for lig in LIGANDS], rotation=30,
                       ha="center", rotation_mode="anchor")
    ax.set_ylabel(r"SASA ($\mathrm{nm^2}$)", fontsize=20)
    ax.set_ylim(bottom=0)
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(2.2)
    ax.tick_params(axis="both", which="major", labelsize=16)
    ax.tick_params(axis="x", pad=26)
    ax.legend(frameon=False, ncol=3, loc="lower center",
              bbox_to_anchor=(0.5, 1.02), fontsize=14, borderaxespad=0)
    return save(fig, directory, "chemical_group_sasa", dpi=600, padding=0.02)


if __name__ == "__main__":
    cli(main)
