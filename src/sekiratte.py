#!/usr/bin/env python3
"""
Sekiro Palette Replacement Tool
Replaces Catppuccin Mocha colors with Sekiro palette
"""

import os
import re
import argparse
from pathlib import Path

# Catppuccin Mocha to Sekiro palette mapping
COLOR_MAPPING = {
    # Base colors
    "#1e1e2e": "#231e1c",  # base
    "#181825": "#1a1614",  # mantle
    "#11111b": "#0f0d0c",  # crust
    # Text & UI
    "#cdd6f4": "#e3d8c9",  # text
    "#bac2de": "#c5b7a3",  # subtext1
    "#a6adc8": "#a09585",  # subtext0
    "#9399b2": "#7a6e64",  # overlay2
    "#7f849c": "#5a5149",  # overlay1
    "#6c7086": "#3a3530",  # overlay0
    # Surfaces
    "#585b70": "#402f28",  # surface2
    "#45475a": "#352c26",  # surface1
    "#313244": "#2a231e",  # surface0
    # Accents
    "#f38ba8": "#9a2a2a",  # red
    "#eba0ac": "#6d1e1e",  # maroon
    "#a6e3a1": "#5c7c46",  # green
    "#fab387": "#d4875d",  # peach
    "#89b4fa": "#3a5a7a",  # blue
    "#b4befe": "#7a6a9a",  # lavender
    "#f9e2af": "#d4af37",  # yellow
    "#f5e0dc": "#e7c8a9",  # rosewater
    # Special tones
    "#f2cdcd": "#c96d6d",  # flamingo
    "#f5c2e7": "#b26888",  # pink
    "#cba6f7": "#8a6a9a",  # mauve
    "#94e2d5": "#4a8a8a",  # teal
    "#89dceb": "#6a9aaa",  # sky
}

# Additional mappings for CSS variable formats
VAR_MAPPING = {
    "var\\(--ctp-base\\)": "var(--base)",
    "var\\(--ctp-mantle\\)": "var(--mantle)",
    "var\\(--ctp-crust\\)": "var(--crust)",
    "var\\(--ctp-text\\)": "var(--text)",
    "var\\(--ctp-subtext1\\)": "var(--subtext1)",
    "var\\(--ctp-subtext0\\)": "var(--subtext0)",
    "var\\(--ctp-overlay2\\)": "var(--overlay2)",
    "var\\(--ctp-overlay1\\)": "var(--overlay1)",
    "var\\(--ctp-overlay0\\)": "var(--overlay0)",
    "var\\(--ctp-surface2\\)": "var(--surface2)",
    "var\\(--ctp-surface1\\)": "var(--surface1)",
    "var\\(--ctp-surface0\\)": "var(--surface0)",
    "var\\(--ctp-red\\)": "var(--red)",
    "var\\(--ctp-maroon\\)": "var(--maroon)",
    "var\\(--ctp-green\\)": "var(--green)",
    "var\\(--ctp-peach\\)": "var(--peach)",
    "var\\(--ctp-blue\\)": "var(--blue)",
    "var\\(--ctp-lavender\\)": "var(--lavender)",
    "var\\(--ctp-yellow\\)": "var(--yellow)",
    "var\\(--ctp-rosewater\\)": "var(--rosewater)",
    "var\\(--ctp-flamingo\\)": "var(--flamingo)",
    "var\\(--ctp-pink\\)": "var(--pink)",
    "var\\(--ctp-mauve\\)": "var(--mauve)",
    "var\\(--ctp-teal\\)": "var(--teal)",
    "var\\(--ctp-sky\\)": "var(--sky)",
}


def replace_colors_in_file(file_path):
    """Replace colors in a single file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Replace hex colors
        for mocha, sekiro in COLOR_MAPPING.items():
            # Case-insensitive replacement
            content = re.sub(re.escape(mocha), sekiro, content, flags=re.IGNORECASE)

        # Replace CSS variables
        for mocha_var, sekiro_var in VAR_MAPPING.items():
            content = re.sub(mocha_var, sekiro_var, content)

        # Replace palette names
        content = content.replace("Catppuccin Mocha", "Sekiro Palette")
        content = content.replace("Catppuccin-Mocha", "Sekiro-Palette")
        content = content.replace("ctp-mocha", "sekiro")

        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  Error processing {file_path}: {str(e)}")
        return False


def process_directory(directory):
    """Process all files in a directory recursively"""
    changed_count = 0
    total_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("."):
                continue  # Skip hidden files

            file_path = os.path.join(root, file)
            total_files += 1

            if file_path.endswith(
                (
                    ".css",
                    ".scss",
                    ".sass",
                    ".less",
                    ".html",
                    ".js",
                    ".ts",
                    ".jsx",
                    ".tsx",
                )
            ):
                print(f"Processing: {file_path}")
                if replace_colors_in_file(file_path):
                    changed_count += 1

    return changed_count, total_files


def main():
    parser = argparse.ArgumentParser(
        description="Replace Catppuccin Mocha colors with Sekiro palette"
    )
    parser.add_argument("directory", help="Directory to process")
    args = parser.parse_args()

    target_dir = Path(args.directory)
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: {target_dir} is not a valid directory")
        return

    print(f"Starting Sekiro palette replacement in: {target_dir}")
    changed, total = process_directory(target_dir)

    print("\n" + "=" * 50)
    print(f"Processing complete!")
    print(f"Total files scanned: {total}")
    print(f"Files modified: {changed}")
    print("=" * 50)
    print("Note: This script replaces color values but doesn't rename variables.")
    print("You may need to manually update variable names in some files.")


if __name__ == "__main__":
    main()
