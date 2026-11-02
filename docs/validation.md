# Validation baseline

Checked on **2026-11-02** with **KiCad 10.0.6** after the supplied-archive update to RP2350B and its supporting circuitry. The PCB, project settings, microcontroller sheet, both buck-regulator sheets, and two symbol libraries change. Custom design rules and all 24 custom footprints are unchanged. The import preserves active design/library/rule files with normalized line endings and retains portable project library tables.

- All **41 active design/library/rule files** match their archive contents after line-ending normalization. Seven custom symbol libraries and 24 custom footprints are bundled.
- All **288 connector pins** match the V6 reference in both schematic and PCB: fixed power/ground, SPI blocks 10–12 and 21–23, I²C columns 16–17, UART only on J1, and per-port AUX assignments.
- J1 is nearest the MCU, J2 is middle, and J3 is farthest.
- **146 schematic components**, **146 PCB footprints**, **1,073 track segments**, and **263 vias**.
- **15 ERC findings** (9 errors, 6 warnings).
- **350 DRC findings** (zero errors, 350 warnings), with **zero unconnected PCB items** reported separately.
- **Zero schematic/PCB parity findings**. All seven schematic previews, board image, and XML netlist export successfully.

These results use the PCB's saved zone fills and the supplied custom design rules. The imported board was not saved or refilled during validation, and all 41 imported files still match the supplied source after line-ending normalization. The custom rules and check severities are preserved as supplied; their fabrication capability claims were not independently verified.

The five previously documented GND-assigned AUX vias now carry `/AUX1`, `/AUX4`, `/AUX7`, `/AUX8`, and `/AUX9`. Their current positions and net-update settings are listed in the [via assignment notes](connector-pinout.md#assigning-aux-via-nets-in-kicad).

## Change from the prior main-branch import

| Measure | Previous import (2026-11-02 routing and vias) | Latest import (2026-11-02 RP2350B) |
| --- | ---: | ---: |
| Schematic components / PCB footprints | 144 / 144 | 146 / 146 |
| Track segments / vias | 1,062 / 265 | 1,073 / 263 |
| ERC errors / warnings | 10 / 6 | 9 / 6 |
| DRC errors / warnings | 0 / 347 | 0 / 350 |
| Dangling-via warnings | 0 | 0 |
| Silkscreen-overlap warnings | 37 | 44 |
| Unconnected PCB items | 0 | 0 |
| Schematic/PCB parity findings | 0 | 0 |

The new source replaces U5's RP2354B symbol with RP2350B and adds C42 (4.7 µF, 16 V) and R55 (33 Ω), together with matching library symbols. The supplied 12 V and 5 V buck-regulator sheets replace their enable-to-input connections with explicit no-connect markers. The PCB reflects the source changes, with 11 more track segments and two fewer vias. Project settings update the used-designator inventory; zone defaults and the custom-rule file are unchanged from the preceding import.

The previous `pin_not_connected` ERC error is no longer reported. DRC adds seven silkscreen-overlap warnings while text-height and text-thickness warnings each fall by two. Thermal-relief and copper-edge-clearance errors remain at zero. The [thermal-relief investigation](thermal-relief.md) remains a historical record of the November 1 board; its experiments were not applied during this import.

## DRC breakdown

| Finding | Count |
| --- | ---: |
| `silk_over_copper` | 199 |
| `text_height` | 64 |
| `text_thickness` | 41 |
| `silk_overlap` | 44 |
| `silk_edge_clearance` | 2 |

## ERC breakdown

| Finding | Count |
| --- | ---: |
| `power_pin_not_driven` | 8 |
| `lib_symbol_mismatch` | 4 |
| `isolated_pin_label` | 1 |
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
