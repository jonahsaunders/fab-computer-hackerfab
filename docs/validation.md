# Validation baseline

Checked on **2026-11-02** with **KiCad 10.0.6** after the latest supplied-archive update. The PCB and project zone defaults change; the schematics, custom design rules, and shared libraries are unchanged. The import preserves active design/library/rule files with normalized line endings and retains portable project library tables.

- All **41 active design/library/rule files** match their archive contents after line-ending normalization. Seven custom symbol libraries and 24 custom footprints are bundled.
- All **288 connector pins** match the V6 reference in both schematic and PCB: fixed power/ground, SPI blocks 10–12 and 21–23, I²C columns 16–17, UART only on J1, and per-port AUX assignments.
- J1 is nearest the MCU, J2 is middle, and J3 is farthest.
- **144 schematic components**, **144 PCB footprints**, **1,065 track segments**, and **248 vias**.
- **16 ERC findings** (10 errors, 6 warnings).
- **352 DRC findings** (zero errors, 352 warnings), with **zero unconnected PCB items** reported separately.
- **Zero schematic/PCB parity findings**. All seven schematic previews, board image, and XML netlist export successfully.

These results use the PCB's saved zone fills and the supplied custom design rules. The imported board was not saved or refilled during validation, and all 41 imported files still match the supplied source after line-ending normalization. The custom rules and check severities are preserved as supplied; their fabrication capability claims were not independently verified.

The five previously documented GND-assigned AUX vias now carry `/AUX1`, `/AUX4`, `/AUX7`, `/AUX8`, and `/AUX9`. Their current positions and net-update settings are listed in the [via assignment notes](connector-pinout.md#assigning-aux-via-nets-in-kicad).

## Change from the prior main-branch import

| Measure | Previous import (2026-11-01 mounting holes) | Latest import (2026-11-02) |
| --- | ---: | ---: |
| Schematic components / PCB footprints | 144 / 144 | 144 / 144 |
| Track segments / vias | 1,063 / 248 | 1,065 / 248 |
| ERC findings | 16 | 16 |
| DRC errors / warnings | 15 / 353 | 0 / 352 |
| Thermal-relief errors | 11 | 0 |
| Copper-edge-clearance errors | 4 | 0 |
| Unconnected PCB items | 0 | 0 |
| Schematic/PCB parity findings | 0 | 0 |

The new source has two more track segments, repositioned mounting holes, and updated copper geometry. Project zone defaults change from thermal relief on all pads to thermal relief on through-hole pads, with a default thermal gap of 0.40 mm instead of 0.50 mm. The custom-rule file and all library files are unchanged.

The previous 11 thermal-relief and four copper-edge-clearance errors are no longer reported. One text-thickness warning is also resolved. The [thermal-relief investigation](thermal-relief.md) remains a historical record of the November 1 board; its experiments were not applied during this import.

## DRC breakdown

| Finding | Count |
| --- | ---: |
| `silk_over_copper` | 199 |
| `text_height` | 66 |
| `text_thickness` | 43 |
| `silk_overlap` | 38 |
| `via_dangling` | 4 |
| `silk_edge_clearance` | 2 |

## ERC breakdown

| Finding | Count |
| --- | ---: |
| `power_pin_not_driven` | 8 |
| `lib_symbol_mismatch` | 4 |
| `isolated_pin_label` | 1 |
| `pin_not_connected` | 1 |
| `multiple_net_names` | 1 |
| `pin_to_pin` | 1 |

The board requires design-rule cleanup and review before fabrication. No bench, firmware, power-up, or crosstalk validation is implied.

## Reproduce

```sh
python scripts/check_repo.py
python scripts/export_design.py
python scripts/check_connector_pinout.py --netlist build/backplane.xml
```

The export script refreshes previews and writes reports under ignored `build/`. It does not save or refill the PCB. KiCad can return success while reporting violations; inspect the reports.
