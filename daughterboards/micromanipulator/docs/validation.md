# Design validation — 2026-11-08

This is a development snapshot, not a manufacturing release. The seven-sheet schematic and 100 × 60 mm PCB both use one RP2350B. The root schematic contains only the 14 external connectors, a ground symbol and six hierarchical blocks. The fixed DIN96 interface and encoder harness pin maps are retained.

| KiCad 10.0.6 check | Result |
| --- | --- |
| Schematic ERC, including four-way junctions | **0 violations** |
| Seven-page SVG audit | **0** text/wire collisions, text/text collisions, interior wire crossings overlapping wire segments or zero-length wires |
| Hierarchy audit | **14** root connectors, **0** root support components, all **7** sheets reachable |
| PCB DRC violations, apart from connectivity | **0** |
| PCB unconnected items | **0** |
| Schematic/PCB parity | **0 issues** |
| Fitted components + bare probe pads / copper layers | **116 + 4 / 4** |
| Host interface / connector footprint audit | **288** host contacts compared; **9** PH and **3** pin-header footprints checked; full interface in host J1/J2 |

The layer order is front signal / inner power / inner ground / back signal. The board contains 1542 manually routed track segments/vias, including 57 ground-stitching vias from the previous revision and three new probe-connection vias. Eight filled zones include the inner power regions, a single connected In2 ground region and grounded outer copper. No autorouter was used. Courtyard, via-endpoint, footprint-filter and pad-type checks are enabled. A native-board comparison confirms all 14 connectors retain their placement, orientation, pad geometry and electrical connections. The two USB CC nets have descriptive names after the hierarchy change described below.

USB support components U12, C66 and R48–R51 now reside in USBInterface. A comparison of native KiCad netlists before and after the move proves that all 145 electrical pin groups are identical. Only `Net-(J18-CC1)` and `Net-(J18-CC2)` were renamed to `/USB_CC1` and `/USB_CC2`. At the hierarchy-only revision, a full parsed-board comparison allowed only those names and the six updated schematic paths and proved unchanged PCB geometry. The later USB placement changes are checked separately below. The root and USB child were also inspected as rendered pages.

All 35 checked local supply/bypass connections have a continuous front-copper path to the served pin. All 48 capacitor ground pads also have explicit front-copper paths to ground vias; their pad-to-pour settings use solid copper. The revised measurements include both supply traces and dedicated ground returns. See the [decoupling review](decoupling-review.md) and [measured lengths](decoupling-paths.csv). The ground-return and stackup decisions are recorded in the [layout review](layout-review.md).

All 32 daughterboard footprint types resolve from project-local libraries. All 116 component instances have models: 115 project-relative files and one embedded upstream STEP model. Six component instances use newly made nominal models (RP2350B, two DRV8837C devices and three TB6612FNG devices); these are identified in the [inventory](model-inventory.csv). USB-C now uses a detailed community STEP model. Its twelve distinct contact positions and four shell-tab locations were checked against the footprint, and its model replacement preserved the footprint geometry and connector position. The native 3D rendering was inspected for component placement and connector access. All 116 procurement entries and package reviews are recorded. Fabricated USB impedance, host mating tolerances, actual load/thermal performance and firmware consolidation remain open. These checks do not establish electrical performance or manufacturing readiness.

The [USB routing revision](usb-routing-review.md) reduces the resistor-to-MCU stubs from 14.407/15.731 mm to 2.652/0.987 mm, with no signal vias after the resistors. Native netlist comparison verifies that only the four equivalent U12 ESD-channel pins changed net membership. All external interfaces are preserved. Both 0201 resistor footprints use manufacturer-recommended lands and bundled models. Three extra ground-transfer vias support the USB launches.

The [connector review](connector-review.md) assigns exact WingTAT/JST/XUNPU/BOOMELE parts to thirteen connectors and verifies their hole patterns against manufacturer drawings. Together with the existing HRO USB-C part, all fourteen external connectors now have ordering codes. The actual host PCB confirms UART direction, I²C and power allocation; slot J3 lacks UART. This selection changes procurement fields only, with all electrical geometry and visible schematic content preserved by parsed-file comparison. Nominal host slot pitch is 26 mm; two populated cards have now been reviewed in a nominal host assembly; real cable bend space and seating tolerances remain open.

