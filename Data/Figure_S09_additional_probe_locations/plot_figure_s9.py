#!/usr/bin/env python3
"""Plot Figure S9 CSVs using the original Supplementary Information style.

Requires numpy and matplotlib. The CSV columns already contain the plotted
normalization and smoothing; this script does not repeat either calculation.
Save this script inside Figure_S09_additional_probe_locations, alongside location_02 and location_03.
Run: python plot_figure_s9.py --show
Outputs: plots/figure_s09.png, .svg, and .pdf.
Ligand labels follow the verified source folders (corrected SI legend).
"""

from pathlib import Path
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


DATA_DIR = Path(__file__).resolve().parent

# Explicit mapping verified against the original plotting scripts and folders.
LIGANDS = [
    ("CB431", "CB431", "#15502b"),
    ("Nuvia_cPrime", "Nuvia cPrime", "#1f8744"),
    ("CB433", "CB433", "#2b79b1"),
    ("CB441", "CB441", "#6552a6"),
    ("CB434", "CB434", "#b0126b"),
    ("CB442", "CB442", "#d25a0e"),
]

MARKER_BETA_PHI = np.array([
    0, 0.4, 0.8, 1.2, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3,
    3.2, 3.4, 3.8, 4.2, 4.6, 5, 5.4, 5.8, 6.2, 6.6, 7, 7.4,
    7.8, 8.2, 8.6, 8.8, 9.2, 9.6, 10, 10.4, 10.8, 11.2, 11.6, 12,
])


def read_curve(path, x_column, y_column):
    if not path.is_file():
        raise FileNotFoundError(f"Missing data file: {path}")
    data = np.genfromtxt(path, delimiter=",", names=True)
    x, y = np.atleast_1d(data[x_column]), np.atleast_1d(data[y_column])
    if len(x) < 2 or not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError(f"Invalid curve data: {path}")
    if np.any(np.diff(x) < 0):
        raise ValueError(f"The x values are not sorted: {path}")
    return x, y


def make_figure(data_dir):
    # Original SI panel settings; the assembled SI page is 799 x 657 points.
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 13,
        "axes.labelsize": 22, "axes.linewidth": 2.2,
        "axes.labelpad": 4, "axes.grid": False,
        "xtick.labelsize": 18, "ytick.labelsize": 18,
        "xtick.major.pad": 3.5, "ytick.major.pad": 3.5,
        "mathtext.fontset": "dejavusans",
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.transparent": False,
        "svg.fonttype": "path", "pdf.fonttype": 42, "ps.fonttype": 42,
    })
    page_width, page_height = 799, 657
    fig = plt.figure(figsize=(page_width / 72, page_height / 72))
    # Left, bottom, width, height in points, measured from the assembled SI.
    panel_boxes = [
        [(83.56, 368.56, 266.18, 235.09), (446.29, 368.56, 266.29, 235.09)],
        [(81.60, 52.20, 266.18, 235.20), (445.09, 52.20, 266.18, 235.20)],
    ]
    axes = np.empty((2, 2), dtype=object)
    for row in range(2):
        for column in range(2):
            left, bottom, width, height = panel_boxes[row][column]
            axes[row, column] = fig.add_axes([
                left / page_width, bottom / page_height,
                width / page_width, height / page_height,
            ])

    for column, location in enumerate(["location_02", "location_03"]):
        for folder, label, color in LIGANDS:
            base = data_dir / location / folder
            x, y = read_curve(base / "occupancy.csv", "beta_phi", "normalized_water_count_plotted")
            axes[0, column].plot(x, y, color=color, lw=2.5, label=label)
            markers = MARKER_BETA_PHI[(MARKER_BETA_PHI >= x[0]) & (MARKER_BETA_PHI <= x[-1])]
            axes[0, column].plot(markers, np.interp(markers, x, y), "o", color=color, ms=4.5)

            x, y = read_curve(base / "free_energy.csv", "normalized_water_count_plotted", "normalized_beta_free_energy_plotted")
            axes[1, column].plot(x, y, color=color, lw=2.5, label=label)
            indices = np.unique(np.r_[np.arange(0, len(x), 2), len(x) - 1])
            axes[1, column].plot(x[indices], y[indices], "o", color=color, ms=4.5)

        axes[0, column].set(xlabel=r"$\beta\phi$",
                            ylabel=r"$\langle N\rangle/N_0$", xlim=(-0.6, 12.6))
        axes[1, column].set(xlabel=r"$\langle N\rangle/N_0$", ylabel=r"$\beta\,F(\langle N\rangle)/N_0$",
                            xlim=(-0.03, 1.05))
        axes[0, column].xaxis.set_major_locator(MultipleLocator(2))
        axes[1, column].xaxis.set_major_locator(MultipleLocator(0.2))
        axes[1, column].xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
        axes[0, column].yaxis.set_major_locator(MultipleLocator(0.2))
        axes[1, column].yaxis.set_major_locator(MultipleLocator(1))
        for row in [0, 1]:
            # Match the original automatic 5% vertical margins.
            axes[row, column].margins(y=0.05)
            axes[row, column].tick_params(direction="out", width=0.8, length=3.5)

    # The original separately assembled legend is smaller than the panel text.
    handles = [Line2D([], [], color=color, lw=5.2, marker="o", ms=8.2, label=label)
               for _, label, color in LIGANDS]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(3.5 / page_width, 1 - 3.2 / page_height),
               ncol=6, frameon=False, fontsize=12.6, borderaxespad=0,
               borderpad=0.3, columnspacing=2.33, handlelength=3.6,
               handletextpad=1.0)
    return fig, axes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parent / "plots")
    parser.add_argument("--show", action="store_true", help="Open an interactive plot window.")
    args = parser.parse_args()
    fig, _ = make_figure(args.data_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for extension in ["png", "svg", "pdf"]:
        target = args.output_dir / f"figure_s09.{extension}"
        # Keep the SI page dimensions; PDF and SVG retain vector curves and text.
        fig.savefig(target, dpi=600, bbox_inches=None)
        print(f"Saved: {target}")
    if args.show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    main()
