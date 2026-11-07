# Micromanipulator daughterboard

Bare-component adaptation of [MicroManipulatorStepper](https://github.com/hacker-fab/MicroManipulatorStepper) for the FAB Computer backplane. The current schematic uses one RP2350B for XYZ motion, rotation, heater and vacuum control.

**Work in progress: schematic and PCB now both use one RP2350B. Manual routing is incomplete: 39 unconnected items remain. Do not manufacture this layout.**

## Open the project

Open [hardware/daughterboard/FabNanoDaughterboard.kicad_pro](hardware/daughterboard/FabNanoDaughterboard.kicad_pro) in **KiCad 10**. The project contains the current six-sheet schematic and the unfinished native PCB layout.

Keep this entire folder together. Custom symbols, footprints and approximate review models live in [hardware/libraries/](hardware/libraries/) and resolve through project-relative library tables. Install KiCad's standard libraries and 3D models as well. The review models are approximate body envelopes for the earlier layout; footprint and model review remains unfinished.

| File or folder | Contents |
| --- | --- |
| [Root schematic](hardware/daughterboard/FabNanoDaughterboard.kicad_sch) | All external connectors and five hierarchical subsheets |
| [PCB layout](hardware/daughterboard/FabNanoDaughterboard.kicad_pcb) | Current 100 × 60 mm, four-layer RP2350B layout; routing unfinished |
| [Front layout preview](docs/layout-incomplete.svg) and [back copper](docs/layout-back-incomplete.svg) | Current unfinished PCB, viewed from the top |
| [Schematic PDF](docs/schematic-review.pdf) | Current six-page schematic review |
| [Schematic previews](docs/schematics/) | Current SVG and PNG pages |
| [Controller decision](docs/controller-decision.txt) | Single-RP2350B resource allocation and migration requirements |
| [Pin allocation](docs/controller-pin-allocation.csv) | Current RP2350B GPIO map |
| [Connector table](docs/connectors.csv) and [wiring table](docs/wiring.csv) | External interfaces and original encoder harness pin order |
| [BOM](docs/bom.csv) | Current schematic parts; supplier selection and assembly review are incomplete |
| [Validation](docs/validation.md) | Current ERC, DRC, parity and visual-audit results |
| [Sources](docs/sources.txt) and [licenses](licenses/) | Upstream references and retained notices |

## Fixed interfaces and remaining work

The daughterboard uses the existing DIN96 contacts and perpendicular mating arrangement, with backplane **12 V and 5 V** and local **5 V to 3.3 V** conversion. No backplane contacts are added. Use a host slot with UART: J1 or J2 in the supplied host revision. The existing XYZ PH8 and rotation encoder connector pin orders are preserved.

The required PCB stack is **front signal / inner power / inner ground / back signal**. The PCB has 116 components, SMD capacitors and perimeter connectors. Manual signal routing, final return-path review, connector accessibility checks and footprint/3D verification remain open. The schematic has USB-C and all external connectors on its top level. Firmware consolidation and electrical, thermal and mechanical validation remain open. No firmware binaries or fabrication files are included in this folder.

## Checks

The current schematic passes KiCad 10.0.6 ERC with four-way-junction checking enabled. The board matches the current 116-component schematic with zero schematic-parity findings. All six rendered pages passed the text/wire, text/text, wire-crossing and overlapping-segment checks. See the [validation notes](docs/validation.md) for the current checks.

Local machine-readable reports belong in the ignored `build/` folder. To repeat the schematic visual audit from this folder:

```sh
mkdir -p build
python scripts/check_schematic_visuals.py
```

The project was imported and the PCB converted to the single-controller design on 2026-11-07. This draft is being updated as routing progresses.
