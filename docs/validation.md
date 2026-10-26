# Validation baseline

Checked on **2026-10-26** with **KiCad 10.0.6** after importing the latest supplied archives. The portable library tables and previously corrected fuse footprint reference were retained.

- All six hierarchical subsheets resolve, and all seven schematic SVGs and the XML netlist export successfully.
- The netlist contains **142 components**; the PCB contains **142 footprints** and **zero routed track segments**.
- Schematic/PCB parity reports **zero findings**.
- ERC reports **80 findings**: 37 errors and 43 warnings. These include 38 isolated pin labels, 27 hierarchical label mismatches, eight undriven power pins, four library symbol mismatches, one unconnected pin, one multiple-net-name finding, and one pin conflict.
- DRC reports **18 findings**: 10 errors and eight warnings, plus **491 unconnected items**. The findings comprise four hole-clearance, six copper-edge-clearance, two silkscreen-edge-clearance, one text-height, four silkscreen-overlap, and one silkscreen-over-copper finding.

These are tool findings requiring design review, not a manufacturing certification. The board is unrouted. No bench testing, power-up, or firmware validation is implied.

## Reproduce

With KiCad 10 and Python 3.10 or newer, run from the repository root:

```sh
python scripts/check_repo.py
python scripts/export_design.py
```

The export script refreshes previews and writes JSON reports and an XML netlist under ignored `build/`. It does not save or refill the PCB. KiCad can return success while reporting violations; inspect the reports.
