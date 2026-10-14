"""Plot protein-adsorption PMFs and their supplied bootstrap uncertainty bands."""
import numpy as np
import matplotlib.pyplot as plt
from _common import DATA, COLORS, label, read_csv, values, style, output_dir, save, cli

DATASET = "protein_adsorption_pmf"
LIGANDS = ("Nuvia_cPrime", "CB434", "CB442")

def main(supplied_output_dir=None):
    """Retain each PMF's original plotted reference and its one-SD bootstrap band."""
    plt.rcdefaults()
    plt.rcParams.update({"pdf.fonttype": 42, "svg.fonttype": "path", "axes.grid": False})
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    directory = output_dir(DATASET, supplied_output_dir)
    paths = []
    for ligand in LIGANDS:
        rows = read_csv(DATA / DATASET / f"{ligand}.csv")
        x = values(rows, "com_distance_nm")
        pmf = values(rows, "pmf_kj_per_mol")
        sd = values(rows, "bootstrap_sd_kj_per_mol")
        lower = values(rows, "pmf_minus_sd_kj_per_mol")
        upper = values(rows, "pmf_plus_sd_kj_per_mol")
        if not (np.allclose(lower, pmf-sd) and np.allclose(upper, pmf+sd)):
            raise ValueError(f"PMF uncertainty edges disagree with SD for {ligand}")
        # The supplied reference min(PMF)=-41.3 kJ/mol is retained separately for each ligand.
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.axhline(0, color=".5", alpha=.4, linewidth=1, zorder=1.5)
        ax.plot(x, pmf, color="#B0126B", linewidth=3, zorder=3)
        ax.fill_between(x, lower, upper, color="#7B0D4A", alpha=.25, linewidth=0, zorder=2)
        ax.set_xlabel("COM distance (nm)", fontsize=18)
        ax.set_ylabel("ΔG (kJ mol⁻¹)", fontsize=18)
        for spine in ax.spines.values():
            spine.set_linewidth(2.5)
            spine.set_color("black")
        ax.tick_params(axis="both", which="both", direction="out", length=7, width=2,
                       labelsize=16, colors="black")
        ax.set_xlim(2, 7.2)
        ax.set_ylim(-55, 20)
        fig.tight_layout()
        paths += save(fig, directory, f"{ligand}_pmf", dpi=600, bbox_inches=None)
    return paths

if __name__ == "__main__":
    cli(main)
