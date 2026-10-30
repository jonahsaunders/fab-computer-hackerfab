# Backplane

Open [`HackerfabBackplane.kicad_pro`](HackerfabBackplane.kicad_pro) with KiCad 10.

| File | Role |
| --- | --- |
| `HackerfabBackplane.kicad_sch` | Root sheet, expansion connectors, and connections between circuit blocks |
| `12V_Buck.kicad_sch` | 12 V supply using TPS5450DDAR |
| `5V_Buck.kicad_sch` | 5 V supply using TPS5450DDAR |
| `3V3_LDO.kicad_sch` | 3.3 V supply using AP2112K-3.3TRG1 |
| `Microcontroller.kicad_sch` | RP2354B, W25Q128JVSIQ flash memory, and supporting circuitry |
| `USB_Voltage_MUX.kicad_sch` | USB/supply selection using TPS2116DRL |
| `Protection.kicad_sch` | Input protection with a fuse, DMP6023LE-13 MOSFET, TVS2700DRVR, and BZT52C12 |
| `HackerfabBackplane.kicad_pcb` | Component placement, board outline, and partial routing |
| `fp-lib-table`, `sym-lib-table` | Project-local registration of the bundled custom libraries |

Keep this directory and `../libraries/` together when copying the project. Standard KiCad libraries are also required. Standard 3D models are optional for circuit editing but needed for a complete 3D preview.

The 2026-10-30 update contains 144 schematic components and 144 PCB footprints, with 788 track segments and 193 vias. KiCad reports zero schematic/PCB parity findings and 41 unconnected PCB items; routing and design review remain.

See the [schematic previews](../../docs/schematics/README.md) and [validation baseline](../../docs/validation.md).

The [connector signal arrangement](../../docs/connector-pinout.md) uses the V6 layout, with SPI at opposite ends and UART only on J1, nearest the MCU. Use the [per-port pin table](../../docs/connector-pinout.csv) for exact signal/NC assignments.
