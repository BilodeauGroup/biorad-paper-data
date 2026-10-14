"""Reproduce numerical water-occupancy and free-energy panels for four radii."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.lines import Line2D
from _common import DATA, LIGANDS, COLORS, label, read_csv, values, style, output_dir, save, cli

DATASET = "probe_radius_dependence"
RADII = (20, 12, 8, 6)
MARKER_X = np.array([0, .4, .8, 1.2, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8,
                     3, 3.2, 3.4, 3.8, 4.2, 4.6, 5, 5.4, 5.8, 6.2, 6.6,
                     7, 7.4, 7.8, 8.2, 8.6, 8.8, 9.2, 9.6, 10, 10.4, 10.8,
                     11.2, 11.6, 12])
MARKER_COUNTS = {ligand: (36 if ligand == "CB442" else 35) for ligand in LIGANDS}


def draw_std_band(ax, x, mean, std, color):
    """Fade only opacity at band ends; keep the exact mean +/- SD envelope.

    A single opacity gradient is clipped to each finite SD envelope.
    The clipping boundary, curves, markers, and text remain vector in SVG.
    """
    from matplotlib.colors import to_rgba
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path as MplPath
    valid = np.isfinite(x) & np.isfinite(mean) & np.isfinite(std)
    indices = np.flatnonzero(valid)
    segments = np.split(indices, np.flatnonzero(np.diff(indices) > 1) + 1)
    bands = []
    for segment in segments:
        if len(segment) < 2:
            continue
        sx, sm, ss = x[segment], mean[segment], std[segment]
        lo, hi = sm - ss, sm + ss
        envelope = np.vstack([np.column_stack([sx, lo]),
                              np.column_stack([sx[::-1], hi[::-1]]),
                              [sx[0], lo[0]]])
        codes = np.full(len(envelope), MplPath.LINETO, dtype=np.uint8)
        codes[0], codes[-1] = MplPath.MOVETO, MplPath.CLOSEPOLY
        clip = PathPatch(MplPath(envelope, codes), transform=ax.transData)
        fade_width = min(0.025 * (x[-1] - x[0]),
                         0.25 * (sx[-1] - sx[0]))
        # A constant RGB hue with variable alpha avoids seams and repeated-blend
        # color rounding. Only the opacity texture is raster; its clip is vector.
        gx = np.linspace(sx[0], sx[-1], 4096)
        if fade_width > 0:
            t = np.clip(np.minimum(gx - sx[0], sx[-1] - gx) / fade_width, 0, 1)
            opacity = 0.5 * t * t * (3 - 2 * t)
        else:
            opacity = np.full(gx.shape, 0.5)
        rgba = np.tile(to_rgba(color), (2, len(gx), 1))
        rgba[:, :, 3] = opacity
        band = ax.imshow(rgba, origin="lower", interpolation="bilinear", aspect="auto",
                         extent=(sx[0], sx[-1], lo.min(), hi.max()), zorder=1)
        band.set_clip_path(clip)
        # Match fill_between's regular axis margins, without imshow's sticky edges.
        band.sticky_edges.x.clear()
        band.sticky_edges.y.clear()
        ax.update_datalim(envelope)
        ax.autoscale_view()
        bands.append(band)
    return bands



def free_energy_marker_positions(folder, ligand, x, inferred):
    """Recover the original R=6 Å display markers from source x coordinates."""
    candidates_by_replica = []
    for replicate in range(1, 4):
        directory = folder / ligand / f"replicate_{replicate:02d}"
        occupancy = read_csv(directory / "occupancy.csv")
        n0 = next(float(row["mean_water_count"]) for row in occupancy if float(row["beta_phi"]) == 0)
        free_energy = read_csv(directory / "free_energy.csv")
        raw_x, raw_y = values(free_energy, "mean_water_count") / n0, values(free_energy, "beta_free_energy")
        order = np.argsort(raw_x)
        raw_x, raw_y = raw_x[order], raw_y[order]
        first, last = np.flatnonzero(np.isfinite(raw_y))[[0, -1]]
        raw_x = raw_x[first:last + 1]
        candidates_by_replica.append(raw_x)
    def supported(coords):
        coords = coords[(coords >= x[0]) & (coords <= x[-1])]
        if ligand == "Nuvia_cPrime":
            return np.unique(np.r_[x[0], coords, x[-1]])
        return coords[np.interp(coords, x, inferred.astype(float)) == 0]
    candidates = supported(candidates_by_replica[0])
    count = MARKER_COUNTS[ligand]
    if len(candidates) < count:
        candidates = supported(np.unique(np.concatenate(candidates_by_replica)))
    if len(candidates) < count:
        raise ValueError(f"Insufficient supported marker positions for {ligand}")
    indices = np.rint(np.linspace(0, len(candidates) - 1, count)).astype(int)
    marks = candidates[indices]
    if ligand != "Nuvia_cPrime":
        marks = marks[np.interp(marks, x, inferred.astype(float)) == 0]
    marks[0], marks[-1] = x[0], x[-1]
    return marks


def main(supplied_output_dir=None):
    """Read saved mean curves and SD, preserving original display exceptions."""
    style()
    plt.rcdefaults()
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "path", "pdf.fonttype": 42})
    directory = output_dir(DATASET, supplied_output_dir)
    paths = []
    for radius in RADII:
        folder = DATA / DATASET / f"radius_{radius:02d}_angstrom"
        for kind, xkey, ykey, sdkey in (
            ("occupancy", "beta_phi", "normalized_water_count_mean", "normalized_water_count_sd"),
            ("free_energy", "normalized_water_count", "normalized_beta_free_energy_mean", "normalized_beta_free_energy_sd"),
        ):
            fig, ax = plt.subplots(figsize=(5, 4.3), dpi=200)
            fig.subplots_adjust(left=.24, right=.98, bottom=.22, top=.98)
            for spine in ax.spines.values():
                spine.set_linewidth(2.2)
            for ligand in LIGANDS:
                rows = read_csv(folder / ligand / f"{kind}_summary.csv")
                x, y, sd = (values(rows, key) for key in (xkey, ykey, sdkey))
                inferred = values(rows, "display_interpolation").astype(bool)
                color = COLORS[ligand]
                ax.plot(x, y, color=color, linewidth=2.5)
                displayed_sd = sd.copy()
                if kind == "occupancy" and ligand == "CB441":
                    # Original figure hides only the final shaded interval.
                    # Preserve its contribution to automatic axis limits.
                    valid = np.isfinite(sd)
                    ax.update_datalim(np.column_stack([np.r_[x[valid], x[valid]],
                                      np.r_[(y-sd)[valid], (y+sd)[valid]]]))
                    interior = MARKER_X[(MARKER_X >= x[0]) & (MARKER_X < x[-1])]
                    if len(interior):
                        displayed_sd[x > interior[-1]] = np.nan
                if radius == 6 and kind == "free_energy":
                    draw_std_band(ax, x, y, displayed_sd, color)
                else:
                    ax.fill_between(x, y - displayed_sd, y + displayed_sd, color=color, alpha=.5, linewidth=0)
                if kind == "occupancy":
                    mx = MARKER_X[(MARKER_X >= x[0]) & (MARKER_X <= x[-1])].copy()
                    if radius == 6:
                        mx = mx[np.interp(mx, x, inferred.astype(float)) == 0]
                    mx[0], mx[-1] = x[0], x[-1]
                    my = np.interp(mx, x, y)
                elif radius == 6:
                    mx = free_energy_marker_positions(folder, ligand, x, inferred)
                    my = np.interp(mx, x, y)
                else:
                    indices = list(range(0, len(x), 2))
                    if len(x) - 1 not in indices:
                        indices.append(len(x) - 1)
                    mx, my = x[indices], y[indices]
                ax.plot(mx, my, linestyle="None", marker="o", markersize=4.5, color=color)
            if kind == "occupancy":
                ax.set_xlabel(r"$\beta\phi$", fontsize=22)
                ax.set_ylabel(r"$\langle N\rangle/N_0$", fontsize=22)
                ax.xaxis.set_major_locator(MultipleLocator(2))
            else:
                ax.set_xlabel(r"$\langle N\rangle/N_0$", fontsize=22)
                ax.set_ylabel(r"$\beta\,F(\langle N\rangle)/N_0$", fontsize=22)
                ax.set_xlim(-.03, 1.05)
                ax.xaxis.set_major_locator(MultipleLocator(.2))
                ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
            ax.tick_params(axis="both", which="major", labelsize=18)
            paths.extend(save(fig, directory, f"radius_{radius:02d}_angstrom_{kind}", dpi=600, padding=.02))
    fig = plt.figure(figsize=(18, 1.2))
    handles = [Line2D([0], [0], color=COLORS[ligand], linewidth=3.5, marker="o", markersize=8,
                      label=label(ligand)) for ligand in LIGANDS]
    fig.legend(handles=handles, loc="center", ncol=6, frameon=False, fontsize=18)
    paths.extend(save(fig, directory, "ligand_legend", dpi=600, padding=.02))
    return paths


if __name__ == "__main__":
    cli(main)
