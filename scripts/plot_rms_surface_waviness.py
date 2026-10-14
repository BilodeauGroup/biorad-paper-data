"""Plot the supplied RMS boundary waviness for each surface."""
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.font_manager import findfont
from _common import DATA, LIGANDS, COLORS, label, read_csv, style, output_dir, save, cli

DATASET = "rms_surface_waviness"

def main(supplied_output_dir=None):
    """Plot the independently calculated RMS waviness values in angstroms."""
    plt.rcdefaults()
    plt.rcParams.update({"pdf.fonttype": 42, "svg.fonttype": "path", "axes.grid": False})
    try:
        findfont("Arial", fallback_to_default=False)
    except ValueError as error:
        raise RuntimeError("Install Arial to reproduce the manuscript waviness panel, then rebuild the Matplotlib font cache.") from error
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Arial"],
                         "mathtext.fontset": "custom", "mathtext.rm": "sans", "mathtext.it": "sans:italic", "mathtext.bf": "sans:bold"})
    rows = read_csv(DATA / DATASET / "rms_waviness.csv")
    lookup = {row["ligand"].replace(" ", "_"): float(row["rms_waviness_angstrom"]) for row in rows}
    directory = output_dir(DATASET, supplied_output_dir)
    fig, ax = plt.subplots(figsize=(5.4, 4.9))
    ax.bar(range(len(LIGANDS)), [lookup[x] for x in LIGANDS], color=[COLORS[x] for x in LIGANDS], width=.55, linewidth=0)
    ax.set_ylabel(r"$\mathrm{W}_{\mathrm{q}}$ (Å)", fontsize=20, labelpad=8)
    ax.set_xticks(range(len(LIGANDS)), [label(x) for x in LIGANDS], rotation=45, ha="center", fontsize=16)
    ax.tick_params(axis="y", labelsize=16, width=1.2, length=5)
    ax.tick_params(axis="x", width=1.2, length=5)
    ax.yaxis.set_major_locator(MultipleLocator(.2))
    ax.set_ylim(0, 1.52)
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)
    return save(fig, directory, "rms_surface_waviness", dpi=600, padding=.02)

if __name__ == "__main__":
    cli(main)
