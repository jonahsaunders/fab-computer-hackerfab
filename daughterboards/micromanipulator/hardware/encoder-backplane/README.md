# Slot-mounted encoder splitter

Open [EncoderBackplane.kicad_pro](EncoderBackplane.kicad_pro) in KiCad 10. This **100 × 26 mm, four-layer** card plugs into an unused backplane slot and connects three existing XYZ magnetic-encoder boards. Keep the sibling `libraries` directory with it.

The motion card reads the encoders through the existing shared SPI0 bus. The host CPU must leave GPIO16–21 as inputs without pulls; SPI0 and all three selects are reserved for this pair. The host board is unchanged. See the [bus map and requirements](../../docs/backplane-encoder-bus.md).

J1/J2/J3 are JST B6B-PH-K-S(LF)(SN), **LCSC C131342**, matching the original PH6 sensor wiring: 1 GND, 2 CS, 3 SCK, 4 MOSI, 5 MISO, 6 3.3 V. Top-entry plugs project from the component face; the connectors sit at the exposed edge. Local KiCad models show their direction and nominal bodies.

J4 is the same DIN96 male right-angle interface as the motion card. An AP2112M-3.3 uses backplane 5 V; no extra contact or development module is used. TP1/TP2 probe 5 V/3.3 V, with TP3/TP4 grounds. All are 0.8 mm surface copper pads without holes or paste. Eleven fitted parts plus four bare probe pads.

[Schematic PDF](../../docs/encoder-backplane-schematic.pdf) · [3D view](../../docs/encoder-backplane.png) · [BOM](../../docs/encoder-backplane-bom.csv) · [Validation](../../docs/validation.md)
