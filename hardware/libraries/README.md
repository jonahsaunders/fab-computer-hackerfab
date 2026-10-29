# HackerFab KiCad libraries

Each `.kicad_sym` file is a symbol library. Its matching `.pretty/` directory contains custom footprints for that category; some symbols instead reference KiCad's standard footprints.

| Library | Category |
| --- | --- |
| `Hack_Chips` | Microcontroller, flash memory, regulators, power-selection ICs, and protection MOSFET |
| `Hack_Connector` | DIN 41612, USB-C, terminal and wire connectors, mounting features, and test points |
| `Hack_Diodes` | Diodes, voltage clamps, and USB protection |
| `Hack_Electromechanical` | Switches |
| `Hack_Opto` | LEDs |
| `Hack_Oscillators` | Crystal oscillator components |
| `Hack_Passives` | Resistors, capacitors, inductors, and fuse |

The backplane registers all seven libraries through project-local `fp-lib-table` and `sym-lib-table` files. Entries resolve from `${KIPRJMOD}/../libraries/`, so they work after cloning into a different location.

The 2026-10-29 update supplies 24 custom footprints. It adds the W25Q128JVSIQ flash-memory symbol and SOIC-8 footprint, plus the DFE252012F-3R3M=P2 inductor symbol and Murata DFE252012F footprint. The QFN-80 and Texas HSOP-8 footprints are also updated.

The supplied fuse symbol now references `Hack_Passives:Fuse_Littelfuse-NANO2-451_453`, matching the repository's earlier correction and the bundled footprint. No fuse reference correction was needed for this import.

Custom embedded 3D models are retained inside the supplied KiCad files. Other models use KiCad's standard `${KICAD10_3DMODEL_DIR}` variable. Install the standard KiCad 10 symbols, footprints, and (for rendering) 3D model packages.

Library filenames and component identifiers are preserved from the supplied archive. An unused misspelled `Hack_Osicllators` registration in the original footprint table was removed; the actual library is `Hack_Oscillators`.
