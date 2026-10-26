#!/usr/bin/env python3
"""Regenerate previews and local reports without modifying the KiCad design."""

import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "hardware/backplane/HackerfabBackplane"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kicad-cli", default="kicad-cli", help="Path to the KiCad 10 CLI executable")
    args = parser.parse_args()
    cli = shutil.which(args.kicad_cli)
    if not cli:
        parser.error("KiCad CLI not found. Add it to PATH or pass --kicad-cli with its full path.")
    version = subprocess.check_output([cli, "version"], text=True).strip()
    if not version.startswith("10."):
        parser.error(f"Expected KiCad 10; found {version}. Review format compatibility before upgrading.")
    for directory in ("docs/schematics", "docs/images", "build"):
        (ROOT / directory).mkdir(parents=True, exist_ok=True)
    commands = [
        ["sch", "export", "svg", "--output", "docs/schematics/", PROJECT + ".kicad_sch"],
        ["sch", "export", "netlist", "--format", "kicadxml", "--output", "build/backplane.xml", PROJECT + ".kicad_sch"],
        ["sch", "erc", "--format", "json", "--output", "build/erc.json", PROJECT + ".kicad_sch"],
        ["pcb", "drc", "--schematic-parity", "--format", "json", "--output", "build/drc.json", PROJECT + ".kicad_pcb"],
        ["pcb", "render", "--width", "1800", "--height", "1400", "--background", "opaque",
         "--quality", "basic", "--rotate", "0,0,0", "--output", "docs/images/backplane.png", PROJECT + ".kicad_pcb"],
    ]
    for command in commands:
        print("Running:", " ".join(command), flush=True)
        subprocess.run([cli, *command], cwd=ROOT, check=True)
    print(f"Exports complete with KiCad {version}. Review build/erc.json and build/drc.json for findings.")


if __name__ == "__main__":
    main()
