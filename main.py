"""Render one image summarizing 24 November 2026 world news.

Reads headlines.json shipped in this repo (no network access) and draws
a single poster PNG, writing it as entry.png under the output directory
(MAKEFUN_OUTPUT_DIR, standing in for /output outside the grader).
"""
import json
import os
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
DATE = "24 November 2026"


def draw() -> Path:
    data = json.loads((ROOT / "headlines.json").read_text(encoding="utf-8"))
    n = len(data["stories"])
    fig, axes = plt.subplots(1, n, figsize=(10.24, 5.76), dpi=100)
    fig.suptitle(f"The World in One Image - {DATE}", fontsize=17, fontweight="bold", y=0.96)
    fig.text(0.5, 0.885, "\n".join(textwrap.wrap(data["summary_line"], 100)),
             ha="center", fontsize=8.5, color="#444444")
    fig.text(0.5, 0.03, "make.fun news-image bounty - @amber-stork-25-6770",
             ha="center", fontsize=7, color="#666666")
    ax_out = axes if n > 1 else [axes]
    for ax, story in zip(ax_out, data["stories"]):
        ax.set_facecolor(story["color"])
        ax.axhspan(-0.5, -0.42, color="#00000030", zorder=0)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor("#101820")
            spine.set_linewidth(2)
        tag_y = 0.90
        head_y = 0.58 if len(story["headline"]) <= 60 else 0.62
        ctx_y = 0.16
        ax.text(0.5, tag_y, story["tag"], ha="center", fontsize=8.5,
                fontweight="bold", color="white", transform=ax.transAxes)
        ax.text(0.5, head_y, "\n".join(textwrap.wrap(story["headline"], 16)),
                ha="center", va="center", fontsize=8, color="white",
                transform=ax.transAxes)
        ax.text(0.5, ctx_y, "\n".join(textwrap.wrap(story["context"], 20)),
                ha="center", fontsize=7, color="#f0f0f0",
                transform=ax.transAxes)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    fig.savefig(out, dpi=100, facecolor="#101820")
    plt.close(fig)
    return out


if __name__ == "__main__":
    print(f"WROTE {draw()}")
