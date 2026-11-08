# Rail probes, connector legends and encoder splitter

The daughterboard remains **100 × 60 mm** with the same four-layer stack, DIN96 interface and connector placements. The probe revision added four exposed copper pads, short sensing branches, connection vias and silkscreen artwork. The later slot-splitter revision changed SPI routing and C4 placement, as documented in the bus review. The vias are separate from the probe surfaces.

| Reference | Signal | Purpose |
| --- | --- | --- |
| TP1 | +5V_BP | Backplane 5 V, before the tool-load fuse F1 |
| TP2 | +3V3 | Local regulator output |
| TP3 | GND | Ground beside TP1, 1.90 mm center-to-center |
| TP4 | GND | Ground beside TP2, 1.15 mm center-to-center |

Each probe is a **0.8 mm round surface pad** on front copper with a solder-mask opening: no drilled hole, no solder-paste aperture and no fitted component. This is smaller than the host's 1.0 × 1.0 mm pads. Pads are labeled `5V`, `3V3` and `GND`; references are available in KiCad and the Power schematic. They are excluded from the BOM and placement files and need no 3D body model. No other rail or signal testpoints were added.

The probe symbols branch directly from the corresponding supply/ground wiring on the Power sheet. The connector-only top sheet is unchanged. The four branches introduce no four-way junctions or text/wire collisions.

## Silkscreen

The front uses the actual FAB and HackerFab vector artwork from the host, scaled into the existing open area. Connector pin legends are on the **back face**, aligned with the solder pads so housings do not hide them. The new text is 0.8 mm or larger with 0.12 mm strokes, preserving the project's existing DRC limits. The DIN table describes this card's actual contact allocation, including unused contacts and UART direction from the card's perspective.

Motor legends use the actual driver output names, not fixed supply polarities. XYZ pins are `BO1, BO2, AO2, AO1`; rotation pins are `OUT1–OUT4`. For the compact endstop legend, `S` means signal and `G` means ground. At J17, `H+` is the heater supply after the thermal cutoff. All other signal legends use their connector pin number.

| Front: probes and logo | Back: connector pin legends |
| --- | --- |
| ![Front rail probes and logo](probe-front.png) | ![Back-face connector legends](pin-labels-back.png) |

## Slot-mounted encoder splitter

The active splitter is now a **100 × 26 mm card in another backplane slot**. It uses SPI0 through the existing DIN96 contacts, with the motion card as master. Host GPIO16–21 must remain inputs without pulls. The original PH8-to-three-PH6 design is kept only as a reference; motion J6 is removed.

The three PH6 output pinouts remain **1 GND, 2 CS, 3 SCK, 4 MOSI, 5 MISO, 6 3.3 V**. The new board has its own 5 V-to-3.3 V regulator, three select pull-ups, FAB logo and back-face pin legends. Its TP1/TP2 are 5 V/3.3 V; TP3/TP4 are ground, each 1.8 mm from its rail pad. They use the same 0.8 mm surface-only footprint.

[Bus map](backplane-encoder-bus.md) · [Splitter 3D](encoder-backplane.png) · [Splitter schematic](encoder-backplane-schematic.pdf) · [Installed pair](host-adjacent-front.png)

`check_probe_access.py` checks all eight bare pads and compares the three PH6 ports against the original board. Both active cards pass ERC, DRC, connectivity and schematic parity; see [validation](validation.md).
