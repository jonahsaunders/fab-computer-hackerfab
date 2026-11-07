# Routed-board review

The board is 100 × 60 mm, with one RP2350B and all external connectors on the perimeter. The DIN96 connector and every harness pinout/placement match the earlier checked board. The native schematic remains unchanged by the routing and ground-finishing pass.

## Bypass paths and ground

All 35 checked local supply paths connect on F.Cu, without a via-plane-via detour. The [path table](decoupling-paths.csv) records actual saved-board trace lengths. The core regulator has direct input/output capacitor returns to PGND. The adjacent front pour is cut back around its switching loop.

In2.Cu contains one connected ground region and no signal tracks. F.Cu ground fills connect the capacitor returns, MCU and driver grounds. B.Cu ground fills support the power stages and board perimeter. Fifty-four additional, individually placed 0.45/0.20 mm stitching vias connect these areas. Disconnected copper islands are removed on every zone. Power-driver ground pads connect solidly to their local pour. These choices improve return geometry; they are not a loop-inductance or EMI measurement.

## Stackup and USB

The physical stackup records the nominal **JLC04161H-7628** construction: F.Cu 35 µm / 7628 prepreg 0.2104 mm / In1.Cu 15.2 µm / core 1.065 mm / In2.Cu 15.2 µm / 7628 prepreg 0.2104 mm / B.Cu 35 µm. Layer functions are signal / power / ground / signal. Overall board thickness is nominally 1.6 mm; published individual layer figures and mask thicknesses are nominal process values, not a mechanical tolerance stack. Confirm the stackup with the fabricator. [JLCPCB stackups](https://jlcpcb.com/impedance).

The principal USB connector-to-series-resistor pair runs on B.Cu with 0.26 mm width and 0.15 mm gap, referenced to In2.Cu. Coplanar B.Cu pour is excluded from the USB/MCU corridor. Connector, ESD and resistor launches use short narrower sections; the resistor-to-MCU sections are not continuously coupled. Thus this is a full-speed USB layout for prototype review, **not a verified 90 Ω/compliance result**. Fabricator impedance confirmation and signal-integrity review of those transitions remain required. The 27 Ω resistors and direct USB supply bypassing follow the [RP2350 hardware guide](https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008280-DS-1-hardware-design-with-rp2350.pdf?disposition=inline).

## Assembly and access

All 31 footprint types are copied into project-local libraries without changing library names. All 116 placed components have local or embedded models. KiCad standard STEP models are used where available. RP2350B, DRV8837C and USB-C have clearly identified nominal VRML models, including an outward-facing USB opening. These models do not substitute for manufacturer tolerance drawings.

The USB connector opens off the left card edge. JST PH and pin-header harnesses mate above the component face; the DIN plug faces the insertion edge. The native 3D view shows these directions and no apparent body collisions. Cable bend space between populated host slots and actual DIN mating depth remain to be checked against the host assembly.

Visible board labels use at least 1.0 mm text height and 0.15 mm stroke. The eleven thermal vias inside soldered exposed pads are explicitly marked **filled and copper-capped**; ordinary stitching vias are tented. Confirm that process and the QFN/WSON stencil apertures with the assembler. [JLCPCB capabilities](https://jlcpcb.com/capabilities/Capabilities).

## Outstanding engineering checks

Exact supplier selections/package drawings, USB transition review, host assembly fit, and power/thermal limits remain open. The source specifies 12 V / 0.4 A axis motors; all tool-load ratings and the 3.3 V rail's worst-case thermal budget are not yet confirmed. The present fuses and copper are design choices, not tested current ratings. Firmware consolidation and electrical/thermal bench validation are also outstanding. No manufacturing or commissioning release is claimed.

[![Native 3D view](board-3d.png)](board-3d.png)
