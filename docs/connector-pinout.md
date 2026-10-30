# Connector signal arrangement

The supplied 2026-10-30 schematic and PCB implement the V6 pin arrangement. SPI0 and SPI1 occupy opposite ends of the signal region, with I²C in the center and AUX contacts between the communication groups. UART RX/TX stay together in column 20 on J1 only.

![Exact signal pin assignments on all three connectors](images/connector-signal-plan.png)

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
| J1 — nearest MCU | AUX1 A14; AUX2 A19; AUX3 C18 | RX A20; TX C20 |
| J2 — middle | AUX4 C13; AUX5 A18; AUX6 C15 | A20/C20 NC |
| J3 — farthest | AUX7 A13; AUX8 A15; AUX9 C14; AUX10 C19 | A20/C20 NC |

AUX10 is a connector-only net with no MCU jumper in the supplied design; its isolated-label warning remains.

## Routing status

The tracked PCB is the supplied partial layout: 788 track segments, 193 vias, and 41 unconnected items. The earlier V6 routing study established a possible route for the pin order; the imported board preserves the user’s own routing progress.

The connector pitch is 2.54 mm and signal pad diameter is 1.80 mm, leaving a 0.74 mm gap. One 0.20 mm trace with 0.20 mm clearance on each side fits that local gap. Complete routes still need to satisfy the board’s clearance, return-path, and signal-integrity requirements.

## Assigning AUX via nets in KiCad

The imported board contains five vias beside the AUX jumper banks that are currently assigned to `GND`. The two top-bank vias have automatic net updates enabled; the three left-bank vias have that option disabled already.

| Via position (X, Y), mm | Current net | Automatic net update | Nearby jumper output |
| --- | --- | --- | --- |
| 130.00, 139.75 | GND | Enabled | R52 pad 1: `/AUX9` |
| 131.00, 138.00 | GND | Enabled | R51 pad 1: `/AUX8` |
| 116.50, 160.50 | GND | Disabled | R44 pad 1: `/AUX1` |
| 116.50, 162.00 | GND | Disabled | R45 pad 1: `/AUX4` |
| 116.50, 163.50 | GND | Disabled | R46 pad 1: `/AUX7` |

To assign a net manually, select the via, open its properties with **E**, clear **Automatically update via nets**, and select the intended `/AUX…` net. The nearby-jumper column identifies the adjacent signal; the via still needs a trace connecting it to the correct pad.

For a new signal via, start routing from the connector-side AUX jumper pad with **X**, then press **V**. The via inherits the routed signal's net. After editing the net or routing, refill zones with **B** and run DRC. A free-standing via placed over a copper zone can initially take that zone's net. See the [KiCad 10 routing and via-property documentation](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html).

The import preserves these vias as supplied. The routing and via-net assignments remain work in progress.

## Validation

All 288 connector contacts were compared against the V6 reference in both the exported schematic netlist and PCB. Power/ground, each port’s AUX allocation, UART only on J1, and connector order match. The bundled checks also verify the source jumper nets.

```sh
python scripts/check_repo.py
python scripts/export_design.py
python scripts/check_connector_pinout.py --netlist build/backplane.xml
```

See the [validation baseline](validation.md) for remaining ERC/DRC findings.
