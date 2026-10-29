# Validation baseline

Checked on **2026-10-29** with **KiCad 10.0.6** after importing the latest supplied archives. The portable library tables were retained; the active sources already include the earlier fuse footprint reference correction.

Rechecked after the [connector signal reordering](connector-pinout.md). All 84 signal/NC pad assignments and their schematic terminals changed. All fixed power/ground pins, nonconnector pin-to-net assignments, MCU/jumper placement, tracks, vias, and zones are unchanged. ERC and DRC finding counts, types, severities, and descriptions match the import baseline. The existing AUX10 warning follows its moved label, and KiCad selects a different existing +3V3 power symbol as the location for the multiple-net-name warning. Schematic/PCB parity remains clean.

- Repository checks pass for all **40 design and library files**, seven custom symbol libraries, project library paths, custom references, and local Markdown links.
- Connector checks pass for **288 pads**, fixed power/ground assignments, paired A/C protocols and adjacent UART contacts, signal inventory, and jumper outputs.
- All six hierarchical subsheets resolve, and all seven schematic SVGs, the board image, and the XML netlist export successfully.
- The netlist contains **144 components**; the PCB contains **144 footprints**, **518 routed track segments**, and **131 vias**.
- Schematic/PCB parity reports **zero findings**.
- ERC reports **16 findings**: 10 errors and six warnings. These comprise eight undriven power pins, four library symbol mismatches, one isolated pin label, one unconnected pin, one multiple-net-name finding, and one pin conflict.
- DRC reports **97 findings**: 75 errors and 22 warnings, plus **107 unconnected items** reported separately.

## Change from the previous import

| Measure | 2026-10-26 | 2026-10-29 |
| --- | ---: | ---: |
| Schematic components / PCB footprints | 142 / 142 | 144 / 144 |
| Routed track segments | 0 | 518 |
| ERC findings | 80 | 16 |
| DRC findings, excluding unconnected items | 18 | 97 |
| Unconnected PCB items | 491 | 107 |
| Schematic/PCB parity findings | 0 | 0 |

Routing has progressed and fewer connections remain open. The new routed layout also exposes track-width, via-size, clearance, and thermal-connection findings that need review. ERC no longer reports hierarchical label mismatches; the remaining unconnected microcontroller pin is `U5:61` (`VREG_AVDD`). The four symbol mismatches affect `Q1`, `C6`, `C12`, and `C13`.

## DRC breakdown

| Finding | Count |
| --- | ---: |
| Track width | 21 |
| Drill out of range | 15 |
| Via diameter | 15 |
| Starved thermal | 9 |
| Silkscreen overlap | 7 |
| Copper-edge clearance | 6 |
| Silkscreen over copper | 5 |
| Copper clearance | 4 |
| Hole clearance | 4 |
| Library footprint mismatch | 4 |
| Dangling via | 2 |
| Silkscreen-edge clearance | 2 |
| Courtyard overlap | 1 |
| Isolated copper | 1 |
| Text height | 1 |

These are tool findings requiring design review, not a manufacturing certification. The board is partially routed. No bench testing, power-up, or firmware validation is implied. The supplied design and check settings were preserved during import; findings were not suppressed or repaired as part of the source update.

## Reproduce

With KiCad 10 and Python 3.10 or newer, run from the repository root:

```sh
python scripts/check_repo.py
python scripts/export_design.py
```

The export script refreshes previews and writes JSON reports and an XML netlist under ignored `build/`. It does not save or refill the PCB. KiCad can return success while reporting violations; inspect the reports.
