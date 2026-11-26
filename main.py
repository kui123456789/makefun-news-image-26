#!/usr/bin/env python3
"""Copy entry.png to the output directory.

The entry image is pre-rendered (see entry.png, produced by draw.py).
The grader runs this script in a pinned image with no network and no
third-party packages, so this file must stay stdlib-only: it simply
copies the pre-rendered image next to the script into the output
directory (MAKEFUN_OUTPUT_DIR, default /output).
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print(f"error: entry.png not found next to main.py: {src}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
