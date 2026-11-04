# Connector signal arrangement

The 2026-11-04 schematic and PCB extend the V6 arrangement with an independent UART on J2. SPI0 and SPI1 occupy opposite ends of the signal region, with I²C in the center and AUX contacts between groups. Both UARTs use column 20: J1 is hardware UART0 and J2 is hardware UART1 (named `UART2` in the schematic). J3 remains NC at A20/C20.

The tables and CSV below are the current reference. The retained [older connector diagram](images/connector-signal-plan.png) predates J2 UART and is historical only.

## Orientation and fixed contacts

Viewed from the PCB front with the MCU below, columns increase left to right. Row A faces the MCU, B is the middle row, and C is the far row. J1 is nearest the MCU, J2 is in the middle, and J3 is farthest. B10–B23 remain GND; all other power/ground contacts retain their previous assignments. Matching protocol groups occupy A/C pairs in each column.

## Signal positions

The table lists reserved functions. The [per-port CSV](connector-pinout.csv) gives the connected or NC status of every A/C signal position and its source jumper. NC contacts must remain unconnected on that connector.

| Column | A — MCU side | C — far side |
| --- | --- | --- |
| 10 | SPI0_CS3 | SPI0_CS2 |
| 11 | SPI0_MOSI | SPI0_CLK |
| 12 | SPI0_CS1 | SPI0_MISO |
| 13 | AUX7 | AUX4 |
| 14 | AUX1 | AUX9 |
| 15 | AUX8 | AUX6 |
| 16 | I2C0_SCL | I2C0_SDA |
| 17 | I2C1_SCL | I2C1_SDA |
| 18 | AUX5 | AUX3 |
| 19 | AUX2 | AUX10 |
| 20 | UART_RX | UART_TX |
| 21 | SPI1_CS3 | SPI1_CS2 |
| 22 | SPI1_MOSI | SPI1_CLK |
| 23 | SPI1_CS1 | SPI1_MISO |

Both SPI buses (including CS1–CS3) and both I²C buses connect to all three ports. Local signals are:

| Connector | AUX contacts | UART contacts |
| --- | --- | --- |
| J1 — nearest MCU | AUX1 A14; AUX2 A19; AUX3 C18 | UART0: RX A20 via R27/GPIO1; TX C20 via R26/GPIO0 |
| J2 — middle | AUX4 C13; AUX5 A18; AUX6 C15 | UART1: RX A20 via R57/GPIO37; TX C20 via R56/GPIO36 |
| J3 — farthest | AUX7 A13; AUX8 A15; AUX9 C14; AUX10 C19 | A20/C20 NC |

AUX10 is a connector-only net with no MCU jumper in the supplied design; its isolated-label warning remains. Treat it as reserved, not a working GPIO. RX/TX directions are from the MCU perspective. `UART2` is a board-level name, not an RP2350 hardware peripheral number.

## Routing status

The tracked PCB preserves the supplied routing: 1,114 track segments, 267 vias, and zero unconnected items. The audit saved corrected copper fills and updated the UART legend. KiCad reports 362 DRC warnings and zero DRC errors with the supplied custom rules; see the [validation baseline](validation.md). The [thermal-relief investigation](thermal-relief.md) documents the earlier November 1 source.

The connector pitch is 2.54 mm and signal pad diameter is 1.80 mm, leaving a 0.74 mm gap. One 0.20 mm trace with 0.20 mm clearance on each side fits that local gap. Complete routes still need to satisfy the board’s clearance, return-path, and signal-integrity requirements.

## Assigning AUX via nets in KiCad

The five vias documented as `GND` in the October 30 import now carry their respective AUX nets. Automatic net updates remain disabled on these five vias. The table shows their current positions and assignments; the latest source moves the AUX1/4/7 group.

| Via position (X, Y), mm | Current net | Automatic net update | Nearby jumper output |
| --- | --- | --- | --- |
| 126.75, 136.50 | `/AUX9` | Disabled | R52 pad 1: `/AUX9` |
| 128.25, 136.25 | `/AUX8` | Disabled | R51 pad 1: `/AUX8` |
| 116.50, 161.20 | `/AUX1` | Disabled | R44 pad 1: `/AUX1` |
| 116.50, 162.70 | `/AUX4` | Disabled | R45 pad 1: `/AUX4` |
| 116.50, 164.20 | `/AUX7` | Disabled | R46 pad 1: `/AUX7` |

To assign a net manually, select the via, open its properties with **E**, clear **Automatically update via nets**, and select the intended `/AUX…` net. A manually assigned net also needs a physical copper connection to the correct pad.

For a new signal via, start routing from the connector-side AUX jumper pad with **X**, then press **V**. The via inherits the routed signal's net. After editing the net or routing, refill zones with **B** and run DRC. A free-standing via placed over a copper zone can initially take that zone's net. See the [KiCad 10 routing and via-property documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html).

The import preserves these vias as supplied. The November 1 mounting-hole footprint change resolved the four previously reported GND unconnected items. Remaining design-rule findings require review.

## Validation

All 288 connector contacts were compared against the updated reference in both the exported schematic netlist and PCB. Power/ground, each port’s AUX allocation, both UARTs, and connector order match. The checks verify source jumper nets and the MCU endpoints of both UARTs. Five regression cases cover the current design, the obsolete J2 NC assignment, swapped UART directions, a wrong MCU endpoint, and a changed power pin.

```sh
python scripts/check_repo.py
python scripts/test_connector_pinout.py
python scripts/export_design.py
python scripts/check_connector_pinout.py --netlist build/backplane.xml
```

See the [validation baseline](validation.md) for remaining ERC/DRC findings.
