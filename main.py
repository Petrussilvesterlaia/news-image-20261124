#!/usr/bin/env python3
"""Entry program for the 24 November 2026 world-news image.

Writes the poster rendered by draw.py to the output directory.
Standard library only: copies the entry.png shipped in this repo.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    sys.exit(main())
