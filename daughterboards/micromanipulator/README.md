# Micromanipulator daughterboard

Bare-component adaptation of [MicroManipulatorStepper](https://github.com/hacker-fab/MicroManipulatorStepper) for the FAB Computer backplane. The current schematic uses one RP2350B for XYZ motion, rotation, heater and vacuum control.

**Manual routing is complete: ERC, DRC, connectivity and schematic/PCB parity all pass. This remains a review draft; procurement, load/thermal limits and final host mating checks are not signed off for manufacture.**

## Open the project

Open [hardware/daughterboard/FabNanoDaughterboard.kicad_pro](hardware/daughterboard/FabNanoDaughterboard.kicad_pro) in **KiCad 10**. The project contains the six-sheet schematic and the routed native PCB layout.

Keep this entire folder together. All 30 used footprint types and all 116 placed models resolve locally or through embedded data. Library names are preserved. Standard STEP models are bundled; RP2350B and DRV8837C use explicitly approximate models where the installed model was missing. USB-C uses a detailed community STEP model for HRO TYPE-C-31-M-12. See the [model inventory](docs/model-inventory.csv). Install KiCad's standard symbol libraries for editing standard symbols.

| File or folder | Contents |
| --- | --- |
| [Root schematic](hardware/daughterboard/FabNanoDaughterboard.kicad_sch) | All external connectors and five hierarchical subsheets |
| [PCB layout](hardware/daughterboard/FabNanoDaughterboard.kicad_pcb) | Routed 100 × 60 mm, four-layer RP2350B layout |
| [Front routing preview](docs/layout-front.svg) and [back routing](docs/layout-back.svg) | Viewed from the top; copper pours hidden to expose the routes |
| [3D view](docs/board-3d.png) | Actual saved board with bundled component models |
| [Power plane](docs/power-plane.svg) and [ground plane](docs/ground-plane.svg) | Filled native inner copper layers |
| [Schematic PDF](docs/schematic-review.pdf) | Current six-page schematic review |
| [Schematic previews](docs/schematics/) | Current SVG and PNG pages |
| [Controller decision](docs/controller-decision.txt) | Single-RP2350B resource allocation and migration requirements |
| [Pin allocation](docs/controller-pin-allocation.csv) | Current RP2350B GPIO map |
| [Connector table](docs/connectors.csv) and [wiring table](docs/wiring.csv) | External interfaces and original encoder harness pin order |
| [Logic supply budget](docs/power-budget.md) | Regulator package choice, current allocation and thermal estimate |
| [BOM](docs/bom.csv) | Current schematic parts; supplier selection and assembly review are incomplete |
| [Validation](docs/validation.md) | Current ERC, DRC, parity and visual-audit results |
| [Decoupling review](docs/decoupling-review.md) | All 48 capacitor returns, direct supply paths, measured lengths and close-ups |
| [Sources](docs/sources.txt) and [licenses](licenses/) | Upstream references and retained notices |

## Fixed interfaces and remaining work

The daughterboard uses the existing DIN96 contacts and perpendicular mating arrangement, with backplane **12 V and 5 V** and local **5 V to 3.3 V** conversion. No backplane contacts are added. Use a host slot with UART: J1 or J2 in the supplied host revision. The existing XYZ PH8 and rotation encoder connector pin orders are preserved.

The PCB stack is **front signal / inner power / inner ground / back signal**. The PCB has 116 components, SMD capacitors and perimeter connectors. All 35 checked local supply paths run directly to their served pins on front copper. All 48 capacitor ground pads have explicit local via returns; pad connections to ground pours use solid copper. Ground pours, 54 additional stitching vias and an unbroken inner ground region provide the returns. Eleven exposed-pad vias are specified as filled and capped. See the [stackup and layout review](docs/layout-review.md).

The schematic has USB-C and all external connectors on its top level. Exact supplier selections, USB signal-integrity confirmation, load/thermal limits, host mating tolerances and firmware consolidation remain open. No firmware binaries or fabrication files are included.

## Checks

The current schematic passes KiCad 10.0.6 ERC with four-way-junction checking enabled. The board matches the current 116-component schematic with zero schematic-parity findings. All six rendered pages passed the text/wire, text/text, wire-crossing and overlapping-segment checks. See the [validation notes](docs/validation.md) for the current checks.

Local machine-readable reports belong in the ignored `build/` folder. To repeat the schematic visual audit from this folder:

```sh
mkdir -p build
python scripts/check_schematic_visuals.py
```

The project was imported and converted to the single-controller design on 2026-11-07. The routed revision is available in the draft pull request; it has not been merged into the repository's main branch.
