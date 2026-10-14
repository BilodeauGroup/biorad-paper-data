"""Shared file handling and display settings for the deposited numerical data."""
from pathlib import Path
import argparse
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Data"
LIGANDS = ("CB431", "Nuvia_cPrime", "CB433", "CB441", "CB434", "CB442")
COLORS = dict(zip(LIGANDS, ("#15502b", "#1f8744", "#2b79b1", "#6552a6", "#b0126b", "#d25a0e")))

def label(name):
    return name.replace("_", " ")

def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))

def values(rows, key):
    return np.array([float(row[key]) if row[key].strip() else np.nan for row in rows])

def style():
    """Reset Matplotlib defaults; each script sets its original panel style."""
    plt.rcdefaults()
    plt.rcParams.update({"pdf.fonttype": 42, "svg.fonttype": "path",
                         "savefig.facecolor": "white"})

def output_dir(dataset, supplied=None):
    path = Path(supplied) if supplied is not None else ROOT / "plots" / dataset
    path.mkdir(parents=True, exist_ok=True)
    return path

def save(fig, directory, stem, dpi=300, padding=0.1, bbox_inches="tight"):
    paths = []
    for suffix in ("pdf", "svg", "png"):
        path = Path(directory) / f"{stem}.{suffix}"
        fig.savefig(path, dpi=dpi, bbox_inches=bbox_inches, pad_inches=padding)
        paths.append(path)
    plt.close(fig)
    return paths

def cli(main):
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("--output-dir", type=Path, help="Folder for PDF, SVG, and PNG files")
    args = parser.parse_args()
    paths = main(args.output_dir)
    if paths is not None:
        print(f"Saved {len(paths)} files.")
