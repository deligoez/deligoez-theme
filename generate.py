#!/usr/bin/env python3
"""
Deligoez Theme Generator — reads palette.json and regenerates all editor themes.

Usage: python3 generate.py
"""

from generators.helpers import load_palette
from generators import generate_all


def main():
    palette = load_palette()
    print("Generating themes from palette.json...")
    generate_all(palette)
    print("Done!")


if __name__ == "__main__":
    main()
