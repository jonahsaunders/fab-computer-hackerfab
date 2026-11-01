# Validation baseline

Checked on **2026-11-01** with **KiCad 10.0.6** after importing the supplied archives. Only the PCB differs from the previous import. The import preserves active design/library files with normalized line endings and retains portable project library tables.

- All **40 active design/library files** match their archive contents after line-ending normalization. Seven custom symbol libraries and 24 custom footprints are bundled.
- All **288 connector pins** match the V6 reference in both schematic and PCB: fixed power/ground, SPI blocks 10–12 and 21–23, I²C columns 16–17, UART only on J1, and per-port AUX assignments.
- J1 is nearest the MCU, J2 is middle, and J3 is farthest.
- **144 schematic components**, **144 PCB footprints**, **1,045 track segments**, and **248 vias**.
- **16 ERC findings** (10 errors, 6 warnings).
- **137 DRC findings** (113 errors, 24 warnings), with **zero unconnected PCB items**.
- **Zero schematic/PCB parity findings**. All seven schematic previews, board image, and XML netlist export successfully.

These results use the PCB's saved zone fills. The board was not refilled or saved during validation, and its contents still match the supplied source after line-ending normalization.

The five previously documented GND-assigned AUX vias now carry `/AUX1`, `/AUX4`, `/AUX7`, `/AUX8`, and `/AUX9`. Their current positions and net-update settings are listed in the [via assignment notes](connector-pinout.md#assigning-aux-via-nets-in-kicad).

## Change from the prior main-branch import

| Measure | 2026-10-30 | 2026-11-01 |
| --- | ---: | ---: |
| Schematic components / PCB footprints | 144 / 144 | 144 / 144 |
| Track segments / vias | 788 / 193 | 1,045 / 248 |
| ERC findings | 16 | 16 |
| DRC findings | 134 | 137 |
| Unconnected PCB items | 41 | 0 |
| Schematic/PCB parity findings | 0 | 0 |

The new source adds 257 track segments and 55 vias, and eliminates the 41 previously reported unconnected items. Its design findings are preserved and documented; this import does not suppress them or alter the supplied copper. Zero unconnected items does not mean the board is ready for fabrication.

## DRC breakdown

| Finding | Count |
| --- | ---: |
| `track_width` | 29 |
| `drill_out_of_range` | 27 |
| `via_diameter` | 27 |
| `starved_thermal` | 13 |
| `silk_over_copper` | 7 |
| `copper_edge_clearance` | 6 |
| `silk_overlap` | 6 |
| `clearance` | 4 |
| `hole_clearance` | 4 |
| `via_dangling` | 4 |
| `lib_footprint_mismatch` | 4 |
| `courtyards_overlap` | 2 |
| `silk_edge_clearance` | 2 |
| `zones_intersect` | 1 |
| `text_height` | 1 |

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
