# Backplane

Open [`HackerfabBackplane.kicad_pro`](HackerfabBackplane.kicad_pro) with KiCad 10.

| File | Role |
| --- | --- |
| `HackerfabBackplane.kicad_sch` | Root sheet, expansion connectors, and connections between circuit blocks |
| `12V_Buck.kicad_sch` | 12 V supply using TPS5450DDAR |
| `5V_Buck.kicad_sch` | 5 V supply using TPS5450DDAR |
| `3V3_LDO.kicad_sch` | 3.3 V supply using AP2112K-3.3TRG1 |
| `Microcontroller.kicad_sch` | RP2354B and supporting circuitry |
| `USB_Voltage_MUX.kicad_sch` | USB/supply selection using TPS2116DRL |
| `HackerfabBackplane.kicad_pcb` | Initial component placement; routing and outline unfinished |
| `fp-lib-table`, `sym-lib-table` | Project-local registration of the bundled custom libraries |

Keep this directory and `../libraries/` together when copying the project. Standard KiCad libraries are also required. Standard 3D models are optional for circuit editing but needed for a complete 3D preview.

See the [schematic previews](../../docs/schematics/README.md) and [validation baseline](../../docs/validation.md).
