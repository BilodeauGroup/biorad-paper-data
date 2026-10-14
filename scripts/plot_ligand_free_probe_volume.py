"""Plot ligand-free probe volume at each supplied cylinder radius."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch
from _common import DATA, COLORS, LIGANDS, label, read_csv, values, style, output_dir, save, cli

DATASET = "ligand_free_probe_volume"

def main(supplied_output_dir=None):
    """Reproduce the radius comparison from the deposited ligand-free volumes."""
    plt.rcdefaults()
    plt.rcParams.update({"pdf.fonttype": 42, "svg.fonttype": "path", "axes.grid": False})
    directory = output_dir(DATASET, supplied_output_dir)
    datasets = {ligand: read_csv(DATA / DATASET / f"{ligand}.csv") for ligand in LIGANDS}
    radii = values(datasets[LIGANDS[0]], "cylinder_radius_angstrom")
    volume = np.array([values(datasets[ligand], "ligand_free_volume_nm3") for ligand in LIGANDS])
    for ligand in LIGANDS:
        if not np.array_equal(values(datasets[ligand], "cylinder_radius_angstrom"), radii):
            raise ValueError(f"Inconsistent cylinder radii for {ligand}")
    fig, ax = plt.subplots(figsize=(9.5, 5.5), dpi=220)
    fig.subplots_adjust(left=.13, right=.98, bottom=.20, top=.84)
    for spine in ax.spines.values():
        spine.set_linewidth(2.2)
    centres, width = np.arange(len(LIGANDS)), .82/len(radii)
    white_blend = (.68, .46, .24, 0)
    blend = lambda color, fraction: np.array(to_rgb(color))*(1-fraction)+fraction
    for j, fraction in enumerate(white_blend):
        for i, ligand in enumerate(LIGANDS):
            ax.bar(centres[i]+(j-(len(radii)-1)/2)*width, volume[i, j], width=width*.94,
                   color=blend(COLORS[ligand], fraction), edgecolor="none", linewidth=0, zorder=2)
    ax.set_ylabel(r"Ligand-free volume (nm$^3$)", fontsize=17)
    ax.set_xticks(centres, [label(ligand) for ligand in LIGANDS], rotation=30, ha="center", rotation_mode="anchor")
    ax.tick_params(axis="both", labelsize=16, length=6, width=1.6)
    ax.tick_params(axis="x", pad=26)
    ax.set_xlim(-.58, len(LIGANDS)-.42)
    ax.set_ylim(0, volume.max()*1.16)
    handles = [Patch(facecolor=blend("#555555", fraction), edgecolor="none", label=f"{radius:g} Å")
               for radius, fraction in zip(radii, white_blend)]
    # The manuscript legend shows radius values without the source script's optional title.
    ax.legend(handles=handles, ncol=4, loc="lower center", bbox_to_anchor=(.5, 1.02), frameon=False,
              fontsize=14, handlelength=1.6, columnspacing=1.6)
    return save(fig, directory, "ligand_free_probe_volume", dpi=600, padding=.02)

if __name__ == "__main__":
    cli(main)
