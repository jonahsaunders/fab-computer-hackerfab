# Validation baseline

Checked on **2026-11-04** with **KiCad 10.0.6**. See the [full design audit](design-audit-2026-11-04.md) for electrical findings, references, and required measurements. The design remains development hardware.

## Scope and results

- Imported ten active backplane files and 31 library files. Of the 41 files, 38 still match the archives after line-ending normalization; the three deliberate exceptions are documented in [provenance](provenance.md). Portable library tables are retained.
- **148 schematic components**, **148 PCB footprints**, **1,114 track segments**, and **267 vias**.
- All **288 connector contacts** agree between the current reference, schematic netlist, and PCB. J1 carries hardware UART0; J2 now carries hardware UART1 through R56/R57; J3's UART positions remain NC. Power, ground, SPI, I²C, and AUX assignments retain their prior positions.
- **15 ERC findings:** 9 errors and 6 warnings.
- **362 DRC warnings, zero DRC errors**, **zero unconnected PCB items**, and **zero schematic/PCB parity findings** under the supplied rule settings.
- Seven schematic SVGs, the board image, and netlist export successfully. Repository checks and five connector regression cases pass.

## Saved copper-fill correction

The source archive's saved fills were stale around changed routing. They produced 14 copper-clearance and 10 drill-to-copper-clearance errors. A fresh fill removed all 24, so the corrected fills were saved to the repository board. A subsequent in-memory refill gives the same finding counts as the final saved fills. No trace, via, footprint geometry, zone definition, or rule was moved or relaxed to clear those errors.

| Measure | Previous main import | Supplied November 4 PCB | Final audited PCB |
| --- | ---: | ---: | ---: |
| Schematic components / footprints | 146 / 146 | 148 / 148 | 148 / 148 |
| Track segments / vias | 1,073 / 263 | 1,114 / 267 | 1,114 / 267 |
| ERC errors / warnings | 9 / 6 | 9 / 6 | 9 / 6 |
| DRC errors / warnings | 0 / 350 | 24 / 362 | 0 / 362 |
| Unconnected PCB items | 0 | 0 | 0 |
| Normal schematic/PCB parity findings | 0 | 0 | 0 |

The earlier [thermal-relief investigation](thermal-relief.md) remains a historical record of the November 1 source.

## DRC breakdown

| Finding | Final count |
| --- | ---: |
| `silk_over_copper` | 199 |
| `text_height` | 66 |
| `text_thickness` | 43 |
| `silk_overlap` | 52 |
| `silk_edge_clearance` | 2 |

These warnings need assembly/fabrication review. The custom-rule header describes 0.5 oz inner copper, while the PCB stackup declares 0.035 mm copper on every layer. DRC is evaluated against supplied rules, not a verified manufacturing contract.

## ERC breakdown

| Finding | Count | Interpretation |
| --- | ---: | --- |
| `power_pin_not_driven` | 8 | Mostly passive power-path modeling; verify sources before adding power flags |
| `pin_to_pin` | 1 | U6's two VOUT pins are modeled as power outputs, although the datasheet joins them |
| `lib_symbol_mismatch` | 4 | Q1 and C6/C12/C13 metadata mismatches; compared pin definitions match |
| `isolated_pin_label` | 1 | AUX10 is only J3:C19 and has no MCU connection |
| `multiple_net_names` | 1 | `+3V3` / `3V3` naming overlap |

No exclusions were added. The supplied project ignores ERC `single_global_label`, `four_way_junction`, `simulation_model_issue`, and `footprint_filter`; it ignores DRC `missing_courtyard`, `track_not_centered_on_via`, `tuning_profile_track_geometries`, `footprint_filters_mismatch`, and `footprint_type_mismatch`.

A temporary copy changed every ignored severity to warning, preserving all other settings. That run reports **16 ERC findings**, **365 DRC warnings**, zero unconnected items, and **one parity warning**. Additional findings are Y1's stale `RPI_COMPILED` footprint filter and three off-center via endpoints, on `+3V3`, `/UART2_TX`, and `/UART2_RX`. The normal zero-parity result must be read with this disclosed filter setting. Temporary severity changes were not applied to the tracked project.

## Audit evidence

These JSON files are snapshots of this audit, rather than reports automatically updated by CI:

- [Archive-to-repository manifest and hashes](audit/2026-11-04/import-manifest.json)
- [As-supplied saved-fill DRC](audit/2026-11-04/drc-as-supplied.json)
- [Final ERC](audit/2026-11-04/erc.json)
- [Final saved-fill DRC](audit/2026-11-04/drc.json)
- [Final in-memory-refilled DRC](audit/2026-11-04/drc-refilled.json)
- [ERC with ignored checks enabled](audit/2026-11-04/erc-all-checks.json)
- [DRC with ignored checks enabled](audit/2026-11-04/drc-all-checks.json)

## Reproduce

```sh
python scripts/check_repo.py
python scripts/test_connector_pinout.py
python scripts/export_design.py
python scripts/check_connector_pinout.py --netlist build/backplane.xml
```

The export script refreshes previews, creates a fresh netlist, and writes ERC, saved-fill DRC, and in-memory-refilled DRC reports under ignored `build/`. It does not save the board. KiCad can return a successful process exit while reporting violations; inspect the JSON findings. The all-checks experiment additionally requires changing each `ignore` severity to `warning` in a separate project copy.

GitHub CI checks repository portability, references, documentation links, connector assignments, and the five connector regression cases. It does not install KiCad or perform bench testing. Passing CI does not establish fabrication readiness, thermal margins, regulator stability, or USB compliance.
