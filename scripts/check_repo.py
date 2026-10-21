#!/usr/bin/env python3
"""Check local KiCad dependencies and documentation links; no third-party packages."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "hardware/backplane"
LIBRARIES = ROOT / "hardware/libraries"
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


for name in ("HackerfabBackplane.kicad_pro", "HackerfabBackplane.kicad_sch",
             "HackerfabBackplane.kicad_pcb", "fp-lib-table", "sym-lib-table"):
    require((BOARD / name).is_file(), f"Missing project file: {name}")

symbols = {}
for path in sorted(LIBRARIES.glob("*.kicad_sym")):
    symbols[path.stem] = set(re.findall(r'^\t\(symbol "([^"]+)"',
                                      path.read_text(encoding="utf-8"), re.M))
require(bool(symbols), "No custom symbol libraries found")

for kind, extension in (("fp", ".pretty"), ("sym", ".kicad_sym")):
    path = BOARD / f"{kind}-lib-table"
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    entries = re.findall(r'\(lib\s+\(name "([^"]+)"\).*?\(uri "([^"]+)"\)', text, re.S)
    names = [name for name, _ in entries]
    require(len(names) == len(set(names)), f"Duplicate library name in {path.name}")
    expected = {p.stem for p in LIBRARIES.glob("*" + extension)}
    require(set(names) == expected, f"Library table does not match bundled libraries: {path.name}")
    for name, uri in entries:
        require(uri == f"${{KIPRJMOD}}/../libraries/{name}{extension}",
                f"Nonportable or unexpected library path: {name}")
        target = Path(uri.replace("${KIPRJMOD}", str(BOARD))).resolve()
        require(target.is_relative_to(ROOT) and target.exists(),
                f"Missing or external library target: {name}")

design_files = [p for p in (ROOT / "hardware").rglob("*") if p.is_file()
                and p.suffix in {".kicad_sch", ".kicad_pcb", ".kicad_sym", ".kicad_mod", ".kicad_pro"}]
for path in design_files:
    text = path.read_text(encoding="utf-8")
    label = path.relative_to(ROOT).as_posix()
    require(not re.search(r'"(?:[A-Za-z]:[/\\]|/(?:Users|home)/)', text),
            f"Machine-specific path in {label}")
    for sheet in re.findall(r'\(property "Sheetfile" "([^"]+)"', text):
        target = (path.parent / sheet).resolve()
        require(target.is_relative_to(ROOT) and target.is_file(), f"Missing sheet: {sheet}")
    for lib, symbol in re.findall(r'\(lib_id "(Hack_[^:"]+):([^"]+)"', text):
        require(symbol in symbols.get(lib, set()), f"Missing custom symbol {lib}:{symbol} in {label}")
    footprints = re.findall(r'\(property "Footprint" "(Hack_[^:"]+):([^"]+)"', text)
    footprints += re.findall(r'^\t\(footprint "(Hack_[^:"]+):([^"]+)"', text, re.M)
    for lib, footprint in footprints:
        require((LIBRARIES / f"{lib}.pretty" / f"{footprint}.kicad_mod").is_file(),
                f"Missing custom footprint {lib}:{footprint} in {label}")

markdown = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
markdown += list((ROOT / "docs").rglob("*.md"))
markdown += list((ROOT / "hardware").rglob("*.md"))
for path in markdown:
    for raw in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding="utf-8")):
        link = urlsplit(raw.strip("<>"))
        if link.scheme or link.netloc or not link.path:
            continue
        target = (path.parent / unquote(link.path)).resolve()
        require(target.is_relative_to(ROOT) and target.exists(),
                f"Broken local link in {path.relative_to(ROOT)}: {raw}")

if errors:
    print("Repository checks failed:\n" + "\n".join(f"- {e}" for e in sorted(set(errors))))
    sys.exit(1)
print(f"OK: {len(design_files)} design files, {len(symbols)} custom symbol libraries, "
      f"project library paths, custom references, and local Markdown links.")
print("Electrical design correctness is checked separately with KiCad ERC/DRC.")
