# Design validation — 2026-11-07

This is a development snapshot, not a manufacturing release. The six-sheet schematic and 100 × 60 mm PCB both use one RP2350B. All 14 external connectors are on the root schematic. The fixed DIN96 interface and encoder harness pin maps are retained.

| KiCad 10.0.6 check | Result |
| --- | --- |
| Schematic ERC, including four-way junctions | **0 violations** |
| Six-page SVG audit | **0** text/wire collisions, text/text collisions, interior wire crossings or overlapping wire segments |
| PCB DRC violations, apart from connectivity | **0** |
| PCB unconnected items | **0** |
| Schematic/PCB parity | **0 issues** |
| Components / copper layers | **116 / 4** |

The layer order is front signal / inner power / inner ground / back signal. The board contains 563 explicit manual route entries and 1382 track segments/vias, including 54 added ground-stitching vias. Eight filled zones include the inner power regions, a single connected In2 ground region and grounded outer copper. No autorouter was used. Courtyard, via-endpoint, footprint-filter and pad-type checks are enabled. A native-board comparison confirms all 14 connectors retain their placement, orientation, pad geometry and nets.

All 35 checked local supply/bypass connections have a continuous front-copper path to the served pin. Six MCU bypass loops previously depended on inner-layer connections; those paths are now direct. See the [decoupling review](decoupling-review.md) and [measured lengths](decoupling-paths.csv). The ground-return and stackup decisions are recorded in the [layout review](layout-review.md).

All 31 footprint types resolve from project-local libraries. All 116 component instances have models: 115 project-relative files and one embedded upstream STEP model. Four component instances use newly made nominal models (RP2350B, two DRV8837C devices and USB-C); these are identified in the [inventory](model-inventory.csv). The native 3D rendering was inspected for component placement and connector access. Exact procurement/package review, USB signal-integrity confirmation, host mating tolerances, load/thermal limits and firmware consolidation remain open. These checks do not establish electrical performance or manufacturing readiness.

## Reproduce

Run from this folder, with KiCad 10 available. Create `build/` first.

```sh
kicad-cli sch erc --format json --severity-all --exit-code-violations --output build/erc-current.json hardware/daughterboard/FabNanoDaughterboard.kicad_sch
kicad-cli pcb drc --format json --severity-all --schematic-parity --output build/drc-current.json hardware/daughterboard/FabNanoDaughterboard.kicad_pcb
kicad-cli sch export svg --output docs/schematics/ hardware/daughterboard/FabNanoDaughterboard.kicad_sch
python scripts/check_schematic_visuals.py
```

Inspect the DRC report: its default exit status does not fail for findings. The repository's root checker validates the host backplane; it does not replace these daughterboard checks.

[![Current PCB, copper pours hidden](layout-front.svg)](layout-front.svg)
