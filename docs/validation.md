# Validation baseline

Checked on **2026-10-30** with **KiCad 10.0.6** after importing the corrected supplied archives. The import preserves active design/library files with normalized line endings and retains portable project library tables.

- All **40 active design/library files** match their archive contents after line-ending normalization. Seven custom symbol libraries and 24 custom footprints are bundled.
- All **288 connector pins** match the V6 reference in both schematic and PCB: fixed power/ground, SPI blocks 10–12 and 21–23, I²C columns 16–17, UART only on J1, and per-port AUX assignments.
- J1 is nearest the MCU, J2 is middle, and J3 is farthest.
- **144 schematic components**, **144 PCB footprints**, **788 track segments**, and **193 vias**.
- **16 ERC findings** (10 errors, 6 warnings).
- **134 DRC findings** (109 errors, 25 warnings), plus **41 unconnected PCB items**.
- **Zero schematic/PCB parity findings**. All seven schematic previews, board image, and XML netlist export successfully.

A second DRC run on a temporary copy with the same libraries and freshly refilled zones reports **122 violations** and **41 unconnected items**. Refilling removes nine copper-clearance and nine hole-clearance findings from the saved fills, and exposes six additional dangling-via findings, for twelve fewer findings overall. The source PCB is preserved byte-for-byte after line-ending normalization; the temporary refill is not saved over it.

Five vias beside the AUX jumper banks are currently assigned to GND. Their net-update settings and nearby AUX nets are listed in the [via assignment notes](connector-pinout.md#assigning-aux-via-nets-in-kicad). Connector pinout agreement does not mean the remaining routes or via assignments are complete.

## Change from the prior main-branch import

| Measure | 2026-10-29 | 2026-10-30 |
| --- | ---: | ---: |
| Schematic components / PCB footprints | 144 / 144 | 144 / 144 |
| Track segments / vias | 518 / 131 | 788 / 193 |
| ERC findings | 16 | 16 |
| DRC findings | 97 | 134 |
| Unconnected PCB items | 107 | 41 |
| Schematic/PCB parity findings | 0 | 0 |

The new source includes additional routing and vias. Its existing design findings are preserved and documented; this import does not suppress them or alter the supplied copper. The separate V6 routing-study results are not the validation baseline for this user-routed PCB.

## DRC breakdown

| Finding | Count |
| --- | ---: |
| `track_width` | 21 |
| `drill_out_of_range` | 20 |
| `via_diameter` | 20 |
| `clearance` | 15 |
| `hole_clearance` | 13 |
| `starved_thermal` | 12 |
| `silk_overlap` | 8 |
| `copper_edge_clearance` | 6 |
| `silk_over_copper` | 6 |
| `lib_footprint_mismatch` | 4 |
| `via_dangling` | 3 |
| `silk_edge_clearance` | 2 |
| `zones_intersect` | 1 |
| `courtyards_overlap` | 1 |
| `isolated_copper` | 1 |
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

The board remains partially routed and requires review before fabrication. No bench, firmware, power-up, or crosstalk validation is implied.

## Reproduce

```sh
python scripts/check_repo.py
python scripts/export_design.py
python scripts/check_connector_pinout.py --netlist build/backplane.xml
```

The export script refreshes previews and writes reports under ignored `build/`. It does not save or refill the PCB. KiCad can return success while reporting violations; inspect the reports.
