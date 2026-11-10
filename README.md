# FAB Computer · HackerFab

A reusable power and control backplane with plug-in boards for HackerFab tools.

[Backplane](#backplane) · [Motion controller](#motion-controller) · [Encoder splitter](#encoder-splitter) · [Plug-in assembly](#plug-in-assembly)

## Boards

### Backplane

[Full-size board render](docs/images/backplane.png) · [L3 inductor close-up](docs/images/backplane-regulator.png)

<a href="docs/images/backplane.png"><img src="docs/images/backplane.png" width="620" alt="Component side of the updated FAB Computer backplane with three DIN96 slots"></a>

*KiCad 3D render of the November 10 backplane layout with revised 12 V and 5 V buck regulator placement.*

### Motion controller

<a href="daughterboards/micromanipulator/docs/board-3d.png"><img src="daughterboards/micromanipulator/docs/board-3d.png" width="620" alt="Motion controller card with its DIN96 connector, USB-C port and motor outputs"></a>

### Encoder splitter

<a href="daughterboards/micromanipulator/docs/encoder-backplane.png"><img src="daughterboards/micromanipulator/docs/encoder-backplane.png" width="620" alt="Encoder splitter card with its DIN96 connector and three encoder ports"></a>

## Plug-in assembly

<a href="daughterboards/micromanipulator/docs/host-adjacent-front.png"><img src="daughterboards/micromanipulator/docs/host-adjacent-front.png" width="700" alt="The motion controller and encoder splitter plugged into the backplane"></a>

*KiCad render with the motion controller in J1 and the encoder splitter in J2.* [Reverse view](daughterboards/micromanipulator/docs/host-adjacent-back.png)

## Design files

| Board | Purpose | Open in KiCad 10 |
| --- | --- | --- |
| Backplane | RP2350B host, three DIN96 slots, shared power and buses | [Project](hardware/backplane/HackerfabBackplane.kicad_pro) · [Schematics](docs/schematics/README.md) |
| Motion controller | Bare RP2350B; XYZ motion, rotation, heater, vacuum and USB-C; 100 × 60 mm | [Project](daughterboards/micromanipulator/hardware/daughterboard/FabNanoDaughterboard.kicad_pro) · [Schematic](daughterboards/micromanipulator/docs/schematic-review.pdf) |
| Encoder splitter | Existing backplane SPI0 to three original PH6 sensor interfaces; 100 × 26 mm | [Project](daughterboards/micromanipulator/hardware/encoder-backplane/EncoderBackplane.kicad_pro) · [Schematic](daughterboards/micromanipulator/docs/encoder-backplane-schematic.pdf) |

Clone the entire repository and keep the local libraries together. Both daughtercards are four-layer designs with no development modules.

Use host **J1 or J2 for motion**, and another slot for the splitter. **The motion controller owns SPI0; host GPIO16–21 must remain inputs with no pulls.** Other cards must leave SPI0 undriven. See the [bus map and firmware requirements](daughterboards/micromanipulator/docs/backplane-encoder-bus.md).

The two daughtercards pass ERC, DRC, connectivity and schematic parity. Physical fit, actual load/thermal measurements, encoder signal integrity and firmware integration remain open. The backplane has its [separate validation record](docs/validation.md). All 5 V loads share the host's **2.5 A power-mux limit**; see [load limits](daughterboards/micromanipulator/docs/load-power-review.md).

[Card details and renders](daughterboards/micromanipulator/README.md) · [Card validation](daughterboards/micromanipulator/docs/validation.md) · [Architecture](docs/architecture.md) · [Connector pinout](docs/connector-pinout.md) · [Contributing](CONTRIBUTING.md)

Backplane sources: **Jonah Saunders**. Project background: **Jonah Saunders and Jacob Rohozen**. [Source history](docs/provenance.md) and [upstream licenses](daughterboards/micromanipulator/licenses/) are retained; no overall project license has been specified.

## Enclosure

[![Wired enclosure cutaway with both harness exits and the connected DC and USB ports](docs/enclosure/images/wired-case.webp)](docs/enclosure/README.md)
