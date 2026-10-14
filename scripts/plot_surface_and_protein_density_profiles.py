"""Plot the deposited surface and bound-protein density profiles."""
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import Polygon
from matplotlib.font_manager import fontManager, FontProperties
from pathlib import Path
from _common import DATA, label, read_csv, values, style, output_dir, save, cli

DATASET = "surface_and_protein_density_profiles"
# Original manuscript marker positions and displayed labels; no new threshold is applied.
ANNOTATIONS = {
    "Nuvia_cPrime": (20.80903434753418, 28.412336349487305, "7.6 Å"),
    "CB434": (21.00843048095703, 30.12529754638672, "9.1 Å"),
    "CB442": (19.533910751342773, 30.69614601135254, "11.1 Å"),
}

# Fixed annotation geometry from the original manuscript panels, in axis fractions.
GRAPHICS = {'Nuvia_cPrime': {'polygons': (((0.3243773607543272, 0.9071709282062153),
                                (0.25715173316593354, 0.9071707855378139),
                                (0.25715173316593354, 0.8976347939263376),
                                (0.3243774036040938, 0.8976349306502222)),
                               ((0.3209404666768077, 0.8880989152606789),
                                (0.3415619168414579, 0.9024029680675774),
                                (0.3209404666768077, 0.9167069019841415)),
                               ((0.2605887129429862, 0.916706783093807),
                                (0.23996726277833594, 0.9024027535347245),
                                (0.2605887129429862, 0.8880987963703444))),
                  'text': (('7.6 ', 0.25082753611699693, 0.9321255516763698),
                           ('Å', 0.31195272813751346, 0.9321255516763698)),
                  'font_size_over_panel_width': 0.03942178524982485},
 'CB434': {'polygons': (((0.3432571068892862, 0.9231661403227054),
                         (0.2627248014604703, 0.9231659916379705),
                         (0.2627248014604703, 0.9136253858368869),
                         (0.3432571068892862, 0.9136255345216218)),
                        ((0.3398201670395037, 0.9040849049309806),
                         (0.36044163473898666, 0.9183958701328052),
                         (0.3398201670395037, 0.932706716386842)),
                        ((0.2661617841600559, 0.9327065974390542),
                         (0.24554031646057292, 0.9183956554962799),
                         (0.2661617841600559, 0.9040847859831928))),
           'text': (('9.1 ', 0.2608844024211086, 0.943969644524536),
                    ('Å', 0.32201393139790335, 0.943969644524536)),
           'font_size_over_panel_width': 0.039421818770959696},
 'CB442': {'polygons': (((0.3502286412899153, 0.9178134958160116),
                         (0.24387037393759256, 0.9178133352364979),
                         (0.24387037393759256, 0.9082727294354144),
                         (0.3502286841397183, 0.908272890014928)),
                        ((0.3467917442899358, 0.8987322544768974),
                         (0.3674132119894188, 0.913043219678722),
                         (0.3467917442899358, 0.9273540659327588)),
                        ((0.24730735663717807, 0.927353946984971),
                         (0.22668588893769506, 0.9130430050421967),
                         (0.24730735663717807, 0.8987321355291095))),
           'text': (('11.1 ', 0.24203468837656217, 0.9398064719491379),
                    ('Å', 0.3240320714201584, 0.9398064719491379)),
           'font_size_over_panel_width': 0.03942181877095969}}

def main(supplied_output_dir=None):
    """Draw original density profiles, normalization, and penetration annotations."""
    plt.rcdefaults()
    plt.rcParams.update({"pdf.fonttype": 42, "svg.fonttype": "path", "axes.grid": False})
    plt.rcParams.update({"font.size": 10, "axes.linewidth": .8, "font.family": "DejaVu Sans"})
    directory = output_dir(DATASET, supplied_output_dir)
    paths = []
    # Aptos is the font used for labels added during manuscript figure assembly.
    regular_aptos = [f.fname for f in fontManager.ttflist if f.name == "Aptos" and "display" not in Path(f.fname).stem.casefold() and f.style == "normal" and f.weight in (400, "normal")]
    if not regular_aptos:
        raise RuntimeError("Install regular Aptos to reproduce the manuscript density annotations, then rebuild the Matplotlib font cache.")
    annotation_font = FontProperties(fname=regular_aptos[0])
    for ligand, (left, right, text) in ANNOTATIONS.items():
        rows = read_csv(DATA / DATASET / f"{ligand}.csv")
        z = values(rows, "z_angstrom")
        # The CSV already retains surface smoothing and the original, distinct normalization areas.
        surface = values(rows, "surface_density_atoms_per_angstrom3")
        protein = values(rows, "protein_density_atoms_per_angstrom3")
        fig, ax = plt.subplots(figsize=(8, 5))
        other = ax.twinx()
        a, = ax.plot(z, surface, color="tab:blue", linewidth=2.5, label="Surface")
        b, = other.plot(z, protein, color="tab:red", linewidth=2.5, label="Protein")
        ax.set_xlabel("z (Å)", fontsize=19)
        ax.set_ylabel("Surface density (atoms/Å³)", fontsize=19, color="tab:blue")
        other.set_ylabel("Protein density (atoms/Å³)", fontsize=19, color="tab:red")
        ax.tick_params(axis="x", labelsize=17)
        ax.tick_params(axis="y", labelsize=17, labelcolor="tab:blue")
        other.tick_params(axis="y", labelsize=17, labelcolor="tab:red")
        ax.set_xlim(2, 80)
        ax.xaxis.set_major_locator(MultipleLocator(20))
        for location in (left, right):
            ax.axvline(location, color="black", linestyle="--")
        ax.legend([a, b], ["Surface", "Protein"], fontsize=15)
        fig.tight_layout()
        fig.canvas.draw()
        graphics = GRAPHICS[ligand]
        for points in graphics["polygons"]:
            ax.add_patch(Polygon(points, closed=True, transform=ax.transAxes,
                                 facecolor="black", edgecolor="none", zorder=5))
        size = graphics["font_size_over_panel_width"]*ax.get_window_extent().width/fig.dpi*72
        for chunk, xpos, ypos in graphics["text"]:
            ax.text(xpos, ypos, chunk, transform=ax.transAxes, ha="left", va="baseline",
                    fontsize=size, fontproperties=annotation_font, zorder=5)
        paths += save(fig, directory, f"{ligand}_density_profiles", dpi=600, bbox_inches=None)
    return paths

if __name__ == "__main__":
    cli(main)
