# Validation baseline

Checked on **2026-10-26** with **KiCad 10.0.6** after importing the latest supplied archives. The portable library tables and previously corrected fuse footprint reference were retained.

- All six hierarchical subsheets resolve, and all seven schematic SVGs and the XML netlist export successfully.
- The netlist contains **142 components**; the PCB contains **142 footprints** and **zero routed track segments**.
- Schematic/PCB parity reports **zero findings**.
- ERC reports **80 findings**: 37 errors and 43 warnings. These include 38 isolated pin labels, 27 hierarchical label mismatches, eight undriven power pins, four library symbol mismatches, one unconnected pin, one multiple-net-name finding, and one pin conflict.
- DRC reports **18 findings**: 10 errors and eight warnings, plus **491 unconnected items**. The findings comprise four hole-clearance, six copper-edge-clearance, two silkscreen-edge-clearance, one text-height, four silkscreen-overlap, and one silkscreen-over-copper finding.

These are tool findings requiring design review, not a manufacturing certification. The board is unrouted. No bench testing, power-up, or firmware validation is implied.

## Thermal-via update — 2026-10-28

The RP2354B and both TPS5450DDAR instances now contain the [embedded thermal vias](thermal-vias.md) and masked back copper from their updated libraries. All 17 holes use 0.30 mm drills and 0.80 mm copper lands, with the exposed pad's GND net and solid zone connections. Fabrication requires epoxy filling, copper capping, and ENIG; ordinary tenting is insufficient for the retained paste pattern.

Checked with **KiCad 10.0.7**, comparing the modified design with the unchanged `f78af98761999674a46416bb6381aacdd00ae58b` baseline using the same executable and standard libraries:

- **DRC:** the same 18 violations, with identical violation details; 491 unconnected items in both versions; zero schematic/PCB parity findings. Airwire endpoint choices can change when connected pad primitives are added; the count and schematic connectivity are unchanged.
- **ERC:** 81 findings in both versions, with identical details (37 errors, 44 warnings). This tool/library version also reports one `same_local_global_label` warning beyond the older 80-finding import baseline; it is not introduced by the thermal-via change.
- **Geometry:** verified hole count, annular rings, hole spacing, exposed-pad containment, GND assignment, solid zone connections, back-copper margins, unique UUIDs, and matching library/board geometry. Original signal pads and paste apertures are unchanged.
- **Manufacturing export check:** native Gerber and separate PTH/NPTH drill exports succeed. The PTH file contains exactly 17 holes at 0.30 mm, and their exported coordinates match U1, U2, and U5. These temporary files in `build/thermal-via-fab-check/` are validation outputs, not a manufacturing release.
- **Previews/checks:** the repository export script completes, the board preview is refreshed, and a thermal-via detail drawing is included. Repository structure checks and `git diff --check` pass.

The board remains unrouted. Ground pours/routing, thermal performance, the existing findings, and the TPS5450 ENA-to-24-V connection still need review before fabrication.

## Reproduce

With KiCad 10 and Python 3.10 or newer, run from the repository root:

```sh
python scripts/check_repo.py
python scripts/export_design.py
```

The export script refreshes previews and writes JSON reports and an XML netlist under ignored `build/`. It does not save or refill the PCB. KiCad can return success while reporting violations; inspect the reports.
