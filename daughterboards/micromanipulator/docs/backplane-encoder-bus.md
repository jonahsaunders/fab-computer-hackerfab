# Encoder SPI through the existing backplane

The 100 × 26 mm encoder card replaces the original cable-connected 8-to-three-6-pin splitter. It fits the same DIN96 sockets as the 100 × 60 mm motion card. The backplane PCB, connector contact assignments and motion-card outline are unchanged. Use host J1 or J2 for motion; the encoder card can occupy any remaining slot.

| Signal | Existing DIN contact | Motion RP2350B GPIO | Source resistor |
| --- | --- | --- | --- |
| CS1 | A12 / SPI0_CS1 | 44 | R52, 33 Ω |
| CS2 | C10 / SPI0_CS2 | 45 | R53, 33 Ω |
| CS3 | A10 / SPI0_CS3 | 46 | R54, 33 Ω |
| SCK | C11 / SPI0_CLK | 2 | R55, 33 Ω |
| MOSI | A11 / SPI0_MOSI | 3 | R56, 33 Ω |
| MISO | C12 / SPI0_MISO | 0 | Direct input |

These six contacts are shared across all three slots and connected to the host through R32–R37. **The motion card is the only SPI0 master. Host GPIO16–21 must remain inputs with no pulls; no other card may drive SPI0 or use its three selects.** SPI1 is unaffected. See [firmware integration](../firmware/README.md).

The splitter takes existing 5 V contacts and makes local 3.3 V with an AP2112M SO-8 regulator. No 3.3 V backplane contact was added. Three 10 kΩ pull-ups keep sensor chip selects inactive during controller reset. The encoder's three PH6 ports preserve the original pin order: **1 GND, 2 CS, 3 SCK, 4 MOSI, 5 MISO, 6 3.3 V**. Each connects to the existing sensor PCB. Rotation encoder J12 remains on the motion card and retains its separate pinout.

The motion card's PH8 J6 and its three CS pull-ups were removed. GPIO44–46 replace GPIO20–22 for shorter source-resistor routes. The slow supply-sense capacitor C4 moved beside its divider; no MCU decoupler moved. C24's supply-plane feed was relocated while retaining its direct capacitor-to-pin trace. A short endstop crossing moved to the back layer. Existing motor, tool, USB and host UART/I²C pin assignments are preserved.

Both cards use front signal / inner power / inner ground / back signal. Long SPI traces run over the inner ground layer; the splitter keeps a continuous ground plane, compact local regulator capacitors and ground stitching. Routing is manual. Begin at 1 MHz and inspect clock/data quality with the actual sensor cables; 8 MHz from the original firmware is not qualified for this new path. The shared slot stubs and the remotely driven MISO remain signal-integrity considerations.

At a provisional 60 mA sensor allocation, the splitter LDO dissipates about (5−3.3)×0.06 = **0.10 W**. This is a planning allocation, not a measured load or an added power allowance. All sensors, host logic and tool loads share the host's 2.5 A 5 V mux limit; see [load limits](load-power-review.md).

[Assembled front](host-adjacent-front.png) · [Reverse](host-adjacent-back.png) · [Splitter schematic](encoder-backplane-schematic.pdf) · [Splitter PCB](encoder-backplane.png)

The assembly render aligns each card's actual DIN A1 origin with its host socket and uses the existing nominal mating-model transform. It shows body placement and connector direction. Seating tolerances, mating housings, cable bend radii and physical access still require a real fit check.
