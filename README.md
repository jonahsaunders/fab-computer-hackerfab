# FAB Computer · HackerFab

A modular control platform for HackerFab equipment: one backplane for power and control, with interchangeable daughter boards for each tool.

**Status: hardware in development · KiCad 10 · three expansion slots**

![KiCad preview of the FAB Computer backplane](docs/images/backplane-2026-11-05.png)

*Preview of the supplied PCB; design-rule review remains before a manufacturing release.*

## The idea

Keep the microcontroller, power supplies, and common interfaces on a reusable backplane. Put tool-specific electronics on daughter boards so future teams can extend a system without redesigning its core. Initial applications described in the project report are nanopositioning and sputtering equipment.

The current backplane sources contain an **RP2350B**, three **96-pin DIN 41612 connectors**, **12 V and 5 V buck regulators**, a **3.3 V LDO**, USB-C and power-selection circuitry, and an input-protection sheet. The intended input supply is **24 V DC**. Shared signals include two I²C buses, two SPI buses, two independent UARTs, and auxiliary GPIO.

## Open the design

1. Install **KiCad 10** with its standard symbol and footprint libraries. The supplied files were saved in KiCad 10 and checked with 10.0.6.
2. Clone the entire repository:

   ```sh
   git clone https://github.com/jonahsaunders/fab-computer-hackerfab.git
   ```

3. Open [`hardware/backplane/HackerfabBackplane.kicad_pro`](hardware/backplane/HackerfabBackplane.kicad_pro) in KiCad's project manager.
4. Open the schematic or PCB from the project manager. The custom libraries are registered in the project's library tables using relative paths; no global library setup is needed for them.

For a browser-only look, start with the [schematic previews](docs/schematics/README.md).

## What's here

| Location | Contents |
| --- | --- |
| [`hardware/backplane/`](hardware/backplane/) | KiCad project, root schematic, six subsheets, PCB, custom design rules, and project library tables |
| [`hardware/libraries/`](hardware/libraries/) | Seven custom symbol libraries and 24 custom footprints, including embedded models where supplied |
| [`daughterboards/micromanipulator/`](daughterboards/micromanipulator/) | Single-RP2350B daughterboard: seven-sheet schematic, manually routed four-layer PCB, local libraries and review previews |
| [`docs/architecture.md`](docs/architecture.md) | System concept, circuit blocks, and scope of future daughter boards |
| [`docs/connector-pinout.md`](docs/connector-pinout.md) | Jumper-based signal order, paired protocols, pin table, and routing guide |
| [`docs/schematics/`](docs/schematics/) | Seven SVG schematic previews exported from the source |
| [`docs/validation.md`](docs/validation.md) | Historical November 4 validation and reproduction steps |
| [`docs/thermal-relief.md`](docs/thermal-relief.md) | Copper-pour diagnosis, affected pads, and temporary-copy experiments |
| [`docs/provenance.md`](docs/provenance.md) | Source archives, background reference, and cleanup details |
| [`scripts/`](scripts/) | Repository checks and reproducible preview/check exports |

## Design images

These previews are exported from the current KiCad files. Select a schematic image to open it at full size.

### Backplane schematic

[![Backplane root schematic](docs/schematics/HackerfabBackplane.svg)](docs/schematics/HackerfabBackplane.svg)

### Microcontroller

[![Microcontroller schematic](docs/schematics/HackerfabBackplane-Microcontroller.svg)](docs/schematics/HackerfabBackplane-Microcontroller.svg)

### 12 V buck regulator

[![12 V buck regulator schematic](docs/schematics/HackerfabBackplane-12V%20Buck%20Regulator.svg)](docs/schematics/HackerfabBackplane-12V%20Buck%20Regulator.svg)

### 5 V buck regulator

[![5 V buck regulator schematic](docs/schematics/HackerfabBackplane-5V%20Buck%20Regulator.svg)](docs/schematics/HackerfabBackplane-5V%20Buck%20Regulator.svg)

### 3.3 V LDO

[![3.3 V LDO schematic](docs/schematics/HackerfabBackplane-3V3%20LDO.svg)](docs/schematics/HackerfabBackplane-3V3%20LDO.svg)

### USB voltage mux

[![USB voltage mux schematic](docs/schematics/HackerfabBackplane-USB%20Voltage%20MUX.svg)](docs/schematics/HackerfabBackplane-USB%20Voltage%20MUX.svg)

### Input protection

[![Input protection schematic](docs/schematics/HackerfabBackplane-Protection.svg)](docs/schematics/HackerfabBackplane-Protection.svg)

## Current state

The repository includes the **backplane hardware and its libraries**, plus the [micromanipulator daughterboard](daughterboards/micromanipulator/). The daughterboard has a seven-sheet schematic and manually routed 100 × 60 mm PCB using one RP2350B. ERC, DRC, connectivity and schematic/PCB parity checks pass; component selection and electrical/mechanical review remain in progress. Firmware, fabrication outputs and bench-test results are not included.

The latest archives were imported on **2026-11-05**. They add four **2.2 kΩ I²C pullups (R58–R61)**, mark **J3:C19 as NC**, and replace **H1–H4** with grounded `MountingHole_3.2mm_M3_Pad_Via` footprints. J1 uses hardware UART0; J2 uses UART1 (named `UART2` in the schematic); J3's UART positions remain NC. The design has **152 components/footprints**, **1,143 track segments**, and **271 vias**.

All 41 backplane design, library, and rule files match the supplied archives after line-ending normalization. Backplane circuitry, routing, copper fills, and component metadata are preserved as supplied. The [validation notes](docs/validation.md) describe the historical November 4 revision. The design remains in development.

## Working on the project

The connector signal assignments use the V6 layout, with SPI buses at opposite ends and matching protocol groups across rows A/C. J1 is nearest the MCU and carries AUX1–3 plus UART; J2 carries AUX4–6 plus the second UART; J3 carries AUX7–9 with the former AUX10 position C19 now NC. Use the [current pin table and diagrams](docs/connector-pinout.md) when routing or designing daughter boards. Power and ground assignments are preserved.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing hardware. Run the lightweight repository checks with Python 3.10 or newer:

```sh
python scripts/check_repo.py
```

To regenerate the schematic previews, board image, and local ERC/DRC reports with KiCad 10:

```sh
python scripts/export_design.py
```

The checks verify repository structure and library portability; they do not certify the electrical design.

## Credits and license

Backplane and library sources supplied by **Jonah Saunders**. Project background is drawn from *Hackerfab Progress Report 1 - FAB Computer*, with sections by **Jonah Saunders** and **Jacob Rohozen**. The report was used as background and is not redistributed here.

A project license has not yet been specified. Existing attribution within supplied files is preserved.
