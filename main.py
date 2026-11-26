"""Entry point for news-image-20261126.

Runs the front-page drawing in draw.py and writes the finished image
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when set).
Standard library plus Pillow only; no network, fully deterministic.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw import build_image


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img = build_image()
    img.save(path, format="PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
