# Validation baseline

Checked on **2026-11-01** with **KiCad 10.0.6** after the later supplied-archive update. The PCB and project net colors change, and the archive adds `HackerfabBackplane.kicad_dru`. The import preserves active design/library/rule files with normalized line endings and retains portable project library tables.

- All **41 active design/library/rule files** match their archive contents after line-ending normalization. Seven custom symbol libraries and 24 custom footprints are bundled.
- All **288 connector pins** match the V6 reference in both schematic and PCB: fixed power/ground, SPI blocks 10–12 and 21–23, I²C columns 16–17, UART only on J1, and per-port AUX assignments.
- J1 is nearest the MCU, J2 is middle, and J3 is farthest.
- **144 schematic components**, **144 PCB footprints**, **1,052 track segments**, and **248 vias**.
- **16 ERC findings** (10 errors, 6 warnings).
- **376 DRC findings** (24 errors, 352 warnings), plus **four unconnected PCB items** reported separately.
- **Zero schematic/PCB parity findings**. All seven schematic previews, board image, and XML netlist export successfully.

These results use the PCB's saved zone fills and the supplied custom design rules. The board was not refilled or saved during validation, and its contents still match the supplied source after line-ending normalization. The custom rules are preserved as supplied; their fabrication capability claims were not independently verified.

The five previously documented GND-assigned AUX vias now carry `/AUX1`, `/AUX4`, `/AUX7`, `/AUX8`, and `/AUX9`. Their current positions and net-update settings are listed in the [via assignment notes](connector-pinout.md#assigning-aux-via-nets-in-kicad).

## Change from the prior main-branch import

| Measure | Earlier 2026-11-01 | Later 2026-11-01 |
| --- | ---: | ---: |
| Schematic components / PCB footprints | 144 / 144 | 144 / 144 |
| Track segments / vias | 1,045 / 248 | 1,052 / 248 |
| ERC findings | 16 | 16 |
| DRC findings | 137 | 376 |
| Unconnected PCB items | 0 | 4 |
| Schematic/PCB parity findings | 0 | 0 |

The new source adds seven track segments and a custom-rule file. Because both the layout and rule set changed, these DRC totals are not a comparison under identical rules. Its design findings are preserved and documented; this import does not suppress them or alter the supplied copper.

The four unconnected findings are on GND: H3 pad 1 to a front-layer track, J3 pads B1 and B32 to the inner-layer GND zone, and disconnected portions of that zone. These findings need review with the current zone fills before fabrication.

## DRC breakdown

| Finding | Count |
| --- | ---: |
| `silk_over_copper` | 199 |
| `text_height` | 64 |
| `text_thickness` | 42 |
| `silk_overlap` | 41 |
| `starved_thermal` | 13 |
| `copper_edge_clearance` | 6 |
| `via_dangling` | 4 |
| `clearance` | 3 |
| `courtyards_overlap` | 2 |
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
