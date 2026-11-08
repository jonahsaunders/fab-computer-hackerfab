# Original splitter — source reference only

The active design is now the [slot-mounted encoder card](../encoder-backplane/). This original 36 × 36 mm PH8-to-three-PH6 project is retained for provenance and sensor pinout comparison. Its PH8 connector is not used by the current motion card, which no longer has J6.

# Original XYZ SPI splitter

Open `EncoderBoard.kicad_pro` in KiCad 10. This is HackerFab's existing 36 × 36 mm passive breakout: one PH8 input (J4) and three PH6 outputs (J1–J3). Connect daughterboard J6 to J4 pin-for-pin. The board carries no encoder ICs or development modules.

See the [pin table and import review](../../docs/probe-and-label-review.md#included-original-spi-splitter). Connector positions, pinout, copper and outline are retained from [MicroManipulatorStepper](https://github.com/hacker-fab/MicroManipulatorStepper/tree/fa9a1f8e6d5365c6d5d5f31054d4f2c95aff8f6a/electronics). Models and footprints resolve within the micromanipulator folder. KiCad's standard symbol libraries are used for editing; the schematic contains its cached symbols.

Only local library/model paths, empty datasheet metadata, the daughterboard J6 caption and ERC annotations were normalized. Both ERC and DRC/parity pass. Mounting pads remain electrically isolated as upstream. The original DIYLC distribution drawing is included alongside the KiCad files. Attribution and terms are in [the retained MIT license](../../licenses/MicroManipulatorStepper-MIT.txt).
