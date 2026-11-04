# Validation baseline

Checked on **2026-11-04** with **KiCad 10.0.6**, using the supplied design files and saved copper fills without modifying the design.

- All **41 active design, library, and rule files** match the supplied archives after line-ending normalization. Portable project library tables are retained.
- **148 schematic components**, **148 PCB footprints**, **1,114 track segments**, and **267 vias**.
- All **288 connector contacts** agree between the current pin reference, schematic netlist, and PCB. J1 carries hardware UART0; J2 carries hardware UART1 through R56/R57, named `UART2` in the schematic; J3's UART positions remain NC.
- **15 ERC findings:** 9 errors and 6 warnings.
- **386 DRC findings:** 24 errors and 362 warnings, with **zero unconnected items** and **zero schematic/PCB parity findings** under the supplied rule settings.
- Seven schematic previews, the board image, and the netlist export successfully. Repository checks pass.

## DRC breakdown

| Finding | Count |
| --- | ---: |
| `clearance` | 14 |
| `hole_clearance` | 10 |
| `silk_over_copper` | 199 |
| `text_height` | 66 |
| `text_thickness` | 43 |
| `silk_overlap` | 52 |
| `silk_edge_clearance` | 2 |

## ERC breakdown

| Finding | Count |
| --- | ---: |
| `power_pin_not_driven` | 8 |
| `pin_to_pin` | 1 |
| `lib_symbol_mismatch` | 4 |
| `isolated_pin_label` | 1 |
| `multiple_net_names` | 1 |

The supplied rule settings and exclusions are unchanged. The earlier [thermal-relief investigation](thermal-relief.md) describes the November 1 source. No bench, firmware, power-up, or manufacturing validation is implied.

## Reproduce

```sh
python scripts/check_repo.py
python scripts/export_design.py
python scripts/check_connector_pinout.py --netlist build/backplane.xml
```

The export script refreshes previews and writes reports under ignored `build/`. It does not refill or save the PCB. KiCad can return success while reporting violations; inspect the reports. GitHub CI checks repository portability, references, documentation links, and connector assignments; it does not run KiCad or bench tests.
