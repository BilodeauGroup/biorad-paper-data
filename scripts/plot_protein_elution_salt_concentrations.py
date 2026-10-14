"""Reproduce the manuscript's protein elution plots from the deposited CSVs."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator
from _common import DATA, LIGANDS, label, read_csv, output_dir, save, cli

DATASET = "protein_elution_salt_concentrations"
PROTEIN_FILES = (("myoglobin", "Myoglobin"), ("cytochrome_c", "Cytochrome-c"),
                 ("hemoglobin", "Hemoglobin"),
                 ("alpha_chymotrypsinogen", "a-chymotrypsinogen"),
                 ("alpha_chymotrypsin", "a-chymotrypsin"),
                 ("lysozyme", "Lysozyme"), ("lactoferrin", "Lactoferrin"))
surfaces = [label(ligand) for ligand in LIGANDS]
proteins = [name for _, name in PROTEIN_FILES]
CB431_INDEX = 0

def load_concentrations():
    """Keep nonbinding entries separate from measured elution concentrations."""
    concentrations, statuses = {}, {}
    for protein, _ in PROTEIN_FILES:
        rows = read_csv(DATA / DATASET / f"{protein}.csv")
        by_ligand = {r["ligand"].replace(" ", "_"): r for r in rows}
        concentrations[protein] = []
        statuses[protein] = []
        for ligand in LIGANDS:
            row = by_ligand[ligand]
            status = row["binding_status"]
            raw = row["elution_nacl_millimolar"].strip()
            if status == "did_not_bind":
                if raw:
                    raise ValueError(f"Nonbinding entry has a concentration: {protein}, {ligand}")
                value = np.nan
            elif status == "reported_concentration":
                value = float(raw)
                if not np.isfinite(value) or value < 0:
                    raise ValueError(f"Invalid concentration: {protein}, {ligand}")
            else:
                raise ValueError(f"Unknown binding status: {status}")
            concentrations[protein].append(value)
            statuses[protein].append(status)
        concentrations[protein] = np.array(concentrations[protein])
    return concentrations, statuses


# DISPLAY NAMES (legend) - use Greek alpha (α)
display_name = {
    "a-chymotrypsin": "α-chymotrypsin",
    "a-chymotrypsinogen": "α-chymotrypsinogen",
    "a-lactalbumin": "α-lactalbumin",
    "bsa": "BSA",
    "cytochrome-c": "cytochrome-c",
    "hemoglobin": "hemoglobin",
    "lactoferrin": "lactoferrin",
    "lysozyme": "lysozyme",
    "myoglobin": "myoglobin",
    "ovalbumin": "ovalbumin",
}

YLABEL_TEXT = "Elution Salt Concentration\n(mM NaCl)"

LABEL_FS = 16
TICK_FS = 15
LEGEND_FS = 15
FIG_DPI = 150

FIGSIZE = (10.0, 4.2)
FRAME_LW = 2.0
TICK_LEN = 5
TICK_W = 1.4

COLORS = ["#7A6F66", "#15502B", "#2B79B1", "#6552A6", "#B0126B", "#1F8744", "#D25A0E"]

TOP_YLIM = (0, 450)
BOT_YLIM = (0, 1598)

TOP_TICK = 100
BOT_TICK = 400

# CB431 marker settings
CROSS_MARKER = "x"
CROSS_SIZE = 45
CROSS_LINEWIDTH = 2.2
CROSS_COLOR = "black"
CB431_CROSS_Y_TOP = 22
CB431_CROSS_Y_BOT = 60

# TRUNCATION STAR settings (low-range figure)
STAR_MARKER = "*"
STAR_SIZE = 120
STAR_COLOR = "black"
STAR_LINEWIDTH = 0.0
STAR_Y_PAD = 15


def style_ax(ax):
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle="-", linewidth=0.6, alpha=0.22, zorder=0)
    ax.tick_params(axis="both", which="major", labelsize=TICK_FS, length=TICK_LEN, width=TICK_W)


def raise_frame(ax, lw=2.0):
    for sp in ax.spines.values():
        if sp.get_visible():
            sp.set_linewidth(lw)
            sp.set_zorder(20)


def add_inside_ylabel(ax):
    # Keep the manuscript's two-line label clear of the tick labels.
    ax.text(-0.16, 0.5, YLABEL_TEXT, transform=ax.transAxes,
            rotation=90, va="center", ha="center", multialignment="center",
            fontsize=LABEL_FS, zorder=30)


def plot_panel(y_mode="top"):
    n_surfaces = len(surfaces)
    n_proteins = len(proteins)

    x = np.arange(n_surfaces)
    group_width = 0.84
    bar_width = group_width / n_proteins
    bw = bar_width

    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=FIG_DPI)
    style_ax(ax)

    for side in ["top", "bottom", "left", "right"]:
        ax.spines[side].set_linewidth(FRAME_LW)
    raise_frame(ax, FRAME_LW)

    if y_mode == "top":
        ylim = TOP_YLIM
        tick = TOP_TICK
        cap = TOP_YLIM[1]
        star_y = max(TOP_YLIM[0], cap - STAR_Y_PAD)
    else:
        ylim = BOT_YLIM
        tick = BOT_TICK
        cap = None
        star_y = None

    for i, p in enumerate(proteins):
        y = np.array(data[p], dtype=float)
        color = COLORS[i % len(COLORS)]
        x_pos = x - group_width / 2 + (i + 0.5) * bar_width
        mask = np.arange(n_surfaces) != CB431_INDEX

        y_plot = np.minimum(y, cap) if y_mode == "top" else y

        ax.bar(
            x_pos[mask], y_plot[mask],
            width=bw,
            color=color,
            edgecolor="none",
            linewidth=0,
            antialiased=False,
            zorder=2,
            label=display_name.get(p, p),
        )

        if y_mode == "top":
            truncated_idx = np.where((y > cap) & mask)[0]
            if truncated_idx.size > 0:
                ax.scatter(
                    x_pos[truncated_idx],
                    np.full(truncated_idx.size, star_y),
                    marker=STAR_MARKER,
                    s=STAR_SIZE,
                    color=STAR_COLOR,
                    linewidths=STAR_LINEWIDTH,
                    zorder=9,
                    clip_on=False,
                )

    cross_y = CB431_CROSS_Y_TOP if y_mode == "top" else CB431_CROSS_Y_BOT
    for index, protein in enumerate(proteins):
        nonbinding = np.array([status == "did_not_bind" for status in statuses[protein]])
        positions = x - group_width / 2 + (index + 0.5) * bar_width
        ax.scatter(positions[nonbinding], np.full(nonbinding.sum(), cross_y),
                   marker=CROSS_MARKER, s=CROSS_SIZE, linewidths=CROSS_LINEWIDTH,
                   color=CROSS_COLOR, zorder=8, clip_on=False)

    # axes / ticks
    ax.set_ylim(ylim)
    ax.yaxis.set_major_locator(MultipleLocator(tick))
    ax.set_xticks(x)
    ax.set_xticklabels(surfaces, rotation=45, ha="center")
    ax.set_xlim(-0.55, n_surfaces - 0.45)

    add_inside_ylabel(ax)

    # annotations
    ax.scatter(
        [0.02], [0.915],
        transform=ax.transAxes,
        marker=CROSS_MARKER,
        s=45,
        linewidths=2.0,
        color=CROSS_COLOR,
        zorder=10,
        clip_on=False,
    )
    ax.text(
        0.045, 0.915,
        "did not bind",
        transform=ax.transAxes,
        ha="left",
        va="center",
        fontsize=15,
    )

    if y_mode == "top":
        ax.scatter(
            [0.02], [0.82],
            transform=ax.transAxes,
            marker=STAR_MARKER,
            s=STAR_SIZE,
            color=STAR_COLOR,
            linewidths=STAR_LINEWIDTH,
            zorder=10,
            clip_on=False,
        )
        ax.text(
            0.045, 0.82,
            "continues",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=15,
        )

        #legend (proteins only)
        handles, labels = ax.get_legend_handles_labels()
        legend_handles = [Line2D([0], [0], color=COLORS[i], lw=8, label=labels[i]) for i in range(len(labels))]
        ax.legend(
            handles=legend_handles,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.35),
            ncol=4,
            frameon=False,
            fontsize=LEGEND_FS,
            handlelength=1.6,
            columnspacing=1.0,
        )

    # margins (now mostly for aesthetics)
    fig.subplots_adjust(top=0.78, left=0.10, right=0.90, bottom=0.22)

    return fig, ax


def main(supplied_output_dir=None):
    """Draw the full and expanded manuscript panels with nonbinding crosses."""
    global data, statuses
    plt.rcdefaults()
    mpl.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    concentrations, saved_statuses = load_concentrations()
    # Nonbinding rows have no numerical concentration. The original bar routine
    # uses zero-height placeholders; crosses are drawn from binding_status.
    data = {name: np.nan_to_num(concentrations[filename], nan=0.0)
            for filename, name in PROTEIN_FILES}
    statuses = {name: saved_statuses[filename] for filename, name in PROTEIN_FILES}
    paths = []
    for mode, suffix in (("bot", "full_range"), ("top", "low_range")):
        fig, _ = plot_panel(mode)
        paths.extend(save(fig, directory, f"{DATASET}_{suffix}", dpi=600, padding=0.06))
    return paths


if __name__ == "__main__":
    cli(main)
