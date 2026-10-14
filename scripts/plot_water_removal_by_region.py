"""Plot normalized water removal from Nuvia cPrime chemical groups and regions."""
import numpy as np
import matplotlib.pyplot as plt
from _common import DATA, read_csv, values, output_dir, save, cli

DATASET = "water_removal_by_region"
REGIONS = (("carboxylate", "Carboxylate", "red"), ("amide", "Amide", "green"),
           ("phenyl", "Phenyl", "mediumorchid"),
           ("ligand_free_region", "Ligand-free region", "deepskyblue"))


MARKER_X = np.array([0, 0.4, 0.8, 1.2, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6,
                     2.8, 3.0, 3.2, 3.4, 3.8, 4.2, 4.6, 5.0, 5.4, 5.8,
                     6.2, 6.6, 7.0, 7.4, 7.8, 8.2, 8.6, 8.8, 9.2, 9.6,
                     10.0, 10.4, 10.8, 11.2, 11.6, 12.0])


def main(supplied_output_dir=None):
    """Draw the regional occupancy panel using its original plotting settings."""
    plt.rcdefaults()
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    fig, ax = plt.subplots(figsize=(7, 5), dpi=200)
    fig.subplots_adjust(left=0.14, right=0.98, bottom=0.14, top=0.98)
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    for region, name, color in REGIONS:
        rows = read_csv(DATA / DATASET / "Nuvia_cPrime" / f"{region}_occupancy.csv")
        x = values(rows, "beta_phi")
        y = values(rows, "normalized_water_count_plotted")
        ax.plot(x, y, color=color, linewidth=2.5, label=name)
        marker_x = MARKER_X[(MARKER_X >= x[0]) & (MARKER_X <= x[-1])]
        ax.plot(marker_x, np.interp(marker_x, x, y), linestyle="None", marker="o",
                markersize=4.5, color=color)
    ax.set_xlabel(r"$\beta\phi$", fontsize=20)
    ax.set_ylabel(r"$\langle N\rangle/N_0$", fontsize=20)
    ax.tick_params(axis="both", which="major", labelsize=16)
    ax.legend(frameon=False, fontsize=14, loc="best")
    return save(fig, directory, DATASET, dpi=600, padding=0.02)


if __name__ == "__main__":
    cli(main)