The subsequent [regulator capacitor selection](power-budget.md#local-capacitor-selection) raises C1/C2 from 1 µF to 4.7 µF and specifies Samsung CL10A475KO8NNNC for C1/C2/C10. Native parsed comparisons permit only those values and procurement fields; pads, nets, models, placement and copper are unchanged. The Power and MotionController pages and complete schematic PDF were regenerated and visually checked. The seven-page visual audit remains clear.

The [gate-driver supply correction](power-budget.md#gate-driver-supply-and-an-open-load-fuse) moves U11 and C64/C65 to the existing backplane 5 V supply before F1. Native netlists confirm exactly three changed pin assignments. All existing track geometry and all footprint geometry remain unchanged; 16 power-track segments and four vias are added. The five inner power zones and In2 ground each retain one connected filled region. ERC, DRC, parity and all seven page audits remain clear.

The [tool-output part selection](tool-parts-review.md) assigns exact JLCPCB codes to U9/U10/U11/Q1/Q2/D2. Manufacturer pin functions and package drawings were checked against the saved board. Parsed comparisons permit hidden procurement fields only and prove unchanged electrical and visual geometry.

The [passive selections](passive-parts-review.md) and [controller/axis-driver review](controller-parts-review.md) resolve 58 more BOM entries. The three axis drivers now use a Toshiba-specific fabrication outline, courtyard and nominal model; all pads, placement and copper are unchanged. The final ten capacitor entries and two fuses are now selected as well. Their exact values and procurement fields agree between schematic, PCB and BOM. Littelfuse-specific reflow lands replace the generic fuse footprint. Common fuse feeds are widened to 1.2 mm, with parallel power vias as recorded in the [load review](load-power-review.md). ERC, DRC, connectivity, parity and schematic visual checks pass on the saved result.

MotionDrivers and MotionGPIO are condensed from A3 to A4 with passives kept beside their circuits. A native netlist comparison preserves all 145 electrical pin groups. All seven final rendered pages were visually inspected and passed the geometric audit, including the added zero-length-wire check.

The DIN model now comes from the host library's WingTAT plug footprint. All 96 solder-tail centers align with the card, and two populated cards were rendered in the actual host J1/J2 positions using a documented nominal seating transform. This is a fit review, not a tolerance or harness qualification. The uniform USB pair estimates 89.96 ohms, with the checked back-layer routes continuously referenced to In2 ground; model limitations are recorded in the USB review.

The right-side power cleanup moves long 3.3 V and unfused 5 V feeds onto the outer signal layers. The inner-layer length of these feeds within x >= 123.5 mm falls from 90.053 to 6.212 mm. All component/pad geometry, net assignments, other-net tracks, capacitor ground returns and project rules are unchanged. All five supply zones and the ground plane each have one connected filled region. DRC, connectivity, parity, host-interface, supply-domain and decoupling checks pass on the saved result. New single-card and adjacent-card assembly views come from the native boards; the root README now presents both designs. See the [power map](power-domains.svg) and [connector review](connector-review.md).

The rail-probe revision adds four 0.8 mm SMD pads (5 V, 3.3 V and two grounds), six short tracks and three vias. Native comparison preserves every original component, pad and track, the 100 × 60 mm outline and project rules. All five supply regions and the inner ground region remain connected. The Power sheet adds direct T branches with no four-way junctions or visual-audit findings. The host logo artwork and back-face pin legends pass the unchanged silkscreen rules. The 32 footprint types include the new model-free copper pad; the existing 116-component BOM and model inventory are unchanged.

The original upstream passive 8-to-three-6-pin SPI splitter is included as a separate project with local footprints/models and explicit power/no-connect annotations. A native comparison preserves its connectors, pads, tracks, filled zone geometry and outline. Its ERC, DRC, connectivity and schematic parity all pass. `scripts/check_probe_access.py` verifies all four probe pads and the complete daughterboard-to-splitter pin mapping. See the [revision review](probe-and-label-review.md).

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
python scripts/check_probe_access.py
```

Inspect the DRC report: its default exit status does not fail for findings. The repository's root checker validates the host backplane; it does not replace these daughterboard checks.

[![Current PCB, copper pours hidden](layout-front.svg)](layout-front.svg)
