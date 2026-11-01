# Validation baseline

Checked on **2026-11-01** with **KiCad 10.0.6** after the latest supplied-archive update. The PCB and mounting-hole library footprint change; the project settings, schematics, and custom design rules are unchanged. The import preserves active design/library/rule files with normalized line endings and retains portable project library tables.

- All **41 active design/library/rule files** match their archive contents after line-ending normalization. Seven custom symbol libraries and 24 custom footprints are bundled.
- All **288 connector pins** match the V6 reference in both schematic and PCB: fixed power/ground, SPI blocks 10–12 and 21–23, I²C columns 16–17, UART only on J1, and per-port AUX assignments.
- J1 is nearest the MCU, J2 is middle, and J3 is farthest.
- **144 schematic components**, **144 PCB footprints**, **1,063 track segments**, and **248 vias**.
- **16 ERC findings** (10 errors, 6 warnings).
- **368 DRC findings** (15 errors, 353 warnings), with **zero unconnected PCB items** reported separately.
- **Zero schematic/PCB parity findings**. All seven schematic previews, board image, and XML netlist export successfully.

These results use the PCB's saved zone fills and the supplied custom design rules. The imported board was not saved during validation, and its contents still match the supplied source after line-ending normalization. A separate temporary-copy refill reproduces the 368 findings and zero unconnected items. The custom rules are preserved as supplied; their fabrication capability claims were not independently verified.

The five previously documented GND-assigned AUX vias now carry `/AUX1`, `/AUX4`, `/AUX7`, `/AUX8`, and `/AUX9`. Their current positions and net-update settings are listed in the [via assignment notes](connector-pinout.md#assigning-aux-via-nets-in-kicad).

## Change from the prior main-branch import

| Measure | Previous import (custom rules) | Latest import (mounting holes) |
| --- | ---: | ---: |
| Schematic components / PCB footprints | 144 / 144 | 144 / 144 |
| Track segments / vias | 1,052 / 248 | 1,063 / 248 |
| ERC findings | 16 | 16 |
| DRC findings | 376 | 368 |
| Unconnected PCB items | 4 | 0 |
| Schematic/PCB parity findings | 0 | 0 |

The new source adds 11 track segments and updates the mounting-hole footprint and its board instances. Its keepout now applies only to the outer copper layers, allowing the inner GND plane to connect. The four previously reported GND unconnected items are resolved. The custom-rule file is unchanged.

There are **11 thermal-relief findings**: eight surface-pad findings with one connected spoke instead of two, and three connector-pad findings with a spoke reaching isolated copper. The [thermal-relief investigation](thermal-relief.md) includes actual copper illustrations and temporary-copy experiments. A focused thermal-gap adjustment cleared five findings in a diagnostic copy; it is not applied to the imported source.

## DRC breakdown

| Finding | Count |
| --- | ---: |
| `silk_over_copper` | 199 |
| `text_height` | 66 |
| `text_thickness` | 44 |
| `silk_overlap` | 38 |
| `starved_thermal` | 11 |
| `copper_edge_clearance` | 4 |
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
