#!/usr/bin/env python3
"""Plot Figure 7 region-water-count data from the six ligand folders.

Run from the repository root:
    python scripts/plot_inner_outer_water_occupancy.py
Requires numpy, scipy, and matplotlib.
The calculation uses three replicas for every ligand, including Nuvia cPrime.
The existing CSV summaries are checked before any figures are generated.
"""
from pathlib import Path
import argparse
import csv

import numpy as np
from scipy.signal import savgol_filter
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

LIGANDS = ("CB431", "Nuvia_cPrime", "CB433", "CB441", "CB434", "CB442")
COLORS = ("#2B79B1", "#D25A0E")
LABELS = ("Inner region", "Outer region")
MARKER_X = np.array([
    0.0, 0.4, 0.8, 1.2, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8,
    3.0, 3.2, 3.4, 3.8, 4.2, 4.6, 5.0, 5.4, 5.8, 6.2, 6.6,
    7.0, 7.4, 7.8, 8.2, 8.6, 8.8, 9.2, 9.6, 10.0, 10.4, 10.8,
    11.2, 11.6, 12.0,
])


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = csv.DictReader(stream)
        return {name: np.array(values, dtype=float) for name, values in
                zip(rows.fieldnames, zip(*[list(row.values()) for row in rows]))}


def prepare_curve(x, y):
    finite = np.isfinite(x) & np.isfinite(y)
    order = np.argsort(x[finite])
    x, y = x[finite][order], y[finite][order]
    unique_x, inverse = np.unique(x, return_inverse=True)
    if len(unique_x) != len(x):
        totals = np.zeros(len(unique_x))
        counts = np.zeros(len(unique_x))
        np.add.at(totals, inverse, y)
        np.add.at(counts, inverse, 1)
        x, y = unique_x, totals / counts
    if len(x) < 9:
        raise ValueError("Expected at least nine valid bias points per replica.")
    return x, savgol_filter(y, 9, 2, mode="interp")


def calculate_summary(folder):
    """Preserve the original smoothing, common grid, and sample-SD method."""
    replicas = [read_csv(folder / f"replicate_{i:02d}" / "region_water_counts.csv")
                for i in (1, 2, 3)]
    result = {}
    for region in ("inner", "outer"):
        curves = [prepare_curve(r["beta_phi"], r[f"{region}_water_count"])
                  for r in replicas]
        low = max(x[0] for x, _ in curves)
        high = min(x[-1] for x, _ in curves)
        reference = curves[0][0]
        x = reference[(reference >= low) & (reference <= high)]
        values = np.array([np.interp(x, xr, yr) for xr, yr in curves])
        result[region] = (x, values.mean(axis=0), values.std(axis=0, ddof=1))
    expected = read_csv(folder / "region_water_counts_summary.csv")
    if not np.all(expected["n_replicates"] == 3):
        raise ValueError(f"{folder.name}: the summary must include three replicas.")
    for region, (x, mean, sd) in result.items():
        for computed, saved in [
            (x, expected["beta_phi"]),
            (mean, expected[f"{region}_water_count_mean"]),
            (sd, expected[f"{region}_water_count_sd"]),
        ]:
            if computed.shape != saved.shape or not np.allclose(computed, saved, rtol=0, atol=5e-12):
                raise ValueError(f"{folder.name}: calculated values differ from the saved summary.")
    return result


def draw_panel(ax, results, combined=False):
    linewidth, markersize = (3.0, 5.5) if combined else (2.5, 4.5)
    label_font, tick_font = (28, 20) if combined else (20, 16)
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    for region, color, label in zip(("inner", "outer"), COLORS, LABELS):
        x, mean, sd = results[region]
        ax.plot(x, mean, color=color, linewidth=linewidth, label=label + " ")
        ax.fill_between(x, mean-sd, mean+sd, color=color, alpha=0.20, linewidth=0)
        marks = MARKER_X[(MARKER_X >= x[0]) & (MARKER_X <= x[-1])]
        ax.plot(marks, np.interp(marks, x, mean), linestyle="None", marker="o",
                markersize=markersize, color=color)
    ax.set_xlabel(r"$\beta\phi$", fontsize=label_font)
    ax.set_ylabel(r"$\langle N\rangle$", fontsize=label_font)
    ax.tick_params(axis="both", which="major", labelsize=tick_font)
    if combined:
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6, min_n_ticks=5))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6, min_n_ticks=5))
    else:
        ax.legend(frameon=False, fontsize=14)


def save_formats(fig, stem, dpi, padding, transparent=False):
    for extension in ("pdf", "svg", "png"):
        fig.savefig(stem.with_suffix(f".{extension}"), dpi=dpi, bbox_inches="tight",
                    pad_inches=padding, transparent=transparent)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parents[1] / "Data" / "inner_outer_water_occupancy")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    results = {ligand: calculate_summary(args.data_dir / ligand) for ligand in LIGANDS}
    print("Verified all six summaries: three replicas per ligand; sample SD (ddof=1).")
    if args.check_only:
        return
    output = args.output_dir or Path(__file__).resolve().parents[1] / "plots" / "inner_outer_water_occupancy"
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path"})
    for ligand, curves in results.items():
        fig, ax = plt.subplots(figsize=(6, 5), dpi=220)
        fig.subplots_adjust(left=0.24, right=0.98, bottom=0.22, top=0.98)
        draw_panel(ax, curves)
        save_formats(fig, output / f"{ligand}_mean_std", dpi=600, padding=0.02)
        plt.close(fig)
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), dpi=160)
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.10, top=0.94, wspace=0.28, hspace=0.30)
    for ax, curves in zip(axes.flat, results.values()):
        draw_panel(ax, curves, combined=True)
    save_formats(fig, output / "figure7_panels", dpi=300, padding=0.04)
    plt.close(fig)
    legend = plt.figure(figsize=(9, 1.1))
    handles = [Line2D([0], [0], color=c, linewidth=3, marker="o", markersize=9, label=l)
               for c, l in zip(COLORS, LABELS)]
    legend.legend(handles=handles, loc="center", ncol=2, frameon=False, fontsize=22,
                  handlelength=2.4, handletextpad=0.7, columnspacing=2.5)
    save_formats(legend, output / "figure7_legend", dpi=300, padding=0.04, transparent=True)
    plt.close(legend)
    print(f"Saved PDF, SVG, and PNG plots in {output}")


if __name__ == "__main__":
    main()
