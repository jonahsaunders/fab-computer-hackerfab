# Backplane

Open [`HackerfabBackplane.kicad_pro`](HackerfabBackplane.kicad_pro) with KiCad 10.

| File | Role |
| --- | --- |
| `HackerfabBackplane.kicad_sch` | Root sheet, expansion connectors, and connections between circuit blocks |
| `12V_Buck.kicad_sch` | 12 V supply using TPS5450DDAR |
| `5V_Buck.kicad_sch` | 5 V supply using TPS5450DDAR |
| `3V3_LDO.kicad_sch` | 3.3 V supply using AP2112K-3.3TRG1 |
| `Microcontroller.kicad_sch` | RP2350B, W25Q128JVSIQ flash memory, and supporting circuitry |
| `USB_Voltage_MUX.kicad_sch` | USB/supply selection using TPS2116DRL |
| `Protection.kicad_sch` | Input protection with a fuse, DMP6023LE-13 MOSFET, TVS2700DRVR, and BZT52C12 |
| `HackerfabBackplane.kicad_pcb` | Component placement, board outline, and routing |
| `HackerfabBackplane.kicad_dru` | Supplied custom design rules labeled JLCPCB 4-layer / 1 oz outer / 0.5 oz inner |
| `fp-lib-table`, `sym-lib-table` | Project-local registration of the bundled custom libraries |

Keep this directory and `../libraries/` together when copying the project. Standard KiCad libraries are also required. Standard 3D models are optional for circuit editing but needed for a complete 3D preview.

The 2026-11-04 import adds J2's independent UART through R56/R57. The design has 148 schematic components and 148 PCB footprints, 1,114 track segments, and 267 vias. The design files match the supplied archive after line-ending normalization. KiCad reports 15 ERC findings, 24 DRC errors and 362 warnings, zero unconnected items, and zero schematic/PCB parity findings under the supplied rule settings. This is development hardware.

See the [schematic previews](../../docs/schematics/README.md) and [validation baseline](../../docs/validation.md).

The [connector signal arrangement](../../docs/connector-pinout.md) uses the V6 layout, with SPI at opposite ends, UART0 on J1 nearest the MCU, and UART1 on J2 (schematic name `UART2`). J3 UART positions remain NC. Use the [per-port pin table](../../docs/connector-pinout.csv) for exact signal/NC assignments.
