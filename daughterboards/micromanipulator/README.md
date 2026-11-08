# Micromanipulator daughterboard

Bare-component adaptation of [MicroManipulatorStepper](https://github.com/hacker-fab/MicroManipulatorStepper) for the FAB Computer backplane. The current schematic uses one RP2350B for XYZ motion, rotation, heater and vacuum control.

**Manual routing is complete: ERC, DRC, connectivity and schematic/PCB parity all pass. All 116 components now have ordering codes and package reviews. This remains a review draft; actual tool currents, thermal performance and final mating tolerances are not signed off for manufacture.**

## Open the project

Open [hardware/daughterboard/FabNanoDaughterboard.kicad_pro](hardware/daughterboard/FabNanoDaughterboard.kicad_pro) in **KiCad 10**. The project contains the seven-sheet schematic and the routed native PCB layout.

Keep this entire folder together. All 32 daughterboard footprint types and all 116 component models resolve locally or through embedded data. Four bare copper probe pads need no body models or purchased parts. Library names are preserved. Standard STEP models are bundled; RP2350B, DRV8837C and TB6612FNG use explicitly approximate models matched to their nominal packages. USB-C uses a detailed community STEP model for HRO TYPE-C-31-M-12. The DIN plug uses the WingTAT-specific STEP supplied with the host library. See the [model inventory](docs/model-inventory.csv). Install KiCad's standard symbol libraries for editing standard symbols.

| File or folder | Contents |
| --- | --- |
| [Root schematic](hardware/daughterboard/FabNanoDaughterboard.kicad_sch) | Only external connectors, ground symbols and six hierarchical subsheets |
| [PCB layout](hardware/daughterboard/FabNanoDaughterboard.kicad_pcb) | Routed 100 × 60 mm, four-layer RP2350B layout |
| [Rail probes and pin legends](docs/probe-and-label-review.md) | 0.8 mm surface pads for 5 V / 3.3 V and ground; logo and back-face connector labels |
| [Original encoder splitter](hardware/encoder-splitter/) | Separate passive PH8-to-three-PH6 board; original geometry and harness pinout |
| [Front routing preview](docs/layout-front.svg) and [back routing](docs/layout-back.svg) | Viewed from the top; copper pours hidden to expose the routes |
| [3D view](docs/board-3d.png) | Actual saved board with bundled component models |
| [Power domains](docs/power-domains.svg), [power plane](docs/power-plane.svg) and [ground plane](docs/ground-plane.svg) | Supply colors and filled native inner copper layers |
| [Installed card](docs/host-single-front.png) and [reverse view](docs/host-single-back.png) | Nominal assembly in the actual backplane; see the connector review for adjacent cards |
| [Schematic PDF](docs/schematic-review.pdf) | Current seven-page schematic review |
| [Schematic previews](docs/schematics/) | Current SVG and PNG pages |
| [Controller decision](docs/controller-decision.txt) | Single-RP2350B resource allocation and migration requirements |
| [Pin allocation](docs/controller-pin-allocation.csv) | Current RP2350B GPIO map |
| [Connector table](docs/connectors.csv) and [wiring table](docs/wiring.csv) | External interfaces and original encoder harness pin order |
| [Connector review](docs/connector-review.md) | Exact connector parts, manufacturer hole-pattern checks and host slot compatibility |
| [Logic supply budget](docs/power-budget.md) | Regulator package choice, current allocation and thermal estimate |
| [Tool-output parts](docs/tool-parts-review.md) | Exact rotation-driver, gate-driver, MOSFET and diode selections with pin/land checks |
| [Passive parts](docs/passive-parts-review.md) | Exact resistor and small-capacitor selections with package checks |
| [Controller and axis-driver parts](docs/controller-parts-review.md) | Flash, clock, inductor, switches, LED and corrected Toshiba package |
| [BOM](docs/bom.csv) | Exact ordering codes for all 116 components; confirm inventory when ordering |
| [Load power review](docs/load-power-review.md) | Source-heater estimate, fuse selections and current limits |
| [Validation](docs/validation.md) | Current ERC, DRC, parity and visual-audit results |
| [USB routing review](docs/usb-routing-review.md) | Local termination resistors, coupled main pair and measured source stubs |
| [Decoupling review](docs/decoupling-review.md) | All 48 capacitor returns, direct supply paths, measured lengths and close-ups |
| [Sources](docs/sources.txt) and [licenses](licenses/) | Upstream references and retained notices |

## Fixed interfaces and remaining work

The daughterboard uses the existing DIN96 contacts and perpendicular mating arrangement, with backplane **12 V and 5 V** and local **5 V to 3.3 V** conversion. No backplane contacts are added. Use a host slot with UART: J1 or J2 in the supplied host revision. The existing XYZ PH8 and rotation encoder connector pin orders are preserved.

The host's 5 V rail passes through a **2.5 A shared TPS2116 mux**. The provisional tool allocation is at most 2 A and must be reduced for host, logic and other-card consumption. Source-heater geometry estimates 1.40 A at 5.25 V; the checked repository does not specify rotation or pump currents. Full simultaneous operation therefore needs actual load verification. See the [power limits](docs/load-power-review.md).

The PCB stack is **front signal / inner power / inner ground / back signal**. The PCB has 116 components, SMD capacitors and perimeter connectors. All 35 checked local supply paths run directly to their served pins on front copper. All 48 capacitor ground pads have explicit local via returns; pad connections to ground pours use solid copper. Ground pours, 57 additional stitching vias and an unbroken inner ground region provide the returns. Eleven exposed-pad vias are specified as filled and capped. See the [stackup and layout review](docs/layout-review.md).

The schematic has USB-C and all external connectors on its top level. USB protection, CC termination and VBUS sensing are in the USBInterface child sheet; the remaining circuitry is in Power, MotionController, MotionGPIO, MotionDrivers and ToolOutputs. The final two large sheets have been condensed to A4 while preserving every electrical pin group. The USB engineering screen estimates 89.96 ohms for the uniform main pair and verifies ground beneath its checked back-layer segments. Nominal populated-host views are included in the connector review. Fabricator impedance confirmation, actual load/thermal measurements, physical host mating and firmware consolidation remain open. No firmware binaries or fabrication files are included.

## Checks

The current schematic passes KiCad 10.0.6 ERC with four-way-junction checking enabled. The board's 116 fitted components and four bare probe pads match the schematic with zero schematic-parity findings. All seven rendered pages passed the text/wire, text/text, wire-crossing and overlapping-segment checks. A separate hierarchy check enforces the connector-only top page. The included original splitter also passes ERC and DRC/parity. See the [validation notes](docs/validation.md) for the current checks.

Local machine-readable reports belong in the ignored `build/` folder. To repeat the schematic visual audit from this folder:

```sh
mkdir -p build
python scripts/check_schematic_visuals.py
python scripts/check_hierarchy.py
```

The project was imported and converted to the single-controller design on 2026-11-07. Native design files, review images and validation notes are maintained together in this folder.
