# System architecture

## Purpose

FAB Computer separates the reusable controller and power circuitry from the interfaces specific to each piece of HackerFab equipment. A new tool adds a daughter board; the backplane provides common infrastructure.

This is the design intent described in the progress report. The repository currently contains the backplane design and shared component libraries, with implementation and validation still in progress.

```mermaid
flowchart LR
    Supply["24 V DC input"] --> Power["Power conversion<br/>12 V · 5 V · 3.3 V"]
    Power --> MCU["RP2350B controller"]
    Supply --> Slots["Three DIN 41612 slots<br/>96 pins per connector"]
    Power --> Slots
    MCU <-->|"I²C · SPI · UART · GPIO"| Slots
    Slots --> Nano["Nanopositioner daughter board<br/>Planned; source not included"]
    Slots --> Sputter["Sputtering daughter board<br/>Planned; source not included"]
    Slots --> Future["Other tool interfaces"]
```

The diagram is a functional overview, not a wiring diagram. Use the KiCad schematics for exact connections and the [validation notes](validation.md) for incomplete circuitry.

## Backplane blocks

| Block | Present in the supplied design |
| --- | --- |
| Controller | RP2350B (`U5`) with W25Q128JVSIQ flash memory (`U7`), supporting crystal, decoupling, and debug signals |
| Expansion | Three DIN 41612 connectors (`J1`–`J3`, `9001-12961C00A`) |
| 12 V and 5 V rails | Two TPS5450DDAR regulators (`U1`, `U2`) |
| 3.3 V rail | AP2112K-3.3TRG1 (`U3`) |
| Input protection | Fuse (`F1`), DMP6023LE-13 MOSFET (`Q1`), TVS2700DRVR (`D7`), and BZT52C12 (`D8`) on `Protection.kicad_sch` |
| USB-related circuitry | USB-C receptacle (`J7`), USBLC6-2SC6 protection (`U4`), and TPS2116DRL power selection (`U6`); connectivity still requires review |
| Communication | Named nets for I²C0/1, SPI0/1 with slot chip selects, UART, and AUX signals |

J1, nearest the MCU, carries `/UART_RX` at A20 and `/UART_TX` at C20 (hardware UART0). J2 carries `/UART2_RX` at A20 and `/UART2_TX` at C20 (hardware UART1, GPIO37/36). Both positions remain unconnected on J3. The [V6 connector arrangement](connector-pinout.md) places SPI0 in columns 10–12, SPI1 in 21–23, and I²C in 16–17. AUX1–3 belong to J1, AUX4–6 to J2, and AUX7–9 to J3, with the former AUX10 position J3:C19 now NC. Use the current per-port pin table when designing a mating board.

## Daughter-board scope

The report describes two initial applications:

- **Nanopositioning:** move the existing development-board-based design toward an integrated daughter board, with motor-drive electronics specific to the tool.
- **Sputtering:** provide equipment interfaces such as RS-485 for a pump, RS-232 for a mass-flow controller, and conditioned analog measurement for a pressure gauge.

RS-485, RS-232, and 0–10 V analog interfaces are system requirements intended for daughter-board circuitry. They are not implemented interfaces on the current backplane. Firmware and daughter-board sources were not supplied.

## Next design milestones

- Complete schematic connectivity and resolve ERC findings.
- Review the connector pinout, component symbols, and footprints.
- Review the supplied 152-footprint PCB and 152-component schematic.
- Finish placement, routing, and design review.
- Prepare manufacturing outputs from a reviewed revision.
- Add daughter-board and firmware sources, then record bench validation.

The report's original checkpoint schedule is historical project context, not evidence that these steps are complete.
