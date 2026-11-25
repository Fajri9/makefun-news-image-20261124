"""Render one image summarizing 24 November 2026 world news.

Reads headlines.json shipped in this repo (no network access) and draws
a single poster PNG to out/news-image-20261124.png.
"""
import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
DATE = "24 November 2026"
OUT = ROOT / "out" / "news-image-20261124.png"


def draw() -> None:
    data = json.loads((ROOT / "headlines.json").read_text(encoding="utf-8"))
    n = len(data["stories"])
    fig, axes = plt.subplots(1, n, figsize=(16, 9))
    fig.suptitle(f"The World in One Image - {DATE}", fontsize=26, fontweight="bold", y=0.97)
    fig.text(0.5, 0.91, "\n".join(textwrap.wrap(data["summary_line"], 110)),
             ha="center", fontsize=13, color="#444444")
    fig.text(0.5, 0.03, "make.fun news-image bounty - @amber-stork-25-6770",
             ha="center", fontsize=10, color="#666666")
    ax_out = axes if n > 1 else [axes]
    for ax, story in zip(ax_out, data["stories"]):
        ax.set_facecolor(story["color"])
        ax.set_xticks([])
        ax.set_yticks([])
        tag_y = 0.90
        head_y = 0.58 if len(story["headline"]) <= 60 else 0.62
        ctx_y = 0.16
        ax.text(0.5, tag_y, story["tag"], ha="center", fontsize=13,
                fontweight="bold", color="white", transform=ax.transAxes)
        ax.text(0.5, head_y, "\n".join(textwrap.wrap(story["headline"], 16)),
                ha="center", va="center", fontsize=12, color="white",
                transform=ax.transAxes)
        ax.text(0.5, ctx_y, "\n".join(textwrap.wrap(story["context"], 26)),
                ha="center", fontsize=11, color="#f0f0f0",
                transform=ax.transAxes)
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=120, facecolor="#101820")
    plt.close(fig)


if __name__ == "__main__":
    draw()
    print(f"WROTE {OUT}")
