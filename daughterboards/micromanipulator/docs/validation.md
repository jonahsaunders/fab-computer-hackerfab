# Design validation — 2026-11-07

This is a development snapshot, not a manufacturing release. The seven-sheet schematic and 100 × 60 mm PCB both use one RP2350B. The root schematic contains only the 14 external connectors, a ground symbol and six hierarchical blocks. The fixed DIN96 interface and encoder harness pin maps are retained.

| KiCad 10.0.6 check | Result |
| --- | --- |
| Schematic ERC, including four-way junctions | **0 violations** |
| Seven-page SVG audit | **0** text/wire collisions, text/text collisions, interior wire crossings or overlapping wire segments |
| Hierarchy audit | **14** root connectors, **0** root support components, all **7** sheets reachable |
| PCB DRC violations, apart from connectivity | **0** |
| PCB unconnected items | **0** |
| Schematic/PCB parity | **0 issues** |
| Components / copper layers | **116 / 4** |
| Host interface / connector footprint audit | **288** host contacts compared; **9** PH and **3** pin-header footprints checked; full interface in host J1/J2 |

The layer order is front signal / inner power / inner ground / back signal. The board contains 1512 manually routed track segments/vias, including 57 added ground-stitching vias. Eight filled zones include the inner power regions, a single connected In2 ground region and grounded outer copper. No autorouter was used. Courtyard, via-endpoint, footprint-filter and pad-type checks are enabled. A native-board comparison confirms all 14 connectors retain their placement, orientation, pad geometry and electrical connections. The two USB CC nets have descriptive names after the hierarchy change described below.

USB support components U12, C66 and R48–R51 now reside in USBInterface. A comparison of native KiCad netlists before and after the move proves that all 145 electrical pin groups are identical. Only `Net-(J18-CC1)` and `Net-(J18-CC2)` were renamed to `/USB_CC1` and `/USB_CC2`. At the hierarchy-only revision, a full parsed-board comparison allowed only those names and the six updated schematic paths and proved unchanged PCB geometry. The later USB placement changes are checked separately below. The root and USB child were also inspected as rendered pages.

All 35 checked local supply/bypass connections have a continuous front-copper path to the served pin. All 48 capacitor ground pads also have explicit front-copper paths to ground vias; their pad-to-pour settings use solid copper. The revised measurements include both supply traces and dedicated ground returns. See the [decoupling review](decoupling-review.md) and [measured lengths](decoupling-paths.csv). The ground-return and stackup decisions are recorded in the [layout review](layout-review.md).

All 31 footprint types resolve from project-local libraries. All 116 component instances have models: 115 project-relative files and one embedded upstream STEP model. Six component instances use newly made nominal models (RP2350B, two DRV8837C devices and three TB6612FNG devices); these are identified in the [inventory](model-inventory.csv). USB-C now uses a detailed community STEP model. Its twelve distinct contact positions and four shell-tab locations were checked against the footprint, and its model replacement preserved the footprint geometry and connector position. The native 3D rendering was inspected for component placement and connector access. Exact procurement/package review, USB signal-integrity confirmation, host mating tolerances, load/thermal limits and firmware consolidation remain open. These checks do not establish electrical performance or manufacturing readiness.

The [USB routing revision](usb-routing-review.md) reduces the resistor-to-MCU stubs from 14.407/15.731 mm to 2.652/0.987 mm, with no signal vias after the resistors. Native netlist comparison verifies that only the four equivalent U12 ESD-channel pins changed net membership. All external interfaces are preserved. Both 0201 resistor footprints use manufacturer-recommended lands and bundled models. Three extra ground-transfer vias support the USB launches.

The [connector review](connector-review.md) assigns exact WingTAT/JST/XUNPU/BOOMELE parts to thirteen connectors and verifies their hole patterns against manufacturer drawings. Together with the existing HRO USB-C part, all fourteen external connectors now have ordering codes. The actual host PCB confirms UART direction, I²C and power allocation; slot J3 lacks UART. This selection changes procurement fields only, with all electrical geometry and visible schematic content preserved by parsed-file comparison. Nominal host slot pitch is 26 mm; a populated assembly and cable-clearance check remains open.

The subsequent [regulator capacitor selection](power-budget.md#local-capacitor-selection) raises C1/C2 from 1 µF to 4.7 µF and specifies Samsung CL10A475KO8NNNC for C1/C2/C10. Native parsed comparisons permit only those values and procurement fields; pads, nets, models, placement and copper are unchanged. The Power and MotionController pages and complete schematic PDF were regenerated and visually checked. The seven-page visual audit remains clear.

The [gate-driver supply correction](power-budget.md#gate-driver-supply-and-an-open-load-fuse) moves U11 and C64/C65 to the existing backplane 5 V supply before F1. Native netlists confirm exactly three changed pin assignments. All existing track geometry and all footprint geometry remain unchanged; 16 power-track segments and four vias are added. The five inner power zones and In2 ground each retain one connected filled region. ERC, DRC, parity and all seven page audits remain clear.

The [tool-output part selection](tool-parts-review.md) assigns exact JLCPCB codes to U9/U10/U11/Q1/Q2/D2. Manufacturer pin functions and package drawings were checked against the saved board. Parsed comparisons permit hidden procurement fields only and prove unchanged electrical and visual geometry.

The [passive selections](passive-parts-review.md) and [controller/axis-driver review](controller-parts-review.md) resolve 58 more BOM entries. The three axis drivers now use a Toshiba-specific fabrication outline, courtyard and nominal model; all pads, placement and copper are unchanged. Twelve capacitor/fuse entries still require exact selection. ERC, DRC, connectivity, parity and schematic visual checks are repeated on the saved result.

## Reproduce

Run from this folder, with KiCad 10 available. Create `build/` first.

```sh
kicad-cli sch erc --format json --severity-all --exit-code-violations --output build/erc-current.json hardware/daughterboard/FabNanoDaughterboard.kicad_sch
kicad-cli pcb drc --format json --severity-all --schematic-parity --output build/drc-current.json hardware/daughterboard/FabNanoDaughterboard.kicad_pcb
kicad-cli sch export svg --output docs/schematics/ hardware/daughterboard/FabNanoDaughterboard.kicad_sch
python scripts/check_schematic_visuals.py
python scripts/check_hierarchy.py
python scripts/check_backplane_interface.py
python scripts/check_power_domains.py
python scripts/check_usb_termination.py
python scripts/check_decoupling.py
python scripts/check_capacitor_returns.py
```

Inspect the DRC report: its default exit status does not fail for findings. The repository's root checker validates the host backplane; it does not replace these daughterboard checks.

[![Current PCB, copper pours hidden](layout-front.svg)](layout-front.svg)
